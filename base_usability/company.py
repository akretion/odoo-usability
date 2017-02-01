# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, _


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
            elif isinstance(field, (str, unicode)) and field in options:
                value = options[field]['value']
                label = options[field].get('label')
                uicon = options[field].get('icon')
            if value:
                prefix = icon and uicon or label
                if prefix:
                    content.append(u'%s %s' % (prefix, value))
                else:
                    content.append(value)
        line = separator.join(content)
        return line

    @api.multi
    def _prepare_header_options(self):
        self.ensure_one()
        options = {
            'phone': {
                'value': self.phone,
                # http://www.fileformat.info/info/unicode/char/1f4de/index.htm
                'icon': u'\U0001F4DE',
                'label': _('Tel:')},
            'fax': {
                'value': self.fax,
                # http://www.fileformat.info/info/unicode/char/1f5b7/index.htm
                'icon': u'\U0001F5B7',
                'label': _('Fax:')},
            'email': {
                'value': self.email,
                # http://www.fileformat.info/info/unicode/char/2709/index.htm
                'icon': u'\u2709',
                'label': _('E-mail:')},
            'website': {
                'value': self.website,
                'icon': u'\U0001f310',
                'label': _('Website:')},
            'vat': {
                'value': self.vat,
                'label': _('TVA :')},  # TODO translate
            }
        return options

    def _report_company_legal_name(self):
        '''Method inherited in the module base_company_extension'''
        self.ensure_one()
        return self.name

    # for reports
    @api.multi
    def _display_report_header(
            self, line_details=[['phone', 'fax', 'website'], ['vat']],
            icon=True, line_separator=' - '):
        self.ensure_one()
        res = u''
        address = self.partner_id._display_address(without_company=True)
        address = address.replace('\n', u' - ')

        line1 = u'%s - %s' % (self._report_company_legal_name(), address)
        lines = [line1]
        options = self._prepare_header_options()
        for details in line_details:
            line = self.generate_line(
                details, options, icon=icon, separator=line_separator)
            lines.append(line)
        res = '\n'.join(lines)
        return res
