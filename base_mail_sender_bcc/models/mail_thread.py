# Copyright 2024 Akretion (https://www.akretion.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_thread_by_email(self, message, recipients_data, msg_vals=False, **kwargs):
        """Prevent BCC for/when:
        1) Odoo-generated notifications (`message_type=notification`). Examples:
            * changelog-messages of fields with `tracking=True`
            * Python-submitted message, such as import reports
        2) Internal users notified by email because of their profile preference
           (`notification_type=email`).
              (!) This is not perfect: If any external partner is among the recipients,
              BCC applies normally. Internal Users will be BCC-ed as soon as at least
              1 external partner is in the recipients.
        """
        should_bcc = (
            message.message_type == "notification" or
            recipients_data and all(r.get("type") == "user" for r in recipients_data)
        )
        if should_bcc:
            self = self.with_context(prevent_send_mail_bcc=True)
        return super()._notify_thread_by_email(
            message, recipients_data, msg_vals=msg_vals, **kwargs
        )
