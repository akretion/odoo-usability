from odoo import api, fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    display_type = fields.Selection(
        [
            ("sale", "Sales"),
            ("purchase", "Purchase"),
            ("cash", "Cash"),
            ("bank", "Bank"),
            ("payment", "Payment"),
            ("general", "Miscellaneous"),
        ],
        required=True,
        help="Select 'Sale' for customer invoices journals.\n"
        "Select 'Purchase' for vendor bills journals.\n"
        "Select 'Cash' or 'Bank' for journals that are used in customer or vendor payments.\n"
        "Select 'General' for miscellaneous operations journals.",
    )
    type = fields.Selection(compute="_compute_type", store=True)
    default_account_id = fields.Many2one(
        comodel_name="account.account",
        compute="_compute_default_account_id",
        readonly=False,
        store=True,
    )
    payment_debit_account_id = fields.Many2one(
        comodel_name="account.account",
        compute="_compute_payment_account_id",
        readonly=False,
        store=True,
    )
    payment_credit_account_id = fields.Many2one(
        comodel_name="account.account",
        compute="_compute_payment_account_id",
        readonly=False,
        store=True,
    )

    @api.depends("display_type")
    def _compute_type(self):
        for record in self:
            if record.display_type == "payment":
                record.type = "bank"
            else:
                record.type = record.display_type

    @api.depends("display_type", "payment_debit_account_id")
    def _compute_default_account_id(self):
        for record in self:
            if record.display_type == "payment":
                record.default_account_id = record.payment_debit_account_id

    @api.depends("display_type", "default_account_id")
    def _compute_payment_account_id(self):
        for record in self:
            if record.type == "cash":
                record.payment_debit_account_id = record.default_account_id
                record.payment_credit_account_id = record.default_account_id

    @api.model
    def _fill_missing_values(self, vals):
        # _fill_missing_values automaticly create a account if not set,
        #  this code bypass this behavior
        if vals.get("display_type") == "payment":
            vals["default_account_id"] = True
        elif vals.get("display_type") == "cash":
            vals["payment_debit_account_id"] = True
            vals["payment_credit_account_id"] = True
        super()._fill_missing_values(vals)
        if vals.get("display_type") == "payment":
            vals.pop("default_account_id")
        # allow journal creation if display_type not define
        if not vals.get("display_type"):
            vals["display_type"] = vals["type"]
        elif vals.get("display_type") == "cash":
            vals.pop("payment_debit_account_id")
            vals.pop("payment_credit_account_id")
