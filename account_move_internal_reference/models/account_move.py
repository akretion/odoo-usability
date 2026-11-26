# Copyright 2026 Akretion (https://www.akretion.com).
# @author Benoît Guillot <benoit.guillot@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    internal_reference = fields.Char(
        string="Internal Reference",
        copy=False,
        tracking=True,
        index="trigram",
        help="Internal reference of the document. It is concatenated in the "
        "label of the receivable/payable line, like the reference and the "
        "payment reference.",
    )
