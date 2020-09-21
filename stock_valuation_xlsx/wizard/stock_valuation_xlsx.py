# -*- coding: utf-8 -*-
# Copyright 2020 Akretion France (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero, float_round
from cStringIO import StringIO
from datetime import datetime
import xlsxwriter
from pprint import pprint


class StockValuationXlsx(models.TransientModel):
    _name = 'stock.valuation.xlsx'
    _description = 'Generate XLSX report for stock valuation'

    export_file = fields.Binary(string='XLSX Report', readonly=True)
    export_filename = fields.Char(readonly=True)
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

    def _check_config(self):
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
        # raise si la valuation method est real

    def _prepare_product_domain(self):
        self.ensure_one()
        domain = [('type', '=', 'product')]
        if self.categ_ids:
            domain += [('categ_id', 'child_of', self.categ_ids.ids)]
        return domain

    def compute_product_data(self, company_id, past_date=False):
        self.ensure_one()
        ppo = self.env['product.product']
        domain = self._prepare_product_domain()
        products = ppo.with_context(active_test=False).search(domain)
        product_ids = [x['id'] for x in products]
        product_id2data = {}
        for p in products:
            standard_price = p.get_history_price(company_id, date=past_date)
            product_id2data[p['id']] = {
                'default_code': p.default_code,
                'name': p.name,
                'categ_id': p.categ_id.id,
                'uom_id': p.uom_id.id,
                'standard_price': standard_price,
                }
        return product_id2data, product_ids

    def id2name(self, product_ids):
        pco = self.env['product.category'].with_context(active_test=False)
        splo = self.env['stock.production.lot'].with_context(active_test=False)
        slo = self.env['stock.location'].with_context(active_test=False)
        puo = self.env['product.uom'].with_context(active_test=False)
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

        lots = splo.search_read([('product_id', 'in', product_ids)], lot_fields)
        for lot in lots:
            lot_id2data[lot['id']] = lot
        loc_id2name = {}
        locs = slo.search_read([('id', 'child_of', self.location_id.id)], ['display_name'])
        for loc in locs:
            loc_id2name[loc['id']] = loc['display_name']

        return categ_id2name, uom_id2name, lot_id2data, loc_id2name

    def compute_data_from_inventory(self, product_ids, prec_qty):
        self.ensure_one()
        # Can he modify UoM ?
        inv_lines = self.env['stock.inventory.line'].search_read([
            ('inventory_id', '=', self.inventory_id.id),
            ('location_id', 'child_of', self.location_id.id),
            ('product_id', 'in', product_ids),
            ('product_qty', '>', 0),
            ], ['product_id', 'location_id', 'prod_lot_id', 'product_qty'])
        res = []
        for l in inv_lines:
            if not float_is_zero(l['product_qty'], precision_digits=prec_qty):
                res.append({
                    'product_id': l['product_id'][0],
                    'lot_id': l['prod_lot_id'] and l['prod_lot_id'][0] or False,
                    'qty': l['product_qty'],
                    'location_id': l['location_id'][0],
                    })
        return res

    def compute_data_from_present_stock(self, company_id, product_ids, prec_qty):
        self.ensure_one()
        quants = self.env['stock.quant'].search_read([
            ('product_id', 'in', product_ids),
            ('location_id', 'child_of', self.location_id.id),
            ('company_id', '=', company_id),
            ], ['product_id', 'lot_id', 'location_id', 'qty'])
        res = []
        for quant in quants:
            if not float_is_zero(quant['qty'], precision_digits=prec_qty):
                res.append({
                    'product_id': quant['product_id'][0],
                    'lot_id': quant['lot_id'] and quant['lot_id'][0] or False,
                    'location_id': quant['location_id'][0],
                    'qty': quant['qty'],
                    })
        return res

    def compute_data_from_past_stock(self, product_ids, prec_qty, past_date):
        self.ensure_one()
        ppo = self.env['product.product']
        products = ppo.with_context(to_date=past_date, location_id=self.location_id.id).browse(product_ids)
        res = []
        for p in products:
            qty = p.qty_available
            if not float_is_zero(qty, precision_digits=prec_qty):
                res.append({
                    'product_id': p.id,
                    'qty': qty,
                    'lot_id': False,
                    'location_id': False,
                    })
        return res

    def group_result(self, data, split_by_lot, split_by_location):
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
        return wdict.values()

    def stringify_and_sort_result(self, product_ids, product_id2data, data, prec_qty, prec_cur_rounding, categ_id2name, uom_id2name, lot_id2data, loc_id2name):
        res = []
        categ_subtotal = self.categ_subtotal
        for l in data:
            product_id = l['product_id']
            qty = float_round(l['qty'], precision_digits=prec_qty)
            standard_price = product_id2data[product_id]['standard_price']
            res.append({
                'product_code': product_id2data[product_id]['default_code'],
                'product_name': product_id2data[product_id]['name'],
                'loc_name': l['location_id'] and loc_id2name[l['location_id']] or '',
                'lot_name': l['lot_id'] and lot_id2data[l['lot_id']]['name'] or '',
                'expiry_date': l['lot_id'] and lot_id2data[l['lot_id']]['expiry_date'] or '',
                'qty': qty,
                'uom_name': uom_id2name[product_id2data[product_id]['uom_id']],
                'standard_price': standard_price,
                'subtotal': float_round(standard_price * qty, precision_rounding=prec_cur_rounding),
                'categ_name': categ_id2name[product_id2data[product_id]['categ_id']],
                'categ_id': categ_subtotal and product_id2data[product_id]['categ_id'] or 0,
                })
        sort_res = sorted(res, key=lambda x: x['product_name'])
        return sort_res

    def generate(self):
        self.ensure_one()
        splo = self.env['stock.production.lot'].with_context(active_test=False)
        pco = self.env['product.category'].with_context(active_test=False)
        self._check_config()
        prec_qty = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        company = self.env.user.company_id
        company_id = company.id
        prec_cur_rounding = company.currency_id.rounding

        split_by_lot = self.split_by_lot
        split_by_location = self.split_by_location
        past_date = False
        if self.source == 'stock' and self.stock_date_type == 'past':
            split_by_lot = False
            split_by_location = False
            past_date = self.past_date
        product_id2data, product_ids = self.compute_product_data(
            company_id, past_date=past_date)
        if self.source == 'stock':
            if self.stock_date_type == 'present':
                data = self.compute_data_from_present_stock(
                    company_id, product_ids, prec_qty)
            elif self.stock_date_type == 'past':
                data = self.compute_data_from_past_stock(
                    product_ids, prec_qty, past_date)
        elif self.source == 'inventory':
            data = self.compute_data_from_inventory(product_ids, prec_qty)
        data_res = self.group_result(data, split_by_lot, split_by_location)
        categ_id2name, uom_id2name, lot_id2data, loc_id2name = self.id2name(product_ids)
        res = self.stringify_and_sort_result(
            product_ids, product_id2data, data_res, prec_qty, prec_cur_rounding,
            categ_id2name, uom_id2name, lot_id2data, loc_id2name)


        file_data = StringIO()
        workbook = xlsxwriter.Workbook(file_data)
        sheet = workbook.add_worksheet('Stock')
        # STYLES
        total_bg_color = '#faa03a'
        categ_bg_color = '#e1daf5'
        col_title_bg_color = '#fff9b4'
        regular_font_size = 10
        doc_title = workbook.add_format({
            'bold': True, 'font_size': regular_font_size + 10,
            'font_color': '#003b6f'})
        doc_subtitle = workbook.add_format({
            'bold': True, 'font_size': regular_font_size})
        col_title = workbook.add_format({
            'bold': True, 'bg_color': col_title_bg_color,
            'text_wrap': True, 'font_size': regular_font_size,
            'align': 'center',
            })
        total_title = workbook.add_format({
            'bold': True, 'text_wrap': True, 'font_size': regular_font_size + 2, 'align': 'right',
            'bg_color': total_bg_color})
        total_currency = workbook.add_format({'num_format': u'# ### ##0.00 €', 'bg_color': total_bg_color})
        regular_date = workbook.add_format({'num_format': 'dd/mm/yyyy'})
        regular_currency = workbook.add_format({'num_format': u'# ### ##0.00 €'})
        regular = workbook.add_format({})
        regular_small = workbook.add_format({'font_size': regular_font_size - 2})
        categ_title = workbook.add_format({
            'bold': True, 'bg_color': categ_bg_color, 'font_size': regular_font_size})
        categ_currency = workbook.add_format({
            'num_format': u'# ### ##0.00 €', 'bg_color': categ_bg_color})
        date_title = workbook.add_format({
            'bold': True, 'font_size': regular_font_size, 'align': 'right'})
        date_title_val = workbook.add_format({
            'bold': True, 'font_size': regular_font_size})

        cols = {
            'product_code': {'width': 16, 'style': regular, 'pos': -1, 'title': _('Product Code')},
            'product_name': {'width': 30, 'style': regular, 'pos': -1, 'title': _('Product Name')},
            'loc_name': {'width': 30, 'style': regular_small, 'pos': -1, 'title': _('Location Name')},
            'lot_name': {'width': 18, 'style': regular, 'pos': -1, 'title': _('Lot')},
            'expiry_date': {'width': 14, 'style': regular_date, 'pos': -1, 'title': _('Expiry Date')},
            'qty': {'width': 10, 'style': regular, 'pos': -1, 'title': _('Qty')},
            'uom_name': {'width': 6, 'style': regular_small, 'pos': -1, 'title': _('UoM')},
            'standard_price': {'width': 18, 'style': regular_currency, 'pos': -1, 'title': _('Price')},
            'subtotal': {'width': 18, 'style': regular_currency, 'pos': -1, 'title': _('Sub-total'), 'formula': True},
            'categ_subtotal': {'width': 18, 'style': regular_currency, 'pos': -1, 'title': _('Categ Sub-total'), 'formula': True},
            'categ_name': {'width': 30, 'style': regular_small, 'pos': -1, 'title': _('Product Category')},
            }
        categ_subtotal = self.categ_subtotal
        col_order = [
            'product_code',
            'product_name',
            split_by_location and 'loc_name' or False,
            split_by_lot and 'lot_name' or False,
            split_by_lot and hasattr(splo, 'expiry_date') and 'expiry_date' or False,
            'qty',
            'uom_name',
            'standard_price',
            'subtotal',
            categ_subtotal and 'categ_subtotal' or 'categ_name',
            ]

        j = 0
        for col in col_order:
            if col:
                cols[col]['pos'] = j
                cols[col]['pos_letter'] = chr(j + 97).upper()
                sheet.set_column(j, j, cols[col]['width'])
                j += 1

        # HEADER
        if past_date:
            # TODO take TZ into account
            stock_time_str = self.past_date
        else:
            stock_time_dt = fields.Datetime.context_timestamp(self, datetime.now())
            stock_time_str = fields.Datetime.to_string(stock_time_dt)
        i = 0
        sheet.write(i, 0, 'Odoo - Stock Valuation', doc_title)
        sheet.set_row(0, 26)
        i += 1
        sheet.write(i, 0, 'Valuation Date: %s' % stock_time_str, doc_subtitle)
