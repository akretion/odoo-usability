# Copyright 2015-2024 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
import logging

logger = logging.getLogger(__name__)


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    @api.model
    def send_email(
            self, message, mail_server_id=None, smtp_server=None, smtp_port=None,
            smtp_user=None, smtp_password=None, smtp_encryption=None,
            smtp_ssl_certificate=None, smtp_ssl_private_key=None,
            smtp_debug=False, smtp_session=None):
        # _prepare_email_message() removes the Bcc header from the message
        # (recipients are still delivered via the SMTP envelope): keep it
        # to log it.
        email_bcc = message['Bcc']
        # Let the native method do the whole connect/prepare/send. Preparing
        # the message here and passing it + the session to super() triggers a
        # SECOND _prepare_email_message() in the native method, which drops
        # the author display name added by the From encapsulation logic
        # (encapsulate_email) introduced in Odoo 18.
        res = super().send_email(
            message, mail_server_id=mail_server_id,
            smtp_server=smtp_server, smtp_port=smtp_port,
            smtp_user=smtp_user, smtp_password=smtp_password,
            smtp_encryption=smtp_encryption, smtp_ssl_certificate=smtp_ssl_certificate,
            smtp_ssl_private_key=smtp_ssl_private_key, smtp_debug=smtp_debug,
            smtp_session=smtp_session)
        logger.info(
            "Sending email from '%s' to '%s' Cc '%s' Bcc '%s' "
            "with subject '%s'.",
            message.get('From'), message.get('To'), message.get('Cc'),
            email_bcc, message.get('Subject'))
        return res
