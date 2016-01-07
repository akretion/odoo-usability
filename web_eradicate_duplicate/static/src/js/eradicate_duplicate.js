/* Web Eradicate Duplicate
   @author: Alexis de Lattre <alexis.delattre@akretion.com>
   Inspired by the module web_hide_duplicate of Aristobulo Meneses
*/

openerp.web_eradicate_duplicate = function (instance) {
    var _t = instance.web._t;

    instance.web.FormView.include({
        load_form: function(data) {
            this._super(data);
            // Remove More > Duplicate button for all users except admin
            if (this.session.uid != 1 && this.sidebar && this.sidebar.items && this.sidebar.items.other) {
                var new_items_other = _.reject(this.sidebar.items.other, function (item) {
                    return item.label === _t('Duplicate');
                });
                this.sidebar.items.other = new_items_other;
            }
        }
    });
};
