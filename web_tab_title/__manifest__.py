# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Web Tab Title',
    'description': """
        Automatically set tab document.title when empty.
        Important limitation: the tab will get its title only once you browse it.
    """,
    'version': '14.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Akretion',
    'website': 'akretion.com',
    'depends': [
        'web',
    ],
    'data': [
    ],
    'demo': [
    ],
    "data": ["views/web_tab_title.xml"],
    "maintainers": ["rvalyi"],
    "installable": False,
}
