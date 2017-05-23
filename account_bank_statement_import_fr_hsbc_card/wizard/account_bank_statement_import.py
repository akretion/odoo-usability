# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import unicodecsv
from tempfile import TemporaryFile
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountBankStatementImport(models.TransientModel):
    _inherit = 'account.bank.statement.import'

    @api.model
    def _check_hsbc_card_csv(self, data_file):
        return data_file.strip().startswith(
            'Titulaire;Division;;Cpt Affaires;Num carte;')

    @api.model
    def _parse_file(self, data_file):
        """ Import a file in French HSBC CSV Credit card format"""
        hsbc_csv = self._check_hsbc_card_csv(data_file)
        if not hsbc_csv:
            return super(AccountBankStatementImport, self)._parse_file(
                data_file)
        transactions = []
        fileobj = TemporaryFile('w+')
        fileobj.write(data_file)
        fileobj.seek(0)
        reader = unicodecsv.DictReader(
            fileobj,
            fieldnames=[
                'company', 'division', 'empty', 'account',
                'card_num', 'title', 'lastname', 'firstname',
                'op_code', 'seller_type', 'seller', 'date', 'acc_date',
                'hour', 'city', 'code', 'label', 'local_amount',
                'local_currency', 'acc_amount', 'acc_currency'],
            delimiter=';',
            quoting=unicodecsv.QUOTE_MINIMAL,
            encoding='latin1')
        i = 0
        start_balance = end_balance = 0.0
        currency_code = 'EUR'
        account_number = 'HSBC_CARD_EUR'
        for line in reader:
            i += 1
            if i == 1:
                continue  # skip title line
            _logger.debug("Line %d: %s" % (i, line))
            if not line:
                continue
            # cleanup
            for key, value in line.iteritems():
                line[key] = value and value.strip() or False
            if not line['date'] or not line['acc_amount']:
                continue
            labels = [
                '%s %s' % (line['firstname'], line['lastname']),
                '%s (%s)' % (line['seller'], line['seller_type']),
                line['city']]
            if line['local_currency'] != currency_code:
                labels.append(
                    '%s %s' % (line['local_amount'], line['local_currency']))
            name = ', '.join(labels)
            amount = float(
                line['acc_amount'].replace(',', '.').replace(' ', '')) * -1
            end_balance += amount
            date_dt = datetime.strptime(line['date'], '%d/%m/%Y')
            date_str = fields.Date.to_string(date_dt)
            if line[u'acc_currency'] != currency_code:
                raise UserError(_(
                    "On line %d of the HSBC CSV file, the column "
                    "'Dev Cpt Affaires' contains '%s' instead of 'EUR'")
                    % (line['acc_currency'], i))
            vals_line = {
                'date': date_str,
                'name': name,
                'ref': False,
                'unique_import_id': '%s-%s-%.2f-%s' % (
                    date_str, line['hour'], amount, name),
                'amount': amount,
                'partner_id': False,
                }
            transactions.append(vals_line)
        vals_bank_statement = {
            'name': _('HSBC Cards'),
            'balance_start': start_balance,
            'balance_end_real': end_balance,
            'transactions': transactions,
            }
        fileobj.close()
        # from pprint import pprint
        # pprint(vals_bank_statement)
        return currency_code, account_number, [vals_bank_statement]
