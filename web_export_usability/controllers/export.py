# coding: utf-8
# © 2017 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import http
from openerp.addons.web.controllers.main import Export
import logging

_logger = logging.getLogger(__name__)


class Export_(Export):

    @http.route('/web/export/formats', type='json', auth="user")
    def formats(self):
        """ Returns all valid export formats

        :returns: for each export format, a pair of identifier
            and printable name
        :rtype: [(str, str)]
        """
        response = super(Export_, self).formats()
        # put xls, before csv
        response.reverse()
        return response
