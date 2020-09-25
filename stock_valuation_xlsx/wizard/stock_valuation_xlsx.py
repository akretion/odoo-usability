# Copyright 2020 Akretion France (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_round
from io import BytesIO
from datetime import datetime
import xlsxwriter
import logging
import base64

logger = logging.getLogger(__name__)


class StockValuationXlsx(models.TransientModel):
    _name = 'stock.valuation.xlsx'
    _description = 'Generate XLSX report for stock valuation'

    export_file = fields.Binary(string='XLSX Report', readonly=True)
    export_filename = fields.Char(readonly=True)
    # I don't use ir.actions.url on v12, because it renders
    # the wizard unusable after the first report generation, which creates
    # a lot of confusion for users
    state = fields.Selection([
        ('setup', 'Setup'),
        ('done', 'Done'),
        ], string='State', default='setup', readonly=True)
    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Warehouse',
        states={'done': [('readonly', True)]})
    location_id = fields.Many2one(
        'stock.location', string='Root Stock Location', required=True,
        domain=[('usage', 'in', ('view', 'internal'))],
        default=lambda self: self._default_location(),
        states={'done': [('readonly', True)]},
        help="The childen locations of the selected locations will "
        u"be taken in the valuation.")
    categ_ids = fields.Many2many(
        'product.category', string='Product Categories',
        states={'done': [('readonly', True)]})
    source = fields.Selection([
        ('inventory', 'Physical Inventory'),
        ('stock', 'Stock Levels'),
        ], string='Source data', default='stock', required=True,
        states={'done': [('readonly', True)]})
    inventory_id = fields.Many2one(
        'stock.inventory', string='Inventory', domain=[('state', '=', 'done')],
        states={'done': [('readonly', True)]})
    stock_date_type = fields.Selection([
        ('present', 'Present'),
        ('past', 'Past'),
        ], string='Present or Past', default='present',
        states={'done': [('readonly', True)]})
    past_date = fields.Datetime(
        string='Past Date', states={'done': [('readonly', True)]},
        default=fields.Datetime.now)
    categ_subtotal = fields.Boolean(
        string='Subtotals per Categories', default=True,
        states={'done': [('readonly', True)]},
        help="Show a subtotal per product category")
    standard_price_date = fields.Selection([
        ('past', 'Past Date or Inventory Date'),
        ('present', 'Current'),
        ], default='past', string='Cost Price Date',
        states={'done': [('readonly', True)]})
    split_by_lot = fields.Boolean(
        string='Display Lots', states={'done': [('readonly', True)]})
    split_by_location = fields.Boolean(
        string='Display Stock Locations', states={'done': [('readonly', True)]})

    @api.model
    def _default_location(self):
        wh = self.env.ref('stock.warehouse0')
        return wh.lot_stock_id

    @api.onchange('warehouse_id')
    def warehouse_id_change(self):
        if self.warehouse_id:
            self.location_id = self.warehouse_id.view_location_id.id

    def _check_config(self, company_id):
        self.ensure_one()
        if (
                self.source == 'stock' and
                self.stock_date_type == 'past' and
                self.past_date > fields.Datetime.now()):
            raise UserError(_("The 'Past Date' must be in the past !"))
        if self.source == 'inventory':
            if not self.inventory_id:
                raise UserError(_("You must select an inventory."))
            elif self.inventory_id.state != 'done':
                raise UserError(_(
                    "The selected inventory (%s) is not in done state.")
                    % self.inventory_id.display_name)
        cost_method_real_count = self.env['ir.property'].search([
            ('company_id', '=', company_id),
            ('name', '=', 'property_cost_method'),
            ('value_text', '=', 'real'),
            ('type', '=', 'selection'),
            ], count=True)
        if cost_method_real_count:
            raise UserError(_(
                "There are %d properties that have "
                "'Costing Method' = 'Real Price'. This costing "
                "method is not supported by this module.")
                % cost_method_real_count)

    def _prepare_product_domain(self):
        self.ensure_one()
        domain = [('type', '=', 'product')]
        if self.categ_ids:
            domain += [('categ_id', 'child_of', self.categ_ids.ids)]
        return domain

    def get_product_ids(self):
        self.ensure_one()
        domain = self._prepare_product_domain()
        products = self.env['product.product'].search(domain)
        return products.ids

    def _prepare_product_fields(self):
        return ['uom_id', 'name', 'default_code', 'categ_id']

    def compute_product_data(
            self, company_id, in_stock_product_ids, standard_price_past_date=False):
        self.ensure_one()
        logger.debug('Start compute_product_data')
        ppo = self.env['product.product']
        ppho = self.env['product.price.history']
        fields_list = self._prepare_product_fields()
        if not standard_price_past_date:
            fields_list.append('standard_price')
        products = ppo.search_read([('id', 'in', in_stock_product_ids)], fields_list)
        product_id2data = {}
        for p in products:
            logger.debug('p=%d', p['id'])
            # I don't call the native method get_history_price()
            # because it requires a browse record and it is too slow
            if standard_price_past_date:
                history = ppho.search_read([
                    ('company_id', '=', company_id),
                    ('product_id', '=', p['id']),
                    ('datetime', '<=', standard_price_past_date)],
                    ['cost'], order='datetime desc, id desc', limit=1)
                standard_price = history and history[0]['cost'] or 0.0
            else:
                standard_price = p['standard_price']
            product_id2data[p['id']] = {'standard_price': standard_price}
            for pfield in fields_list:
                if pfield.endswith('_id'):
                    product_id2data[p['id']][pfield] = p[pfield][0]
                else:
                    product_id2data[p['id']][pfield] = p[pfield]
        logger.debug('End compute_product_data')
        return product_id2data

    def id2name(self, product_ids):
        logger.debug('Start id2name')
        pco = self.env['product.category']
        splo = self.env['stock.production.lot']
        slo = self.env['stock.location'].with_context(active_test=False)
        puo = self.env['uom.uom'].with_context(active_test=False)
        categ_id2name = {}
        categ_domain = []
        if self.categ_ids:
            categ_domain = [('id', 'child_of', self.categ_ids.ids)]
        for categ in pco.search_read(categ_domain, ['display_name']):
            categ_id2name[categ['id']] = categ['display_name']
        uom_id2name = {}
        uoms = puo.search_read([], ['name'])
        for uom in uoms:
            uom_id2name[uom['id']] = uom['name']
        lot_id2data = {}
        lot_fields = ['name']
        if hasattr(splo, 'expiry_date'):
            lot_fields.append('expiry_date')

        lots = splo.search_read(
            [('product_id', 'in', product_ids)], lot_fields)
        for lot in lots:
            lot_id2data[lot['id']] = lot
        loc_id2name = {}
        locs = slo.search_read(
            [('id', 'child_of', self.location_id.id)], ['display_name'])
        for loc in locs:
            loc_id2name[loc['id']] = loc['display_name']
        logger.debug('End id2name')
        return categ_id2name, uom_id2name, lot_id2data, loc_id2name

    def compute_data_from_inventory(self, product_ids, prec_qty):
        self.ensure_one()
        logger.debug('Start compute_data_from_inventory')
        # Can he modify UoM ?
        inv_lines = self.env['stock.inventory.line'].search_read([
            ('inventory_id', '=', self.inventory_id.id),
            ('location_id', 'child_of', self.location_id.id),
            ('product_id', 'in', product_ids),
            ('product_qty', '>', 0),
            ], ['product_id', 'location_id', 'prod_lot_id', 'product_qty'])
        res = []
        in_stock_products = {}
        for l in inv_lines:
            if not float_is_zero(l['product_qty'], precision_digits=prec_qty):
                res.append({
                    'product_id': l['product_id'][0],
                    'lot_id': l['prod_lot_id'] and l['prod_lot_id'][0] or False,
                    'qty': l['product_qty'],
                    'location_id': l['location_id'][0],
                    })
                in_stock_products[l['product_id'][0]] = True
        logger.debug('End compute_data_from_inventory')
        return res, in_stock_products

    def compute_data_from_present_stock(self, company_id, product_ids, prec_qty):
        self.ensure_one()
        logger.debug('Start compute_data_from_present_stock')
        quants = self.env['stock.quant'].search_read([
            ('product_id', 'in', product_ids),
            ('location_id', 'child_of', self.location_id.id),
            ('company_id', '=', company_id),
            ], ['product_id', 'lot_id', 'location_id', 'quantity'])
        res = []
        in_stock_products = {}
        for quant in quants:
            if not float_is_zero(quant['quantity'], precision_digits=prec_qty):
                res.append({
                    'product_id': quant['product_id'][0],
                    'lot_id': quant['lot_id'] and quant['lot_id'][0] or False,
                    'location_id': quant['location_id'][0],
                    'qty': quant['quantity'],
                    })
                in_stock_products[quant['product_id'][0]] = True
        logger.debug('End compute_data_from_present_stock')
        return res, in_stock_products

    def compute_data_from_past_stock(self, product_ids, prec_qty, past_date):
        self.ensure_one()
        logger.debug('Start compute_data_from_past_stock past_date=%s', past_date)
        ppo = self.env['product.product']
        products = ppo.with_context(to_date=past_date, location_id=self.location_id.id).browse(product_ids)
        res = []
        in_stock_products = {}
        for product in products:
            qty = product.qty_available
            if not float_is_zero(qty, precision_digits=prec_qty):
                res.append({
                    'product_id': product.id,
                    'qty': qty,
                    'lot_id': False,
                    'location_id': False,
                    })
                in_stock_products[product.id] = True
        logger.debug('End compute_data_from_past_stock')
        return res, in_stock_products

    def group_result(self, data, split_by_lot, split_by_location):
        logger.debug(
            'Start group_result split_by_lot=%s, split_by_location=%s',
            split_by_lot, split_by_location)
        wdict = {}
        for l in data:
            key_list = [l['product_id']]
            if split_by_lot:
                key_list.append(l['lot_id'])
            if split_by_location:
                key_list.append(l['location_id'])
            key = tuple(key_list)
            wdict.setdefault(key, dict(product_id=l['product_id'], lot_id=l['lot_id'], location_id=l['location_id'], qty=0.0))
            wdict[key]['qty'] += l['qty']
        logger.debug('End group_result')
        return wdict.values()

    def stringify_and_sort_result(
            self, product_ids, product_id2data, data,
            prec_qty, prec_price, prec_cur_rounding, categ_id2name,
            uom_id2name, lot_id2data, loc_id2name):
        logger.debug('Start stringify_and_sort_result')
        res = []
        for l in data:
            product_id = l['product_id']
            qty = float_round(l['qty'], precision_digits=prec_qty)
            standard_price = float_round(
                product_id2data[product_id]['standard_price'],
                precision_digits=prec_price)
            subtotal = float_round(
                standard_price * qty, precision_rounding=prec_cur_rounding)
            res.append(dict(
                product_id2data[product_id],
                product_name=product_id2data[product_id]['name'],
                loc_name=l['location_id'] and loc_id2name[l['location_id']] or '',
                lot_name=l['lot_id'] and lot_id2data[l['lot_id']]['name'] or '',
                expiry_date=l['lot_id'] and lot_id2data[l['lot_id']].get('expiry_date'),
                qty=qty,
                uom_name=uom_id2name[product_id2data[product_id]['uom_id']],
                standard_price=standard_price,
                subtotal=subtotal,
                categ_name=categ_id2name[product_id2data[product_id]['categ_id']],
                ))
        sort_res = sorted(res, key=lambda x: x['product_name'])
        logger.debug('End stringify_and_sort_result')
        return sort_res

    def generate(self):
        self.ensure_one()
        logger.debug('Start generate XLSX stock valuation report')
        splo = self.env['stock.production.lot'].with_context(active_test=False)
        prec_qty = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        prec_price = self.env['decimal.precision'].precision_get('Product Price')
        company = self.env.user.company_id
        company_id = company.id
        prec_cur_rounding = company.currency_id.rounding
        self._check_config(company_id)

        product_ids = self.get_product_ids()
        if not product_ids:
            raise UserError(_("There are no products to analyse."))
        split_by_lot = self.split_by_lot
        split_by_location = self.split_by_location
        if self.source == 'stock':
            if self.stock_date_type == 'present':
                past_date = False
                data, in_stock_products = self.compute_data_from_present_stock(
                    company_id, product_ids, prec_qty)
            elif self.stock_date_type == 'past':
                split_by_lot = False
                split_by_location = False
                past_date = self.past_date
                data, in_stock_products = self.compute_data_from_past_stock(
                    product_ids, prec_qty, past_date)
        elif self.source == 'inventory':
            past_date = self.inventory_id.date
            data, in_stock_products = self.compute_data_from_inventory(product_ids, prec_qty)
        standard_price_past_date = past_date
        if not (self.source == 'stock' and self.stock_date_type == 'present') and self.standard_price_date == 'present':
            standard_price_past_date = False
        in_stock_product_ids = list(in_stock_products.keys())
        product_id2data = self.compute_product_data(
            company_id, in_stock_product_ids,
            standard_price_past_date=standard_price_past_date)
        data_res = self.group_result(data, split_by_lot, split_by_location)
        categ_id2name, uom_id2name, lot_id2data, loc_id2name = self.id2name(product_ids)
        res = self.stringify_and_sort_result(
            product_ids, product_id2data, data_res, prec_qty, prec_price, prec_cur_rounding,
            categ_id2name, uom_id2name, lot_id2data, loc_id2name)

        logger.debug('Start create XLSX workbook')
        file_data = BytesIO()
        workbook = xlsxwriter.Workbook(file_data)
        sheet = workbook.add_worksheet('Stock')
        styles = self._prepare_styles(workbook, company, prec_price)
        cols = self._prepare_cols()
        categ_subtotal = self.categ_subtotal
        # remove cols that we won't use
        if not split_by_lot:
            cols.pop('lot_name', None)
            cols.pop('expiry_date', None)
        if not hasattr(splo, 'expiry_date'):
            cols.pop('expiry_date', None)
        if not split_by_location:
            cols.pop('loc_name', None)
        if not categ_subtotal:
            cols.pop('categ_subtotal', None)

        j = 0
        for col, col_vals in sorted(cols.items(), key=lambda x: x[1]['sequence']):
            cols[col]['pos'] = j
            cols[col]['pos_letter'] = chr(j + 97).upper()
            sheet.set_column(j, j, cols[col]['width'])
            j += 1

        # HEADER
        now_dt = fields.Datetime.context_timestamp(self, datetime.now())
        now_str = fields.Datetime.to_string(now_dt)
        if past_date:
            stock_time_utc_dt = past_date
            stock_time_dt = fields.Datetime.context_timestamp(self, stock_time_utc_dt)
            stock_time_str = fields.Datetime.to_string(stock_time_dt)
        else:
            stock_time_str = now_str
        if standard_price_past_date:
            standard_price_date_str = stock_time_str
        else:
            standard_price_date_str = now_str
        i = 0
        sheet.write(i, 0, 'Odoo - Stock Valuation', styles['doc_title'])
        sheet.set_row(0, 26)
        i += 1
        sheet.write(i, 0, 'Inventory Date: %s' % stock_time_str, styles['doc_subtitle'])
        i += 1
        sheet.write(i, 0, 'Cost Price Date: %s' % standard_price_date_str, styles['doc_subtitle'])
        i += 1
        sheet.write(i, 0, 'Stock location (children included): %s' % self.location_id.complete_name, styles['doc_subtitle'])
        if self.categ_ids:
            i += 1
            sheet.write(i, 0, 'Product Categories: %s' % ', '.join([categ.display_name for categ in self.categ_ids]), styles['doc_subtitle'])
        i += 1
        sheet.write(i, 0, 'Generated on %s by %s' % (now_str, self.env.user.name), styles['regular_small'])

        # TITLE of COLS
        i += 2
        for col in cols.values():
            sheet.write(i, col['pos'], col['title'], styles['col_title'])

        i += 1
        sheet.write(i, cols['subtotal']['pos'] - 1, _("TOTAL:"), styles['total_title'])
        total_row = i

        # LINES
        if categ_subtotal:
            categ_ids = categ_id2name.keys()
        else:
            categ_ids = [0]

        total = 0.0
        letter_qty = cols['qty']['pos_letter']
        letter_price = cols['standard_price']['pos_letter']
        letter_subtotal = cols['subtotal']['pos_letter']
        crow = 0
        lines = res
        for categ_id in categ_ids:
            ctotal = 0.0
            categ_has_line = False
            if categ_subtotal:
                # skip a line and save it's position as crow
                i += 1
                crow = i
                lines = filter(lambda x: x['categ_id'] == categ_id, res)
            for l in lines:
                i += 1
                total += l['subtotal']
                ctotal += l['subtotal']
                categ_has_line = True
                subtotal_formula = '=%s%d*%s%d' % (letter_qty, i + 1, letter_price, i + 1)
                sheet.write_formula(i, cols['subtotal']['pos'], subtotal_formula, styles['regular_currency'], l['subtotal'])
                for col_name, col in cols.items():
                    if not col.get('formula'):
                        if col.get('type') == 'date' and l[col_name]:
                            l[col_name] = fields.Date.from_string(l[col_name])
                        sheet.write(i, col['pos'], l[col_name], styles[col['style']])
            if categ_subtotal:
                if categ_has_line:
                    sheet.write(crow, 0, categ_id2name[categ_id], styles['categ_title'])
                    for x in range(cols['categ_subtotal']['pos'] - 1):
                        sheet.write(crow, x + 1, '', styles['categ_title'])

                    cformula = '=SUM(%s%d:%s%d)' % (letter_subtotal, crow + 2, letter_subtotal, i + 1)
                    sheet.write_formula(crow, cols['categ_subtotal']['pos'], cformula, styles['categ_currency'], float_round(ctotal, precision_rounding=prec_cur_rounding))
                else:
                    i -= 1  # go back to skipped line

        # Write total
        total_formula = '=SUM(%s%d:%s%d)' % (letter_subtotal, total_row + 2, letter_subtotal, i + 1)
        sheet.write_formula(total_row, cols['subtotal']['pos'], total_formula, styles['total_currency'], float_round(total, precision_rounding=prec_cur_rounding))

        workbook.close()
        logger.debug('End create XLSX workbook')
        file_data.seek(0)
        filename = 'Odoo_stock_%s.xlsx' % stock_time_str.replace(' ', '-').replace(':', '_')
        export_file_b64 = base64.b64encode(file_data.read())
        self.write({
            'state': 'done',
            'export_filename': filename,
            'export_file': export_file_b64,
            })
        # action = {
        #    'name': _('Stock Valuation XLSX'),
        #    'type': 'ir.actions.act_url',
        #    'url': "web/content/?model=%s&id=%d&filename_field=export_filename&"
        #           "field=export_file&download=true&filename=%s" % (
        #               self._name, self.id, self.export_filename),
        #    'target': 'self',
        #    }
        action = self.env['ir.actions.act_window'].for_xml_id(
            'stock_valuation_xlsx', 'stock_valuation_xlsx_action')
        action['res_id'] = self.id
        return action

    def _prepare_styles(self, workbook, company, prec_price):
        total_bg_color = '#faa03a'
        categ_bg_color = '#e1daf5'
        col_title_bg_color = '#fff9b4'
        regular_font_size = 10
        currency_num_format = u'# ### ##0.00 %s' % company.currency_id.symbol
        price_currency_num_format = u'# ### ##0.%s %s' % ('0' * prec_price, company.currency_id.symbol)
        styles = {
            'doc_title': workbook.add_format({
                'bold': True, 'font_size': regular_font_size + 10,
                'font_color': '#003b6f'}),
            'doc_subtitle': workbook.add_format({
                'bold': True, 'font_size': regular_font_size}),
            'col_title': workbook.add_format({
                'bold': True, 'bg_color': col_title_bg_color,
                'text_wrap': True, 'font_size': regular_font_size,
                'align': 'center',
                }),
            'total_title': workbook.add_format({
                'bold': True, 'text_wrap': True, 'font_size': regular_font_size + 2,
                'align': 'right', 'bg_color': total_bg_color}),
            'total_currency': workbook.add_format({
                'num_format': currency_num_format, 'bg_color': total_bg_color}),
            'regular_date': workbook.add_format({'num_format': 'dd/mm/yyyy'}),
            'regular_currency': workbook.add_format({'num_format': currency_num_format}),
            'regular_price_currency': workbook.add_format({'num_format': price_currency_num_format}),
            'regular': workbook.add_format({}),
            'regular_small': workbook.add_format({'font_size': regular_font_size - 2}),
            'categ_title': workbook.add_format({
                'bold': True, 'bg_color': categ_bg_color,
                'font_size': regular_font_size}),
            'categ_currency': workbook.add_format({
                'num_format': currency_num_format, 'bg_color': categ_bg_color}),
            'date_title': workbook.add_format({
                'bold': True, 'font_size': regular_font_size, 'align': 'right'}),
            'date_title_val': workbook.add_format({
                'bold': True, 'font_size': regular_font_size}),
            }
        return styles

    def _prepare_cols(self):
        cols = {
            'default_code': {'width': 18, 'style': 'regular', 'sequence': 10, 'title': _('Product Code')},
            'product_name': {'width': 40, 'style': 'regular', 'sequence': 20, 'title': _('Product Name')},
            'loc_name': {'width': 25, 'style': 'regular_small', 'sequence': 30, 'title': _('Location Name')},
            'lot_name': {'width': 18, 'style': 'regular', 'sequence': 40, 'title': _('Lot')},
            'expiry_date': {'width': 11, 'style': 'regular_date', 'sequence': 50, 'title': _('Expiry Date'), 'type': 'date'},
            'qty': {'width': 8, 'style': 'regular', 'sequence': 60, 'title': _('Qty')},
            'uom_name': {'width': 5, 'style': 'regular_small', 'sequence': 70, 'title': _('UoM')},
            'standard_price': {'width': 14, 'style': 'regular_price_currency', 'sequence': 80, 'title': _('Cost Price')},
            'subtotal': {'width': 16, 'style': 'regular_currency', 'sequence': 90, 'title': _('Sub-total'), 'formula': True},
            'categ_subtotal': {'width': 16, 'style': 'regular_currency', 'sequence': 100, 'title': _('Categ Sub-total'), 'formula': True},
            'categ_name': {'width': 40, 'style': 'regular_small', 'sequence': 110, 'title': _('Product Category')},
            }
        return cols
