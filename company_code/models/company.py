# Copyright 2019 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def name_get(self):
        return self.env['res.company']._add_company_code(super())


class ResCompany(models.Model):
    _inherit = 'res.company'

    code = fields.Char(required=True)

    def _add_company_code(self, super_object):
        ""
        """ Helper function
            Add the `code` field to your name:

            def name_get(self):
                return self.env['res.company']._add_company_code(super())
        """
        records = super_object.__self__
        if records and records[0]._name == 'res.company':
            codes = {x.id: x.code for x in records}
        else:
            codes = {x.id: x['company_id']['code'] for x in records
                     if getattr(x, 'company_id')}
        res = [(elm[0], '%s (%s)' % (elm[1], codes[elm[0]] or ''))
               for elm in super_object.name_get()]
        print(res)
        return res

    def name_get(self):
        return self.env['res.company']._add_company_code(super())
