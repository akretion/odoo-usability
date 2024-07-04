# Copyright 2014-2022 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Usability',
    'version': '16.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Usability improvements on sale module',
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': [
        'sale',
#        'account_usability',  # for company view
        'base_view_inheritance_extension',
        ],
    'data': [
        'views/sale_order.xml',
        'views/product_category.xml',
        'views/sale_report.xml',
        'views/product_pricelist_item.xml',
        'views/account_move.xml',
#         'views/res_company.xml',  TODO uncomment once account_usa is ported
        "views/res_partner.xml",
        ],
    'installable': True,
}
