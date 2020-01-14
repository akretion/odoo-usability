# Copyright 2016-2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Intrastat Product Type',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'summary': 'Adds a special field Intrastat Type on Products',
    'description': """
Intrastat Product Type
======================

This module is designed for a very special usage scenario. Some companies want to handle the delivery of services the same way as they handle the delivery of goods ; they want to show the services in the delivery note, etc. So, those companies configure the services with Type = *Consumable*. This works well to have the services on the outgoing pickings, but it is a problem for the intrastat declarations.

This module adds a field *Intrastat Type* on the Product Form with 2 possible options: *Product* or *Service*. The intrastat declaration will use this field instead of the native *Type* field.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['intrastat_product', 'l10n_fr_intrastat_service'],
    'data': ['product_view.xml'],
    'post_init_hook': 'set_intrastat_type_on_products',
    'installable': True,
}
