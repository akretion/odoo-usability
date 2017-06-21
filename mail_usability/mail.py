# -*- coding: utf-8 -*-
##############################################################################
#
#    Mail Usability module for Odoo
#    Copyright (C) 2016 Akretion (http://www.akretion.com)
#    @author Benoît Guillot <benoit.guillot@akretion.com>
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

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    notify_email = fields.Selection(
        selection_add=[
            ('all_except_notification', 'All Messages Except Notifications')],
        default='all_except_notification')


class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.model
    def send_get_mail_body(self, mail, partner=None):
        """
        Avoid unwanted links in mail footer.
        """
        return mail.body_html


class MailNotification(models.Model):
    _inherit = 'mail.notification'

    @api.cr_uid_id_context
    def get_signature_footer(
            self, cr, uid, user_id, res_model=None, res_id=None, context=None,
            user_signature=True):
        """
        Remove : "Sent by 'Your Company' using Odoo" from signature.
        """
        footer = super(MailNotification, self).get_signature_footer(
            cr, uid, user_id, res_model=res_model, res_id=res_id,
            context=context, user_signature=user_signature)
        footer = footer[:footer.find('\n<br /><small>Sent by ')]
        footer = footer[:footer.find(u'\n<br /><small>Envoyé par ')]
        return footer

    @api.multi
    def get_partners_to_email(self, message):
        notify_pids = super(MailNotification, self).get_partners_to_email(
            message)
        for notif in self:
            if (
                    notif.partner_id.id in notify_pids and
                    message.type == 'notification' and
                    notif.partner_id.notify_email ==
                    'all_except_notification'):
                notify_pids.remove(notif.partner_id.id)
        return notify_pids
