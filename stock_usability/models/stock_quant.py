# Copyright 2014-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.tools import float_compare, float_is_zero
from odoo.exceptions import UserError
import logging
logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    product_barcode = fields.Char(
        related='product_id.barcode', string="Product Barcode")

    def action_stock_move_lines_reserved(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock.stock_move_line_action")
        action['domain'] = [
            ('state', 'not in', ('draft', 'done', 'cancel')),
            ('product_id', '=', self.product_id.id),
            ('location_id', '=', self.location_id.id),
            ('lot_id', '=', self.lot_id.id or False),
            '|',
            ('package_id', '=', self.package_id.id or False),
            ('result_package_id', '=', self.package_id.id or False),
        ]
        action['context'] = {'create': 0, 'stock_move_line_main_view': True}
        return action

    @api.model
    def _fix_reserved_quantity(self):
        # called by a script when we start to have wrong 'reserved_quantity' on quants
        logger.info('START _fix_reserved_quantity')
        self._cr.execute("DELETE FROM stock_move_line WHERE move_id is null")
        self._cr.execute('SELECT id FROM stock_quant WHERE reserved_quantity > quantity AND reserved_quantity > 0')
        qty_quant_digits = 4
        all_rows = self._cr.fetchall()
        logger.info('%d bad quants detected', len(all_rows))
        for row in all_rows:
            quant_id = row[0]
            quant = self.env['stock.quant'].browse(quant_id)
            logger.info('Processing quant ID %s product %s lot %s location %s package %s quantity %s reserved_quantity %s', quant.id, quant.product_id.display_name, quant.lot_id.display_name or '-', quant.location_id.display_name, quant.package_id.display_name, quant.quantity, quant.reserved_quantity)
            reserved_quantity_cmp = float_compare(quant.reserved_quantity, 0, precision_digits=qty_quant_digits)
            # should never happen
            if reserved_quantity_cmp < 0:
                raise UserError(_("On quant ID %d, reserved_quantity is negative (%s).") % (quant_id, quant.reserved_quantity))
            if not reserved_quantity_cmp:
                logger.info('Quant ID %d as reserved_quantity = 0 after proper rounding', quant.id)
                continue
            if quant.package_id:
                logger.warning("Skipping quant ID %d because this script doesn't support packages for the moment", quant.id)
                continue
            if quant.location_id.should_bypass_reservation():
                logger.warning('Skipping quant ID %d because the location is marked as should bypass resa', quant.id)
                continue
            ml_domain = [
                ('product_id', '=', quant.product_id.id),
                ('location_id', '=', quant.location_id.id),
                ('state', 'not in', ('done', 'draft', 'cancel')),
                ('lot_id', '=', quant.lot_id.id or False),
                ('company_id', '=', quant.company_id.id),
                ]
            move_lines = self.env['stock.move.line'].sudo().search(ml_domain)
            if not move_lines:
                quant.sudo().write({'reserved_quantity': 0})
            for move_line in move_lines:
                move_line.button_do_unreserve()
            move_lines = self.env['stock.move.line'].sudo().search(ml_domain)
            if not move_lines:
                quant.sudo().write({'reserved_quantity': 0})
            else:
                raise UserError(_("Product moves are still present after full unreserve on quant ID %d. This should never happen.") % quant.id)
        logger.info('END _fix_reserved_quantity')
