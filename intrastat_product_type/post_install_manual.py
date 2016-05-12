# -*- coding: utf-8 -*-

# POST-INIT-HOOK doesn't work in v7 (only v8 and above)
# So the SQL needs to be executed manually
def set_intrastat_type_on_products(cr, pool):
    cr.execute(
        "UPDATE product_template SET intrastat_type='service' "
        "WHERE type='service'")
    return
