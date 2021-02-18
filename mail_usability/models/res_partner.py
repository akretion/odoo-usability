# Copyright 2016-2019 Akretion France (http://www.akretion.com)
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    opt_out = fields.Boolean(track_visibility='onchange')

    @api.model
    def _notify(self, message, rdata, record, force_send=False,
                send_after_commit=True, model_description=False,
                mail_auto_delete=True):
        # use an empty layout for notification by default
        if not message.layout:
            message.layout = 'mail_usability.message_notification_email_usability'
        # Never auto delete notification email
        # fucking to hard to debug when message have been delete
        mail_auto_delete = False
        return super(ResPartner, self)._notify(
            message=message, rdata=rdata, record=record,
            force_send=force_send, send_after_commit=send_after_commit,
            model_description=model_description, mail_auto_delete=mail_auto_delete)
