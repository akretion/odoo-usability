# Copyright 2017-2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError
from datetime import datetime
from odoo.tools.misc import format_datetime
import pytz


class BankReconciliationXlsx(models.AbstractModel):
    _name = "report.bank.reconciliation.xlsx"
    _description = "Bank Reconciliation XLSX Report"
    _inherit = "report.report_xlsx.abstract"

    def _domain_add_move_state(self, wizard, domain):
        if wizard.move_state == 'posted':
            domain.append(('parent_state', '=', 'posted'))
        elif wizard.move_state == 'draft_posted':
            domain.append(('parent_state', 'in', ('draft', 'posted')))

    def _get_account_balance(self, account, wizard):
        domain = [
            ('account_id', '=', account.id),
            ('date', '<=', wizard.date),
            ('company_id', '=', wizard.company_id.id),
            ]
        self._domain_add_move_state(wizard, domain)
        res_rg = self.env['account.move.line'].read_group(domain, ['balance:sum'], [])
        account_bal = res_rg and res_rg[0].get('balance', 0.0) or 0.0
        return account_bal

    def _prepare_payment_move_lines(self, journal, account, wizard, unreconciled_only=True):
        domain = [
            ("company_id", "=", wizard.company_id.id),
            ("account_id", "=", account.id),
            ("journal_id", "=", journal.id),
            ("date", "<=", wizard.date),
            ]
        if unreconciled_only:
            limit_datetime_naive = datetime.combine(wizard.date, datetime.max.time())
            tz = pytz.timezone(self.env.user.tz)
            limit_datetime_aware = tz.localize(limit_datetime_naive)
            limit_datetime_utc = limit_datetime_aware.astimezone(pytz.utc)
            limit_datetime = limit_datetime_utc.replace(tzinfo=None)
            domain += [
                '|', ('full_reconcile_id', '=', False),
                ('full_reconcile_id.create_date', '>', limit_datetime)]
        self._domain_add_move_state(wizard, domain)
        mlines = self.env["account.move.line"].search(domain)
        res = []
        for mline in mlines:
            move = mline.move_id
            cpart = []
            for line in move.line_ids:
                if (
                    line.account_id != account
                    and line.account_id.code not in cpart
                ):
                    cpart.append(line.account_id.code)
            counterpart = " ,".join(cpart)
            res.append(
                {
                    "date": mline.date,
                    "ref": move.ref or "",
                    "label": mline.name,
                    "partner": mline.partner_id.display_name or "",
                    "amount": mline.balance,
                    "move_name": move.name,
                    "counterpart": counterpart,
                }
            )
        return res

    def _write_move_lines_block(self, jdi, row, account, add2total=True):
        sheet = jdi['sheet']
        style = jdi['style']
        style_suffix = not add2total and '_warn' or ''
        subtotal = 0.0
        mlines = self._prepare_payment_move_lines(jdi['journal'], account, jdi['wizard'])
        if mlines or add2total:
            sheet.write(row, 0, '%s  %s' % (account.name, account.code), style['title' + style_suffix])
            sheet.write(row, 1, "", style['title' + style_suffix])

        if not mlines:
            if add2total:
                sheet.write(row, 2, _("None"), style['none'])
            else:
                return
        else:
            row += 1
            col_labels = [
                _("Date"),
                _("Partner"),
                _("Amount"),
                _("Move Number"),
                _("Counter-part"),
                _("Ref."),
                _("Label"),
            ]
            col = 0
            for col_label in col_labels:
                sheet.write(row, col, col_label, style['col_header'])
                col += 1
            row += 1
            start_line = row + 1
            for mline in mlines:
                sheet.write(row, 0, mline["date"], style['regular_date'])
                sheet.write(row, 1, mline["partner"], style['regular'])
                sheet.write(row, 2, mline["amount"], style['currency'])
                sheet.write(row, 3, mline["move_name"], style['regular'])
                sheet.write(row, 4, mline["counterpart"], style['regular'])
                sheet.write(row, 5, mline["ref"], style['regular'])
                sheet.write(row, 6, mline["label"], style['regular'])
                subtotal += mline["amount"]
                row += 1
            end_line = row

            for col in range(1):
                sheet.write(row, col, "", style['title' + style_suffix])
            sheet.write(row, 1, _("Sub-total:") + ' ', style['title_right' + style_suffix])

            formula = '=SUM(%s%d:%s%d)' % (
                jdi['total_col'], start_line, jdi['total_col'], end_line)
            sheet.write_formula(row, 2, formula, style['currency_bg' + style_suffix], subtotal)
            if add2total:
                jdi['total'] += subtotal
                jdi['total_formula'] += '+%s%d' % (jdi['total_col'], row + 1)
        return row

    def generate_xlsx_report(self, workbook, data, wizard):
        if not wizard.journal_ids:
            raise UserError(_("No bank journal selected."))
        date_dt = wizard.date
        company = wizard.company_id
        style = self._get_style(workbook, company)
        move_state_label = dict(
            wizard.fields_get('move_state', 'selection')['move_state']['selection'])
        generated_on_label = _('Generated on %s') % format_datetime(
            self.env, datetime.utcnow())
        for journal in wizard.journal_ids:
            row = 0
            sheet = workbook.add_worksheet(journal.code or journal.name)
            jdi = {
                'wizard': wizard,
                'journal': journal,
                'style': style,
                'sheet': sheet,
                'total': 0.0,
                'total_formula': '=',
                'total_col': 'C',
                }
            sheet.write(
                row,
                0,
                _("Bank Reconciliation Report"),
                style['doc_title'],
            )
            row += 1
            sheet.write(row, 0, generated_on_label, style['small'])
            sheet.set_row(0, 26)
            sheet.set_column(0, 0, 10)
            sheet.set_column(1, 1, 35)
            sheet.set_column(2, 2, 15)
            sheet.set_column(3, 3, 15)
            sheet.set_column(4, 4, 25)
            sheet.set_column(5, 5, 30)
            sheet.set_column(6, 6, 60)
            row += 3
            sheet.write(row, 0, _("Company"), style['wizard_field'])
            sheet.write(row, 1, wizard.company_id.display_name, style['wizard_value'])
            row += 1
            sheet.write(row, 0, _("Date"), style['wizard_field'])
            sheet.write(row, 1, date_dt, style['wizard_value_date'])
            row += 1
            sheet.write(row, 0, _("Journal"), style['wizard_field'])
            sheet.write(row, 1, journal.display_name, style['wizard_value'])
            row += 1
            sheet.write(row, 0, _("Entries"), style['wizard_field'])
            sheet.write(row, 1, move_state_label[wizard.move_state], style['wizard_value'])

            # 1) Show balance of bank account
            row += 3
            bank_account = journal.default_account_id
            for col in range(1):
                sheet.write(row, col, "", style['title'])
            sheet.write(row, 1, _("Balance %s:") % bank_account.code + ' ', style['title_right'])
            account_bal = self._get_account_balance(bank_account, wizard)

            sheet.write(row, 2, account_bal, style['currency_bg'])
            jdi['total'] += account_bal
            jdi['total_formula'] += '%s%d' % (jdi['total_col'], row + 1)

            row += 2
            # 2) Show payment lines IN (debit)
            debit_account = journal.payment_debit_account_id
            row = self._write_move_lines_block(jdi, row, debit_account)
            row += 2
            # 3) Show payment lines OUT (credit)
            credit_account = journal.payment_credit_account_id
            row = self._write_move_lines_block(jdi, row, credit_account)
            row += 2

            for col in range(1):
                sheet.write(row, col, "", style['title'])
            sheet.write(row, 1, _("TOTAL:") + ' ', style['title_right'])
            sheet.write_formula(
                row, 2, jdi['total_formula'], style['currency_bg'], jdi['total'])
            row += 3

            # 4) Show suspense account lines
            row = self._write_move_lines_block(
                jdi, row, journal.suspense_account_id, add2total=False)

    def _get_style(self, workbook, company):
        style = {}
        font_size = 10
        light_grey = "#eeeeee"
        title_blue = "#e6e6fa"
        subtotal_orange = "#ffcc00"
        title_warn = "#ff9999"
        subtotal_warn = "#ffff99"
        light_purple = "#ffdeff"
        lang_code = self.env.user.lang
        lang = False
        if lang_code:
            lang = self.env["res.lang"].search([("code", "=", lang_code)])
        if not lang:
            lang = self.env["res.lang"].search([], limit=1)
        xls_date_format = (
            lang.date_format.replace("%Y", "yyyy")
            .replace("%m", "mm")
            .replace("%d", "dd")
            .replace("%y", "yy")
        )

        style['doc_title'] = workbook.add_format(
            {"bold": True, "font_size": font_size + 4})
        style['small'] = workbook.add_format({"font_size": font_size - 3})
        style['col_header'] = workbook.add_format(
            {
                "bold": True,
                "bg_color": light_grey,
                "text_wrap": True,
                "font_size": font_size,
                "align": "center",
            }
        )
        title_style = {
            "bold": True,
            "bg_color": title_blue,
            "font_size": font_size,
            "align": "left",
            }
        style['title_right'] = workbook.add_format(dict(title_style, align="right"))
        style['title'] = workbook.add_format(dict(title_style))
        style['wizard_field'] = workbook.add_format(dict(title_style, bg_color=light_grey))
        wizard_value_style = {
                "bg_color": light_purple,
                "bold": True,
                "font_size": font_size,
                "align": "left",
            }

        style['wizard_value'] = workbook.add_format(wizard_value_style)
        style['wizard_value_date'] = workbook.add_format(
            dict(wizard_value_style, num_format=xls_date_format))
        style['none'] = workbook.add_format(
            {"bold": True, "font_size": font_size, "align": "right", "bg_color": subtotal_orange}
        )
        # WARN for suspense account
        style['title_warn'] = workbook.add_format(
            dict(title_style, align="left", bg_color=title_warn))
        style['title_right_warn'] = workbook.add_format(
            dict(title_style, align="right", bg_color=title_warn))
        style['regular'] = workbook.add_format({"font_size": font_size})
        if "%" in xls_date_format:
            # fallback
            xls_date_format = "yyyy-mm-dd"
        style['regular_date'] = workbook.add_format(
            {"num_format": xls_date_format, "font_size": font_size, "align": "left"}
        )
        cur_format = "#,##0.00 %s" % (
            company.currency_id.symbol or company.currency_id.name
        )
        # It seems that Excel replaces automatically the decimal
        # and thousand separator by those of the language under which
        # Excel runs
        currency_style = {"num_format": cur_format, "font_size": font_size}
        style['currency'] = workbook.add_format(currency_style)
        style['currency_bg'] = workbook.add_format(
            dict(currency_style, bg_color=subtotal_orange))
        style['currency_bg_warn'] = workbook.add_format(
            dict(currency_style, bg_color=subtotal_warn))
        return style
