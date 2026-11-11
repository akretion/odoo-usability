# Copyright 2015-2026 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # tracking=True is handled in the 'mail' module, and base_usability
    # doesn't depend on 'mail', so adding tracking on res.partner fields
    # has been moved to mail_usability
    ref = fields.Char(copy=False)

    @api.constrains('parent_id', 'is_company')
    def _check_parent_child_partner(self):
        for partner in self:
            if partner.parent_id and partner.parent_id.parent_id:
                raise ValidationError(self.env._(
                    "Partner '%(partner)s' has a parent partner '%(parent_partner)s' "
                    "which itself has a parent partner '%(parent_parent_partner)s'. "
                    "This is not allowed.",
                    partner=partner.name,
                    parent_partner=partner.parent_id.name,
                    parent_parent_partner=partner.parent_id.parent_id.name))
            if partner.parent_id and partner.is_company:
                raise ValidationError(self.env._(
                    "Partner '%(partner)s' has a parent partner '%(parent_partner)s', "
                    "so it must be configured as an Individual (configuration as "
                    "Company is only for parent partners).",
                    partner=partner.name,
                    parent_partner=partner.parent_id.name,
                    ))

# I hope it's fixed now in v20 => comment
#    def _display_address(self, without_company=False):
#        '''Remove empty lines'''
#        res = super()._display_address(without_company=without_company)
#        while "\n\n" in res:
#            res = res.replace('\n\n', '\n')
#        return res

    # for reports
    def _display_full_address(
            self,
            details=['company', 'name', 'address', 'phone', 'mobile', 'email'],
            icon=True):
        self.ensure_one()
        # To make the icons work with py3o with PDF export, on the py3o server:
        # 1) sudo apt-get install fonts-symbola
        # 2) start libreoffice in xvfb (don't use --headless) (To confirm)
        if self.is_company:
            company = self.name
            name = False
            name_no_title = False
        else:
            company = self.parent_id and self.parent_id.is_company and\
                self.parent_id.name or False
            if hasattr(self, "name_with_title"):  # OCA module partner_title
                name = self.name_with_title
            else:
                name = self.name
            name_no_title = self.name
        siren = self._get_additional_identifier('FR_SIREN')
        siret = self._get_additional_identifier('FR_SIRET')
        options = {
            'name': {
                'value': name,
                },
            'company': {
                'value': company,
                },
            'name_no_title': {
                'value': name_no_title,
                },
            'phone': {
                'value': self.phone,
                # http://www.fileformat.info/info/unicode/char/1f4de/index.htm
                'icon': '\U0001F4DE',
                'label': self.env._('Tel:'),
                },
            'email': {
                'value': self.email,
                # http://www.fileformat.info/info/unicode/char/2709/index.htm
                'icon': '\u2709',
                'label': self.env._('E-mail:'),
                },
            'website': {
                'value': self.website,
                # http://www.fileformat.info/info/unicode/char/1f310/index.htm
                'icon': '\U0001f310',
                'label': self.env._('Website:'),
                },
            'address': {
                'value': self._display_address(without_name=True),
                },
            'vat': {
                'value': self.commercial_partner_id.vat,
                'label': self.env._('VAT Number:'),
                },
            'siren': {
                'value': siren,
                'label': self.env._("SIREN:"),
                },
            'siret': {
                'value': siret,
                'label': self.env._("SIRET:"),
                },
            'commercial_ref': {
                'value': self.commercial_partner_id.ref,
                'label': self.env._('Customer Number:'),
                },
            'ref': {
                'value': self.ref,
                'label': self.env._('Customer Number:'),
                },
            # Same with 'supplier_' prefix, to change the label
            'supplier_commercial_ref': {
                'value': self.commercial_partner_id.ref,
                'label': self.env._('Supplier Number:'),
                },
            'supplier_ref': {
                'value': self.ref,
                'label': self.env._('Supplier Number:'),
                },
            }
        if hasattr(self, "mobile"):  # OCA module partner_mobile
            options['mobile'] = {
                'value': self.mobile,
                # http://www.fileformat.info/info/unicode/char/1f4f1/index.htm
                'icon': '\U0001F4F1',
                'label': self.env._('Mobile:'),
                }
        res = []
        for detail in details:
            if options.get(detail) and options[detail]['value']:
                entry = options[detail]
                prefix = icon and entry.get('icon') or entry.get('label')
                if prefix:
                    res.append('%s %s' % (prefix, entry['value']))
                else:
                    res.append('%s' % entry['value'])
        res = '\n'.join(res)
        return res
