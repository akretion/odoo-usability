# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'MRP Usability',
    'version': '0.1',
    'category': 'Manufacturing',
    'license': 'AGPL-3',
    'summary': 'Usability improvements on manufacturing',
    'description': """
MRP Usability
=============

Small usability improvements on MRP:

* order by id desc

* show field date_start and date_finished on mrp.production form view

* show more fields on stock move form

* show bom type in tree view + add group by

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['mrp'],
    'data': ['mrp_view.xml'],
    'installable': True,
}
