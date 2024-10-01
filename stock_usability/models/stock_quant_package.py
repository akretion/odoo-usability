# Copyright 2024 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
import logging

logger = logging.getLogger(__name__)


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    @api.model
    def _cron_auto_unpack_on_internal_locations(self):
        # Problem in v10: when you manage packs in Odoo for customer pickings,
        # you have the following problem: when you return a customer picking,
        # if you return all the products that were in the same pack, the pack
        # is returned, so you have in your stock one or several quants
        # inside a pack. This is a problem when you want to ship those
        # products again.
        # I provide the code in this module, but not the cron, because in some
        # scenarios, you may want to have packs in your stock.
        # Just add the cron in the specific module of your project.
        # Underlying problem solved in Odoo v11. Don't port that to v14 !
        logger.info('START cron auto unpack on internal locations')
        int_locs = self.env['stock.location'].search([('usage', '=', 'internal')])
        packages = self.search([('location_id', 'in', int_locs.ids)])
        logger.info('Unpacking %d packages on internal locations', len(packages))
        packages.unpack()
        logger.info('END cron auto unpack on internal locations')
