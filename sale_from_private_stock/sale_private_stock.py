# -*- coding: utf-8 -*-
# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import UserError


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    private_stock_out_type_id = fields.Many2one(
        'stock.picking.type', string='Private Stock Out Type')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    default_sale_route_id = fields.Many2one(
        'stock.location.route', string="Default Stock Location Route",
        company_dependent=True,
        domain=[('usage', '=', 'internal')],
        help="Stock location route used by default in sale order lines"
        "for this customer.")

    @api.multi
    def _create_private_location_records(self, location_name):
        self.ensure_one()
        assert location_name, 'missing arg location_name'
        slo = self.env['stock.location']
        swo = self.env['stock.warehouse']
        pro = self.env['procurement.rule']
        slro = self.env['stock.location.route']
        company = self.env.user.company_id
        warehouses = swo.search([
            ('company_id', '=', company.id),
            ('private_stock_out_type_id', '!=', False)])
        if not warehouses:
            raise UserError(_(
                "No warehouse with a 'Private Stock Out Type' in the "
                "company %s") % company.name)
        warehouse = warehouses[0]
        private_stock_loc = slo.create({
            'name': location_name,
            'location_id': warehouse.view_location_id.id,
            'usage': 'internal',
            'company_id': company.id,
            'partner_id': self.id,
            })
        rule = pro.create({
            'name': _('From specific stock %s to customer') % location_name,
            'company_id': company.id,
            'warehouse_id': warehouse.id,
            'action': 'move',
            'location_id': self.property_stock_customer.id,
            'location_src_id': private_stock_loc.id,
            'procure_method': 'make_to_stock',
            'picking_type_id': warehouse.private_stock_out_type_id.id,
            'partner_address_id': self.id,
            })

        route = slro.create({
            'name': _('Take from %s') % location_name,
            'sequence': 1000,
            'pull_ids': [(6, 0, [rule.id])],
            'product_selectable': False,
            'product_categ_selectable': False,
            'warehouse_selectable': False,
            'sale_selectable': True,
            })
        return {
            'location': private_stock_loc,
            'rule': rule,
            'route': route,
            }

    @api.multi
    def create_private_location_route(self):
        self.ensure_one()
        assert not self.default_sale_route_id,\
            'Already has a default_sale_route_id'
        location_name = self._context.get('location_name') or self.name
        res_dict = self._create_private_location_records(
            location_name)
        self.default_sale_route_id = res_dict['route'].id


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _set_default_sale_route(self):
        commercial_partner = self.order_id.partner_id.commercial_partner_id
        if commercial_partner.default_sale_route_id:
            self.route_id = commercial_partner.default_sale_route_id
