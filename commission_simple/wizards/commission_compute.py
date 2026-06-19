# Copyright 2019-2024 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from odoo.tools.misc import format_date
import logging
logger = logging.getLogger(__name__)


class CommissionCompute(models.TransientModel):
    _name = 'commission.compute'
    _description = 'Compute Commissions'

    company_id = fields.Many2one('res.company', required=True)
    date_start = fields.Date(string="Period Start Date", required=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        company = self.env.company
        last_commission_result = self.env['commission.result'].search([
            ('company_id', '=', company.id),
            ], order='date_start desc', limit=1)
        if last_commission_result:
            last_start_date = last_commission_result.date_start
            commissions_last_start_date = self.env['commission.result'].search([
                ('date_start', '=', last_start_date),
                ('company_id', '=', company.id),
                ], order="date_end asc", limit=1)
            min_end_date = commissions_last_start_date.date_end
            date_start = min_end_date + timedelta(1)
        else:
            today = fields.Date.context_today(self)
            date_start = datetime(today.year, today.month, 1)
        res.update({
            'company_id': company.id,
            'date_start': date_start,
            })
        return res

    def run(self):
        self.ensure_one()
        if not self.date_start:
            raise UserError(_("Missing Period Start Date."))
        creso = self.env['commission.result']
        existing_commissions = creso.search_read([
            ('date_start', '=', self.date_start),
            ('company_id', '=', self.company_id.id),
            ], ['assignment_id'])
        exclude_assignment_ids = [x['assignment_id'][0] for x in existing_commissions if x['assignment_id']]
        com_result_ids = self._core_compute(exclude_assignment_ids)
        if not com_result_ids:
            raise UserError(_('No commissions generated.'))
        action = self.env['ir.actions.actions']._for_xml_id(
            'commission_simple.commission_result_action')
        action.update({
            'views': False,
            'domain': f"[('id', 'in', {com_result_ids})]",
            })
        return action

    def _core_compute(self, exclude_assignment_ids):
        rules = self.env['commission.rule'].load_all_rules()
        com_result_ids = []
        assignments = self.env['commission.profile.assignment'].search(
            [('company_id', '=', self.company_id.id), ('id', 'not in', exclude_assignment_ids)])
        date_range_type2date_range = {}
        for assignment in assignments:
            profile = assignment.profile_id
            date_range_type = profile.date_range_type_id
            if not date_range_type:
                raise UserError(_("Missing commission periodicity on commission profile '%s'.") % profile.display_name)
            if date_range_type not in date_range_type2date_range:
                domain = [
                    ('date_start', '=', self.date_start),
                    ('type_id', '=', date_range_type.id),
                    ]
                date_range = self.env['date.range'].search(
                    domain + [('company_id', '=', self.company_id.id)], limit=1)
                if not date_range:
                    date_range = self.env['date.range'].search(
                        domain + [('company_id', '=', False)], limit=1)
                if not date_range:
                    logger.info('There is no date range with type %s starting on %s. Skipping commission generation for assignment ID %s', date_range_type.name, self.date_start, assignment.id)
                    continue
                date_range_type2date_range[date_range_type] = date_range
            com_result = assignment._generate_commission_result(date_range_type2date_range[date_range_type], rules)
            if com_result:
                com_result_ids.append(com_result.id)
            else:
                logger.info("No commission for %s", assignment._get_partner().display_name)
        return com_result_ids
