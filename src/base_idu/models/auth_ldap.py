# -*- coding: utf-8 -*-
##############################################################################
#
#    Grupo I+D+I
#    Subdirección Técnica de Recursos Tecnológicos
#    Instituto de Desarrollo Urbano - IDU - Bogotá - Colombia
#    Copyright (C) IDU (<http://www.idu.gov.co>)
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

from openerp import models, fields, api, exceptions
from openerp.exceptions import Warning, AccessError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import sys
import logging

logging.basicConfig()
_logger = logging.getLogger('CompanyLDAP')

class CompanyLDAP(models.Model):
    _name = "res.company.ldap"
    _inherit = ['res.company.ldap',]

    # -------------------
    # Fields
    # -------------------

    # -------------------
    # methods
    # -------------------

    @api.model
    def get_or_create_user(self, conf, login, ldap_entry):
        nombre_completo_usuario = ldap_entry[1]['displayName'][0]
        nombre_area = ldap_entry[1]['department'][0]
        nombres = ldap_entry[1]['givenName'][0]
        apellidos = ldap_entry[1]['sn'][0]
        email = ldap_entry[1]['mail'][0]
        numero_cc = ldap_entry[1]['ipPhone'][0]
        grups_employee = self.env['res.groups'].search([
            ('name','=','Employee')
        ])

        res = super(CompanyLDAP, self).get_or_create_user(conf, login, ldap_entry)

        # Get Usuario
        user = self.env['res.users'].search([
            ('id','=',res)
        ])
        # Actualizar Usuario
        user.write({
            'name': nombre_completo_usuario,
            'groups_id': [(4,grups_employee.id)],
        })
        # Actualizar Partner
        partner = self.env['res.partner'].search([('id','=',user.partner_id.id)])
        partner.write({
            'email': email,
            'tipo_persona': 'nat',
            'nombres': nombres,
            'apellidos': apellidos,
        })
        try:
            if numero_cc:
                partner.write({
                    'identificacion_tipo': 'CC',
                    'identificacion_numero': numero_cc,
                })
        except Exception as e:
            try:
                if numero_cc:
                    partner.write({
                        'identificacion_tipo': 'CC',
                        'identificacion_numero': numero_cc+'-0',
                    })
            except Exception as e:
                _logger.warning('No se pudo asignar el numero de documento a {0}[{1}]: {2}'.format(email, partner.id, e))
        # Buscar Empleado
        empleado = self.env['hr.employee'].search([('work_email','=',email)])
        if not empleado:
            # Crear Empleado
            new_employee = self.env['hr.employee'].create({
                'name': nombre_completo_usuario,
                'user_id': user.id,
                'department_id': self.find_area(nombre_area, nombre_completo_usuario),
                'address_home_id': user.partner_id.id,
                'work_email': email,
                'identification_id': numero_cc,
            })
        return res

    @api.model
    def find_area(self, name_area, name_user):
        area = self.env['hr.department'].search([
            ('abreviatura','=',name_area.strip())
        ])
        if area is None:
            _logger.warning("EL Area: " + name_area + " No se encuentar definida en la BD. Usuario: " + name_user)
            return None
        else:
            return area.id