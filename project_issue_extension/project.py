# -*- encoding: utf-8 -*-
##############################################################################
#
#    Project Issue Extension module for OpenERP
#    Copyright (C) 2014 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm, fields


class project_issue(orm.Model):
    _inherit = 'project.issue'

    def name_get(self, cr, uid, ids, context=None):
        res = []
        if isinstance(ids, (int, long)):
            ids = [ids]
        for record in self.browse(cr, uid, ids, context=context):
            res.append((record.id, u'[%s] %s' % (record.number, record.name)))
        return res

    _columns = {
        'number': fields.char('Number', size=32),
        'create_date': fields.datetime('Creation Date', readonly=True),
        'target_date': fields.datetime('Target Resolution Date'),
        'product_ids': fields.many2many(
            'product.product', string="Related Products"),
    }

    _defaults = {
        'number': lambda self, cr, uid, context:
        self.pool['ir.sequence'].next_by_code(
            cr, uid, 'project.issue', context=context),
    }

    _sql_constraints = [(
        'number_company_uniq',
        'unique(number, company_id)',
        'An issue with the same number already exists for this company !'
        )]

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default.update({
            'number': self.pool['ir.sequence'].next_by_code(
                cr, uid, 'project.issue', context=context),
        })
        return super(project_issue, self).copy(
            cr, uid, id, default=default, context=context)
