# Copyright 2021 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

class HrPayrollStructureType(models.Model):
    _inherit = 'hr.payroll.structure.type'

    active = fields.Boolean(default=True)
