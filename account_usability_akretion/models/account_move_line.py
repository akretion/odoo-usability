# Copyright 2015-2026 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
import logging

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    # Native order:
    # _order = "date desc, move_name desc, id"
    # Problem: when you manually create a journal entry, the
    # order of the lines is inverted when you save ! It is quite annoying for
    # the user...
# Maybe it's not the case in 20
#    _order = "date desc, id asc"

    # for optional display in list view
    product_barcode = fields.Char(related='product_id.barcode', string="Product Barcode")

    def show_account_move_form(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            'account.action_move_line_form')
        action.update({
            'res_id': self.move_id.id,
            'view_id': False,
            'views': False,
            'view_mode': 'form,list',
        })
        return action

#    def update_matching_number(self):
#        records = self.search([("matching_number", "=", "P")])
#        _logger.info(f"Update partial reconcile number for {len(records)} lines")
#        records._compute_matching_number()

#    def _compute_matching_number(self):
        # TODO maybe it will be better to have the same maching_number for
        # all partial so it will be easier to group by
#        super()._compute_matching_number()
#        for record in self:
#            if record.matching_number == "P":
#                record.matching_number = ", ".join([
#                    "a%d" % pr.id
#                    for pr in record.matched_debit_ids + record.matched_credit_ids
#                ])

    def _compute_name(self):
        # This is useful when you want to have the product code in a dedicated
        # column in your customer invoice report
        # The same ir.config_parameter is used in sale_usability,
        # purchase_usability and account_usability
        no_product_code_param = self.env['ir.config_parameter'].sudo().get_bool(
            'usability.line_name_no_product_code')
        if no_product_code_param and no_product_code_param == 'True':
            self = self.with_context(display_default_code=False)
        return super()._compute_name()

#    def reconcile(self):
#        """Explicit error message if unposted lines"""
#        unposted_ids = self.filtered(lambda l: l.move_id.state != "posted")
#        if unposted_ids:
#            m = _("Please post the following entries before reconciliation :")
#            sep = "\n - "
#            unpost = sep.join([am.display_name for am in unposted_ids.move_id])
#            raise UserError(m + sep + unpost)
#        return super().reconcile()
