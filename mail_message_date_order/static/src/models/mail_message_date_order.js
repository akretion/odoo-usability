odoo.define("mail_message_date_order/static/src/models/mail_message_date_order.js", function(require) {
  "use strict";

  function factory(dependencies) {
    class ThreadCache extends dependencies['mail.model'] {

      /**
       * @override
       */
      _computeOrderedMessages() {
          const res = super._computeOrderedMessages(...arguments);
          console.log("---IN OVERRIDE ORDERED MESSAGES cache");
          // return [['replace', this.messages.sort((m1, m2) => m1.date._d < m2.date._d ? -1 : 1)]];
          return res;
      }



    }
  }

});
