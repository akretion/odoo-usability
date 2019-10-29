# -*- coding: utf-8 -*-
# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ref = fields.Char(copy=False)  # To avoid blocking duplicate

    _sql_constraints = [(
        'ref_unique',
        'unique(ref)',
        'A partner already exists with this internal reference!'
        )]

    # in v10, display_name is store=True by default
    # so, when we inherit name_get() and use additionnal fields, we
    # have to inherit @api.depends of _compute_display_name() too
    @api.depends(
        'is_company', 'name', 'parent_id.name', 'type', 'company_name',
        'ref', 'parent_id.ref')
    def _compute_display_name(self):
        super(ResPartner, self)._compute_display_name()

    @api.multi
    def name_get(self):
        res = []
        for partner in self:
            name = partner.name or ''
            # START modif of native name_get() method
            if partner.ref:
                name = u"[%s] %s" % (partner.ref, name)
            # END modif of native name_get() method
            if partner.company_name or partner.parent_id:
                if not name and partner.type in ['invoice', 'delivery', 'other']:
                    name = dict(self.fields_get(['type'])['type']['selection'])[partner.type]
                if not partner.is_company:
                    # START modif of native name_get() method
                    company_name = partner.commercial_company_name or partner.parent_id.name
                    if partner.parent_id.ref:
                        company_name = u"[%s] %s" % (partner.parent_id.ref, company_name)
                    name = "%s, %s" % (company_name, name)
                    # END modif of native name_get() method
            if self._context.get('show_address_only'):
                name = partner._display_address(without_company=True)
            if self._context.get('show_address'):
                name = name + "\n" + partner._display_address(without_company=True)
            name = name.replace('\n\n', '\n')
            name = name.replace('\n\n', '\n')
            if self._context.get('show_email') and partner.email:
                name = "%s <%s>" % (name, partner.email)
            if self._context.get('html_format'):
                name = name.replace('\n', '<br/>')
            res.append((partner.id, name))
        return res
