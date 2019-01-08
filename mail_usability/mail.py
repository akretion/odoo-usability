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


class TemplatePreview(models.TransientModel):
    _inherit = "email_template.preview"

    res_id = fields.Integer(compute='_compute_res_id')
    object_id = fields.Reference(selection='_reference_models')

    @api.model
    def default_get(self, fields):
        result = super(TemplatePreview, self).default_get(fields)
        if result.get('model_id'):
            model = self.env['ir.model'].browse(result['model_id'])
            result['object_id'] = model.model
        return result

    def _reference_models(self):
        result = self.default_get(['model_id'])
        if result.get('model_id'):
            model = self.env['ir.model'].browse(result['model_id'])
            return [(model.model, model.name)]
        else:
            models = self.env['ir.model'].search([('state', '!=', 'manual')])
            return [(model.model, model.name)
                    for model in models
                    if not model.model.startswith('ir.')]

    @api.depends('object_id')
    def _compute_res_id(self):
        for record in self:
            if self.object_id:
                record.res_id = self.object_id.id

    def send(self):
        template = self.env['mail.template'].browse(
            self._context['template_id'])
        template.send_mail(
            self.res_id, force_send=True, raise_exception=True)


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

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
