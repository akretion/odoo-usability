# -*- coding: utf-8 -*-
# Copyright 2016-2019 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def set_intrastat_type_on_products(cr, registry):
    cr.execute(
        "UPDATE product_template SET intrastat_type='service' "
        "WHERE type='service'")
    return
