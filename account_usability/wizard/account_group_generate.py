# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountGroupGenerate(models.TransientModel):
    _name = 'account.group.generate'
    _description = 'Generate Account Groups'

    name_prefix = fields.Char(string='Prefix', required=True, default='Comptes')
    level = fields.Integer(default=2, required=True)

    def run(self):
        if self.level < 1:
            raise UserError(_("The level must be >= 1."))
        assert isinstance(level, int)
        ago = self.env['account.group']
        company = self.env.company
        groups = ago.search([('company_id', '=', company.id)])
        if groups:
            raise UserError(_(
                "%d account groups already exists in company '%s'. This wizard is "
                "designed to generate account groups from scratch.")
                % (len(groups), company.display_name))
        accounts = self.search([('company_id', '=', company.id)])
        struct = {'childs': {}}
        for account in accounts:
            if len(account.code) <= self.level:
                raise UserError(_(
                    "The code of account '%s' is %d caracters. "
                    "It cannot be inferior to level (%d).")
                    % (account.display_name, len(account.code), self.level))
            n = 1
            parent = struct
            gparent = False
            while n <= level:
                group_code = account.code[:n]
                if group_code not in parent['childs']:
                    new_group = ago.create({
                        'name': '%s %s' % (name_prefix or '', group_code),
                        'code_prefix_start': group_code,
                        'parent_id': gparent and gparent.id or False,
                        'company_id': company.id,
                        })
                    parent['childs'][group_code] = {'obj': new_group, 'childs': {}}
                parent = parent['childs'][group_code]
                gparent = parent['obj']
                n += 1
            account.write({'group_id': gparent.id})
        action = {
            'type': 'ir.actions.act_window',
            'name': _('Account Groups'),
            'view_mode': 'tree,form',
            'res_model': 'account.group',
            }
        return action

