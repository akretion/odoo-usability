# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProcurementSchedulerLog(models.Model):
    _name = 'procurement.scheduler.log'
    _description = 'Logs of the Procurement Scheduler'
    _order = 'create_date desc'

    company_id = fields.Many2one(
        'res.company', string='Company', readonly=True)
    start_datetime = fields.Datetime(string='Start Date', readonly=True)
