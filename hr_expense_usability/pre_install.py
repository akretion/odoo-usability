# -*- coding: utf-8 -*-
# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, SUPERUSER_ID


# I can't create decimal precision via hr_expense_data.xml because it's
# too "late" in the module installation process: in this case,
# demo data and post_install.py data have a unit_amount truncated at 2 digits
# That's why I create the decimal precision via a pre_init_hook
def create_decimal_precision(cr):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        env['decimal.precision'].create({
            'name': 'Expense Unit Price',
            'digits': 3,
            })
