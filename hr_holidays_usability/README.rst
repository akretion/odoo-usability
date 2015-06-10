HR Holidays Usability
=====================

This module adds what I consider the minimum usability level for the holiday management module in Odoo:

 * By default, if you only use the official *hr_holidays* module, there the number of days is not automatically computed from the start date and end date. This module fixes it : it counts the number of days following a computation method that is defined on the object hr.holiday.status. It also replaces the datetime field for start/end dates by a date field plus a selection field to indicated morning/noon/evening.

 * It depends on the OCA module *hr_public_holidays* to easily define the bank holidays per country. It takes those bank holidays into account when counting the number of days.

 * It sends an email to the manager when the employee submits a holiday requests (with the employee in Cc) and it sends an email to the employee (with the manager in Cc) when the holiday request is validated/refused.

Credits
=======

Contributors
------------

* Alexis de Lattre <alexis.delattre@akretion.com>
