# -*- coding: utf-8 -*-
##############################################################################
#
#    Product Usability module for Odoo
#    Copyright (C) 2015-2016 Akretion (http://www.akretion.com)
#    Copyright (C) 2004-2016 Odoo SA (http://www.odoo.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm, fields
from openerp import SUPERUSER_ID
import openerp.addons.decimal_precision as dp


class ProductTemplate(orm.Model):
    _inherit = 'product.template'

    _columns = {
        'price_history_ids': fields.one2many(
            'product.price.history', 'product_template_id',
            string='Product Price History')
        }

    # All the code below is copyright Odoo SA
    def _set_standard_price(
            self, cr, uid, product_tmpl_id, value, context=None):
        ''' Store the standard price change in order to be able to
        retrieve the cost of a product template for a given date'''
        if context is None:
            context = {}
        if not context.get('dont_create_price_history'):
            price_history_obj = self.pool['product.price.history']
            user_company = self.pool['res.users'].browse(
                cr, uid, uid, context=context).company_id.id
            company_id = context.get('force_company', user_company)
            price_history_obj.create(cr, SUPERUSER_ID, {
                'product_template_id': product_tmpl_id,
                'cost': value,
                'company_id': company_id,
                'origin': context.get('product_price_history_origin', False),
                }, context=context)

    def create(self, cr, uid, vals, context=None):
        product_template_id = super(ProductTemplate, self).create(
            cr, uid, vals, context=context)
        self._set_standard_price(
            cr, uid, product_template_id,
            vals.get('standard_price', 0.0), context=context)
        return product_template_id

    def write(self, cr, uid, ids, vals, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        if 'standard_price' in vals:
            for prod_template_id in ids:
                self._set_standard_price(
                    cr, uid, prod_template_id,
                    vals['standard_price'], context=context)
        res = super(ProductTemplate, self).write(
            cr, uid, ids, vals, context=context)
        return res


class ProductProduct(orm.Model):
    _inherit = 'product.product'

    # unfortunately required in old-API...
    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default.update({
            'price_history_ids': False,
            })
        return super(ProductProduct, self).copy(
            cr, uid, id, default=default, context=context)


class ProductPriceHistory(orm.Model):
    # This is a backport of the datamodel of v8
    # The code below is (C) Odoo SA
    _name = 'product.price.history'
    _rec_name = 'datetime'
    _order = 'datetime desc'

    _columns = {
        'company_id': fields.many2one('res.company', required=True),
        'product_template_id': fields.many2one(
            'product.template', 'Product Template',
            required=True, ondelete='cascade'),
        'datetime': fields.datetime('Historization Time'),
        'cost': fields.float(
            'Historized Cost',
            digits_compute=dp.get_precision('Product Price')),
        # the 'origin' field is not in v8, it's an idea of mine !
        'origin': fields.char('Origin'),
    }

    def _get_default_company(self, cr, uid, context=None):
        if 'force_company' in context:
            return context['force_company']
        else:
            company = self.pool['res.users'].browse(
                cr, uid, uid, context=context).company_id
            return company.id if company else False

    _defaults = {
        'datetime': fields.datetime.now,
        'company_id': _get_default_company,
    }
