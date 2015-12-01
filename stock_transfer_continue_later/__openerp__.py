# -*- coding: utf-8 -*-
##############################################################################
#
#    Stock Transfer Continue Later module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
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


{
    'name': 'Stock Transfer Continue Later',
    'version': '0.2',
    'category': 'Inventory, Logistic, Storage',
    'license': 'AGPL-3',
    'summary': "Add button 'Save and continue later' on picking Transfer wizard",
    'description': """
Stock Transfer Continue Later
=============================

This module adds a button *Save and Continue Later* on the Transfer pop-up of the picking. This is usefull for example if you have a big reception and you cannot handle it in one go but you work on it in several steps before you validate the full transfer.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['stock'],
    'data': ['wizard/stock_transfer_details.xml'],
    'installable': True,
}
