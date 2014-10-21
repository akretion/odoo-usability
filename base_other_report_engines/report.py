# -*- encoding: utf-8 -*-
##############################################################################
#
#    Base Other Report Engines module for OpenERP/Odoo
#    Copyright (C) 2014 Akretion (http://www.akretion.com)
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

from openerp.osv import orm


class Report(orm.Model):
    _inherit = "report"

    def _get_report_from_name(self, cr, uid, report_name):
        """Remove condition ('report_type', 'in', qwebtypes)"""
        report_obj = self.pool['ir.actions.report.xml']
        conditions = [('report_name', '=', report_name)]
        idreport = report_obj.search(cr, uid, conditions)[0]
        return report_obj.browse(cr, uid, idreport)
