# Copyright 2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools, Command, _
from odoo.exceptions import UserError
from datetime import datetime
from odoo.tools.misc import format_datetime


class CommissionResultXlsx(models.AbstractModel):
    _name = "report.commission_simple.report_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Commission Result XLSX"

    def generate_xlsx_report(self, workbook, data, objects):
        # for some strange reasons, lang is not kept in context
        self = self.with_context(lang=self.env.user.lang)
        result = objects[0]
        sheet = workbook.add_worksheet(result.date_range_id.name)
        styles = self._prepare_styles(workbook, result.company_id)
        title = _("Commissions of %(partner)s for period %(period)s", partner=result.partner_id.name, period=result.date_range_id.name)
        now_str = format_datetime(self.env, datetime.now())
        i = 0
        sheet.write(i, 0, title, styles['title'])
        sheet.write(i, 5, _('Generated from Odoo on %s by %s') % (now_str, self.env.user.name), styles['regular_small'])
        i += 1
        sheet.write(i, 0, _('Start Date'), styles['subtitle'])
        sheet.write(i, 1, result.date_start, styles['subtitle_date'])
        i += 1
        sheet.write(i, 0, _('End Date'), styles['subtitle'])
        sheet.write(i, 1, result.date_end, styles['subtitle_date'])
        i += 1
        sheet.write(i, 0, _('Currency'), styles['subtitle'])
        sheet.write(i, 1, result.company_id.currency_id.name, styles['subtitle'])
        i += 1
        sheet.write(i, 0, _('Base Total'), styles['subtitle'])
        sheet.write(i, 1, result.base_total, styles['subtitle_amount'])
        i += 1
        sheet.write(i, 0, _('Amount Total'), styles['subtitle'])
        sheet.write(i, 1, result.amount_total, styles['subtitle_amount'])
        i += 3
        cols = self._prepare_xlsx_cols()
        coldict = {}
        pos = 0
        for key, label, width, style_suffix in cols:
            coldict[key] = {
                "label": label,
                "width": width,
                "pos": pos,
                "style": style_suffix and f"regular_{style_suffix}" or "regular",
            }
            pos += 1
        # header
        for col_key, col_vals in coldict.items():
            sheet.write(i, col_vals['pos'], col_vals['label'], styles['col_title'])
            sheet.set_column(col_vals['pos'], col_vals['pos'], col_vals['width'])
        # table content
        for line in result._prepare_xlsx_lines():
            i += 1
            for col_key, value in line._prepare_commission_xlsx().items():
                sheet.write(i, coldict[col_key]["pos"], value, styles[coldict[col_key]["style"]])

    def _prepare_xlsx_cols(self):
        cols = [  # key, label, width, style_suffix
            ("inv.name", _("Invoice"), 14, False),
            ("inv.date", _("Invoice Date"), 11, "date"),
            ("inv.partner", _("Customer"), 50, False),
            ("product", _("Product"), 35, False),
            ("qty", _("Quantity"), 8, "qty"),
            ("uom", _("Unit"), 8, False),
            ("commission_base", _("Commission Base"), 14, "amount"),
            ("commission_rate", _("Commission Rate"), 10, "rate"),
            ("commission_amount", _("Commission Amount"), 14, "amount"),
            ]
        return cols

    def _prepare_styles(self, workbook, company):
        col_title_bg_color = '#eeeeee'
        prec_qty = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        prec_rate = self.env['decimal.precision'].precision_get('Commission Rate')
        prec_price = self.env['decimal.precision'].precision_get('Product Price')
        regular_font_size = 10
        date_format = "dd/mm/yyyy"  # TODO depend on lang
        num_format_amount = f"# ##0.{'0' * company.currency_id.decimal_places}"
        num_format_qty = f"# ##0.{'0' * prec_qty}"
        num_format_rate = f"""0.{'0' * prec_rate} " "%"""
        num_format_price = f"# ##0.{'0' * prec_price}"
        styles = {
            'title': workbook.add_format({
                'bold': True, 'font_size': regular_font_size + 10,
                'font_color': '#003b6f'}),
            'subtitle': workbook.add_format({
                'bold': True, 'font_size': regular_font_size}),
            'subtitle_date': workbook.add_format({
                'bold': True, 'font_size': regular_font_size, 'num_format': date_format}),
            'subtitle_amount': workbook.add_format({
                'bold': True, 'font_size': regular_font_size, 'num_format': num_format_amount}),
            'col_title': workbook.add_format({
                'bold': True, 'bg_color': col_title_bg_color,
                'text_wrap': True, 'font_size': regular_font_size,
                'align': 'center',
                }),
            'regular_date': workbook.add_format({'num_format': date_format}),
            'regular_amount': workbook.add_format({'num_format': num_format_amount}),
            'regular_rate': workbook.add_format({'num_format': num_format_rate}),
            'regular_qty': workbook.add_format({'num_format': num_format_qty}),
            'regular_price': workbook.add_format({'num_format': num_format_price}),
            'regular': workbook.add_format({}),
            'regular_small': workbook.add_format({'font_size': regular_font_size - 2}),
            }
        return styles
