# SPDX-FileCopyrightText: 2026 Akretion
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "POS Sale Report Tax Amount",
    "summary": "Add sub total amount by tax to the sale report",
    "version": "16.0.1.0.0",
    "category": "Point of sale",
    "website": "http://www.akretion.com",
    "author": "Akretion",
    "license": "AGPL-3",
    "depends": ["point_of_sale"],
    "data": ["report/pos.xml"],
    "excludes": [
        "pos_daily_sales_reports" # replaces part of report_saledetails
    ],
}
