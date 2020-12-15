# -*- coding: utf-8 -*-
# Copyright 2019 Barroux Abbey
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestPartnerPhone(TransactionCase):

    def setUp(self):
        super(TestPartnerPhone, self).setUp()

    def _check_result(self, partner, result):
        rppo = self.env['res.partner.phone']
        pphone_email = rppo.search(
            [('type', '=', '1_email_primary'), ('partner_id', '=', partner.id)])
        if result['email']:
            self.assertEqual(partner.email, result['email'])
            self.assertEqual(len(pphone_email), 1)
            self.assertEqual(pphone_email.email, result['email'])
        else:
            self.assertFalse(partner.email)
            self.assertFalse(pphone_email)
        if result['phone']:
            self.assertEqual(partner.phone, result['phone'])
        else:
            self.assertFalse(partner.phone)
        if result['mobile']:
            self.assertEqual(partner.mobile, result['mobile'])
        else:
            self.assertFalse(partner.mobile)
        field2type = {
            'phone': '3_phone_primary',
            'mobile': '5_mobile_primary',
            'fax': '7_fax_primary',
            }
        for field, value in result.items():
            if field in field2type:
                type = field2type[field]
                pphone = rppo.search(
                    [('type', '=', type), ('partner_id', '=', partner.id)])
                if value:
                    self.assertEqual(len(pphone), 1)
                    self.assertEqual(pphone.phone, value)
                else:
                    self.assertFalse(pphone)

    def test_create_partner(self):
        rpo = self.env['res.partner']
        p = rpo.create({
            'name': 'Test Me',
            'email': 'testme@example.com',
            'phone': '+33198089246',
            'mobile': '+33198089247',
            })
        result = {
            'email': 'testme@example.com',
            'phone': '+33198089246',
            'mobile': '+33198089247',
            }
        self._check_result(p, result)
        p2 = rpo.create({
            'name': 'Test me now',
            'email': 'testmenow@example.com',
            'phone': '+33972727272',
            })
        result = {
            'email': 'testmenow@example.com',
            'phone': '+33972727272',
            'mobile': False,
            }
        self._check_result(p2, result)
        p3 = rpo.create({
            'name': 'Test me now',
            'phone_ids': [
                (0, 0, {'type': '3_phone_primary', 'phone': '+33972727272'}),
                (0, 0, {'type': '1_email_primary', 'email': 'tutu@example.fr'})],
            })
        result = {
            'email': 'tutu@example.fr',
            'phone': '+33972727272',
            'mobile': False,
            }
        self._check_result(p3, result)

    def test_write_partner(self):
        p1 = self.env['res.partner'].create({
            'name': 'test me now',
            'country_id': self.env.ref('base.fr').id,
            })
        result_none = {
            'email': False,
            'phone': False,
            'mobile': False,
            }
        self._check_result(p1, result_none)
        p1.write({
            'mobile': '+33198089247',
            'email': 'testmenow@example.com',
            })
        result = {
            'email': 'testmenow@example.com',
            'phone': False,
            'mobile': '+33198089247',
            }
        self._check_result(p1, result)
        p1.write({
            'email': 'testmenow2@example.com',
            'phone': False,
            'mobile': '+33472727272',
            })
        result = {
            'email': 'testmenow2@example.com',
            'phone': False,
            'mobile': '+33472727272',
            }
        self._check_result(p1, result)
        p1.write({
            'phone': False,
            'mobile': False,
            'email': False,
            })
        self._check_result(p1, result_none)
        p2 = self.env['res.partner'].create({'name': 'Toto', 'email': 'toto@example.com'})
        p_multi = p1 + p2
        p_multi.write({'email': 'all@example.com', 'phone': '+33560606070'})
        result = {
            'email': 'all@example.com',
            'phone': '+33560606070',
            'mobile': False,
            }
        self._check_result(p1, result)
        self._check_result(p2, result)
