# -*- coding: utf-8 -*-

from odoo import models, fields


class IrModel(models.Model):
    _inherit = 'ir.model'

    mail_follower = fields.Boolean(string='Follow', default=False,
                                   help='Check if you want create followers'
                                        ' on this model')
