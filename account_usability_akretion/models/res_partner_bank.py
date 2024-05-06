# Copyright 2015-2022 Akretion France (http://www.akretion.com/)
# @author: Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    def name_get(self):
        res = []
        for acc in self:
            name = acc.acc_number
            if acc.currency_id:
                name = "%s (%s)" % (name, acc.currency_id.name)
            if acc.bank_id.name:
                name = "%s - %s" % (name, acc.bank_id.name)
            res += [(acc.id, name)]
        return res

