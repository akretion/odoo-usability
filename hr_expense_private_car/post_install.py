# -*- coding: utf-8 -*-
# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, SUPERUSER_ID

KM_PRICES = {
    'FR': [
        {'name': u"[FR] 1-3 CV, < 5 000 km",  'unit_amount': 0.41},
        {'name': u"[FR] 4 CV, < 5 000 km",    'unit_amount': 0.493},
        {'name': u"[FR] 5 CV, < 5 000 km",    'unit_amount': 0.543},
        {'name': u"[FR] 6 CV, < 5 000 km",    'unit_amount': 0.568},
        {'name': u"[FR] 7+ CV, < 5 000 km",   'unit_amount': 0.595},
        {'name': u"[FR] 1-3 CV, 5-20 000 km", 'unit_amount': 0.245},
        {'name': u"[FR] 4 CV, 5-20 000 km",   'unit_amount': 0.277},
        {'name': u"[FR] 5 CV, 5-20 000 km",   'unit_amount': 0.305},
        {'name': u"[FR] 6 CV, 5-20 000 km",   'unit_amount': 0.32},
        {'name': u"[FR] 7+ CV, 5-20 000 km",  'unit_amount': 0.337},
        {'name': u"[FR] 1-3 CV, > 20 000 km", 'unit_amount': 0.245},
        {'name': u"[FR] 4 CV, > 20 000 km",   'unit_amount': 0.277},
        {'name': u"[FR] 5 CV, > 20 000 km",   'unit_amount': 0.305},
        {'name': u"[FR] 6 CV, > 20 000 km",   'unit_amount': 0.32},
        {'name': u"[FR] 7+ CV, > 20 000 km",  'unit_amount': 0.337},
        ]
    }


def create_private_car_km_prices(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        companies = env['res.company'].search([])
        for company in companies:
            company_country_code = company.country_id.code and\
                company.country_id.code.upper() or False
            if company_country_code in KM_PRICES:
                for record in KM_PRICES[company_country_code]:
                    env['private.car.km.price'].create({
                        'name': record['name'],
                        'unit_amount': record['unit_amount'],
                        'company_id': company.id,
                        })
    return
