# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from email.header import decode_header
from email.errors import HeaderParseError

from odoo import models, api
from odoo.addons.base.ir.ir_mail_server import extract_rfc2822_addresses
import logging

logger = logging.getLogger(__name__)


def decode(email_header):
    result = []
    try:
        for value, encoding in decode_header(email_header):
            if encoding is not None:
                result.append(value.decode(encoding))
            else:
                result.append(unicode(value))
    except HeaderParseError:
        return email_header
    return u' '.join(result)


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
        attachment_names = [
            decode(part.get_filename())
            for part in message.walk()
            if part.get_content_maintype() not in ('multipart', 'text')]
        logger.info(
            "Sending email from '%s' to '%s' Cc '%s' Bcc '%s' "
            "with subject '%s' and attachments %s",
            smtp_from, decode(message.get('To')), decode(message.get('Cc')),
            decode(message.get('Bcc')), decode(message.get('Subject')),
            u', '.join([u"'%s'" % n for n in attachment_names])
        )
        return super(IrMailServer, self).send_email(
            message, mail_server_id=mail_server_id,
            smtp_server=smtp_server, smtp_port=smtp_port,
            smtp_user=smtp_user, smtp_password=smtp_password,
            smtp_encryption=smtp_encryption, smtp_debug=smtp_debug)
