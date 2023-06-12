# Copyright 2023 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Project Usability',
    'version': '14.0.1.0.0',
    'category': 'Services/Project',
    'license': 'AGPL-3',
    'summary': 'Usability improvements on project module',
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': [
        'project',
        ],
    'data': [
        'views/project_project.xml',
        ],
    'installable': True,
}
