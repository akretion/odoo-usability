# -*- coding: utf-8 -*-
# Copyright 2020 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Base Dynamic List',
    'version': '10.0.1.0.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'summary': 'Dynamic lists',
    'description': """
Base Dynamic List
=================

Very often during an Odoo implementation, we need to add selection fields on a native objet, and we don't want to have a hard-coded selection list (fields.Selection), but a selection list that can be changed by users (Many2one field). For that, the developper needs to add a new object (with just a 'name' and 'sequence' field) with a form/tree view. The goal of this module is to speed-up this process by defining a dynamic list object that already has all the required views.

This module provides several ready-to-go objects:

* simple list : fields *name*, *sequence* and *active*
* translatable list : fields *name* with translate=True, *sequence* and *active*
* code list : fields *code* (unique), *name*, *sequence* and *active*
* translatable code list : fields *code* (unique), *name* with translate=True, *sequence* and *active*

These objects are readable by the employee group. The system group has full rights on it.

To use it, you need to do 2 or 3 things :

1) Add an entry in the domain field and the object you selected:

domain = fields.Selection(selection_add=[('risk.type', "Risk Type")])

2) Add the many2one field on your object:

risk_type_id = fields.Many2one(
    'dynamic.list', string="Risk Type",
    ondelete='restrict', domain=[('domain', '=', 'risk.type')])


3) Optionally, you can add a dedicated action and a menu entry (otherwize, you can use the generic menu entry under *Settings > Technical > Dynamic Lists*:

<record id="dynamic_list_risk_type_action" model="ir.actions.act_window">
    <field name="name">Risk Type</field>
    <field name="res_model">dynamic.list</field>
    <field name="view_mode">tree,form</field>
    <field name="domain">[('domain', '=', 'risk.type')]</field>
    <field name="context">{'default_domain': 'risk.type'}</field>
</record>

<menuitem id="dynamic_list_risk_type_menu" action="dynamic_list_risk_type_action"
parent="parent_menu_xmlid"/>

Limitation: when you want to have different access rights on these lists depending on the source object, you should prefer to use dedicated objects.
""",
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/dynamic_list.xml',
        ],
    'installable': True,
}
