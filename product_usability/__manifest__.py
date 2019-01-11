# © 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Product Usability',
    'version': '12.0.1.0.0',
    'category': 'Product',
    'license': 'AGPL-3',
    'summary': 'Small usability enhancements to the product module',
    'description': """
Product Usability
=================

The usability enhancements include:

* show the object product.price.history in the product template form view

* wider name field in product form view

* hide description field on product (description_sale must be use instead of description)

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['product'],
    'data': [
        'security/product_security.xml',
        'product_view.xml',
        ],
    'installable': True,
}
