# -*- coding: utf-8 -*-
##############################################################################
#
#    Account Move Line Start End Dates XLS module for Odoo
#    Copyright (C) 2014-2016 Akretion (http://www.akretion.com/)
#    @author: Alexis de Lattre <alexis.delattre@akretion.com>
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

import xlwt
import logging
from openerp import models, api

_logger = logging.getLogger(__name__)

try:
    from openerp.addons.report_xls.utils import _render
    from openerp.addons.report_xls.report_xls import report_xls
except (ImportError, IOError) as err:
    _logger.debug(err)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def _report_xls_fields(self):
        res = super(AccountMoveLine, self)._report_xls_fields()
        return res + ['start_date', 'end_date']

    @api.model
    def _report_xls_template(self):
        res = super(AccountMoveLine, self)._report_xls_template()
        bc = '22'
        aml_cell_style_date = xlwt.easyxf(
            'borders: left thin, right thin, top thin, bottom thin, '
            'left_colour %s, right_colour %s, top_colour %s, '
            'bottom_colour %s; align: horz left;'
            % (bc, bc, bc, bc), num_format_str=report_xls.date_format)
        res.update({
            'start_date': {
                'header': [1, 13, 'text', _render("_('Start Date')")],
                'lines': [1, 0, _render(
                    "line.start_date and line.start_date != 'False' and "
                    "'date' or 'text'"), _render(
                    "line.start_date and line.start_date != 'False' and "
                    "datetime.strptime(line.start_date, '%Y-%m-%d') or None"),
                    None, aml_cell_style_date],
                'totals': [1, 0, 'text', None]},
            'end_date': {
                'header': [1, 13, 'text', _render("_('End Date')")],
                'lines': [1, 0, _render(
                    "line.end_date and line.end_date != 'False' and "
                    "'date' or 'text'"), _render(
                    "line.end_date and line.end_date != 'False' and "
                    "datetime.strptime(line.end_date, '%Y-%m-%d') or None"),
                    None, aml_cell_style_date],
                'totals': [1, 0, 'text', None]},
            })
        return res
