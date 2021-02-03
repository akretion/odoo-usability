# Copyright 2016-2020 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero
from stdnum.ean import is_valid
import base64
import re


class ProductPrintZplBarcode(models.TransientModel):
    _name = 'product.print.zpl.barcode'
    _description = 'Generate and print product barcodes in ZPL'

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        assert self._context.get('active_model') == 'product.product',\
            'wrong active_model, should be product.product'
        product_id = self._context.get('active_id')
        product = self.env['product.product'].browse(product_id)
        if not product:
            raise UserError(_('Missing Product'))
        if not product.barcode:
            raise UserError(_(
                "Product '%s' doesn't have a barcode") % product.display_name)
        nomenclature = self.env.ref('barcodes.default_barcode_nomenclature')
        company = self.env.company
        posconfig = self.env['pos.config'].sudo().search(
            [('company_id', '=', company.id)], limit=1)
        if posconfig:
            pricelist = posconfig.pricelist_id
        else:
            pricelist = self.env['product.pricelist'].search([
                '|', ('company_id', '=', False),
                ('company_id', '=', company.id),
                ], limit=1)
        if not pricelist:
            raise UserError(_(
                "There are no pricelist in company %s ?") % company.name)

        printer = self.env['printing.printer'].get_default()
        res.update({
            'nomenclature_id': nomenclature.id,
            'pricelist_id': pricelist.id,
            'currency_id': pricelist.currency_id.id,
            'barcode': product.barcode,
            'product_name': product.name,
            'product_id': product_id,
            'zpl_printer_id': printer and printer.id or False,
        })
        return res

    product_id = fields.Many2one(
        'product.product', string='Product', required=True, readonly=True)
    uom_id = fields.Many2one(
        related='product_id.uom_id', readonly=True)
    # 1 line = un peu moins de 30
    product_name = fields.Char('Product Label', required=True, size=56)
    nomenclature_id = fields.Many2one(
        'barcode.nomenclature', 'Barcode Nomenclature', required=True)
    rule_id = fields.Many2one(
        'barcode.rule', string='Barcode Rule', readonly=True,
        compute='_compute_rule_id')
    barcode_type = fields.Selection(
        related='rule_id.type', readonly=True, string="Barcode Type")
    label_size = fields.Selection([
        ('38x25', '38x25 mm'),
        ], required=True, default='38x25', string='Label Size')
    pricelist_id = fields.Many2one(
        'product.pricelist', string='Pricelist', required=True)
    currency_id = fields.Many2one(
        related='pricelist_id.currency_id', readonly=True)
    # TODO: for the moment, we only support weight, but...
    quantity = fields.Float(digits='Stock Weight')
    price_uom = fields.Monetary(
        readonly=True, string="Price per Unit of Measure",
        compute='_compute_price')  # given by pricelist
    price = fields.Monetary(compute='_compute_price', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    state = fields.Selection([
        ('step1', 'Step1'),
        ('step2', 'Step2'),
        ], default='step1', readonly=True)
    zpl_file = fields.Binary(string='ZPL File', readonly=True)
    zpl_filename = fields.Char('ZPL Filename')
    barcode = fields.Char(readonly=True)
    copies = fields.Integer(
        string='Number of Labels', default=1, required=True)
    zpl_printer_id = fields.Many2one(
        'printing.printer', string='ZPL Printer')

    @api.depends('pricelist_id', 'quantity', 'product_id')
    def _compute_price(self):
        # for regular barcodes
        for wiz in self:
            if wiz.pricelist_id and wiz.product_id:
                price_uom = wiz.pricelist_id.get_product_price(
                    wiz.product_id, 1, False)
                wiz.price_uom = price_uom
                wiz.price = price_uom * wiz.quantity

    @api.depends('nomenclature_id')
    def _compute_rule_id(self):
        for wiz in self:
            match_rule = False
            if wiz.nomenclature_id and wiz.barcode:
                for rule in wiz.nomenclature_id.rule_ids:
                    match = wiz.nomenclature_id.match_pattern(
                        wiz.barcode, rule.pattern)
                    if match.get('match'):
                        match_rule = rule.id
                        break
            wiz.rule_id = match_rule

    def _prepare_price_weight_barcode_type(self):
        dpo = self.env['decimal.precision']
        bno = self.env['barcode.nomenclature']
        prec = dpo.precision_get('Stock Weight')
        value = self.quantity
        pbarcode = self.barcode
        if float_is_zero(value, precision_digits=prec):
            raise UserError(_(
                "The quantity (%s) must be positive !") % value)
        # check prefix
        pattern = self.rule_id.pattern
        if '{' not in pattern:
            raise UserError(_(
                "The barcode rule '%s' has a pattern '%s' which doesn't "
                "contain a integer and decimal part between '{}'.")
                % (self.rule_id.name, pattern))
        prefix = pattern.split('{')[0]
        assert len(prefix) >= 1
        if len(prefix) > len(pbarcode):
            raise UserError(_(
                "The barcode of the product (%s) has %d characters, "
                "which is smaller than the %d characters of the prefix "
                "of the barcode pattern (%s).")
                % (pbarcode, len(pbarcode), len(prefix), prefix))
        barcode = pbarcode[0:len(prefix)]
        # print "barcode=", barcode
        # print "pattern=", pattern
        m = re.search('\{N+D+\}', pattern)
        # print "m=", m
        assert m
        pattern_val = m.group(0)
        pattern_val = pattern_val[1:-1]
        # print "pattern_val=", pattern_val
        max_value = 10**pattern_val.count('N')
        if float_compare(value, max_value, precision_digits=prec) != -1:
            raise UserError(_(
                "The value to encode in the barcode (%s) is superior "
                "to the maximum value allowed by the barcode pattern (%s).")
                % (value, max_value))
        value_str = str(value)
        value_str_split = value_str.split('.')
        assert len(value_str_split) == 2
        value_n = value_str_split[0]
        value_d = value_str_split[1]
        assert len(value_n) <= pattern_val.count('N')
        barcode += value_n.zfill(pattern_val.count('N'))
        # end fill doesn't exists... so:
        # 1) make sure we have enough 0 after
        value_d_ext = value_d + '0' * pattern_val.count('D')
        # 2) cut at the right size
        barcode += value_d_ext[0:pattern_val.count('D')]
        # print "barcode=", barcode
        # Add checksum
        if self.rule_id.encoding == 'ean13':
            barcode = bno.sanitize_ean(barcode)
            # print "barcode FINAL=", barcode
        zpl_unicode = self._price_weight_barcode_type_zpl() % {
            'product_name': self.product_name,
            'ean_zpl_command': len(self.barcode) == 8 and 'B8' or 'BE',
            'ean_no_checksum': barcode[:-1],
            'price_uom': self.price_uom,
            'price': self.price,
            'currency_symbol': self.currency_id.symbol,
            'copies': self.copies,
            'quantity': value,
            'uom_name': self.uom_id.name,
        }
        zpl_bytes = zpl_unicode.encode('utf-8')
        vals = {
            'zpl_file': base64.encodebytes(zpl_bytes),
            'barcode': barcode,
            }
        return vals

    @api.model
    def _price_weight_barcode_type_zpl(self):
        label = """
^XA
^CI28
^PW304
^LL200
^LH0,20
^CF0,30
^FO15,0^FB270,1,0,C^FD%(price).2f %(currency_symbol)s^FS
^CF0,20
^FO15,30^FB270,3,0,C^FD%(product_name)s^FS
^CF0,25
^FO15,75^FB270,1,0,C^FD%(quantity).3f %(uom_name)s    %(price_uom).2f %(currency_symbol)s/%(uom_name)s^FS
^FO60,110^%(ean_zpl_command)sN,50^FD%(ean_no_checksum)s^FS
^PQ%(copies)s
^XZ
"""
        return label

    @api.model
    def _product_barcode_type_zpl(self):
        label = """
^XA
^CI28
^PW304
^LL200
^LH0,20
^CF0,30
^FO15,0^FB270,1,0,C^FD%(price_uom).2f %(currency_symbol)s^FS
^CF0,20
^FO15,30^FB270,3,0,C^FD%(product_name)s^FS
^FO60,100^%(ean_zpl_command)sN,60^FD%(ean_no_checksum)s^FS
^PQ%(copies)s
^XZ
"""
        return label

    def _prepare_product_barcode_type(self):
        zpl_unicode = self._product_barcode_type_zpl() % {
            'product_name': self.product_name,
            'ean_zpl_command': len(self.barcode) == 8 and 'B8' or 'BE',
            'ean_no_checksum': self.barcode[:-1],
            'price_uom': self.price_uom,
            'currency_symbol': self.currency_id.symbol,  # symbol is a required field
            'copies': self.copies,
        }
        zpl_bytes = zpl_unicode.encode('utf-8')
        vals = {
            'zpl_file': base64.encodebytes(zpl_bytes),
            'barcode': self.barcode,  # unchanged
            }
        return vals

    def generate(self):
        assert self.barcode
        if len(self.barcode) not in (8, 13):
            raise UserError(_(
                "This wizard only supports EAN8 and EAN13 for the moment. "
                "Barcode '%s' has %d digits.") % (
                self.barcode,
                len(self.barcode)))
        if not is_valid(self.barcode):
            raise UserError(_(
                "The barcode '%s' is not a valid EAN barcode "
                "(wrong checksum).") % self.barcode)
        if not self.copies:
            raise UserError(_("The number of copies cannot be 0"))
        if self.barcode_type in ('price', 'weight'):
            vals = self._prepare_price_weight_barcode_type()
        elif self.barcode_type == 'product':
            vals = self._prepare_product_barcode_type()
        else:
            raise UserError(_(
                "Barcode Type %s is not supported for the moment")
                % self.barcode_type)
        vals.update({
            'state': 'step2',
            'zpl_filename': 'barcode_%s.zpl' % vals['barcode'],
            })
        self.write(vals)
        action = self.env.ref('product_print_zpl_barcode.product_print_zpl_barcode_action').sudo().read()[0]
        action.update({
            'res_id': self.id,
            'context': self._context,
            'views': False})
        return action

    def print_zpl(self):
        if not self.zpl_printer_id:
            raise UserError(_(
                "You must select a ZPL Printer."))
        self.zpl_printer_id.print_document(
            self.zpl_filename, base64.decodebytes(self.zpl_file), format='raw')
        action = True
        if self._context.get('print_and_new'):
            action = self.env.ref('product_print_zpl_barcode.product_print_zpl_barcode_action').sudo().read()[0]
            action.update({
                'views': False,
                'context': self._context,
                })
        return action
