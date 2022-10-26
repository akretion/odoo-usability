# Copyright 2015-2022 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
import logging

logger = logging.getLogger(__name__)


class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    def _procure_orderpoint_confirm(
            self, use_new_cursor=False, company_id=None, raise_user_error=True):
        logger.info(
            'procurement scheduler: START to create moves from '
            'orderpoints')
        res = super()._procure_orderpoint_confirm(
            use_new_cursor=use_new_cursor, company_id=company_id,
            raise_user_error=raise_user_error)
        logger.info(
            'procurement scheduler: END creation of moves from '
            'orderpoints')
        return res
