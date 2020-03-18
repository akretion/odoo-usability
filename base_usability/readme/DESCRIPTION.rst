This module adds the following functions:

* Adds *track_visibility='onchange'* on all the important fields of the Partner object
* By default, Odoo doesn't display the title field on all the partner form views. This module fixes it (it replaces the module base_title_on_partner)
* Adds a log message at INFO level when sending an email via SMTP
* Displays the local modules with installable filter
* A group by "State" is added to module search view
* Provides a _display_report_header method on the res.company object and _display_full_address on res.partner which are useful for reporting.
* Add model in cron tree view
* Add prefix field in sequence search view
* Better search and form view for country and state
* Display technical name of modules in kanban view
* Change module filter to `installable`
* Add widget=handle on sequence of res.partner.bank 
* Add city and country in partner tree view
* Add widget="email" on email of contacts
* Add script to fix partners related to users in multi-company setup
* Add methods for py3o reports
* Add name_get() on ir.model
* Language wizard defaults to ".po"
* Add tracking on partner fields
* Handle lang in name_title field
* Remove empty lines in address
* Add bank Name field on res.partner.bank
* Partners auto-created for users are Suppliers and not Customers
