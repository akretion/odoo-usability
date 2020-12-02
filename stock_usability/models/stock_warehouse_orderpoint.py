# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
import logging

logger = logging.getLogger(__name__)


class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    @api.model
    def _procure_orderpoint_confirm(
            self, use_new_cursor=False, company_id=False, raise_user_error=True):
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

    # This is for the button shortcut "reordering rules" on
    # stock.location form view, so that the location_id has the
    # good value, not the default stock location of the first WH of the company
    @api.model
    def default_get(self, fields_list):
        if self._context.get('default_location_id'):
            location = self.env['stock.location'].browse(
                self._context['default_location_id'])
            wh = location.get_warehouse()
            if location and wh:
                self = self.with_context(default_warehouse_id=wh.id)
        return super().default_get(fields_list)

    # This SQL constraint blocks the use of the "active" field
    # but I think it's not very useful to have such an "active" field
    # on orderpoints ; when you think the order point is bad, you update
    # the min/max values, you don't de-active it !
    _sql_constraints = [(
        'company_wh_location_product_unique',
        'unique(company_id, warehouse_id, location_id, product_id)',
        'An orderpoint already exists for the same company, same warehouse, '
        'same stock location and same product.'
        )]
