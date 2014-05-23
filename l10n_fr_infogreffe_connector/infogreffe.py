# -*- coding: utf-8 -*-
##############################################################################
#
#    L10n FR infogreffe connector module for OpenERP
#    Copyright (C) 2014 Akretion (http://www.akretion.com/)
#    Copyright (C) 2014 Kiplink (http://www.kiplink.fr/)
#    @author: Alexis de Lattre <alexis.delattre@akretion.com>
#    @author: Alexandre Fournier <alexandre.fournier@kiplink.fr>
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
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

URL = 'https://www.infogreffe.fr'


class res_partner(orm.Model):
    _inherit = 'res.partner'

    _columns = {
        'infogreffe_date': fields.date('Date', readonly=True),
        'infogreffe_turnover': fields.integer(u'Turnover (€)', readonly=True),
        'infogreffe_profit': fields.integer(u'Profit (€)', readonly=True),
        'infogreffe_headcount': fields.integer('Headcount', readonly=True),
    }

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default.update({
            'infogreffe_date': False,
            'infogreffe_turnover': False,
            'infogreffe_profit': False,
            'infogreffe_headcount': False,
            })
        return super(res_partner, self).copy(
            cr, uid, id, default=default, context=context)

    def get_json_company_from_siren(self, cr, uid, siren, context=None):
        params = {
            'sirenOuSiret':   siren,
            'etabSecondaire': 'false',
            'etsRadiees':     'false',
            'typeEntreprise': 'TOUS'
            }

        url = URL + '/services/entreprise/rest/recherche/parEntreprise'
        resp = requests.get(url=url, params=params)
        data = resp.json()
        return data

    def get_soup_extrait_from_siren(self, cr, uid, siren, context=None):
        data = self.get_json_company_from_siren(
            cr, uid, siren, context=context)
        data = data['entrepRCSStoreResponse']['items'][0]
        name = data['libelleEntreprise']['denomination'].lower()
        url = URL + '/societes/entreprise-societe/%s-%s-%s.html' % (
            data['siren'], name, data['etablissementChrono'])
        resp = requests.get(url=url)
        soup = BeautifulSoup(resp.text)
        return soup

    def convert_to_integer(self, cr, uid, raw_value, context=None):
        if not raw_value:
            return False
        val1 = raw_value.strip()
        #print "val1=", val1
        # Remove short spaces
        val2 = val1.replace(u'\xA0', '')
        #print "val2=", val2
        val3 = val2.replace('K', '000')
        #print "val3=", val3
        # Remove euro symbol
        val4 = val3.replace(u'\u20ac', '')
        #print "val4=", val4
        val5 = val4.replace(' ', '')
        #print "val5=", val5
        return int(val5)

    def button_get_from_infogreffe(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'Only 1 ID'
        partner = self.browse(cr, uid, ids[0], context=context)
        if not partner.siren:
            raise orm.except_orm(
                _('Error:'),
                _("Missing SIREN on partner '%s'. It is needed to download "
                    "data from Infogreffe") % partner.name)

        logger.info("Connecting to infogreffe with SIREN %s" % partner.siren)
        soup = self.get_soup_extrait_from_siren(
            cr, uid, partner.siren, context=context)
        trs = soup.find(id='chiffresCles').find('tbody').find_all('tr')
        vals = {
            'infogreffe_date': False,
            'infogreffe_turnover': False,
            'infogreffe_profit': False,
            'infogreffe_headcount': False,
            }

        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) != 4:
                continue
            try:
                date = datetime.strptime(tds[0].text.strip(), '%d/%m/%Y')
                raw_turnover = tds[1].text
                turnover = self.convert_to_integer(
                    cr, uid, raw_turnover, context=context)
                raw_profit = tds[2].text
                profit = self.convert_to_integer(
                    cr, uid, raw_profit, context=context)
                headcount_raw = tds[3].text.strip()
                headcount = self.convert_to_integer(
                    cr, uid, headcount_raw, context=context)
            except:
                logger.warning('Cannot parse infogreffe results')
                continue
            if not vals['infogreffe_date'] or vals['infogreffe_date'] < date:
                vals = {
                    'infogreffe_date': date,
                    'infogreffe_turnover': turnover,
                    'infogreffe_profit': profit,
                    'infogreffe_headcount': headcount,
                    }
                logger.debug('Infogreffe result line = %s' % vals)

        self.write(cr, uid, ids[0], vals, context=context)
        logger.debug(
            u'Partner %s updated with Infogreffe data %s'
            % (partner.name, vals))
        return True
