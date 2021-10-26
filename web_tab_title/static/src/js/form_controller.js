/* global vis, py */
odoo.define("web_tab_title.FormController", function (require) {
    "use strict";

    var FormController = require('web.FormController');

    var TabTitleController = FormController.include({

        on_attach_callback: function () {
            this._super.apply(this, arguments);

            if (document.title == "Odoo") {
              var form_name_elem = $("div.oe_title>h1");
              if (form_name_elem.length == 0) {
                form_name_elem = $('span.o_field_char[name="name"]')
              }
              var title = form_name_elem.text();
              if (title !== '') {
                // alternatively we could access the record
                // in views/basic/basic_model.js
                // but we would also we miss the model name
                document.title = title + " - Odoo";
              }
            }

        },

    });

    return TabTitleController;
});
