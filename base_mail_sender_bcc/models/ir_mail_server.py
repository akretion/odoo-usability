# Copyright 2017-2022 Akretion France
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, tools

class IrMailServer(models.Model):
    _inherit = 'ir.mail_server'

    def build_email(
        self, email_from, email_to, subject, body, email_cc=None,
        email_bcc=None, **kwargs
    ):
        """Add `email_from` in BCC right before sending the email, if:
         * Not prevented by context key `prevent_send_mail_bcc`
         * The `email_from` is an Odoo internal user. Else we might add in BCC
           and external partner when re-routing incoming emails to internal
           users who choosed `notification_type=email` in their preferences
        """
        should_bcc = email_from and not self._context.get("prevent_send_mail_bcc")
        if should_bcc:
            email_from_normalized = tools.email_normalize_all(email_from)
            user_from = self.env["res.users"].search(
                domain=[("email", "=", email_from_normalized)],
                limit=1,
            )
            should_bcc = bool(user_from) and user_from._is_internal()

        if should_bcc:
            if email_bcc is None:
                email_bcc = [email_from]
            elif isinstance(email_bcc, list) and email_from not in email_bcc:
                email_bcc.append(email_from)
        
        return super().build_email(
            email_from, email_to, subject, body, email_cc=email_cc,
            email_bcc=email_bcc, **kwargs
        )

    def _prepare_email_message(self, message, smtp_session):
        """Update context key `send_validated_to` with the possible
        added BCC email addresses"""
        if message['Bcc']:
            validated_to = self.env.context.get('send_validated_to') or []
            email_bcc_normalized = tools.email_normalize_all(message['Bcc'])
            for email in email_bcc_normalized:
                if email not in validated_to:
                    validated_to.append(email)
            self = self.with_context(send_validated_to=validated_to)
        return super()._prepare_email_message(
            message, smtp_session
        )
