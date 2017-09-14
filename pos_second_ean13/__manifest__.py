# -*- coding: utf-8 -*-
# Copyright (C) 2016-2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>


{
    'name': 'POS Second EAN13',
    'version': '10.0.1.0.0',
    'category': 'Point Of Sale',
    'license': 'AGPL-3',
    'summary': "Add a second EAN13 on products",
    'description': """
POS Second EAN13
================

This module adds a second EAN13 field on products. This feature has been asked by librairies that often have the same book available from 2 different sources with different EAN13 (to keep things simple, I didn't want to handle N EAN13 ; a second EAN13 was enough for most cases). This module also provides a patch to apply on the source code of Odoo (file *patch-point_of_sale-second_ean13.diff*) : this patch modifies the javascript code of the official *point_of_sale* module of Odoo.

I recommend to also install the module *pos_no_product_template_menu* because the second EAN13 is only shown in the product.product form view (I don't want to add the hack to have the second EAN13 field on product.template form view, in order to keep this module as simple as possible).

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['product'],
    'data': ['product_view.xml'],
    'installable': True,
}
