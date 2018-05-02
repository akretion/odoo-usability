# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Invoice Del Attachment Cancel module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def invoice_filename_to_match(self):
        # I cannot use
        # safe_eval(report.attachment, {'object': obj, 'time': time})
        # Because, when this code is executed, the obj.state is not 'open'
        # nor 'paid', so we can't get the filename that way
        return 'INV%.pdf'

    @api.multi
    def action_cancel_draft(self):
        res = super(AccountInvoice, self).action_cancel_draft()
        iao = self.env['ir.attachment']
        for invoice in self:
            # search for attachments
            if 'out' in invoice.type:
                filename_to_match = invoice.invoice_filename_to_match()
                attachs = iao.search([
                    ('res_id', '=', invoice.id),
                    ('res_model', '=', self._name),
                    ('type', '=', 'binary'),
                    ('datas_fname', '=like', filename_to_match),
                    ])
                if len(attachs) == 1:
                    # delete attachment
                    attach = attachs[0]
                    attach_name = attach.name
                    # I need sudo() because the user that has the right to
                    # do a "back2draft" on an invoice may not have the right
                    # to delete an account.invoice
                    attachs.sudo().unlink()
                    invoice.message_post(
                        _('Attachement %s has been deleted') % attach_name)
        return res
