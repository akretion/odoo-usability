# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

from openerp import models, fields, tools


class MergePartnerAutomatic(models.TransientModel):
    _inherit = 'base.partner.merge.automatic.wizard'

    group_by_customer = fields.Boolean('Customer', default=True)
    group_by_supplier = fields.Boolean('Supplier', default=True)

    def _generate_query(self, fields, maximum_group=100):
        sql = super(MergePartnerAutomatic, self)._generate_query(
            fields, maximum_group=maximum_group)
        name_sql_original = 'lower(name)'
        if name_sql_original in sql:
            if tools.config.get('unaccent', False):
                sql = sql.replace(
                    name_sql_original,
                    "unaccent(lower(replace(name, ' ', '')))")
            else:
                sql = sql.replace(
                    name_sql_original,
                    "lower(replace(name, ' ', ''))")

        return sql
