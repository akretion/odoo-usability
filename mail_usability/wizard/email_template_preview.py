# -*- coding: utf-8 -*-
# Copyright 2019 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class TemplatePreview(models.TransientModel):
    _inherit = "email_template.preview"

    res_id = fields.Integer(compute='_compute_res_id')
    object_id = fields.Reference(selection='_reference_models')

    @api.model
    def default_get(self, fields):
        result = super(TemplatePreview, self).default_get(fields)
        if result.get('model_id'):
            model = self.env['ir.model'].browse(result['model_id'])
            result['object_id'] = model.model
        return result

    def _reference_models(self):
        result = self.default_get(['model_id'])
        if result.get('model_id'):
            model = self.env['ir.model'].browse(result['model_id'])
            return [(model.model, model.name)]
        else:
            models = self.env['ir.model'].search([('state', '!=', 'manual')])
            return [(model.model, model.name)
                    for model in models
                    if not model.model.startswith('ir.')]

    @api.depends('object_id')
    def _compute_res_id(self):
        for record in self:
            if self.object_id:
                record.res_id = self.object_id.id

    def send(self):
        template = self.env['mail.template'].browse(
            self._context['template_id'])
        template.send_mail(
            self.res_id, force_send=True, raise_exception=True)
