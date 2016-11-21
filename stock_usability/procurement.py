# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    @api.model
    def _procure_orderpoint_confirm(
            self, use_new_cursor=False, company_id=False):
        logger.info(
            'procurement scheduler: START to create procurements from '
            'orderpoints')
        res = super(ProcurementOrder, self)._procure_orderpoint_confirm(
            use_new_cursor=use_new_cursor, company_id=company_id)
        logger.info(
            'procurement scheduler: END creation of procurements from '
            'orderpoints')
        return res

    # Why is this code in stock_usability and not in procurement_usability ?
    # For a very good reason
    # The stock module inherits run_scheduler(). So, if we want to have the
    # START and END log message and a good end date
    # for procurement.scheduler.log, the method below must be called first,
    # so we must be "above" all modules that call run_scheduler()
    @api.model
    def run_scheduler(
            self, use_new_cursor=False, company_id=False):
        '''Inherit to add info logs'''
        logger.info(
            'START procurement scheduler '
            '(company ID=%d, uid=%d, use_new_cursor=%s)',
            company_id, self._uid, use_new_cursor)
        start_datetime = datetime.now()
        res = super(ProcurementOrder, self).run_scheduler(
            use_new_cursor=use_new_cursor, company_id=company_id)
        logger.info(
            'END procurement scheduler '
            '(company ID=%d, uid=%d, use_new_cursor=%s)',
            company_id, self._uid, use_new_cursor)
        try:
            # I put it in a try/except, to be sure that, even if the user
            # the execute the scheduler doesn't have create right on
            # procurement.scheduler.log
            self.env['procurement.scheduler.log'].create({
                'company_id': company_id,
                'start_datetime': start_datetime,
                })
            # If I don't do an explicit cr.commit(), it doesn't create
            # the procurement.scheduler.log... I don't know why
            self._cr.commit()
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
