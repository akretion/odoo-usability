# Copyright 2016-2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import typing

from odoo import models
from odoo.tools import misc, float_compare
from odoo.tools.misc import SENTINEL, Sentinel
from odoo.api import Environment


class BaseUsabilityInstalled(models.AbstractModel):
    _name = "base.usability.installed"
    _description = "Base Usability Installed"


formatLang_original = misc.formatLang


def formatLang(
    env: Environment,
    value: float | typing.Literal[''],
    digits: int = 2,
    grouping: bool = True,
    monetary: bool | Sentinel = SENTINEL,
    dp: str | None = None,
    currency_obj=None,
    rounding_method: typing.Literal['HALF-UP', 'HALF-DOWN', 'HALF-EVEN', "UP", "DOWN"] = 'HALF-EVEN',
    rounding_unit: typing.Literal['decimals', 'units', 'thousands', 'lakhs', 'millions'] = 'decimals',
    int_no_digits: bool = True,
) -> str:
    if (
            'base.usability.installed' in env and
            int_no_digits and
            (not monetary or monetary == Sentinel.SENTINEL) and
            isinstance(value, float) and
            dp):
        prec = env['decimal.precision'].precision_get(dp)
        if not float_compare(value, int(value), precision_digits=prec):
            digits = 0
            dp = False
    res = formatLang_original(
        env, value, digits=digits, grouping=grouping,
        monetary=monetary, dp=dp, currency_obj=currency_obj,
        rounding_method=rounding_method, rounding_unit=rounding_unit)
    return res


misc.formatLang = formatLang
