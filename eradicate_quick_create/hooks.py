# Copyright 2019 Akretion France
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID
from odoo.api import Environment


def web_m2x_options_create(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    config_parameter = env['ir.config_parameter'].search(
        [('key', '=', 'web_m2x_options.create')])
    if config_parameter and config_parameter.value != 'False':
        config_parameter.value = 'False'
    else:
        env['ir.config_parameter'].create({
            'key': 'web_m2x_options.create',
            'value': 'False',
            })
