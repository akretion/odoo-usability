# -*- coding: utf-8 -*-
##############################################################################
#
#    Aeroo Report to Printer module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api, _
from openerp.exceptions import Warning as UserError


class PrintingPrinter(models.Model):
    _inherit = 'printing.printer'

    @api.multi
    def aeroo_print_document(self, report_name, object_id, copies=1):
        '''
        Send an aeroo report to CUPS server for printing

        Usage example :

        Add this button in an inherit of the view 'stock.view_picking_form':
        <button name="print_delivery" type="object" states="done"
            string="Print 2 copies"/>

        Add this code in the StockPicking class that inherit 'stock.picking'

        @api.multi
        def print_delivery(self):
            if not self.env.user.printing_printer_id:
                raise UserError(_(
                    "Missing 'Default Printer' in your preferences"))
            self.env.user.printing_printer_id.aeroo_print_document(
                'stock.report_picking', self.env.context['active_id'],
                copies=2)
        '''
        self.ensure_one()
        report = self.env['ir.actions.report.xml']._lookup_report(report_name)
        report_xml = self.env['report']._get_report_from_name(report_name)
        data = {
            'model': report_xml.model,
            'id': object_id,
            'report_type': 'aeroo',
            }
        aeroo_report_content, aeroo_report_format = report.create(
            self.env.cr, self.env.uid, [object_id],
            data, context=dict(self.env.context))
        if aeroo_report_format in ('pdf', 'raw'):
            self.print_document(
                report_name, aeroo_report_content, aeroo_report_format, copies)
        else:
            raise UserError(_(
                "Format '%s' is not supported for printing")
                % aeroo_report_format)
        return True
