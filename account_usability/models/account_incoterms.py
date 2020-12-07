# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountIncoterms(models.Model):
    _inherit = 'account.incoterms'

    @api.depends('code', 'name')
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '[%s] %s' % (rec.code, rec.name)))
        return res
