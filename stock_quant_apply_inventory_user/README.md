By default, users must be part of the *Stock Manager* group to modify the stock level of a product... but, when a user belongs to that group, he can change the configuration of stock locations, picking types, etc. which can break the configuration.

With this module, a user part of the *Stock User* group can modify the stock level of a product.

**WARNING**: this module requires to apply a patch on the stock module of Odoo. The patch is available in the root directory of the module, cf file ```odoo-stock_apply_inventory_by_user.diff```
