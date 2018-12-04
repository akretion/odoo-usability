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

    def _notify_by_email(
        self, message, force_send=False, send_after_commit=True,
        user_signature=True):
        if not self._context.get('custom_layout'):
            self = self.with_context(
                custom_layout='mail_usability.mail_template_notification')
	return super(ResPartner, self)._notify_by_email(
            message, force_send=force_send,
            send_after_commit=send_after_commit,
            user_signature=user_signature)


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
        # Do not implicitly follow an object by just sending a message
	return super(MailThread,
            self.with_context(mail_create_nosubscribe=True)
            ).message_post(
                body=body, subject=subject, message_type=message_type,
                subtype=subtype, parent_id=parent_id, attachments=attachments,
                content_subtype=content_subtype, **kwargs)
