# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from openupgradelib import openupgrade


def install_sale_report_module(cr):
    cr.execute(
        """
        UPDATE ir_module_module
        SET state = 'to install'
        WHERE name = 'pos_sale_report_tax_amount'
        AND state = 'uninstalled'
        """
    )


@openupgrade.migrate()
def migrate(env, version):
    install_sale_report_module(env.cr)
