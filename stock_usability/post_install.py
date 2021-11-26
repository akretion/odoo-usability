# Copyright 2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import SUPERUSER_ID, api

logger = logging.getLogger(__name__)


def create_config_parameter_immediate_tranfer(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        ico = env["ir.config_parameter"]
        conf_param = ico.search([("key", "=", "stock.no_default_immediate_tranfer")])
        if not conf_param:
            ico.create(
                {
                    "key": "stock.no_default_immediate_tranfer",
                    "value": "True",
                }
            )
            logger.info(
                "ir.config_parameter stock.no_default_immediate_tranfer created"
            )
        else:
            logger.info(
                "ir.config_parameter stock.no_default_immediate_tranfer "
                "already exists"
            )
