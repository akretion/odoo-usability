# -*- coding: utf-8 -*-
# © 2014-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class Report(models.Model):
    _inherit = "report"

    def _get_report_from_name(self, report_name):
        """Remove condition ('report_type', 'in', qwebtypes)
        This code is copyright Odoo S.A.
        """
        report_obj = self.env['ir.actions.report.xml']
        conditions = [('report_name', '=', report_name)]
        context = self.env['res.users'].context_get()
        return report_obj.with_context(context).search(conditions, limit=1)
