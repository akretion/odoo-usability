# Copyright 2015-2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from odoo.tools.misc import format_amount


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.model
    def generate_line(self, fields, options, icon=True, separator=' - '):
        assert fields
        assert options
        content = []
        for field in fields:
            value = False
            if isinstance(field, tuple) and len(field) == 2:
                value = field[0]
                label = field[1]
                uicon = False
            elif isinstance(field, str) and field in options:
                value = options[field]['value']
                label = options[field].get('label')
                uicon = options[field].get('icon')
            if value:
                prefix = icon and uicon or label
                if prefix:
                    content.append('%s %s' % (prefix, value))
                else:
                    content.append(value)
        line = separator.join(content)
        return line

    def _prepare_header_options(self):
        self.ensure_one()
        options = {
            'phone': {
                'value': self.phone,
                # http://www.fileformat.info/info/unicode/char/1f4de/index.htm
                'icon': '\U0001F4DE',
                'label': _('Tel:'),
                },
            'email': {
                'value': self.email,
                # http://www.fileformat.info/info/unicode/char/2709/index.htm
                'icon': '\u2709',
                'label': _('E-mail:'),
                },
            'website': {
                'value': self.website,
                'icon': '\U0001f310',
                'label': _('Website:'),
                },
            'vat': {
                'value': self.vat,
                'label': _('VAT:'),
                },
            'ape': {
                'value': hasattr(self, 'ape') and self.ape or False,
                'label': _('APE:'),
                },
            'siret': {
                'value': hasattr(self, 'siret') and self.siret or False,
                'label': _('SIRET:'),
                },
            'siren': {
                'value': hasattr(self, 'siren') and self.siren or False,
                'label': _('SIREN:'),
                },
            'rcs_siren': {
                'value': hasattr(self, 'siren') and self.siren and self.company_registry and f"{self.company_registry} {self.siren}",
                'label': 'RCS',
                },
            'eori': {
                'value': self._get_eori(),
                'label': _('EORI:'),
                },
            'capital': {
                # 'capital_amount' added by base_company_extension
                'value': hasattr(self, 'capital_amount') and self.capital_amount and format_amount(self.env, self.capital_amount, self.currency_id) or False,
                'label': _('Capital:'),
                },
            }
        # 'legal_type' added by base_company_extension
        if hasattr(self, 'legal_type') and self.legal_type:
            options['capital']['label'] = _('%s with a capital of') % self.legal_type
        return options

    def _get_eori(self):
        eori = False
        if self.partner_id.country_id.code == 'FR' and hasattr(self, 'siret') and self.siret:
            # Currently migrating from EORI-SIRET to EORI-SIREN :
            # https://www.pwcavocats.com/fr/ealertes/ealertes-france/2023/avril/reforme-numero-eori-siren-siret.html
            # But, for the moment, we continue to use EORI-SIRET
            eori = f'FR{self.siret}'
        return eori

    def _report_company_legal_name(self):
        '''Method inherited in the module base_company_extension'''
        self.ensure_one()
        return self.name

    def _report_header_line_details(self):
        """This method is designed to be inherited"""
        # I decided not to put email in the default header because only a few very small
        # companies have a generic company email address
        line_details = [['phone', 'website', 'rcs_siren', 'capital'], ['vat', 'siret', 'eori', 'ape']]
        return line_details

    # for reports
    def _display_report_header(
            self, line_details=None, icon=True, line_separator=' - '):
        self.ensure_one()
        if line_details is None:
            line_details = self._report_header_line_details()
        res = ''
        address = self.partner_id._display_address(without_company=True)
        address = address.replace('\n', ' - ')

        line1 = '%s - %s' % (self._report_company_legal_name(), address)
        lines = [line1]
        options = self._prepare_header_options()
        for details in line_details:
            line = self.generate_line(
                details, options, icon=icon, separator=line_separator)
            lines.append(line)
        res = '\n'.join(lines)
        return res
