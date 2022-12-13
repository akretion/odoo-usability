# Copyright 2015-2022 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountIncoterms(models.Model):
    _inherit = 'account.incoterms'

    _sql_constraints = [(
        'code_unique',
        'unique(code)',
        'This incoterm code already exists.')]

    @api.depends('code', 'name')
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '[%s] %s' % (rec.code, rec.name)))
        return res

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        if name and operator == 'ilike':
            recs = self.search([('code', '=ilike', name + '%')] + args, limit=limit)
            if recs:
                return recs.name_get()
        return super().name_search(name=name, args=args, operator=operator, limit=limit)
