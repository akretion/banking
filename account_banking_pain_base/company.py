# -*- encoding: utf-8 -*-
##############################################################################
#
#    PAIN Base module for OpenERP
#    Copyright (C) 2013 Akretion (http://www.akretion.com)
#    Copyright (C) 2013 Noviat (http://www.noviat.com)
#    @author: Alexis de Lattre <alexis.delattre@akretion.com>
#    @author: Luc de Meyer (Noviat)
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


class res_company(orm.Model):
    _inherit = 'res.company'

    _columns = {
        'initiating_party_issuer': fields.char(
            'Initiating Party Issuer', size=35,
            help="This will be used as the 'Initiating Party Issuer' in the "
            "PAIN files generated by OpenERP."),
    }

    def _get_initiating_party_identifier(
            self, cr, uid, company_id, context=None):
        '''The code here may be different from one country to another.
        If you need to add support for an additionnal country, you can
        contribute your code here or inherit this function in the
        localization modules for your country'''
        assert isinstance(company_id, int), 'Only one company ID'
        company = self.browse(cr, uid, company_id, context=context)
        company_vat = company.vat
        party_identifier = False
        if company_vat:
            country_code = company_vat[0:2].upper()
            if country_code == 'BE':
                party_identifier = company_vat[2:].replace(' ', '')
            elif country_code == 'ES':
               party_identifier = company.sepa_creditor_identifier
        return party_identifier

    def _initiating_party_issuer_default(self, cr, uid, context=None):
        '''If you need to add support for an additionnal country, you can
        add an entry in the dict "party_issuer_per_country" here
        or inherit this function in the localization modules for
        your country'''
        initiating_party_issuer = ''
        # If your country require the 'Initiating Party Issuer', you should
        # contribute the entry for your country in the dict below
        party_issuer_per_country = {
            'BE': 'KBO-BCE',  # KBO-BCE = the registry of companies in Belgium
        }
        company_id = self._company_default_get(
            cr, uid, 'res.company', context=context)
        if company_id:
            company = self.browse(cr, uid, company_id, context=context)
            country_code = company.country_id.code
            initiating_party_issuer = party_issuer_per_country.get(
                country_code, '')
        return initiating_party_issuer

    def _initiating_party_issuer_def(self, cr, uid, context=None):
        return self._initiating_party_issuer_default(
            cr, uid, context=context)

    _defaults = {
        'initiating_party_issuer': _initiating_party_issuer_def,
    }
