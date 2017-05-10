# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    lunch_voucher_natixis_customer_code = fields.Char(
        string='Natixis Customer Ref', size=7)
    lunch_voucher_natixis_delivery_code = fields.Char(
        string='Natixis Delivery Code', size=7)
