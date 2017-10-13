# -*- coding: utf-8 -*-
# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError
from datetime import datetime, timedelta
import logging
logger = logging.getLogger(__name__)


class ResUsersAuthLog(models.Model):
    _name = 'res.users.auth.log'
    _description = 'Users Authentication Logs'
    _order = 'date desc'
    _rec_name = 'date'

    user_id = fields.Many2one(
        'res.users', string='User', ondelete='cascade', readonly=True)
    login = fields.Char(string='Login', readonly=True)
    date = fields.Datetime(
        string='Authentication Date', required=True, readonly=True)
    result = fields.Selection([
        ('success', 'Success'),
        ('failure', 'Failure'),
        ], string='Result', required=True, readonly=True)

    @api.model
    def create(self, vals):
        if not self._context.get('authenticate_create'):
            raise UserError(_(
                "You cannot manually create an authentication log."))
        return super(ResUsersAuthLog, self).create(vals)

    @api.multi
    def write(self, vals):
        raise UserError(_("You cannot modify an authentication log."))

    @api.model
    def _purge_old_auth_logs(self):
        expiry_date = datetime.today() - timedelta(days=365)
        self._cr.execute(
            "DELETE FROM res_users_auth_log WHERE date <= %s", (expiry_date, ))
        logger.info('Auth logs older than %s have been purged', expiry_date)
