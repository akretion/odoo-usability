# Copyright (C) 2016-2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero
import logging

logger = logging.getLogger(__name__)


class MrpBomLabourLine(models.Model):
    _name = 'mrp.bom.labour.line'
    _description = 'Labour lines on BOM'

    bom_id = fields.Many2one(
        comodel_name='mrp.bom',
        string='Labour Lines',
        ondelete='cascade')

    labour_time = fields.Float(
        string='Labour Time',
        required=True,
        digits=dp.get_precision('Labour Hours'),
        help="Average labour time for the production of "
             "items of the BOM, in hours.")

    labour_cost_profile_id = fields.Many2one(
        comodel_name='labour.cost.profile',
        string='Labour Cost Profile',
        required=True)

    note = fields.Text(
        string='Note')

    _sql_constraints = [(
        'labour_time_positive',
        'CHECK (labour_time >= 0)',
        "The value of the field 'Labour Time' must be positive or 0.")]


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    @api.depends(
        'labour_line_ids.labour_time',
        'labour_line_ids.labour_cost_profile_id.hour_cost')
    def _compute_total_labour_cost(self):
        for bom in self:
            cost = 0.0
            for lline in bom.labour_line_ids:
                cost += lline.labour_time *\
                    lline.labour_cost_profile_id.hour_cost
            bom.total_labour_cost = cost

    @api.depends(
        'bom_line_ids.product_id.standard_price',
        'total_labour_cost', 'extra_cost')
    def _compute_total_cost(self):
        for bom in self:
            comp_cost = 0.0
            for line in bom.bom_line_ids:
                comp_price = line.product_id.standard_price
                comp_qty_product_uom = line.product_uom_id._compute_quantity(
                    line.product_qty, line.product_id.uom_id)
                comp_cost += comp_price * comp_qty_product_uom
            total_cost = comp_cost + bom.extra_cost + bom.total_labour_cost
            bom.total_components_cost = comp_cost
            bom.total_cost = total_cost

    labour_line_ids = fields.One2many(
        'mrp.bom.labour.line', 'bom_id', string='Labour Lines')
    total_labour_cost = fields.Float(
        compute='_compute_total_labour_cost', readonly=True,
        digits=dp.get_precision('Product Price'),
        string="Total Labour Cost", store=True)
    extra_cost = fields.Float(
        string='Extra Cost', track_visibility='onchange',
        digits=dp.get_precision('Product Price'),
        help="Extra cost for the production of the quantity of "
        "items of the BOM, in company currency. "
        "You can use this field to enter the cost of the consumables "
        "that are used to produce the product but are not listed in "
        "the BOM")
    total_components_cost = fields.Float(
        compute='_compute_total_cost', readonly=True,
        digits=dp.get_precision('Product Price'),
        string='Total Components Cost')
    total_cost = fields.Float(
        compute='_compute_total_cost', readonly=True,
        string='Total Cost',
        digits=dp.get_precision('Product Price'),
        help="Total Cost = Total Components Cost + "
        "Total Labour Cost + Extra Cost")
    company_currency_id = fields.Many2one(
        related='company_id.currency_id', string='Company Currency')

    @api.model
    def _phantom_update_product_standard_price(self):
        logger.info('Start to auto-update cost price from phantom bom')
        boms = self.search([('type', '=', 'phantom')])
        boms.with_context(
            product_price_history_origin='Automatic update of Phantom BOMs')\
            .manual_update_product_standard_price()
        logger.info('End of the auto-update cost price from phantom bom')
        return True

    def manual_update_product_standard_price(self):
        if 'product_price_history_origin' not in self._context:
            self = self.with_context(
                product_price_history_origin='Manual update from BOM')
        precision = self.env['decimal.precision'].precision_get(
            'Product Price')
        for bom in self:
            wproduct = bom.product_id
            if not wproduct:
                wproduct = bom.product_tmpl_id
            if float_compare(
                    wproduct.standard_price, bom.total_cost,
                    precision_digits=precision):
                wproduct.with_context().write(
                    {'standard_price': bom.total_cost})
                logger.info(
                    'Cost price updated to %s on product %s',
                    bom.total_cost, wproduct.display_name)
        return True


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    standard_price = fields.Float(
        related='product_id.standard_price',
        readonly=True,
        string='Standard Price')