#        sheet.write(i, 3, stock_time_str, date_title_val)
        i += 1
        sheet.write(i, 0, 'Stock location (children included): %s' % self.location_id.display_name, doc_subtitle)
        if self.categ_ids:
            i += 1
            sheet.write(i, 0, 'Product Categories: %s' % ', '.join([categ.display_name for categ in self.categ_ids]), doc_subtitle)

        # TITLE of COLS
        i += 2
        for col in cols.values():
            if col['pos'] >= 0:
                sheet.write(i, col['pos'], col['title'], col_title)

        i += 1
        sheet.write(i, cols['subtotal']['pos'] - 1, _("TOTAL:"), total_title)
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
        for categ_id in categ_ids:
            ctotal = 0.0
            categ_has_line = False
            if categ_subtotal:
                i += 1
                crow = i
                sheet.write(crow, 0, categ_id2name[categ_id], categ_title)
                for x in range(cols['categ_subtotal']['pos'] - 1):
                    sheet.write(crow, x + 1, '', categ_title)
            for l in filter(lambda x: x['categ_id'] == categ_id, res):
                i += 1
                total += l['subtotal']
                ctotal += l['subtotal']
                categ_has_line = True
                subtotal_formula = '=%s%d*%s%d' % (letter_qty, i + 1, letter_price, i + 1)
                sheet.write_formula(i, cols['subtotal']['pos'], subtotal_formula, regular_currency, l['subtotal'])
                for col_name, col in cols.items():
                    if col['pos'] >= 0 and not col.get('formula'):
                        sheet.write(i, col['pos'], l[col_name], col['style'])
            if categ_subtotal:
                if categ_has_line:
                    cformula = '=SUM(%s%d:%s%d)' % (letter_subtotal, crow + 2, letter_subtotal, i + 1)
                    sheet.write_formula(crow, cols['categ_subtotal']['pos'], cformula, categ_currency, float_round(ctotal, precision_rounding=prec_cur_rounding))
                else:
                    i -= 1  # re-write on previous categ
                    for x in range(cols['categ_subtotal']['pos']):
                        sheet.write(crow, x, '', regular)

        # Write total
        total_formula = '=SUM(%s%d:%s%d)' % (letter_subtotal, total_row + 2, letter_subtotal, i + 1)
        sheet.write_formula(total_row, cols['subtotal']['pos'], total_formula, total_currency, float_round(total, precision_rounding=prec_cur_rounding))

        workbook.close()
        file_data.seek(0)
        filename = 'Odoo_stock_%s.xlsx' % stock_time_str.replace(' ', '-').replace(':', '_')
        export_file_b64 = file_data.read().encode('base64')
        self.write({
            'state': 'done',
            'export_filename': filename,
            'export_file': export_file_b64,
            })
        action = self.env['ir.actions.act_window'].for_xml_id(
            'stock_valuation_xlsx', 'stock_valuation_xlsx_action')
        action.update({
            'res_id': self.id,
            })
        return action
