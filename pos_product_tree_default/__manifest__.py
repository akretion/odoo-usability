# Copyright 2021 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'POS Product Tree Default',
    'version': '14.0.1.0.0',
    'category': 'Product',
    'license': 'AGPL-3',
    'summary': 'Tree view by default instead of kanban for Products',
    'description': """
        Replace default kanban view by tree view for product menu in Point of Sale
        main menu
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['point_of_sale'],
    'data': [
        'views/product_template.xml'
    ],
    'installable': True,
}
