# Copyright 2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class SaleInvoiceDiscountAllLines(models.TransientModel):
    _name = 'sale.invoice.discount.all.lines'
    _description = 'None'
    # Remove because this feature is now mostly native
    # TODO 04/07/2024 remove later to avoid ORM bug: it crashes when reloading module
    # KeyError: 'sale.invoice.discount.all.lines'
