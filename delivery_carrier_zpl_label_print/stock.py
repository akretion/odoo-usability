# -*- coding: utf-8 -*-
##############################################################################
#
#    Delivery Carrier ZPL Label Print module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm, fields
from openerp.tools.translate import _
import logging
import base64

logger = logging.getLogger(__name__)


class ResUsers(orm.Model):
    _inherit = 'res.users'

    _columns = {
        'label_printer_id': fields.many2one('printing.printer',
                                            'Default Label Printer'),
        }



class StockPicking(orm.Model):
    _inherit = 'stock.picking'

    def _compute_delivery_labels(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for picking in self.browse(cr, uid, ids, context=context):
            label_ids = self.pool['shipping.label'].search(
                cr, uid, [('res_id', '=', picking.id)], context=context)
            print "label_ids=", label_ids
            if label_ids:
                res[picking.id] = True
            else:
                res[picking.id] = False
        print "res=", res
        return res

    _columns = {
        'has_delivery_labels': fields.function(
            _compute_delivery_labels, type='boolean',
            string='Has Delivery Labels', readonly=True),
    }


class StockPickingOut(orm.Model):
    _inherit = 'stock.picking.out'

    def _compute_delivery_labels(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for picking in self.browse(cr, uid, ids, context=context):
            label_ids = self.pool['shipping.label'].search(
                cr, uid, [('res_id', '=', picking.id)], context=context)
            print "label_ids=", label_ids
            if label_ids:
                res[picking.id] = True
            else:
                res[picking.id] = False
        print "res=", res
        return res

    _columns = {
        'has_delivery_labels': fields.function(
            _compute_delivery_labels, type='boolean',
            string='Has Delivery Labels', readonly=True),
    }

    def print_zpl_label_picking_list(
            self, cr, uid, picking_list, context=None):
        zpl_files = []  # list of tuple (filename, file)
        # GET ZPL files
        user = self.pool['res.users'].browse(cr, uid, uid, context=context)
        if not user.label_printer_id:
            raise orm.except_orm(
                _('Erreur:'),
                _('No Default Label Printer configured for the user %s')
                % user.name)
        printer_id = user.label_printer_id.id
        for picking in picking_list:
            if picking.state != 'done':
                raise orm.except_orm(
                    _('Error:'),
                    _("The delivery order %s hasn't been validated.")
                    % picking.name)
            label_ids = self.pool['shipping.label'].search(
                cr, uid, [('res_id', '=', picking.id)], context=context)
            logger.info('%d labels found for picking %s',
                        len(label_ids), picking.name)
            if not label_ids:
                raise orm.except_orm(
                    _('Error:'),
                    _("No ZPL file attached to the Delivery order %s."
                      "You should click on the button "
                      "'Create Shipping Label' of the Delivery order.")
                    % picking.name)
            labels = self.pool['shipping.label'].browse(
                cr, uid, label_ids, context=context)
            for label in labels:
                zpl_files.append(
                    (label.name, base64.decodestring(label.datas)))
        # NOW PRINT !
        logger.info('Starting to print %d ZPL files' % len(zpl_files))
        for zpl_fname, zpl_file in zpl_files:
            logger.info('Starting to send ZPL file %s' % zpl_fname)
            self.pool['printing.printer'].print_document(
                cr, uid, [printer_id], zpl_fname,
                zpl_file, 'raw', context=context)
            # 4e arg = nom de report bidon... ça ne sert pas a priori
            logger.info('ZPL file %s sent' % zpl_fname)
        logger.info('Printing of ZPL files finished')
        return True

    def print_zpl_delivery_label(self, cr, uid, ids, context=None):
        assert len(ids) == 1, "only 1 id"
        picking = self.browse(cr, uid, ids[0], context=context)
        return self.print_zpl_label_picking_list(
            cr, uid, [picking], context=context)


