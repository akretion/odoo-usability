# -*- coding: utf-8 -*-
##############################################################################
#
#    Base Usability module for Odoo
#    Copyright (C) 2016 Akretion (http://www.akretion.com)
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

from openerp import models, fields
from datetime import datetime
import pytz


class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    def _interpolation_dict_context(self, context=None):
        if context is None:
            context = {}
        t = False
        if context.get('force_sequence_date'):
            date_str = context['force_sequence_date']
            if isinstance(date_str, (str, unicode)) and len(date_str) == 10:
                t = fields.Date.from_string(date_str)
        if not t:
            t = datetime.now(pytz.timezone(context.get('tz') or 'UTC'))
        sequences = {
            'year': '%Y', 'month': '%m', 'day': '%d', 'y': '%y', 'doy': '%j',
            'woy': '%W',
            'weekday': '%w', 'h24': '%H', 'h12': '%I', 'min': '%M', 'sec': '%S'
        }
        return {
            key: t.strftime(sequence)
            for key, sequence in sequences.iteritems()}
