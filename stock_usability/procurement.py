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
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    def _procure_orderpoint_confirm(
            self, cr, uid, use_new_cursor=False, company_id=False,
            context=None):
        logger.info(
            'procurement scheduler: START to create procurements from '
            'orderpoints')
        res = super(ProcurementOrder, self)._procure_orderpoint_confirm(
            cr, uid, use_new_cursor=use_new_cursor, company_id=company_id,
            context=context)
        logger.info(
            'procurement scheduler: END creation of procurements from '
            'orderpoints')
        return res

    # Why is this code in stock_usability and not in procurement_usability ?
    # For a very good reason
    # The stock module inherits run_scheduler(). So, if we want to have the START and
    # END log message and a good end date for procurement.scheduler.log
    # the method below must be called first, so we must be "above" all
    # modules that call run_scheduler()
    def run_scheduler(
            self, cr, uid, use_new_cursor=False, company_id=False,
            context=None):
        '''Inherit to add info logs'''
        logger.info(
            'START procurement scheduler '
            '(company ID=%d, uid=%d, use_new_cursor=%s)',
            company_id, uid, use_new_cursor)
        start_datetime = datetime.now()
        res = super(ProcurementOrder, self).run_scheduler(
            cr, uid, use_new_cursor=use_new_cursor, company_id=company_id,
            context=context)
        logger.info(
            'END procurement scheduler '
            '(company ID=%d, uid=%d, use_new_cursor=%s)',
            company_id, uid, use_new_cursor)
        try:
            # I put it in a try/except, to be sure that, even if the user
            # the execute the scheduler doesn't have create right on
            # procurement.scheduler.log
            self.pool['procurement.scheduler.log'].create(
                cr, uid, {
                    'company_id': company_id,
                    'start_datetime': start_datetime,
                    }, context=context)
            # If I don't do an explicit cr.commit(), it doesn't create
            # the procurement.scheduler.log... I don't know why
            cr.commit()
        except:
            logger.warning('Could not create procurement.scheduler.log')
        return res


class ProcurementSchedulerLog(models.Model):
    _name = 'procurement.scheduler.log'
    _description = 'Logs of the Procurement Scheduler'
    _order = 'create_date desc'

    company_id = fields.Many2one(
        'res.company', string='Company', readonly=True)
    start_datetime = fields.Datetime(string='Start Date', readonly=True)
