# Copyright 2020-2023 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.osv import expression


class DynamicList(models.Model):
    _name = 'dynamic.list'
    _description = 'Dynamic List (non translatable)'
    _order = 'sequence, id'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    domain = fields.Selection([], string='Domain', required=True, index=True)

    _sql_constraint = [(
        'domain_name_uniq',
        'unique(domain, name)',
        'This entry already exists!'
        )]


class DynamicListTranslate(models.Model):
    _name = 'dynamic.list.translate'
    _description = 'Translatable Dynamic List'
    _order = 'sequence, id'

    name = fields.Char(translate=True, required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    domain = fields.Selection([], string='Domain', required=True, index=True)

    _sql_constraint = [(
        'domain_name_uniq',
        'unique(domain, name)',
        'This entry already exists!'
        )]


class DynamicListCode(models.Model):
    _name = 'dynamic.list.code'
    _description = 'Dynamic list with code'
    _order = 'sequence, id'
    _rec_names_search = ['code', 'name']

    code = fields.Char(required=True)
    name = fields.Char(translate=True, required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    domain = fields.Selection([], string='Domain', required=True, index=True)

    _sql_constraint = [(
        'domain_code_uniq',
        'unique(domain, code)',
        'This code already exists!'
        )]

    @api.depends('code', 'name')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = '[%s] %s' % (rec.code, rec.name)


class DynamicListCodeTranslate(models.Model):
    _name = 'dynamic.list.code.translate'
    _description = 'Translatable dynamic list with code'
    _order = 'sequence, id'
    _rec_names_search = ['code', 'name']

    code = fields.Char(required=True)
    name = fields.Char(translate=True, required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    domain = fields.Selection([], string='Domain', required=True, index=True)

    _sql_constraint = [(
        'domain_code_uniq',
        'unique(domain, code)',
        'This code already exists!'
        )]

    @api.depends('code', 'name')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = '[%s] %s' % (rec.code, rec.name)
