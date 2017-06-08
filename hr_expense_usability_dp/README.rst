======================================
HR Expense Usability Decimal Precision
======================================

I want to be able to have a decimal precision different from the default 'Product Price' precision. But, if I create this new decimal precision via the XML data of the *hr_expense_usability* module, it won't apply on demo data nor data created via post_install script, because it's too "late" in the module installation process. I tried to create this new decimal precision via a *pre_init_hook*, but it doesn't work. So I decided to make a small module that only creates this decimal precision and the *hr_expense_usability* module depends on it.

Credits
=======

Contributors
------------

* Alexis de Lattre <alexis.delattre@akretion.com>
