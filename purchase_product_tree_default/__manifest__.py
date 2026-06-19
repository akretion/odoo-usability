# Copyright 2019-2022 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Purchase Product Tree Default',
    'version': '18.0.1.0.0',
    'category': 'Product',
    'license': 'AGPL-3',
    'summary': 'List view by default instead of kanban for Products',
    'description': """
        Replace default kanban view by list view for product menu in Purchase
        main menu
    """,
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['purchase'],
    'data': [
        'views/product_template.xml'
    ],
    'installable': True,
}
