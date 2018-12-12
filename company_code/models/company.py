# Copyright 2019 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    code = fields.Char(
        required=True, default='CODE',
        help="Field used in object name as suffix")

    def _add_company_code(self, super_object):
        ""
        """ Add the `code` field to your _rec_name. Use it like that:

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
        return res

    def name_get(self):
        return self.env['res.company']._add_company_code(super())
