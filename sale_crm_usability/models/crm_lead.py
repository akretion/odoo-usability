# Copyright 2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def action_view_sale_quotation(self):
        action = super().action_view_sale_quotation()
        if 'search_default_partner_id' in action['context']:
            action['context'].pop('search_default_partner_id')
        return action
