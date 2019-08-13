# Copyright (C) 2015-2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Sale Margin No Onchange',
    'version': '12.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Copy standard price on sale order line and compute margins',
    'description': """
This module copies the field *standard_price* of the product on the sale order line when the sale order line is created and then computes the margin of the sale order and the sale order line (in the currency of the quotation, in the currency of the company and the margin rate).

I decided to develop this module as an alternative to the OCA sale margin modules because I wanted a small and simple module. The module *account_invoice_margin*, available in the same Github repository, do the same thing on customer invoices.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale'],
    'data': ['sale_view.xml'],
    'installable': True,
}
