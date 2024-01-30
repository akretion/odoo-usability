# Copyright 2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
import ipaddress


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    zpl_printer_ip = fields.Char(
        config_parameter="product_print_zpl_barcode.printer_ip",
        string="ZPL Printer IP Address")

    @api.constrains('zpl_printer_ip')
    def _check_zpl_printer_ip(self):
        for wiz in self:
            if wiz.zpl_printer_ip:
                try:
                    ipaddress.ip_address(wiz.zpl_printer_ip)
                except Exception as e:
                    raise ValidationError(str(e))
