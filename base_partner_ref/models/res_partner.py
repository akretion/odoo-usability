# Copyright 2017-2023 Akretion France (https://akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
import re


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ref = fields.Char(copy=False)  # To avoid blocking duplicate

    _sql_constraints = [(
        'ref_unique',
        'unique(ref)',
        'A partner already exists with this internal reference!'
        )]

    # add 'ref' in depends
    @api.depends('ref')
    def _compute_display_name(self):
        super()._compute_display_name()

    def _get_complete_name(self):
        self.ensure_one()
        displayed_types = self._complete_name_displayed_types
        type_description = dict(self._fields['type']._description_selection(self.env))
        name = self.name or ''
        # START modif of native method
        if not self._context.get('show_address') and self.ref:
            name = "[%s] %s" % (self.ref, name)
        # END modif of native method
        if self.company_name or self.parent_id:
            if not name and self.type in displayed_types:
                name = type_description[self.type]
            if not self.is_company:
                name = f"{self.commercial_company_name or self.sudo().parent_id.name}, {name}"
                # START modif of native method
                if not self._context.get('show_address') and self.parent_id.ref:
                    name = f"[{self.parent_id.ref}] {name}"
                # END modif of native method
        return name.strip()

    # native _rec_names_search contains "ref", so no need to inherit name_search()
