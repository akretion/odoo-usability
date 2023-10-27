# Copyright 2015-2022 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Product Usability',
    'version': '16.0.1.0.0',
    'category': 'Product',
    'license': 'AGPL-3',
    'summary': 'Small usability enhancements to the product module',
    'description': """
Product Usability
=================

The usability enhancements include:

* hide description field on product (description_sale must be use instead of description)

* add a field barcode_type in product form view

* allow to search a product by supplier

* set a search view for product packaging

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['product'],
    "external_dependencies": {"python": ["stdnum"]},
    'data': [
        'views/product_supplierinfo_view.xml',
        'views/product_pricelist_view.xml',
        'views/product_pricelist_item.xml',
        'views/product_template_view.xml',
        'views/product_product.xml',
        'views/product_config_menu.xml',
        'views/product_category_view.xml',
        'views/product_packaging.xml',
    ],
    'installable': True,
}
