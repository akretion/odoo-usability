# coding: utf-8
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Calendar Default Values',
    'summary': 'Makes calendar creation quicker',
    'description': """
Calendar Default Values
=======================

Define opening hours for each day of week at calendar creation.

Method to override for behavior customization:

    - get_my_calendar_data()
    - map_day()
    - string_format()

""",
    'version': '10.0.1.0.0',
    'author': 'Akretion',
    'category': 'base',
    'depends': [
        'resource',
    ],
    'website': 'http://www.akretion.com/',
    'data': [
        'calendar_view.xml',
    ],
    'license': 'AGPL-3',
}
