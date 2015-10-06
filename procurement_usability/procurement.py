# -*- encoding: utf-8 -*-
##############################################################################
#
#    Procurement Usability module for Odoo
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

from openerp import models, fields
import logging

logger = logging.getLogger(__name__)


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    def run_scheduler(
            self, cr, uid, use_new_cursor=False, company_id=False,
            context=None):
        '''Inherit to add info logs'''
        logger.info(
            'START procurement scheduler (company ID=%d, uid=%d)',
            company_id, uid)
        res = super(ProcurementOrder, self).run_scheduler(
            cr, uid, use_new_cursor=use_new_cursor, company_id=company_id,
            context=context)
        logger.info(
            'END procurement scheduler (company ID=%d, uid=%d)',
            company_id, uid)
        return res


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    sale_ids = fields.One2many(
        'sale.order', 'procurement_group_id', string='Sale Orders',
        readonly=True)
    picking_ids = fields.One2many(
        'stock.picking', 'group_id', string='Pickings', readonly=True)
