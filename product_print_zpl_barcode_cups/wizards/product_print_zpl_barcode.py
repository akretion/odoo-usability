# Copyright 2025 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
import base64


class ProductPrintZplBarcode(models.TransientModel):
    _inherit = 'product.print.zpl.barcode'

    zpl_printer_id = fields.Many2one('printing.printer', string='ZPL Printer')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        printer = self.env['printing.printer'].get_default()
        res['zpl_printer_id'] = printer and printer.id or False
        return res

    def print_zpl(self):
        if self.zpl_printer_id:
            self.zpl_printer_id.print_document(
                None, base64.decodebytes(self.zpl_file), format='raw')
        else:
            return super().print_zpl()
