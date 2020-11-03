# -*- coding: utf-8 -*-
# Copyright 2020 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def sale_confirm_wizard_button(self):
        """This method is designed to be inherited.
        For example, inherit it if you don't want to start the wizard in
        some scenarios"""
        action = self.env.ref(
            'sale_confirm_wizard.sale_confirm_action').read()[0]
        return action
