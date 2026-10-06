# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ContactConverter(models.AbstractModel):
    _inherit = 'ir.qweb.field.contact'

    @api.model
    def value_to_html(self, value, options):
        # The Internal Reference must remain visible in the backend UI but must not
        # appear on the documents rendered with QWeb
        if value:
            value = value.with_context(no_partner_ref=True)
        return super().value_to_html(value, options)


class Many2OneConverter(models.AbstractModel):
    _inherit = 'ir.qweb.field.many2one'

    @api.model
    def value_to_html(self, value, options):
        if value and value._name == 'res.partner':
            value = value.with_context(no_partner_ref=True)
        return super().value_to_html(value, options)
