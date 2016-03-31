# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

from openerp import models, api


class CrmMakeSale(models.TransientModel):
    _inherit = 'crm.make.sale'

    @api.multi
    def makeOrder(self):
        # the button to start this wizard is only available in form view
        # This code should be updated when we will have a _prepare method
        # in the create of the sale order
        self.ensure_one()
        value = super(CrmMakeSale, self).makeOrder()
        if value.get('res_model') == 'sale.order' and value.get('res_id'):
            so = self.env['sale.order'].browse(value['res_id'])
            so.lead_id = self._context.get('active_id')
        return value
