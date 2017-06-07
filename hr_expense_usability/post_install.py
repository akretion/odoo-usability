# -*- coding: utf-8 -*-
# © 2016-2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, SUPERUSER_ID

PRODUCTS = {
    'FR': [
        {'default_code': '1-3CV_0-5000km',
         'name': u"Frais kilométriques: 1-3 CV, < 5 000 km",
         'cost': 0.41},
        {'default_code': '4CV_0-5000km',
         'name': u"Frais kilométriques: 4 CV, < 5 000 km",
         'cost': 0.493},
        {'default_code': '5CV_0-5000km',
         'name': u"Frais kilométriques: 5 CV, < 5 000 km",
         'cost': 0.543},
        {'default_code': '6CV_0-5000km',
         'name': u"Frais kilométriques: 6 CV, < 5 000 km",
         'cost': 0.568},
        {'default_code': '7+CV_0-5000km',
         'name': u"Frais kilométriques: 7+ CV, < 5 000 km",
         'cost': 0.595},
        {'default_code': '1-3CV_5-20000km',
         'name': u"Frais kilométriques: 1-3 CV, 5-20 000 km",
         'cost': 0.245},
        {'default_code': '4CV_5-20000km',
         'name': u"Frais kilométriques: 4 CV, 5-20 000 km",
         'cost': 0.277},
        {'default_code': '5CV_5-20000km',
         'name': u"Frais kilométriques: 5 CV, 5-20 000 km",
         'cost': 0.305},
        {'default_code': '6CV_5-20000km',
         'name': u"Frais kilométriques: 6 CV, 5-20 000 km",
         'cost': 0.32},
        {'default_code': '7+CV_5-20000km',
         'name': u"Frais kilométriques: 7+ CV, 5-20 000 km",
         'cost': 0.337},
        {'default_code': '1-3CV_+20000km',
         'name': u"Frais kilométriques: 1-3 CV, > 20 000 km",
         'cost': 0.245},
        {'default_code': '4CV_+20000km',
         'name': u"Frais kilométriques: 4 CV, > 20 000 km",
         'cost': 0.277},
        {'default_code': '5CV_+20000km',
         'name': u"Frais kilométriques: 5 CV, > 20 000 km",
         'cost': 0.305},
        {'default_code': '6CV_+20000km',
         'name': u"Frais kilométriques: 6 CV, > 20 000 km",
         'cost': 0.32},
        {'default_code': '7+CV_+20000km',
         'name': u"Frais kilométriques: 7+ CV, > 20 000 km",
         'cost': 0.337},
        ]
    }


def create_private_car_expense_products(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        companies = env['res.company'].search([])
        country_codes = []
        for company in companies:
            company_country_code = company.country_id.code and\
                company.country_id.code.upper() or False
            if company_country_code not in country_codes:
                country_codes.append(company_country_code)
        categ_id = env.ref('hr_expense.cat_expense').id
        km_uom_id = env.ref('product.product_uom_km').id
        for country_code in country_codes:
            if country_code in PRODUCTS:
                for product in PRODUCTS[country_code]:
                    env['product.product'].create({
                        'name': product['name'],
                        'default_code': product.get('default_code'),
                        'categ_id': categ_id,
                        'sale_ok': False,
                        'purchase_ok': False,
                        'can_be_expensed': False,
                        'private_car_expense_ok': True,
                        'type': 'service',
                        'list_price': False,
                        'standard_price': product['cost'],
                        'uom_id': km_uom_id,
                        'uom_po_id': km_uom_id,
                        'taxes_id': False,
                        'supplier_taxes_id': False,
                        })
    return
