# coding: utf-8
# alexis de latte @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    description_sale = fields.Text(translate=False)
    description_purchase = fields.Text(translate=False)
    description = fields.Text(translate=False)
    name = fields.Char(translate=False)


class ProductCategory(models.Model):
    _inherit = "product.category"

    name = fields.Char(translate=False)


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    name = fields.Char(translate=False)


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    name = fields.Char(translate=False)


class ProductUomCateg(models.Model):
    _inherit = 'product.uom.categ'

    name = fields.Char(translate=False)


class ProductUom(models.Model):
    _inherit = 'product.uom'

    name = fields.Char(translate=False)


class ProductPackaging(models.Model):
    _inherit = 'product.packaging'

    name = fields.Char(translate=False)
