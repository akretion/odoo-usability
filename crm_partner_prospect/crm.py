# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.multi
    def _lead_create_contact(self, name, is_company, parent_id=False):
        partner = super(CrmLead, self)._lead_create_contact(
            name, is_company, parent_id=parent_id)
        partner.write({'prospect': True, 'customer': False})
        return partner
