# Copyright 2014-2020 Akretion France (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'POS Config Single User',
    'version': '14.0.1.0.0',
    'category': 'Point Of Sale',
    'license': 'AGPL-3',
    'summary': 'Configure on each pos.config a single user allowed to start it',
    'description': """
POS Config Single User
======================

New parameter on pos.config: the (only) user allowed to start sessions of this pos.config.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['point_of_sale'],
    'data': ['pos_view.xml'],
    'installable': True,
}
