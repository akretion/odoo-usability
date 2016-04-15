# -*- coding: utf-8 -*-


def set_intrastat_type_on_products(cr, pool):
    cr.execute(
        "UPDATE product_template SET intrastat_type='service' "
        "WHERE type='service'")
    return
