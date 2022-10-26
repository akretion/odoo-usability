# Copyright 2015-2022 Akretion France (http://www.akretion.com/)
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
        # Start copy from native method
        smtp_from, smtp_to_list, message = self._prepare_email_message(
            message, smtp_session)
        # End copy from native method
        logger.info(
            "Sending email from '%s' to '%s' Cc '%s' Bcc '%s' "
            "with subject '%s'",
            smtp_from, message.get('To'), message.get('Cc'),
            message.get('Bcc'), message.get('Subject'))
        return super().send_email(
            message, mail_server_id=mail_server_id,
            smtp_server=smtp_server, smtp_port=smtp_port,
            smtp_user=smtp_user, smtp_password=smtp_password,
            smtp_encryption=smtp_encryption, smtp_ssl_certificate=smtp_ssl_certificate,
            smtp_ssl_private_key=smtp_ssl_private_key, smtp_debug=smtp_debug,
            smtp_session=smtp_session)
