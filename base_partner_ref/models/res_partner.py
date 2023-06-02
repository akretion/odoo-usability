# Copyright 2017-2023 Akretion France (https://akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
import re


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ref = fields.Char(copy=False)  # To avoid blocking duplicate
    invalidate_display_name = fields.Boolean()

    _sql_constraints = [(
        'ref_unique',
        'unique(ref)',
        'A partner already exists with this internal reference!'
        )]

    # add 'ref' in depends
    @api.depends('ref', 'invalidate_display_name')
    def _compute_display_name(self):
        super()._compute_display_name()

    def _get_name(self):
        partner = self
        name = partner.name or ''

        # START modif of native method
        if partner.ref:
            name = "[%s] %s" % (partner.ref, name)
        # END modif of native method
        if partner.company_name or partner.parent_id:
            if not name and partner.type in ['invoice', 'delivery', 'other']:
                name = dict(self.fields_get(
                    ['type'])['type']['selection'])[partner.type]
            if not partner.is_company:
                # START modif of native name_get() method
                company_name = partner.commercial_company_name or\
                    partner.sudo().parent_id.name
                if partner.parent_id.ref:
                    company_name = "[%s] %s" % (partner.parent_id.ref, company_name)
                name = "%s, %s" % (company_name, name)
                # END modif of native name_get() method
        if self._context.get('show_address_only'):
            name = partner._display_address(without_company=True)
        if self._context.get('show_address'):
            name = name + "\n" + partner._display_address(without_company=True)
        name = re.sub(r'\s+\n', '\n', name)
        if self._context.get('partner_show_db_id'):
            name = "%s (%s)" % (name, partner.id)
        if self._context.get('address_inline'):
            splitted_names = name.split("\n")
            name = ", ".join([n for n in splitted_names if n.strip()])
        if self._context.get('show_email') and partner.email:
            name = "%s <%s>" % (name, partner.email)
        if self._context.get('html_format'):
            name = name.replace('\n', '<br/>')
        if self._context.get('show_vat') and partner.vat:
            name = "%s ‒ %s" % (name, partner.vat)
        return name.strip()

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        if name and operator == 'ilike':
            recs = self.search([('ref', '=', name)] + args, limit=limit)
            if recs:
                rec_childs = self.search([('id', 'child_of', recs.ids)])
                return rec_childs.name_get()
        return super().name_search(name=name, args=args, operator=operator, limit=limit)
