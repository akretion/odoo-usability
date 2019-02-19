# -*- coding: utf-8 -*-
# Copyright (C) 2016-2017 Akretion (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, api
import logging
_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def _active_message_auto_subscribe_notify(self):
        _logger.debug('Skip automatic subscribe notification')
        return False

    def _message_auto_subscribe_notify(self, partner_ids):
        if self._active_message_auto_subscribe_notify():
            return super(MailThread, self)._message_auto_subscribe_notify(
                partner_ids)
        else:
            return True

    @api.multi
    @api.returns('self', lambda value: value.id)
    def message_post(self, body='', subject=None, message_type='notification',
                     subtype=None, parent_id=False, attachments=None,
                     content_subtype='html', **kwargs):
        if not 'mail_create_nosubscribe' in self._context:
            # Do not implicitly follow an object by just sending a message
            self = self.with_context(mail_create_nosubscribe=True)
	return super(MailThread,
            self.with_context(mail_create_nosubscribe=True)
            ).message_post(
                body=body, subject=subject, message_type=message_type,
                subtype=subtype, parent_id=parent_id, attachments=attachments,
                content_subtype=content_subtype, **kwargs)
