# -*- coding: utf-8 -*-
#  Copyright (C) 2016-2018 Akretion (http://www.akretion.com)
#  @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'L10n FR Intrastat Product ODS',
    'version': '10.0.0.1.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'summary': 'Adds a Py3o ODS report on DEB',
    'description': """
L10n FR Intrastat Product ODS
=============================

This module will add a Py3o ODS report on French Intrastat Product Declaration (DEB).

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': "Akretion",
    'website': 'http://www.akretion.com',
    'depends': ['l10n_fr_intrastat_product', 'report_py3o'],
    'data': ['report.xml'],
    'installable': True,
}
