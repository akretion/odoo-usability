# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    picking_ids = fields.One2many(
        'stock.picking', 'group_id', string='Pickings', readonly=True)

    @api.model
    def run_scheduler(self, use_new_cursor=False, company_id=False):
        '''Inherit to add info logs'''
        logger.info(
            'START procurement scheduler '
            '(company ID=%d, uid=%d, use_new_cursor=%s)',
            company_id, self._uid, use_new_cursor)
        start_datetime = datetime.now()
        res = super().run_scheduler(
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
        except Exception as e:
            logger.warning(
                'Could not create procurement.scheduler.log (error: %s)', e)
        return res
