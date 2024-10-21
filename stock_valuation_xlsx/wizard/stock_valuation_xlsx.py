# Copyright 2020-2024 Akretion France (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from odoo.tools import float_is_zero, float_round
from io import BytesIO
from datetime import datetime
import xlsxwriter
import logging
import base64

logger = logging.getLogger(__name__)


class StockValuationXlsx(models.TransientModel):
    _name = 'stock.valuation.xlsx'
    _check_company_auto = True
    _description = 'Generate XLSX report for stock valuation'

    export_file = fields.Binary(string='XLSX Report', readonly=True, attachment=True)
    export_filename = fields.Char(readonly=True)
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company,
        required=True)
    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Warehouse', check_company=True,
        domain="[('company_id', '=', company_id)]")
    location_id = fields.Many2one(
        'stock.location', string='Root Stock Location', required=True, check_company=True,
        compute='_compute_location_id', readonly=False, precompute=True, store=True,
        domain="[('usage', 'in', ('view', 'internal')), ('company_id', 'in', [False, company_id])]",
        help="The childen locations of the selected locations will "
        "be taken in the valuation.")
    categ_ids = fields.Many2many(
        'product.category', string='Product Category Filter',
        help="Leave this field empty to have a stock valuation for all your products.",
        )
    stock_date_type = fields.Selection([
        ('present', 'Present'),
        ('past', 'Past'),
        ], string='Present or Past', default='present', required=True)
    past_date = fields.Datetime(
        string='Past Date', default=fields.Datetime.now)
    categ_subtotal = fields.Boolean(
        string='Subtotals per Categories', default=True,
        help="Show a subtotal per product category.")
    standard_price_date = fields.Selection([
        ('past', 'Past Date'),
        ('present', 'Current'),
        ], default='past', string='Cost Price Date')
    has_expiry_date = fields.Boolean(
        default=lambda self: self._default_has_expiry_date(), readonly=True)
    apply_depreciation = fields.Boolean(
        string='Apply Depreciation Rules', default=True)
    split_by_lot = fields.Boolean(string='Display Lots')
    split_by_location = fields.Boolean(string='Display Stock Locations')

    @api.model
    def _default_has_expiry_date(self):
        has_expiry_date = False
        if hasattr(self.env['stock.lot'], 'expiry_date'):
            has_expiry_date = True
        return has_expiry_date

    @api.depends('warehouse_id', 'company_id')
    def _compute_location_id(self):
        for wiz in self:
            wh = wiz.warehouse_id
            if not wh:
                wh = self.env["stock.warehouse"].search([('company_id', '=', wiz.company_id.id)], limit=1)
            if wh:
                wiz.location_id = wh.view_location_id.id

    def _check_config(self):
        self.ensure_one()
        if (
                self.stock_date_type == 'past' and
                self.past_date > fields.Datetime.now()):
            raise UserError(_("The 'Past Date' must be in the past !"))
        cost_method_real_count = self.env['ir.property'].sudo().search([
            ('company_id', '=', self.company_id.id),
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
        return ['uom_id', 'name', 'default_code', 'barcode', 'categ_id']

    def _prepare_expiry_depreciation_rules(self, company_id, past_date):
        rules = self.env['stock.expiry.depreciation.rule'].search_read([('company_id', '=', company_id)], ['start_limit_days', 'ratio'], order='start_limit_days desc')
        if past_date:
            date_dt = fields.Date.to_date(past_date)  # convert datetime to date
        else:
            date_dt = fields.Date.context_today(self)
        for rule in rules:
            rule['start_date'] = date_dt - relativedelta(days=rule['start_limit_days'])
        logger.debug('depreciation_rules=%s', rules)
        return rules

    @api.model
    def compute_product_data(self, company_id, filter_product_ids, standard_price_dict):
        # standard_price_dict is a dictionnary with:
        # keys = the keys that we expect in the result dict
        # values : a datetime object (for past date) or False (False means PRESENT)
        logger.debug(
            'Start compute_product_data standard_price_dict=%s', standard_price_dict)
        ppo = self.env['product.product'].with_company(company_id)
        svlo = self.env['stock.valuation.layer']
        fields_list = self._prepare_product_fields()
        # Do we need the present date?
        if not all(standard_price_dict.values()):
            fields_list.append('standard_price')
        products = ppo.search_read([('id', 'in', filter_product_ids)], fields_list)
        product_id2data = {}
        for p in products:
            logger.debug('p=%d', p['id'])
            product_id2data[p['id']] = {}
            for std_price_field_name, std_price_date in standard_price_dict.items():
                if not std_price_date:  # present
                    product_id2data[p['id']][std_price_field_name] = p['standard_price']
                else:
                    layer_rg = svlo._read_group(
                        [
                            ('product_id', '=', p['id']),
                            ('company_id', '=', company_id),
                            ('create_date', '<=', std_price_date),
                        ],
                        ['value', 'quantity'],
                        [])
                    standard_price = 0
                    if layer_rg and layer_rg[0]['quantity']:
                        standard_price = layer_rg[0]['value'] / layer_rg[0]['quantity']
                    product_id2data[p['id']][std_price_field_name] = standard_price
            for pfield in fields_list:
                if pfield.endswith('_id'):
                    product_id2data[p['id']][pfield] = p[pfield][0]
                else:
                    product_id2data[p['id']][pfield] = p[pfield]
        logger.debug('End compute_product_data')
        return product_id2data

    @api.model
    def product_categ_id2name(self, categories):
        pco = self.env['product.category']
        categ_id2name = {}
        categ_domain = []
        if categories:
            categ_domain = [('id', 'child_of', categories.ids)]
        for categ in pco.search_read(categ_domain, ['display_name']):
            categ_id2name[categ['id']] = categ['display_name']
        return categ_id2name

    @api.model
    def uom_id2name(self):
        puo = self.env['uom.uom'].with_context(active_test=False)
        uom_id2name = {}
        uoms = puo.search_read([], ['name'])
        for uom in uoms:
            uom_id2name[uom['id']] = uom['name']
        return uom_id2name

    @api.model
    def prodlot_id2data(self, product_ids, has_expiry_date, depreciation_rules):
        slo = self.env['stock.lot']
        lot_id2data = {}
        lot_fields = ['name']
        if has_expiry_date:
            lot_fields.append('expiry_date')

        lots = slo.search_read(
            [('product_id', 'in', product_ids)], lot_fields)
        for lot in lots:
            lot_id2data[lot['id']] = lot
            lot_id2data[lot['id']]['depreciation_ratio'] = 0
            if depreciation_rules and lot.get('expiry_date'):
                expiry_date = lot['expiry_date']
                for rule in depreciation_rules:
                    if expiry_date <= rule['start_date']:
                        lot_id2data[lot['id']]['depreciation_ratio'] = rule['ratio'] / 100.0
                        break
        return lot_id2data

    @api.model
    def stock_location_id2name(self, location):
        slo = self.env['stock.location'].with_context(active_test=False)
        loc_id2name = {}
        locs = slo.search_read(
            [('id', 'child_of', self.location_id.id)], ['display_name'])
        for loc in locs:
            loc_id2name[loc['id']] = loc['display_name']
        return loc_id2name

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
        products = ppo.with_context(to_date=past_date, location=self.location_id.id).browse(product_ids)
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
            uom_id2name, lot_id2data, loc_id2name, apply_depreciation):
        logger.debug('Start stringify_and_sort_result')
        res = []
        for l in data:
            product_id = l['product_id']
            qty = float_round(l['qty'], precision_digits=prec_qty)
            standard_price = float_round(
                product_id2data[product_id]['standard_price'],
                precision_digits=prec_price)
            subtotal_before_depreciation = float_round(
                standard_price * qty, precision_rounding=prec_cur_rounding)
            depreciation_ratio = 0
            if apply_depreciation and l['lot_id']:
                depreciation_ratio = lot_id2data[l['lot_id']].get('depreciation_ratio', 0)
                subtotal = float_round(
                    subtotal_before_depreciation * (1 - depreciation_ratio),
                    precision_rounding=prec_cur_rounding)
            else:
                subtotal = subtotal_before_depreciation
            res.append(dict(
                product_id2data[product_id],
                product_name=product_id2data[product_id]['name'],
                loc_name=l['location_id'] and loc_id2name[l['location_id']] or '',
                lot_name=l['lot_id'] and lot_id2data[l['lot_id']]['name'] or '',
                expiry_date=l['lot_id'] and lot_id2data[l['lot_id']].get('expiry_date'),
                depreciation_ratio=depreciation_ratio,
                qty=qty,
                uom_name=uom_id2name[product_id2data[product_id]['uom_id']],
                standard_price=standard_price,
                subtotal_before_depreciation=subtotal_before_depreciation,
                subtotal=subtotal,
                categ_name=categ_id2name[product_id2data[product_id]['categ_id']],
                ))
        sort_res = sorted(res, key=lambda x: x['product_name'])
        logger.debug('End stringify_and_sort_result')
        return sort_res

    def generate(self):
        self.ensure_one()
        logger.debug('Start generate XLSX stock valuation report')
        prec_qty = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        prec_price = self.env['decimal.precision'].precision_get('Product Price')
        company = self.company_id
        company_id = company.id
        prec_cur_rounding = company.currency_id.rounding
        self._check_config()

        if (
                self.stock_date_type == 'past' or
                not self.split_by_lot or
                not self.has_expiry_date):
            apply_depreciation = False
        else:
            apply_depreciation = self.apply_depreciation
        product_ids = self.get_product_ids()
        if not product_ids:
            raise UserError(_("There are no products to analyse."))
        if self.stock_date_type == 'present':
            split_by_lot = self.split_by_lot
            split_by_location = self.split_by_location
            past_date = False
            standard_price_past_date = False
            data, in_stock_products = self.compute_data_from_present_stock(
                company_id, product_ids, prec_qty)
        elif self.stock_date_type == 'past':
            split_by_lot = False
            split_by_location = False
            past_date = self.past_date
            standard_price_past_date = past_date
            data, in_stock_products = self.compute_data_from_past_stock(
                product_ids, prec_qty, past_date)
        else:
            raise
        depreciation_rules = []
        if apply_depreciation:
            depreciation_rules = self._prepare_expiry_depreciation_rules(company_id, past_date)
            if not depreciation_rules:
                raise UserError(_(
                    "The are not stock depreciation rule for company '%s'.")
                    % company.display_name)
        in_stock_product_ids = list(in_stock_products.keys())
        product_id2data = self.compute_product_data(
            company_id, in_stock_product_ids,
            {'standard_price': standard_price_past_date})
        data_res = self.group_result(data, split_by_lot, split_by_location)
        categ_id2name = self.product_categ_id2name(self.categ_ids)
        uom_id2name = self.uom_id2name()
        lot_id2data = self.prodlot_id2data(in_stock_product_ids, self.has_expiry_date, depreciation_rules)
        loc_id2name = self.stock_location_id2name(self.location_id)
        res = self.stringify_and_sort_result(
            product_ids, product_id2data, data_res, prec_qty, prec_price, prec_cur_rounding,
            categ_id2name, uom_id2name, lot_id2data, loc_id2name, apply_depreciation)

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
        if not self.has_expiry_date:
            cols.pop('expiry_date', None)
        if not split_by_location:
            cols.pop('loc_name', None)
        if not categ_subtotal:
            cols.pop('categ_subtotal', None)
        if not apply_depreciation:
            cols.pop('depreciation_ratio', None)
            cols.pop('subtotal_before_depreciation', None)

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
        if apply_depreciation:
            letter_subtotal_before_depreciation = cols['subtotal_before_depreciation']['pos_letter']
            letter_depreciation_ratio = cols['depreciation_ratio']['pos_letter']
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
                qty_by_price_formula = '=%s%d*%s%d' % (letter_qty, i + 1, letter_price, i + 1)
                if apply_depreciation:
                    sheet.write_formula(i, cols['subtotal_before_depreciation']['pos'], qty_by_price_formula, styles['regular_currency'], l['subtotal_before_depreciation'])
                    subtotal_formula = '=%s%d*(1 - %s%d)' % (letter_subtotal_before_depreciation, i + 1, letter_depreciation_ratio, i + 1)
                else:
                    subtotal_formula = qty_by_price_formula
                sheet.write_formula(i, cols['subtotal']['pos'], subtotal_formula, styles['regular_currency'], l['subtotal'])
                for col_name, col in cols.items():
                    if not col.get('formula'):
                        if not l[col_name]:
                            l[col_name] = ''  # to avoid display of 31/12/1899 (dates) or '0' (char)
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
            'export_filename': filename,
            'export_file': export_file_b64,
            })
        action = {
            'name': _('Stock Valuation XLSX'),
            'type': 'ir.actions.act_url',
            'url': "web/content/?model=%s&id=%d&filename_field=export_filename&"
                   "field=export_file&download=true&filename=%s" % (
                       self._name, self.id, self.export_filename),
            'target': 'new',
            }
        return action

    def _prepare_styles(self, workbook, company, prec_price):
        total_bg_color = '#faa03a'
        categ_bg_color = '#e1daf5'
        col_title_bg_color = '#fff9b4'
        regular_font_size = 10
        currency_num_format = '# ### ##0.00 %s' % company.currency_id.symbol
        price_currency_num_format = '# ### ##0.%s %s' % ('0' * prec_price, company.currency_id.symbol)
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
            'regular_int_percent': workbook.add_format({'num_format': '0.%'}),
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
            'barcode': {'width': 18, 'style': 'regular', 'sequence': 15, 'title': _('Product Barcode')},
            'product_name': {'width': 40, 'style': 'regular', 'sequence': 20, 'title': _('Product Name')},
            'loc_name': {'width': 25, 'style': 'regular_small', 'sequence': 30, 'title': _('Location Name')},
            'lot_name': {'width': 18, 'style': 'regular', 'sequence': 40, 'title': _('Lot')},
            'expiry_date': {'width': 11, 'style': 'regular_date', 'sequence': 50, 'title': _('Expiry Date'), 'type': 'date'},
            'qty': {'width': 8, 'style': 'regular', 'sequence': 60, 'title': _('Qty')},
            'uom_name': {'width': 5, 'style': 'regular_small', 'sequence': 70, 'title': _('UoM')},
            'standard_price': {'width': 14, 'style': 'regular_price_currency', 'sequence': 80, 'title': _('Cost Price')},
            'subtotal_before_depreciation': {'width': 16, 'style': 'regular_currency', 'sequence': 90, 'title': _('Sub-total'), 'formula': True},
            'depreciation_ratio': {'width': 10, 'style': 'regular_int_percent', 'sequence': 100, 'title': _('Depreciation')},
            'subtotal': {'width': 16, 'style': 'regular_currency', 'sequence': 110, 'title': _('Sub-total'), 'formula': True},
            'categ_subtotal': {'width': 16, 'style': 'regular_currency', 'sequence': 120, 'title': _('Categ Sub-total'), 'formula': True},
            'categ_name': {'width': 40, 'style': 'regular_small', 'sequence': 130, 'title': _('Product Category')},
            }
        return cols
