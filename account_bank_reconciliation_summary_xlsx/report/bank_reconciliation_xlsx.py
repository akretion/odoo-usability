# Copyright 2017-2024 Akretion France (http://www.akretion.com/)
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

    def _prepare_payment_move_lines(self, jdi, account, unreconciled_only=True):
        domain = [
            ("company_id", "=", jdi['company'].id),
            ("account_id", "=", account.id),
            ("journal_id", "=", jdi['journal'].id),
            ("date", "<=", jdi['wizard'].date),
            ]
        if jdi['wizard'].move_state == 'posted':
            domain.append(('parent_state', '=', 'posted'))
        elif jdi['wizard'].move_state == 'draft_posted':
            domain.append(('parent_state', 'in', ('draft', 'posted')))
        if unreconciled_only:
            limit_datetime_naive = datetime.combine(jdi['wizard'].date, datetime.max.time())
            tz = pytz.timezone(self.env.user.tz)
            limit_datetime_aware = tz.localize(limit_datetime_naive)
            limit_datetime_utc = limit_datetime_aware.astimezone(pytz.utc)
            limit_datetime = limit_datetime_utc.replace(tzinfo=None)
            domain += [
                '|', ('full_reconcile_id', '=', False),
                ('full_reconcile_id.create_date', '>', limit_datetime)]
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
            if jdi['currency'] == mline.currency_id:
                amount = mline.amount_currency
            else:
                amount = mline.currency_id._convert(
                    mline.amount_currency, jdi['currency'], jdi['company'], mline.date)
            res.append(
                {
                    "date": mline.date,
                    "ref": move.ref or "",
                    "label": mline.name,
                    "partner": mline.partner_id.display_name or "",
                    "amount": amount,
                    "move_name": move.name,
                    "counterpart": counterpart,
                }
            )
        return res

    def _write_move_lines_block(self, jdi, row, account, add2total=True):
        # Returns row
        # For suspense lines, it may not add any cells if there are no suspense lines
        # => in this case, it doesn't increment row
        # If it adds cells, it returns row + 2 to add 2 empty rows at the end
        sheet = jdi['sheet']
        style = jdi['style']
        style_suffix = not add2total and '_warn' or ''
        subtotal = 0.0
        mlines = self._prepare_payment_move_lines(jdi, account)
        if mlines or add2total:
            sheet.write(row, 0, '%s  %s' % (account.name, account.code), style[f"title{style_suffix}"])
            sheet.write(row, 1, "", style[f"title{style_suffix}"])

        if not mlines:
            if add2total:
                sheet.write(row, 2, _("None"), style['none'])
            else:
                return row
        else:
            row += 1
            col_labels = [
                _("Date"),
                _("Partner"),
                _("Amount"),
                _("Journal Entry"),
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
                sheet.write(row, 2, mline["amount"], style[jdi['currency']])
                sheet.write(row, 3, mline["move_name"], style['regular'])
                sheet.write(row, 4, mline["counterpart"], style['regular'])
                sheet.write(row, 5, mline["ref"], style['regular'])
                sheet.write(row, 6, mline["label"], style['regular'])
                subtotal += mline["amount"]
                row += 1
            end_line = row

            for col in range(1):
                sheet.write(row, col, "", style[f"title{style_suffix}"])
            sheet.write(row, 1, _("Sub-total:") + ' ', style[f"title_right{style_suffix}"])

            formula = f"=SUM({jdi['total_col']}{start_line}:{jdi['total_col']}{end_line})"
            sheet.write_formula(row, 2, formula, style[f"{jdi['currency']}_bg{style_suffix}"], subtotal)
            if add2total:
                jdi['total'] += subtotal
                jdi['total_formula'] += f"+{jdi['total_col']}{row + 1}"
        return row + 2

    def generate_xlsx_report(self, workbook, data, wizard):
        lang = self.env.user.lang
        self = self.with_context(lang=lang)
        wizard = wizard.with_context(lang=lang)
        if not wizard.journal_ids:
            raise UserError(_("No bank journal selected."))
        date_dt = wizard.date
        company = wizard.company_id
        style = self._get_style(workbook, company)
        move_state_label = dict(
            wizard.fields_get('move_state', 'selection')['move_state']['selection'])
        generated_on_label = _('Generated from Odoo on %s by %s') % (
            format_datetime(self.env, datetime.utcnow()),
            self.env.user.name)
        for journal in wizard.journal_ids:
            row = 0
            sheet = workbook.add_worksheet(journal.code or journal.name)
            bank_account = journal.default_account_id
            jdi = {
                'wizard': wizard,
                'company': company,
                'journal': journal,
                'currency': journal.currency_id or company.currency_id,
                'bank_account': bank_account,
                'style': style,
                'workbook': workbook,
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
            sheet.write(row, 1, company.display_name, style['wizard_value'])
            row += 1
            sheet.write(row, 0, _("Date"), style['wizard_field'])
            sheet.write(row, 1, date_dt, style['wizard_value_date'])
            row += 1
            sheet.write(row, 0, _("Journal"), style['wizard_field'])
            sheet.write(row, 1, journal.display_name, style['wizard_value'])
            row += 1
            sheet.write(row, 0, _("Currency"), style['wizard_field'])
            sheet.write(row, 1, jdi['currency'].name, style['wizard_value'])
            row += 1
            sheet.write(row, 0, _("Entries"), style['wizard_field'])
            sheet.write(row, 1, move_state_label[wizard.move_state], style['wizard_value'])

            # Setup check
            if journal.currency_id and journal.currency_id != company.currency_id:
                if journal.currency_id != bank_account.currency_id:
                    raise UserError(_(
                        "On bank journal %(journal)s which is configured with currency "
                        "%(journal_currency)s, the account %(account)s must be configured "
                        "with the same currency (current account currency: %(account_currency)s).",
                        journal=journal.display_name,
                        journal_currency=journal.currency_id.name,
                        account=bank_account.display_name,
                        account_currency=bank_account.currency_id.name or _('None')))
                bad_line_count = self.env['account.move.line'].search_count([
                    ('company_id', '=', company.id),
                    ('journal_id', '=', journal.id),
                    ('account_id', '=', bank_account.id),
                    ('currency_id', '!=', jdi['currency'].id),
                    ])
                if bad_line_count:
                    raise UserError(_(
                        "The are %(count)s journal items in account %(account)s "
                        "that have a currency other than %(currency)s or where "
                        "currency is not set.",
                        count=bad_line_count,
                        account=bank_account.display_name,
                        currency=jdi['currency'].name))

            # 1) Show balance of bank account
            row += 3
            for col in range(1):
                sheet.write(row, col, "", style['title'])
            sheet.write(row, 1, _("Balance %s:") % bank_account.code + ' ', style['title_right'])
            if wizard.move_state == 'posted':
                domain = [('parent_state', '=', 'posted')]
            else:
                # by default, the native method _get_journal_bank_account_balance()
                # has ('parent_state', '!=', 'cancel')
                domain = None
            account_bal, nb_lines = journal._get_journal_bank_account_balance(domain=domain)

            sheet.write(row, 2, account_bal, style[f"{jdi['currency']}_bg"])
            jdi['total'] += account_bal
            jdi['total_formula'] += f"{jdi['total_col']}{row + 1}"

            row += 2
            # 2) Show payment lines IN (debit)
            debit_account = journal.payment_debit_account_id
            row = self._write_move_lines_block(jdi, row, debit_account)
            # 3) Show payment lines OUT (credit)
            credit_account = journal.payment_credit_account_id
            row = self._write_move_lines_block(jdi, row, credit_account)

            for col in range(1):
                sheet.write(row, col, "", style['title'])
            sheet.write(row, 1, _("TOTAL:") + ' ', style['title_right'])
            sheet.write_formula(
                row, 2, jdi['total_formula'], style[f"{jdi['currency']}_bg"], jdi['total'])
            total_row = row
            row += 2

            # 4) Show suspense account lines
            row = self._write_move_lines_block(
                jdi, row, journal.suspense_account_id, add2total=False)

            # Static cells
            for col in range(1):
                sheet.write(row, col, "", style['title'])
            sheet.write(row, 1, _("Bank Balance:") + ' ', style['title_right'])
            sheet.write(row, 2, 0, style[f"{jdi['currency']}_bg_manual"])
            bank_bal_row = row
            row += 2
            for col in range(1):
                sheet.write(row, col, "", style['title'])
            sheet.write(row, 1, _("Difference:") + ' ', style['title_right'])
            sheet.write_formula(
                row, 2, f"={jdi['total_col']}{total_row + 1}-{jdi['total_col']}{bank_bal_row + 1}",
                style[f"{jdi['currency']}_bg"], jdi['total'])
            row += 2
            for col in range(1):
                sheet.write(row, col, "", style['title'])
            sheet.write(row, 1, _("Justification:") + ' ', style['title_right'])
            justif_lines = 6
            sheet.write_formula(
                row, 2, f"=SUM({jdi['total_col']}{row+3}:{jdi['total_col']}{row+3+justif_lines-1})",
                style[f"{jdi['currency']}_bg"], 0)
            row += 1
            col_labels = [
                _("Date"),
                _("Description"),
                _("Amount"),
            ]
            col = 0
            for col_label in col_labels:
                sheet.write(row, col, col_label, style['col_header'])
                col += 1
            for x in range(justif_lines):
                row += 1
                sheet.write(row, 0, "", style['regular_date'])
                sheet.write(row, 1, "", style['regular'])
                sheet.write(row, 2, "", style[jdi['currency']])

    def _get_style(self, workbook, company):
        style = {}
        font_size = 10
        light_grey = "#eeeeee"
        light_blue = "#e0edff"
        subtotal_orange = "#ffcc00"
        subtotal_warn = "#ffff99"
        amount_manual = "#ffeeab"
        title_warn = "#ff9999"
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
            "bg_color": light_blue,
            "font_size": font_size,
            "align": "left",
            }
        style['title_right'] = workbook.add_format(dict(title_style, align="right"))
        style['title'] = workbook.add_format(dict(title_style))
        style['wizard_field'] = workbook.add_format(dict(title_style, bg_color=light_grey))
        wizard_value_style = {
                "bg_color": light_blue,
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
        style['regular'] = workbook.add_format({"font_size": font_size, "border": 1})
        if "%" in xls_date_format:
            # fallback
            xls_date_format = "yyyy-mm-dd"
        style['regular_date'] = workbook.add_format(
            {"num_format": xls_date_format, "font_size": font_size, "align": "left", "border": 1}
        )
        for currency in self.env['res.currency'].search([]):
            symbol = currency.symbol or currency.name
            decimals = '0' * currency.decimal_places
            if currency.position == 'before':
                cur_format = f"{symbol} #,##0.{decimals}"
            else:
                cur_format = f"#,##0.{decimals} {symbol}"
            # It seems that Excel replaces automatically the decimal
            # and thousand separator by those of the language under which
            # Excel runs
            currency_style = {"num_format": cur_format, "font_size": font_size}
            style[currency] = workbook.add_format(dict(currency_style, border=1))
            style[f'{currency}_bg'] = workbook.add_format(
                dict(currency_style, bg_color=subtotal_orange))
            style[f'{currency}_bg_warn'] = workbook.add_format(
                dict(currency_style, bg_color=subtotal_warn))
            style[f'{currency}_bg_manual'] = workbook.add_format(
                dict(currency_style, bg_color=amount_manual))
        return style
