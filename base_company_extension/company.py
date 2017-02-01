# -*- coding: utf-8 -*-
# © 2014-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    capital_amount = fields.Monetary(string='Capital Amount')
    # in v9, title is only for contacts, not for companies
    legal_type = fields.Char(
        string="Legal Type", help="Type of Company, e.g. SARL, SAS, ...")

    def _report_company_legal_name(self):
        self.ensure_one()
        if self.legal_type:
            name = u'%s %s' % (self.name, self.legal_type)
        else:
            name = self.name
        return name

    _sql_constraints = [(
        'capital_amount_positive',
        'CHECK (capital_amount >= 0)',
        "The value of the field 'Capital Amount' must be positive."
        )]
