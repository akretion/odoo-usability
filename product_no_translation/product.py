# -*- coding: utf-8 -*-
# © 2014-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    name = fields.Char(translate=False)
    description = fields.Text(translate=False)
    description_purchase = fields.Text(translate=False)
    description_sale = fields.Text(translate=False)


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
