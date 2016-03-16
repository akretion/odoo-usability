# coding: utf-8
# © 2016 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from lxml import etree


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    @api.model
    def _get_attributes_to_filter(self):
        """ Inherit if you want reduce the list """
        return [(x.id, x.name)
                for x in self.env['product.attribute'].search([])]

    @api.model
    def _customize_attribute_filters(self, my_filter):
        """ Inherit if you to customize search filter display"""
        return {
            'string': "%s" % my_filter[1],
            'help': 'Filtering by Attribute',
            'domain': "[('attribute_id','=', %s)]" % my_filter[0]}

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        """ customize xml output
        """
        res = super(ProductAttributeValue, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if view_type == 'search':
            filters_to_create = self._get_attributes_to_filter()
            doc = etree.XML(res['arch'])
            for my_filter in filters_to_create:
                elm = etree.Element(
                    'filter', **self._customize_attribute_filters(my_filter))
                doc[0].addprevious(elm)
            res['arch'] = etree.tostring(doc, pretty_print=True)
        return res
