# Copyright 2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, SUPERUSER_ID


def update_partner_display_name(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    partners = env['res.partner'].with_context(active_test=False).search(
        [('ref', '!=', False)])
    partners.write({'invalidate_display_name': True})
