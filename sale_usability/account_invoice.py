# Copyright (C) 2015-2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from collections import OrderedDict


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def py3o_lines_layout_groupby_order(self, subtotal=True):
        # This method is an alternative to the method py3o_lines_layout()
        # defined above: you just have to change the call in the invoice
        # ODT template
        self.ensure_one()
        res1 = OrderedDict()
        # {categ(1): {'lines': [l1, l2], 'subtotal': 23.32}}
        soo = self.env['sale.order']
        for line in self.invoice_line_ids:
            order = line.sale_line_ids and line.sale_line_ids[0].order_id\
                or soo
            if order in res1:
                res1[order]['lines'].append(line)
                res1[order]['subtotal'] += line.price_subtotal
            else:
                res1[order] = {
                    'lines': [line],
                    'subtotal': line.price_subtotal}
        # from pprint import pprint
        # pprint(res1)
        res2 = []
        if len(res1) == 1 and not res1.keys()[0]:
            # No order at all
            for line in res1.values()[0]['lines']:
                res2.append({'line': line})
        else:
            for order, ldict in res1.items():
                res2.append({'categ': order})
                for line in ldict['lines']:
                    res2.append({'line': line})
                if subtotal:
                    res2.append({'subtotal': ldict['subtotal']})
        # res2:
        # [
        #    {'categ': categ(1)},
        #    {'line': invoice_line(2)},
        #    {'line': invoice_line(3)},
        #    {'subtotal': 8932.23},
        # ]
        # pprint(res2)
        return res2
