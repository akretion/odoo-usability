# -*- coding: utf-8 -*-
# Copyright (C) 2021 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProcurementMassCancel(models.TransientModel):
    _name = 'procurement.mass.cancel'
    _description = 'Procurement Order Mass Cancel'

    def run(self):
        assert self.env.context.get('active_model') == 'procurement.order'
        active_ids = self.env.context.get('active_ids')
        assert active_ids
        procs = self.env['procurement.order'].browse(active_ids)
        procs.cancel()  # they already do the filtered on state != done
