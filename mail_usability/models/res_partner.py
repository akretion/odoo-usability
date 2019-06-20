# -*- coding: utf-8 -*-
# Copyright (C) 2016-2019 Akretion (http://www.akretion.com)
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    notify_email = fields.Selection(
        selection_add=[
            ('all_except_notification', 'All Messages Except Notifications')],
        default='all_except_notification')
    opt_out = fields.Boolean(track_visibility='onchange')

    def _should_be_notify_by_email(self, message):
        if message.message_type == 'notification':
            if self.notify_email == 'always':
                return True
            else:
                return False
        else:
            return True

    def _notify_by_email(
        self, message, force_send=False, send_after_commit=True,
        user_signature=True):

        # use an empty layout for notification by default
        if not self._context.get('custom_layout'):
            self = self.with_context(
                custom_layout='mail_usability.mail_template_notification')

        # Filter the partner that should receive the notification
        filtered_partners = self.filtered(
            lambda p: p._should_be_notify_by_email(message)
            )

	return super(ResPartner, filtered_partners)._notify_by_email(
            message, force_send=force_send,
            send_after_commit=send_after_commit,
            user_signature=user_signature)

    def _notify_prepare_email_values(self, message):
        res = super(ResPartner, self)._notify_prepare_email_values(message)
        # Never auto delete notification email
        # fucking to hard to debug when message have been delete
        res['auto_delete'] = False
        return res
