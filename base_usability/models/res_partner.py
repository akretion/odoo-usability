# Copyright 2015-2020 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # tracking=True is handled in the 'mail' module, and base_usability
    # doesn't depend on 'mail', so adding tracking on res.partner fields
    # has been moved to mail_usability
    ref = fields.Char(copy=False)
    # For reports
    name_title = fields.Char(compute="_compute_name_title", string="Name with Title")

    @api.depends("name", "title")
    def _compute_name_title(self):
        for partner in self:
            name_title = partner.name
            if partner.title and not partner.is_company:
                partner_lg = partner
                # If prefer to read the lang of the partner than the lang
                # of the context. That way, an English man will be displayed
                # with his title in English whatever the environment
                if partner.lang:
                    partner_lg = partner.with_context(lang=partner.lang)
                title = partner_lg.title.shortcut or partner_lg.title.name
                name_title = " ".join([title, name_title])
            partner.name_title = name_title

    def _display_address(self, without_company=False):
        """Remove empty lines"""
        res = super()._display_address(without_company=without_company)
        while "\n\n" in res:
            res = res.replace("\n\n", "\n")
        return res

    # for reports
    def _display_full_address(
        self,
        details=["company", "name", "address", "phone", "mobile", "email"],
        icon=True,
    ):
        self.ensure_one()
        # To make the icons work with py3o with PDF export, on the py3o server:
        # 1) sudo apt-get install fonts-symbola
        # 2) start libreoffice in xvfb (don't use --headless) (To confirm)
        if self.is_company:
            company = self.name
            name = False
            name_no_title = False
            title = False
            title_short = False
        else:
            company = (
                self.parent_id
                and self.parent_id.is_company
                and self.parent_id.name
                or False
            )
            name = self.name_title
            name_no_title = self.name
            title = self.title.name
            title_short = self.title.shortcut
        options = {
            "name": {
                "value": name,
            },
            "company": {
                "value": company,
            },
            "title": {
                "value": title,
            },
            "title_short": {
                "value": title_short,
            },
            "name_no_title": {
                "value": name_no_title,
            },
            "phone": {
                "value": self.phone,
                # http://www.fileformat.info/info/unicode/char/1f4de/index.htm
                "icon": "\U0001F4DE",
                "label": _("Tel:"),
            },
            "mobile": {
                "value": self.mobile,
                # http://www.fileformat.info/info/unicode/char/1f4f1/index.htm
                "icon": "\U0001F4F1",
                "label": _("Mobile:"),
            },
            "email": {
                "value": self.email,
                # http://www.fileformat.info/info/unicode/char/2709/index.htm
                "icon": "\u2709",
                "label": _("E-mail:"),
            },
            "website": {
                "value": self.website,
                # http://www.fileformat.info/info/unicode/char/1f310/index.htm
                "icon": "\U0001f310",
                "label": _("Website:"),
            },
            "address": {
                "value": self._display_address(without_company=True),
            },
            "vat": {
                "value": self.commercial_partner_id.vat,
                "label": _("VAT Number:"),
            },
            "commercial_ref": {
                "value": self.commercial_partner_id.ref,
                "label": _("Customer Number:"),
            },
            "ref": {
                "value": self.ref,
                "label": _("Customer Number:"),
            },
            # Same with 'supplier_' prefix, to change the label
            "supplier_commercial_ref": {
                "value": self.commercial_partner_id.ref,
                "label": _("Supplier Number:"),
            },
            "supplier_ref": {
                "value": self.ref,
                "label": _("Supplier Number:"),
            },
        }
        res = []
        for detail in details:
            if options.get(detail) and options[detail]["value"]:
                entry = options[detail]
                prefix = icon and entry.get("icon") or entry.get("label")
                if prefix:
                    res.append("%s %s" % (prefix, entry["value"]))
                else:
                    res.append("%s" % entry["value"])
        res = "\n".join(res)
        return res
