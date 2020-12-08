# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.tools.misc import formatLang


class AccountPartialReconcile(models.Model):
    _inherit = "account.partial.reconcile"
    _rec_name = "id"

    def name_get(self):
        res = []
        for rec in self:
            # There is no seq for partial rec, so I simulate one with the ID
            # Prefix for full rec: 'A' (upper case)
            # Prefix for partial rec: 'a' (lower case)
            amount_fmt = formatLang(
                self.env, rec.amount, currency_obj=rec.company_currency_id)
            name = 'a%d (%s)' % (rec.id, amount_fmt)
            res.append((rec.id, name))
        return res
