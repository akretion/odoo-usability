# -*- coding: utf-8 -*-
# Copyright 2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
import logging
logger = logging.getLogger(__name__)


class CommissionCompute(models.TransientModel):
    _name = 'commission.compute'
    _description = 'Compute Commissoins'

    @api.model
    def _default_date_range(self):
        drange_type = self.env.user.company_id.commission_date_range_type_id
        if not drange_type:
            return False
        today = fields.Date.from_string(fields.Date.context_today(self))
        first_day_last_month = today + relativedelta(months=-1, day=1)
        dranges = self.env['date.range'].search([
            '|', ('company_id', '=', self.env.user.company_id.id),
            ('company_id', '=', False),
            ('type_id', '=', drange_type.id),
            ('date_start', '=', fields.Date.to_string(first_day_last_month))
            ])
        return dranges and dranges[0] or dranges

    date_range_id = fields.Many2one(
        'date.range', required=True, string='Period',
        default=lambda self: self._default_date_range())
    date_start = fields.Date(related='date_range_id.date_start', readonly=True)
    date_end = fields.Date(related='date_range_id.date_end', readonly=True)

    def run(self):
        self.ensure_one()
        creso = self.env['commission.result']
        ruo = self.env['res.users']
        date_range = self.date_range_id
        existing_res = creso.search([('date_range_id', '=', date_range.id)])
        if existing_res:
            raise UserError(
                u'Il existe déjà des commissions pour cette période.')
        com_result_ids = self.core_compute()
        if not com_result_ids:
            raise UserError(_('No commission generated.'))
        action = self.env['ir.actions.act_window'].for_xml_id(
            'commission_simple', 'commission_result_action')
        action.update({
            'views': False,
            'domain': "[('id', 'in', %s)]" % com_result_ids,
            })
        return action

    def core_compute(self):
        rules = self.env['commission.rule'].load_all_rules()
        ailo = self.env['account.invoice.line']
        ruo = self.env['res.users']
        com_result_ids = []
        for user in ruo.with_context(active_test=False).search([]):
            if user.commission_profile_id:
                if user.commission_profile_id.id not in rules:
                    raise UserError(_(
                        "The commission profile '%s' doesn't have any rules.")
                        % user.commission_profile_id.name)
                com_result = ailo.compute_commission_for_one_user(user, self.date_range_id, rules)
                if com_result:
                    com_result_ids.append(com_result.id)
            else:
                logger.debug(
                    "Commission computation: salesman '%s' "
                    "doesn't have a commission profile",
                    user.name)
        return com_result_ids


