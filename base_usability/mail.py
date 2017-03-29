# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api
from odoo.addons.base.ir.ir_mail_server import extract_rfc2822_addresses
import logging

logger = logging.getLogger(__name__)


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    @api.model
    def send_email(
            self, message, mail_server_id=None, smtp_server=None,
            smtp_port=None, smtp_user=None, smtp_password=None,
            smtp_encryption=None, smtp_debug=False):
        # Start copy from native method
        smtp_from = message['Return-Path'] or\
            self._get_default_bounce_address() or message['From']
        from_rfc2822 = extract_rfc2822_addresses(smtp_from)
        smtp_from = from_rfc2822[-1]
        # End copy from native method
        logger.info(
            "Sending email from '%s' to '%s' Cc '%s' Bcc '%s' "
            "with subject '%s'",
            smtp_from, message.get('To'), message.get('Cc'),
            message.get('Bcc'), message.get('Subject'))
        return super(IrMailServer, self).send_email(
            message, mail_server_id=mail_server_id,
            smtp_server=smtp_server, smtp_port=smtp_port,
            smtp_user=smtp_user, smtp_password=smtp_password,
            smtp_encryption=smtp_encryption, smtp_debug=smtp_debug)
