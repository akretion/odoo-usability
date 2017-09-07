# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

from openerp import models, fields


class CrmCaseCateg(models.Model):
    _inherit = 'crm.case.categ'

    name = fields.Char(translate=False)
