# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Invoice Del Attachment Cancel module for OpenERP
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

from openerp.osv import orm
from openerp.tools.translate import _


class AccountInvoice(orm.Model):
    _inherit = 'account.invoice'

    def action_cancel(self, cr, uid, ids, context=None):
        res = super(AccountInvoice, self).action_cancel(
            cr, uid, ids, context=context)
        iao = self.pool['ir.attachment']
        for invoice in self.browse(cr, uid, ids, context=context):
            # search for attachments
            if 'out' in invoice.type:
                attach_ids = iao.search(
                    cr, uid, [
                        ('res_id', '=', invoice.id),
                        ('res_model', '=', self._name),
                        ('type', '=', 'binary'),
                        ('datas_fname', '=like', 'INV%.pdf'),
                        ], context=context)
                if len(attach_ids) == 1:
                    # delete attachment
                    attach = iao.browse(
                        cr, uid, attach_ids[0], context=context)
                    attach_name = attach.name
                    iao.unlink(cr, uid, attach_ids, context=context)
                    self.message_post(
                        cr, uid, invoice.id,
                        _('Attachement %s has been deleted') % attach_name)
        return res
