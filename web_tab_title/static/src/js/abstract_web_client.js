/* global vis, py */
odoo.define("web_tab_title.AbstractWebClient", function (require) {
    "use strict";

    var AbstractWebClient = require('web.AbstractWebClient');

    var TabTitleAbstractWebClient = AbstractWebClient.include({

        _title_changed: function () {
            // like the original except we change the title
            // only when it's different from "Odoo" to avoid
            // resetting the tab title when switching tabs.
            var parts = _.sortBy(_.keys(this.get("title_part")), function (x) { return x; });
            var tmp = "";
            _.each(parts, function (part) {
                var str = this.get("title_part")[part];
                if (str) {
                    tmp = tmp ? tmp + " - " + str : str;
                }
            }, this);
            if (tmp != "Odoo") {
                document.title = tmp;
            }
        },

    });

    return TabTitleAbstractWebClient;
});
