# Copyright 2022 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Move Label Copy',
    'version': '14.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'When creating a Journal Entry manually, copy label from line to line',
    'description': """
Account Move Label Copy
=======================

This module is ONLY for users who don't accept to use the 'Reference' (ref) to store the description of the journal entry (the recommended method), but want to use the label on the lines for that purpose (name field of account.move.line). With this module, the label of the first line will be copied by default to the other lines upon creation of each line.

I don't recommend the use of this module.
""",
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': [
        'account',
        'base_view_inheritance_extension',
        ],
    'data': [
        'views/account_move.xml',
        ],
    'installable': False,
}
