# Copyright 2016-2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero
from stdnum.ean import is_valid, calc_check_digit
import base64
import re
import socket
import ipaddress

import logging
logger = logging.getLogger(__name__)
TIMEOUT = 5
PRINTER_PORT = 9100


class ProductPrintZplBarcode(models.TransientModel):
    _name = 'product.print.zpl.barcode'
    _description = 'Generate and print product barcodes in ZPL'
    _check_company_auto = True

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
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
                "There are no pricelist in company '%s'.") % company.name)

        printer_ip = self.env['ir.config_parameter'].sudo().get_param(
            'product_print_zpl_barcode.printer_ip')

        line_ids = []
        if self._context.get('active_model') == 'product.product':
            product_ids = self._context.get('active_ids')
            products = self.env['product.product'].browse(product_ids)
            if not products:
                raise UserError(_('Missing Products'))
            for product in products:
                self._update_line_ids(line_ids, product)
        elif self._context.get('active_model') == 'product.template':
            product_tmpl_ids = self._context.get('active_ids')
            product_tmpls = self.env['product.template'].browse(product_tmpl_ids)
            for product_tmpl in product_tmpls:
                for product in product_tmpl.product_variant_ids:
                    self._update_line_ids(line_ids, product)
        elif self._context.get('active_model') == 'stock.picking':
            prec = self.env['decimal.precision'].precision_get(
                'Product Unit of Measure')
            picking = self.env['stock.picking'].browse(self._context['active_id'])
            for ml in picking.move_line_ids:
                if (
                        ml.product_id and
                        ml.product_id.must_print_barcode and
                        float_compare(ml.qty_done, 0, precision_digits=prec) > 0):
                    self._update_line_ids(
                        line_ids, ml.product_id, int(round(ml.qty_done)))
        else:
            raise UserError(_(
                "Wrong active_model in context (%s).")
                % self._context.get('active_model'))
        res.update({
            'company_id': company.id,
            'nomenclature_id': nomenclature.id,
            'pricelist_id': pricelist.id,
            'zpl_printer_ip': printer_ip,
            'line_ids': line_ids,
        })
        return res

    @api.model
    def _update_line_ids(self, line_ids, product, copies=1):
        if product.barcode:
            line_ids.append((0, 0, {
                'barcode': product.barcode,
                'product_name': product.name,
                'product_id': product.id,
                'copies': copies,
                }))
        else:
            logger.warning("Product '%s' doesn't have a barcode", product.display_name)

    company_id = fields.Many2one(  # default value set by default_get
        'res.company', required=True, ondelete='cascade')
    nomenclature_id = fields.Many2one(
        'barcode.nomenclature', 'Barcode Nomenclature', required=True,
        states={'step2': [('readonly', True)]})
    # label_size: remove readonly=True when we will support more labels
    label_size = fields.Selection([
        ('38x25', '38x25 mm'),
        ], required=True, default='38x25', readonly=True)
    pricelist_id = fields.Many2one(
        'product.pricelist', string='Pricelist', required=True,
        states={'step2': [('readonly', True)]}, check_company=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]"
        )
    state = fields.Selection([
        ('step1', 'Step1'),
        ('step2', 'Step2'),
        ], default='step1', readonly=True)
    zpl_file = fields.Binary(string='ZPL File', readonly=True)
    zpl_filename = fields.Char('ZPL Filename')
    zpl_printer_ip = fields.Char(string='ZPL Printer IP Address')
    line_ids = fields.One2many(
        'product.print.zpl.barcode.line', 'parent_id',
        string='Lines', states={'step2': [('readonly', True)]})

    def generate(self):
        """Called by button for the wizard, 1st step"""
        self.ensure_one()
        zpl_strings = []
        for line in self.line_ids:
            barcode = line.barcode
            product_name = line.product_name
            assert barcode
            barcode_len = len(barcode)
            if barcode_len not in (8, 13):
                raise UserError(_(
                    "Line '%s': barcode '%s' has %d digits. "
                    "This wizard only supports EAN8 and EAN13 for the moment.")
                    % (product_name, barcode, barcode_len))
            if not is_valid(barcode):
                raise UserError(_(
                    "Line '%s': the barcode '%s' is not a valid EAN barcode "
                    "(wrong checksum).") % (product_name, barcode))
            if line.copies <= 0:
                raise UserError(_(
                    "On line '%s', the number of copies must be strictly positive."
                    ) % product_name)
            if line.barcode_type in ('price', 'weight'):
                barcode, zpl_str = line._prepare_price_weight_barcode_type()
            elif line.barcode_type == 'product':
                barcode, zpl_str = line._prepare_product_barcode_type()
            else:
                raise UserError(_(
                    "Line '%s': barcode type '%s' is not supported for the moment")
                    % (product_name, line.barcode_type))
            line.write({'barcode': barcode})
            zpl_strings.append(zpl_str)

        zpl_filename = "barcodes.zpl"
        if len(self.line_ids) == 1:
            zpl_filename = "barcode_%s.zpl" % self.line_ids[0].barcode

        zpl_str = '\n'.join(zpl_strings)
        zpl_bytes = zpl_str.encode('utf-8')
        vals = {
            'zpl_file': base64.encodebytes(zpl_bytes),
            'state': 'step2',
            'zpl_filename': zpl_filename,
            }
        self.write(vals)
        action = self.env["ir.actions.actions"]._for_xml_id(
            'product_print_zpl_barcode.product_print_zpl_barcode_action')
        action.update({
            'res_id': self.id,
            'context': self._context,
            'views': False})
        return action

    def print_zpl(self):
        if not self.zpl_printer_ip:
            raise UserError(_(
                "You must configure the IP address of the ZPL Printer."))
        try:
            ip = ipaddress.ip_address(self.zpl_printer_ip)
        except Exception as e:
            raise UserError(str(e))
        version = ip.version
        # TODO works with DNS ?
        if version == 6:  # IPv6
            socket_inet = socket.AF_INET6
        else:  # IPv4
            socket_inet = socket.AF_INET
        with socket.socket(socket_inet, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            try:
                s.connect((str(ip), PRINTER_PORT))
            except Exception as e:
                raise UserError(_(
                    "Cannot connect to ZPL printer on %(ip)s. Error: %(error)s",
                    ip=ip, error=e))
            zpl_file_bytes = base64.decodebytes(self.zpl_file)
            s.send(zpl_file_bytes)
            s.close()


class ProductPrintZplBarcodeLine(models.TransientModel):
    _name = 'product.print.zpl.barcode.line'
    _description = 'Line of the print ZPL barcode wizard'

    parent_id = fields.Many2one(
        'product.print.zpl.barcode', ondelete='cascade')
    product_id = fields.Many2one(
        'product.product', string='Product', readonly=True)
    uom_id = fields.Many2one(related='product_id.uom_id', string='UoM')
    # 1 line = a bit less than 30
    # I don't make product_name a stored computed field because I'm afraid
    # that we may not take the lang of the user
    product_name = fields.Char('Product Label', required=True, size=56)
    rule_id = fields.Many2one(
        'barcode.rule', string='Barcode Rule', compute='_compute_rule_id')
    barcode_type = fields.Selection(related='rule_id.type', string="Barcode Type")
    currency_id = fields.Many2one(related='parent_id.pricelist_id.currency_id')
    # TODO: for the moment, we only support weight, but...
    quantity = fields.Float(digits='Stock Weight', string='Qty')
    price_uom = fields.Monetary(
        string="Price/UoM", compute='_compute_price')  # given by pricelist
    price = fields.Monetary(compute='_compute_price')
    barcode = fields.Char(readonly=True)
    copies = fields.Integer(string='# Labels', default=1, required=True)

    @api.depends('parent_id.pricelist_id', 'quantity', 'product_id')
    def _compute_price(self):
        # for regular barcodes
        for line in self:
            pricelist = line.parent_id.pricelist_id
            price_uom = price = 0.0
            if pricelist and line.product_id:
                price_uom = pricelist._get_product_price(line.product_id, 1, False)
                price = price_uom * line.quantity
            line.price_uom = price_uom
            line.price = price

    @api.depends('parent_id.nomenclature_id')
    def _compute_rule_id(self):
        for line in self:
            nomenclature = line.parent_id.nomenclature_id
            match_rule = False
            if nomenclature and line.barcode:
                for rule in nomenclature.rule_ids:
                    match = nomenclature.match_pattern(
                        line.barcode, rule.pattern)
                    if match.get('match'):
                        match_rule = rule.id
                        break
            line.rule_id = match_rule

    def _prepare_price_weight_barcode_type(self):
        dpo = self.env['decimal.precision']
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
        # print("barcode=", barcode)
        # print("pattern=", pattern)
        m = re.search(r'\{N+D+\}', pattern)
        # print("m=", m)
        assert m
        pattern_val = m.group(0)
        pattern_val = pattern_val[1:-1]
        # print("pattern_val=", pattern_val)
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
        # print("barcode=", barcode)
        # Add checksum
        if self.rule_id.encoding == 'ean13':
            # I don't call bno.sanitize_ean() due to this bug:
            # https://github.com/odoo/odoo/pull/114112
            barcode = barcode + calc_check_digit(barcode)
            assert len(barcode) == 13
            assert is_valid(barcode)
            # print("barcode FINAL=", barcode)
        zpl_str = self._price_weight_barcode_type_zpl() % {
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
        return (barcode, zpl_str)

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
        zpl_str = self._product_barcode_type_zpl() % {
            'product_name': self.product_name,
            'ean_zpl_command': len(self.barcode) == 8 and 'B8' or 'BE',
            'ean_no_checksum': self.barcode[:-1],
            'price_uom': self.price_uom,
            'currency_symbol': self.currency_id.symbol,  # symbol is a required field
            'copies': self.copies,
        }
        return (self.barcode, zpl_str)
