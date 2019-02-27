# -*- coding: utf-8 -*-
# Copyright 2019 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class ResBank(models.Model):
    _inherit = 'res.bank'

    @api.multi
    @api.depends('name', 'bic')
    def name_get(self):
        result = []
        for bank in self:
            name = bank.name
            if bank.bic:
                name = u'[%s] %s' % (bank.bic, name)
            result.append((bank.id, name))
        return result
