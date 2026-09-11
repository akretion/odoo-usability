Stock Valuation XLSX History
============================

Schedule the valuation and variation XLSX wizards provided by
``stock_valuation_xlsx`` and retain their files as permanent attachments.
The reports retain the calculations and limitations of that module.

Configuration
-------------

Inventory managers can create configurations under **Inventory > Configuration
> Scheduled Stock XLSX Exports**. Choose the report type, company, root location
(including children), product categories, dates and report options.

* **Rolling Dates** recalculates each date at execution time using an offset in
  24-hour days. A variation defaults to the previous 30 days through the present.
* **Fixed Dates** reuses the specified timestamps on every execution.
* Present valuation and present variation end dates always use current stock.
* Archive a configuration to exclude it from scheduled executions.
* **Generate Now** generates, saves and downloads a report immediately.

Two active daily scheduled actions are installed: **Stock XLSX: Export
Valuations** and **Stock XLSX: Export Variations**. Each executes all active
configurations of its report type. No configurations are created automatically.
Administrators can change the interval, next execution and execution user under
**Settings > Technical > Automation > Scheduled Actions** in developer mode.
If changing the execution user, use an inventory manager with access to every
company whose exports should run. By default the actions run as Odoo's system
user and process each configuration in its own company context.

Failed generation raises an error to Odoo's scheduler and rolls back that cron
execution, including earlier exports in the same execution. Correct the reported
configuration before retrying. Large reports may require increasing Odoo's cron
execution limits.

Usage
-----

Inventory users can open **Inventory > Reporting > Stock XLSX Export History**
and use the **Download** button on each row. The detail view contains the exact
wizard parameters and resolved timestamps used for the export. Files remain
available after the temporary wizard or configuration is deleted.

History and downloads follow the user's allowed companies. Inventory users have
read access; inventory managers can manage configurations and delete history.
Every successful execution creates a new record, even for identical parameters.
There is no automatic retention cleanup.

The dependency's valuation wizard currently determines its cost date from its
temporality even though it exposes a Cost Price Date option. This module passes
that option through unchanged and does not change the report calculation.

Credits
-------

* Akretion

License: AGPL-3.0 or later.
