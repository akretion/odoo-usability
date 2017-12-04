# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

from odoo import models


class ResourceCalendarLeaves(models.Model):
    _inherit = "resource.calendar.leaves"

    def name_get(self):
        res = []
        for caleaves in self:
            name = caleaves.name
            if caleaves.resource_id:
                if name:
                    name = '%s (%s)' % (name, caleaves.resource_id.name)
                else:
                    name = caleaves.resource_id.name
            res.append((caleaves.id, name))
        return res
