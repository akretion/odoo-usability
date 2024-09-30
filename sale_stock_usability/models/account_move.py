# Copyright 2024 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _report_get_sale_pickings(self, sale_order=None):
        self.ensure_one()
        # the sale_order arg is usefull when using
        # py3o_lines_layout_groupby_order() to display the delivery orders
        # linked to a specific sale_order
        assert self.move_type in ('out_invoice', 'out_refund')
        sale_orders = sale_order or self.sale_ids
        picking_domain = [
            ('id', 'in', sale_orders.picking_ids.ids),
            ('state', '=', 'done'),
            ('date_done', '<', self.create_date),
            ('company_id', '=', self.company_id.id),
            ]
        previous_inv = self.env['account.move'].search([
            ('move_type', 'in', ('out_invoice', 'out_refund')),
            ('create_date', '<', self.create_date),
            ('id', 'in', sale_orders.invoice_ids.ids),
            ('company_id', '=', self.company_id.id),
            ], limit=1, order='id desc')
        if previous_inv:
            picking_domain.append(('date_done', '>', previous_inv.create_date))
        pickings = self.env['stock.picking'].search(picking_domain)
        return pickings
