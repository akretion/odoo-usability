# Copyright 2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Product Fiscal Classification - Sale',
    'version': '16.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Glue module between account_product_fiscal_classification and sale',
    'description': """
This module adds a **Start Date** and **End Date** field on invoice
lines. For example, if you have an insurance contrat for your company
that run from April 1st 2013 to March 31st 2014, you will enter these
dates as start and end dates on the supplier invoice line. If your
fiscal year ends on December 31st 2013, 3 months of expenses are part of
the 2014 fiscal year and should not be part of the 2013 fiscal year. So,
thanks to this module, you will create a *Prepaid Expense* on December
31st 2013 and OpenERP will identify this expense with the 3 months that
are after the cut-off date and propose to generate the appropriate
cut-off journal entry.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'maintainers': ['alexis-via'],
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['sale', 'account_product_fiscal_classification'],
    "data": ['report/sale_report_view.xml'],
    'auto_install': True,
}
