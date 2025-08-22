# -*- coding: utf-8 -*-

from odoo import models, api
from email.utils import formataddr


class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.multi
    def send(self, auto_commit=False, raise_exception=False):
        for mail in self:
            email_to = []
            for partner in mail.recipient_ids:
                for partner_email in [formataddr((partner.name, partner.email))]:
                    email_to.append(partner_email)
            mail.email_to = email_to
        return super(MailMail, self).send(auto_commit=auto_commit,
                                          raise_exception=raise_exception)

    @api.multi
    def send_get_mail_to(self, partner=None):
        super(MailMail, self).send_get_mail_to(partner=partner)
        self.ensure_one()
        email_to = []
        for partner in self.recipient_ids:
            email_to.append(formataddr((partner.name, partner.email)))
        self.recipient_ids = [(6, 0, [])]
        return email_to
