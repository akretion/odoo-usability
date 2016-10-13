# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>


from openerp.osv import orm, fields
from openerp.tools.translate import _


class ProductTemplate(orm.Model):
    _inherit = 'product.template'

    _columns = {
        'intrastat_type': fields.selection([
            ('product', 'Product'),
            ('service', 'Service'),
            ], string='Intrastat Type', required=True,
            help="Type of product used for the intrastat declarations. "
            "For example, you can configure a product with "
            "'Product Type' = 'Consumable' and 'Intrastat Type' = 'Service'.")
        }

    _defaults = {
        'intrastat_type': 'product',
    }

    def _check_intrastat_product(self, cr, uid, ids):
        for pt in self.browse(cr, uid, ids):
            if pt.intrastat_type == 'product' and pt.type == 'service':
                raise orm.except_orm(
                    _("Error"),
                    _("On the product '%s', you cannot set Product Type to "
                      "'Service' and Intrastat Type to 'Product'.") % pt.name)
            if pt.intrastat_type == 'service' and pt.type == 'product':
                raise orm.except_orm(
                    _("Error"),
                    _("On the product '%s', you cannot set Intrastat Type to "
                      "'Service' and Product Type to 'Stockable product' "
                      "(but you can set Product Type to 'Consumable' or "
                      "'Service').") % pt.name)
        return True

    _constraints = [(
        _check_intrastat_product,
        'error msg in raise',
        ['type', 'intrastat_type'],
    )]


class ReportIntrastatCommon(orm.Model):
    _inherit = "report.intrastat.common"

    def _is_service(self, cr, uid, invoice_line, context=None):
        if invoice_line.product_id.intrastat_type == 'service':
            return True
        else:
            return False
