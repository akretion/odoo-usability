# Copyright 2019-2022 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def prepare_update_wizard(self):
        self.ensure_one()
        wizard = self.env['account.move.update']
        res = wizard._prepare_default_get(self)
        action = self.env.ref(
            'account_invoice_update_wizard.account_invoice_update_action'
        ).read()[0]
        action['name'] = "Update Wizard"
        action['res_id'] = wizard.create(res).id
        return action
