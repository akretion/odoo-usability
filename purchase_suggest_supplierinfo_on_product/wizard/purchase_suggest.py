# -*- coding: utf-8 -*-

from openerp import models, fields, api, _


class PurchaseSuggestionGenerate(models.TransientModel):
    _inherit = 'purchase.suggest.generate'

    seller_ids = fields.Many2many(
        required=True,
        domain=[('supplier', '=', True), ('parent_id', '=', False)])

    @api.model
    def _prepare_suggest_line(self, product_id, qty_dict):
        sline = super(PurchaseSuggestionGenerate, self)._prepare_suggest_line(
            product_id, qty_dict)
        sline['company_id'] = self.env.user.company_id.id
        if sline['seller_id'] not in self.seller_ids.ids:
            product = self.env['product.product'].browse(sline['product_id'])
            for supplierinfo in product.seller_ids:
                if supplierinfo.name in self.seller_ids:
                    sline['seller_id'] = supplierinfo.name.id
        return sline

    @api.model
    def generate_products_dict(self):
        ppo = self.env['product.product']
        products = {}
        product_domain = self._prepare_product_domain()
        product_domain.append(('purchase_ok', '=', True))
        product_to_analyse = ppo.search(product_domain)
        for product in product_to_analyse:
            products[product.id] = {
                'min_qty': 0.0,
                'max_qty': 0.0,
                'draft_po_qty': 0.0,  # This value is set later on
                'orderpoint': False,
                'product': product,
                }
        return products

    @api.multi
    def run(self):
        self.ensure_one()
        pso = self.env['purchase.suggest']
        polo = self.env['purchase.order.line']
        puo = self.env['product.uom']
        p_suggest_lines = []
        products = self.generate_products_dict()
        polines = polo.search([
            ('state', '=', 'draft'), ('product_id', 'in', products.keys())])
        for line in polines:
            qty_product_po_uom = puo._compute_qty_obj(
                line.product_uom, line.product_qty, line.product_id.uom_id)
            products[line.product_id.id]['draft_po_qty'] += qty_product_po_uom
        virtual_qties = self.pool['product.product']._product_available(
            self._cr, self._uid, products.keys(),
            context={'location': self.location_id.id})
        for product_id, qty_dict in products.iteritems():
            qty_dict['virtual_available'] =\
                virtual_qties[product_id]['virtual_available']
            qty_dict['incoming_qty'] =\
                virtual_qties[product_id]['incoming_qty']
            qty_dict['outgoing_qty'] =\
                virtual_qties[product_id]['outgoing_qty']
            qty_dict['qty_available'] =\
                virtual_qties[product_id]['qty_available']
            vals = self._prepare_suggest_line(product_id, qty_dict)
            if vals:
                p_suggest_lines.append(vals)
        p_suggest_lines_sorted = sorted(
            p_suggest_lines, key=lambda to_sort: to_sort['seller_id'])
        if p_suggest_lines_sorted:
            p_suggest_ids = []
            for p_suggest_line in p_suggest_lines_sorted:
                p_suggest = pso.create(p_suggest_line)
                p_suggest_ids.append(p_suggest.id)
            action = self.env['ir.actions.act_window'].for_xml_id(
                'purchase_suggest', 'purchase_suggest_action')
            action.update({
                'target': 'current',
                'domain': [('id', 'in', p_suggest_ids)],
                'context': {'purchase_suggest_supplier': True}
            })
            return action
        else:
            raise Warning(_(
                "There are no purchase suggestions to generate."))


class PurchaseSuggest(models.TransientModel):
    _inherit = 'purchase.suggest'

    draft_po_qty = fields.Float(readonly=False)
