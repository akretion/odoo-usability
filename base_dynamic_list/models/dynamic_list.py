# Copyright 2020-2023 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


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
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '[%s] %s' % (rec.code, rec.name)))
        return res

    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        if args is None:
            args = []
        ids = []
        if name and operator == 'ilike':
            ids = list(self._search([('code', '=', name)] + args, limit=limit))
            if ids:
                return ids
        return super()._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)


class DynamicListCodeTranslate(models.Model):
    _name = 'dynamic.list.code.translate'
    _description = 'Translatable dynamic list with code'
    _order = 'sequence, id'

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
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '[%s] %s' % (rec.code, rec.name)))
        return res

    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        if args is None:
            args = []
        ids = []
        if name and operator == 'ilike':
            ids = list(self._search([('code', '=', name)] + args, limit=limit))
            if ids:
                return ids
        return super()._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)
