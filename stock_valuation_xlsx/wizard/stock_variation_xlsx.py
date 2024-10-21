# Copyright 2020-2024 Akretion France (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_round
from io import BytesIO
import base64
from datetime import datetime
import xlsxwriter
import logging
logger = logging.getLogger(__name__)


class StockVariationXlsx(models.TransientModel):
    _name = 'stock.variation.xlsx'
    _check_company_auto = True
    _description = 'Generate XLSX report for stock valuation variation between 2 dates'

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
        help="Leave this fields empty to have a stock valuation for all your products.")
    start_date = fields.Datetime(
        string='Start Date', required=True)
    standard_price_start_date_type = fields.Selection([
        ('start', 'Start Date'),
        ('present', 'Current'),
        ], default='start', required=True,
        string='Cost Price for Start Date')
    end_date_type = fields.Selection([
        ('present', 'Present'),
        ('past', 'Past'),
        ], string='End Date Type', default='present', required=True)
    end_date = fields.Datetime(
        string='End Date', default=fields.Datetime.now)
    standard_price_end_date_type = fields.Selection([
        ('end', 'End Date'),
        ('present', 'Current'),
        ], default='end', string='Cost Price for End Date', required=True)
    categ_subtotal = fields.Boolean(
        string='Subtotals per Categories', default=True,
        help="Show a subtotal per product category.")

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
        present = fields.Datetime.now()
        if self.end_date_type == 'past':
            if not self.end_date:
                raise UserError(_("End Date is missing."))
            if self.end_date > present:
                raise UserError(_("The end date must be in the past."))
            if self.end_date <= self.start_date:
                raise UserError(_("The start date must be before the end date."))
        else:
            if self.start_date >= present:
                raise UserError(_("The start date must be in the past."))
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
        # Should we also add inactive products ??
        products = self.env['product.product'].search(domain)
        return products.ids

    def compute_data_from_stock(self, product_ids, prec_qty, start_date, end_date_type, end_date, company_id):
        self.ensure_one()
        logger.debug('Start compute_data_from_stock past_date=%s end_date_type=%s, end_date=%s', start_date, end_date_type, end_date)
        ppo = self.env['product.product']
        smo = self.env['stock.move']
        sqo = self.env['stock.quant']
        ppo_loc = ppo.with_context(location=self.location_id.id).with_company(company_id)
        # Inspired by odoo/addons/stock/models/product.py
        # method _compute_quantities_dict()
        domain_quant_loc, domain_move_in_loc, domain_move_out_loc = ppo_loc._get_domain_locations()
        domain_quant = [('product_id', 'in', product_ids)] + domain_quant_loc
        domain_move_in = [('product_id', 'in', product_ids), ('state', '=', 'done')] + domain_move_in_loc
        domain_move_out = [('product_id', 'in', product_ids), ('state', '=', 'done')] + domain_move_out_loc
        quants_res = dict((item['product_id'][0], item['quantity']) for item in sqo._read_group(domain_quant, ['product_id', 'quantity'], ['product_id'], orderby='id'))
        domain_move_in_start_to_end = [('date', '>', start_date)] + domain_move_in
        domain_move_out_start_to_end = [('date', '>', start_date)] + domain_move_out
        if end_date_type == 'past':

            domain_move_in_end_to_present = [('date', '>', end_date)] + domain_move_in
            domain_move_out_end_to_present = [('date', '>', end_date)] + domain_move_out
            moves_in_res_end_to_present = dict((item['product_id'][0], item['product_qty']) for item in smo._read_group(domain_move_in_end_to_present, ['product_id', 'product_qty'], ['product_id'], orderby='id'))
            moves_out_res_end_to_present = dict((item['product_id'][0], item['product_qty']) for item in smo._read_group(domain_move_out_end_to_present, ['product_id', 'product_qty'], ['product_id'], orderby='id'))

            domain_move_in_start_to_end += [('date', '<', end_date)]
            domain_move_out_start_to_end += [('date', '<', end_date)]

        moves_in_res_start_to_end = dict((item['product_id'][0], item['product_qty']) for item in smo._read_group(domain_move_in_start_to_end, ['product_id', 'product_qty'], ['product_id'], orderby='id'))
        moves_out_res_start_to_end = dict((item['product_id'][0], item['product_qty']) for item in smo._read_group(domain_move_out_start_to_end, ['product_id', 'product_qty'], ['product_id'], orderby='id'))

        product_data = {}  # key = product_id , value = dict
        for product in ppo.browse(product_ids):
            end_qty = quants_res.get(product.id, 0.0)
            if end_date_type == 'past':
                end_qty += moves_out_res_end_to_present.get(product.id, 0.0) - moves_in_res_end_to_present.get(product.id, 0.0)
            in_qty = moves_in_res_start_to_end.get(product.id, 0.0)
            out_qty = moves_out_res_start_to_end.get(product.id, 0.0)
            start_qty = end_qty - in_qty + out_qty
            if (
                    not float_is_zero(start_qty, precision_digits=prec_qty) or
                    not float_is_zero(in_qty, precision_digits=prec_qty) or
                    not float_is_zero(out_qty, precision_digits=prec_qty) or
                    not float_is_zero(end_qty, precision_digits=prec_qty)):
                product_data[product.id] = {
                    'product_id': product.id,
                    'start_qty': start_qty,
                    'in_qty': in_qty,
                    'out_qty': out_qty,
                    'end_qty': end_qty,
                    }
        logger.debug('End compute_data_from_stock')
        return product_data

    def stringify_and_sort_result(
            self, product_data, product_id2data, prec_qty, prec_price, prec_cur_rounding,
            categ_id2name, uom_id2name):
        logger.debug('Start stringify_and_sort_result')
        res = []
        for product_id, l in product_data.items():
            start_qty = float_round(l['start_qty'], precision_digits=prec_qty)
            in_qty = float_round(l['in_qty'], precision_digits=prec_qty)
            out_qty = float_round(l['out_qty'], precision_digits=prec_qty)
            end_qty = float_round(l['end_qty'], precision_digits=prec_qty)
            start_standard_price = float_round(
                product_id2data[product_id]['start_standard_price'],
                precision_digits=prec_price)
            end_standard_price = float_round(
                product_id2data[product_id]['end_standard_price'],
                precision_digits=prec_price)
            start_subtotal = float_round(
                start_standard_price * start_qty, precision_rounding=prec_cur_rounding)
            end_subtotal = float_round(
                end_standard_price * end_qty, precision_rounding=prec_cur_rounding)
            variation = float_round(
                end_subtotal - start_subtotal, precision_rounding=prec_cur_rounding)
            res.append(dict(
                product_id2data[product_id],
                product_name=product_id2data[product_id]['name'],
                start_qty=start_qty,
                start_standard_price=start_standard_price,
                start_subtotal=start_subtotal,
                in_qty=in_qty,
                out_qty=out_qty,
                end_qty=end_qty,
                end_standard_price=end_standard_price,
                end_subtotal=end_subtotal,
                variation=variation,
                uom_name=uom_id2name[product_id2data[product_id]['uom_id']],
                categ_name=categ_id2name[product_id2data[product_id]['categ_id']],
                ))
        sort_res = sorted(res, key=lambda x: x['product_name'])
        logger.debug('End stringify_and_sort_result')
        return sort_res

    def generate(self):
        self.ensure_one()
        logger.debug('Start generate XLSX stock variation report')
        svxo = self.env['stock.valuation.xlsx']
        prec_qty = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        prec_price = self.env['decimal.precision'].precision_get('Product Price')
        company = self.company_id
        company_id = company.id
        prec_cur_rounding = company.currency_id.rounding
        self._check_config()

        product_ids = self.get_product_ids()
        if not product_ids:
            raise UserError(_("There are no products to analyse."))

        product_data = self.compute_data_from_stock(
            product_ids, prec_qty, self.start_date, self.end_date_type, self.end_date,
            company_id)
        standard_price_start_date = standard_price_end_date = False
        if self.standard_price_start_date_type == 'start':
            standard_price_start_date = self.start_date
        if self.standard_price_end_date_type == 'end' and self.end_date_type == 'past':
            standard_price_end_date = self.end_date

        product_id2data = svxo.compute_product_data(
            company_id, list(product_data.keys()), {
                'start_standard_price': standard_price_start_date,
                'end_standard_price': standard_price_end_date})
        categ_id2name = svxo.product_categ_id2name(self.categ_ids)
        uom_id2name = svxo.uom_id2name()
        res = self.stringify_and_sort_result(
            product_data, product_id2data, prec_qty, prec_price, prec_cur_rounding,
            categ_id2name, uom_id2name)

        logger.debug('Start create XLSX workbook')
        file_data = BytesIO()
        workbook = xlsxwriter.Workbook(file_data)
        sheet = workbook.add_worksheet('Stock_Variation')
        styles = svxo._prepare_styles(workbook, company, prec_price)
        cols = self._prepare_cols()
        categ_subtotal = self.categ_subtotal
        # remove cols that we won't use
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
        start_time_utc_dt = self.start_date
        start_time_dt = fields.Datetime.context_timestamp(self, start_time_utc_dt)
        start_time_str = fields.Datetime.to_string(start_time_dt)
        if self.end_date_type == 'past':
            end_time_utc_dt = self.end_date
            end_time_dt = fields.Datetime.context_timestamp(self, end_time_utc_dt)
            end_time_str = fields.Datetime.to_string(end_time_dt)
        else:
            end_time_str = now_str
        if standard_price_start_date:
            standard_price_start_date_str = start_time_str
        else:
            standard_price_start_date_str = now_str
        if standard_price_end_date:
            standard_price_end_date_str = end_time_str
        else:
            standard_price_end_date_str = now_str
        i = 0
        sheet.write(i, 0, 'Odoo - Stock Valuation Variation', styles['doc_title'])
        sheet.set_row(0, 26)
        i += 1
        sheet.write(i, 0, 'Start Date: %s' % start_time_str, styles['doc_subtitle'])
        i += 1
        sheet.write(i, 0, 'Cost Price Start Date: %s' % standard_price_start_date_str, styles['doc_subtitle'])
        i += 1
        sheet.write(i, 0, 'End Date: %s' % end_time_str, styles['doc_subtitle'])
        i += 1
        sheet.write(i, 0, 'Cost Price End Date: %s' % standard_price_end_date_str, styles['doc_subtitle'])
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
        sheet.write(i, 0, _("TOTALS:"), styles['total_title'])
        total_row = i

        # LINES
        if categ_subtotal:
            categ_ids = categ_id2name.keys()
        else:
            categ_ids = [0]

        start_total = end_total = variation_total = 0.0
        letter_start_qty = cols['start_qty']['pos_letter']
        letter_in_qty = cols['in_qty']['pos_letter']
        letter_out_qty = cols['out_qty']['pos_letter']
        letter_end_qty = cols['end_qty']['pos_letter']
        letter_start_price = cols['start_standard_price']['pos_letter']
        letter_end_price = cols['end_standard_price']['pos_letter']
        letter_start_subtotal = cols['start_subtotal']['pos_letter']
        letter_end_subtotal = cols['end_subtotal']['pos_letter']
        letter_variation = cols['variation']['pos_letter']
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
                start_total += l['start_subtotal']
                end_total += l['end_subtotal']
                variation_total += l['variation']
                ctotal += l['variation']
                categ_has_line = True
                end_qty_formula = '=%s%d+%s%d-%s%d' % (letter_start_qty, i + 1, letter_in_qty, i + 1, letter_out_qty, i + 1)
                sheet.write_formula(i, cols['end_qty']['pos'], end_qty_formula, styles[cols['end_qty']['style']], l['end_qty'])
                start_subtotal_formula = '=%s%d*%s%d' % (letter_start_qty, i + 1, letter_start_price, i + 1)
                sheet.write_formula(i, cols['start_subtotal']['pos'], start_subtotal_formula, styles[cols['start_subtotal']['style']], l['start_subtotal'])
                end_subtotal_formula = '=%s%d*%s%d' % (letter_end_qty, i + 1, letter_end_price, i + 1)
                sheet.write_formula(i, cols['end_subtotal']['pos'], end_subtotal_formula, styles[cols['end_subtotal']['style']], l['end_subtotal'])
                variation_formula = '=%s%d-%s%d' % (letter_end_subtotal, i + 1, letter_start_subtotal, i + 1)
                sheet.write_formula(i, cols['variation']['pos'], variation_formula, styles[cols['variation']['style']], l['variation'])
                sheet.write_formula(i, cols['end_subtotal']['pos'], end_subtotal_formula, styles[cols['end_subtotal']['style']], l['end_subtotal'])
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

                    cformula = '=SUM(%s%d:%s%d)' % (letter_variation, crow + 2, letter_variation, i + 1)
                    sheet.write_formula(crow, cols['categ_subtotal']['pos'], cformula, styles['categ_currency'], float_round(ctotal, precision_rounding=prec_cur_rounding))
                else:
                    i -= 1  # go back to skipped line

        # Write total
        start_total_formula = '=SUM(%s%d:%s%d)' % (letter_start_subtotal, total_row + 2, letter_start_subtotal, i + 1)
        sheet.write_formula(total_row, cols['start_subtotal']['pos'], start_total_formula, styles['total_currency'], float_round(start_total, precision_rounding=prec_cur_rounding))
        end_total_formula = '=SUM(%s%d:%s%d)' % (letter_end_subtotal, total_row + 2, letter_end_subtotal, i + 1)
        sheet.write_formula(total_row, cols['end_subtotal']['pos'], end_total_formula, styles['total_currency'], float_round(end_total, precision_rounding=prec_cur_rounding))
        variation_total_formula = '=SUM(%s%d:%s%d)' % (letter_variation, total_row + 2, letter_variation, i + 1)
        sheet.write_formula(total_row, cols['variation']['pos'], variation_total_formula, styles['total_currency'], float_round(variation_total, precision_rounding=prec_cur_rounding))

        workbook.close()
        logger.debug('End create XLSX workbook')
        file_data.seek(0)
        filename = 'Odoo_stock_%s_%s.xlsx' % (
            start_time_str.replace(' ', '-').replace(':', '_'),
            end_time_str.replace(' ', '-').replace(':', '_'))
        export_file_b64 = base64.b64encode(file_data.read())
        self.write({
            'export_filename': filename,
            'export_file': export_file_b64,
            })
        action = {
            'name': _('Stock Variation XLSX'),
            'type': 'ir.actions.act_url',
            'url': "web/content/?model=%s&id=%d&filename_field=export_filename&"
                   "field=export_file&download=true&filename=%s" % (
                       self._name, self.id, self.export_filename),
            'target': 'new',
            }
        return action

    def _prepare_cols(self):
        cols = {
            'default_code': {'width': 18, 'style': 'regular', 'sequence': 10, 'title': _('Product Code')},
            'barcode': {'width': 18, 'style': 'regular', 'sequence': 15, 'title': _('Product Barcode')},
            'product_name': {'width': 40, 'style': 'regular', 'sequence': 20, 'title': _('Product Name')},
            'uom_name': {'width': 5, 'style': 'regular_small', 'sequence': 30, 'title': _('UoM')},
            'start_qty': {'width': 8, 'style': 'regular', 'sequence': 40, 'title': _('Start Qty')},
            'start_standard_price': {'width': 14, 'style': 'regular_price_currency', 'sequence': 50, 'title': _('Start Cost Price')},
            'start_subtotal': {'width': 16, 'style': 'regular_currency', 'sequence': 60, 'title': _('Start Value'), 'formula': True},
            'in_qty': {'width': 8, 'style': 'regular', 'sequence': 70, 'title': _('In Qty')},
            'out_qty': {'width': 8, 'style': 'regular', 'sequence': 80, 'title': _('Out Qty')},
            'end_qty': {'width': 8, 'style': 'regular', 'sequence': 90, 'title': _('End Qty'), 'formula': True},
            'end_standard_price': {'width': 14, 'style': 'regular_price_currency', 'sequence': 100, 'title': _('End Cost Price')},
            'end_subtotal': {'width': 16, 'style': 'regular_currency', 'sequence': 110, 'title': _('End Value'), 'formula': True},
            'variation': {'width': 16, 'style': 'regular_currency', 'sequence': 120, 'title': _('Variation'), 'formula': True},
            'categ_subtotal': {'width': 16, 'style': 'regular_currency', 'sequence': 130, 'title': _('Categ Sub-total'), 'formula': True},
            'categ_name': {'width': 40, 'style': 'regular_small', 'sequence': 140, 'title': _('Product Category')},
            }
        return cols
