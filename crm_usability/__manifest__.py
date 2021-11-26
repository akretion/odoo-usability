# Copyright 2016-2021 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

{
    "name": "CRM Usability",
    "version": "14.0.1.0.0",
    "category": "Customer Relationship Management",
    "license": "AGPL-3",
    "summary": "CRM usability enhancements",
    "description": """
CRM Usability
=============

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    "author": "Akretion",
    "website": "https://github.com/OCA/odoo-usability",
    "depends": ["crm"],
    "data": [
        "views/crm_lead.xml",
    ],
    "installable": True,
}
