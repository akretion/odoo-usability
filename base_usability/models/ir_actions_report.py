# Copyright 2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    # since v13, print_report_name is a translatable field
    # It means that you can't set the value via an inherit of
    # ir.actions.report as XML
    # I think it was easier when this field was not translatable
    print_report_name = fields.Char(translate=False)