class LabourCostProfile(models.Model):
    _name = 'labour.cost.profile'
    _inherit = ['mail.thread']
    _description = 'Labour Cost Profile'

    name = fields.Char(
        string='Name',
        required=True,
        track_visibility='onchange')

    hour_cost = fields.Float(
        string='Cost per Hour',
        required=True,
        digits=dp.get_precision('Product Price'),
        track_visibility='onchange',
        help="Labour cost per hour per person in company currency")

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
        default=lambda self: self.env['res.company']._company_default_get())

    company_currency_id = fields.Many2one(
        related='company_id.currency_id',
        readonly=True,
        store=True,
        string='Company Currency')

    @api.depends('name', 'hour_cost', 'company_currency_id.symbol')
    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, u'%s (%s %s)' % (
                record.name, record.hour_cost,
                record.company_currency_id.symbol)))
        return res


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    unit_cost = fields.Float(
        string='Unit Cost', readonly=True,
        digits=dp.get_precision('Product Price'),
        help="This cost per unit in the unit of measure of the product "
        "in company currency takes into account "
        "the cost of the raw materials and the labour cost defined on"
        "the BOM.")

    company_currency_id = fields.Many2one(
        related='company_id.currency_id', readonly=True,
        string='Company Currency')

    def compute_order_unit_cost(self):
        self.ensure_one()
        mo_total_price = 0.0  # In the UoM of the M0
        labor_cost_per_unit = 0.0  # In the UoM of the product
        extra_cost_per_unit = 0.0  # In the UoM of the product
        # I read the raw materials MO, not on BOM, in order to make
        # it work with the "dynamic" BOMs (few raw material are auto-added
        # on the fly on MO)
        prec = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for raw_smove in self.move_raw_ids:
            # I don't filter on state, in order to make it work with
            # partial productions
            # For partial productions, mo.product_qty is not updated
            # so we compute with fully qty and we compute with all raw
            # materials (consumed or not), so it gives a good price
            # per unit at the end
            raw_price = raw_smove.product_id.standard_price
            raw_material_cost = raw_price * raw_smove.product_qty
            logger.info(
                'MO %s product %s: raw_material_cost=%s',
                self.name, raw_smove.product_id.display_name,
                raw_material_cost)
            mo_total_price += raw_material_cost
        if self.bom_id:
            bom = self.bom_id
            # if not bom.total_labour_cost:
            #    raise orm.except_orm(
            #        _('Error:'),
            #        _("Total Labor Cost is 0 on bill of material '%s'.")
            #        % bom.name)
            if float_is_zero(bom.product_qty, precision_digits=prec):
                raise UserError(_(
                    "Missing Product Quantity on bill of material '%s'.")
                    % bom.display_name)
            bom_qty_product_uom = bom.product_uom_id._compute_quantity(
                bom.product_qty, bom.product_tmpl_id.uom_id)
            assert bom_qty_product_uom > 0, 'BoM qty should be positive'
            labor_cost_per_unit = bom.total_labour_cost / bom_qty_product_uom
            extra_cost_per_unit = bom.extra_cost / bom_qty_product_uom
        # mo_standard_price and labor_cost_per_unit are
        # in the UoM of the product (not of the MO/BOM)
        mo_qty_product_uom = self.product_uom_id._compute_quantity(
            self.product_qty, self.product_id.uom_id)
        assert mo_qty_product_uom > 0, 'MO qty should be positive'
        mo_standard_price = mo_total_price / mo_qty_product_uom
        logger.info(
            'MO %s: labor_cost_per_unit=%s extra_cost_per_unit=%s',
            self.name, labor_cost_per_unit, extra_cost_per_unit)
        mo_standard_price += labor_cost_per_unit
        mo_standard_price += extra_cost_per_unit
        return mo_standard_price

    def post_inventory(self):
        '''This is the method where _action_done() is called on finished move
        So we write on 'price_unit' of the finished move and THEN we call
        super() which will call _action_done() which itself calls
        product_price_update_before_done()'''
        for order in self:
            if order.product_id.cost_method == 'average':
                unit_cost = order.compute_order_unit_cost()
                order.unit_cost = unit_cost
                logger.info('MO %s: unit_cost=%s', order.name, unit_cost)
                for finished_move in order.move_finished_ids.filtered(
                        lambda x: x.product_id == order.product_id):
                    finished_move.price_unit = unit_cost
        return super(MrpProduction, self).post_inventory()
