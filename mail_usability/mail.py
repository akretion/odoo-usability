# -*- coding: utf-8 -*-
# Copyright (C) 2016-2017 Akretion (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    notify_email = fields.Selection(
        selection_add=[
            ('all_except_notification', 'All Messages Except Notifications')],
        default='all_except_notification')

    @api.multi
    def _notify(
            self, message, force_send=False, send_after_commit=True,
            user_signature=True):
        if message.message_type == 'notification':
            message_sudo = message.sudo()
            email_channels = message.channel_ids.filtered(
                lambda channel: channel.email_send)
            bad_email = message_sudo.author_id and\
                message_sudo.author_id.email or message.email_from
            self.sudo().search([
                '|',
                ('id', 'in', self.ids),
                ('channel_ids', 'in', email_channels.ids),
                ('email', '!=', bad_email),
                ('notify_email', '=', 'always')])._notify_by_email(
                    message, force_send=force_send,
                    send_after_commit=send_after_commit,
                    user_signature=user_signature)
            self._notify_by_chat(message)
            return True
        else:
            return super(ResPartner, self)._notify(
                message, force_send=force_send,
                send_after_commit=send_after_commit,
                user_signature=user_signature)
