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
import sys
import logging

logging.basicConfig()
_logger = logging.getLogger('create_user')


# -------------------
# methods
# -------------------

def find_area(odoo, name_area, name_user):
    area = odoo.env['hr.department'].sudo().search([
        ('abreviatura','=',name_area.strip())
    ])
    if area is None:
        _logger.warning("El área: '" + name_area + "' no se encuentra definida en la BD. Usuario: " + name_user)
        return None
    else:
        return area.id

def requires_name_update(odoo, name):
    numero_espacios = name.find(" ")
    if numero_espacios >= 2:
        return False
    else:
        return True

def update_user_searching(odoo, nombres, apellidos, partner_id, search_login=None, search_id_user=None):
    if not search_login and not search_id_use:
        _logger.warning("Debe ingresar algunos de estos dos parametros: search_login, search_id_user")

    grups_employee = odoo.env['res.groups'].sudo().search([
        ('name','=','Employee')
    ])

    if search_login:
        usuario_obj = odoo.env['res.users']
        usuario = usuario_obj.sudo().search([('login','=',search_login)])
    elif search_id_use:
        usuario_obj = odoo.env['res.users']
        usuario = usuario_obj.sudo().search([('id','=',search_id_user)])

    if usuario:
        usuario.sudo().write(
        {
            'name': '{} {}'.format(nombres, apellidos),
            'nombres': nombres,
            'apellidos': apellidos,
            'tz': 'America/Bogota',
            'partner_id': partner_id,
            'groups_id': [(4,grups_employee.id)],
        })

def update_user(odoo, nombres, apellidos, partner_id, object_user):
    groups_employe = odoo.env.ref('base.group_user')

    new_user = object_user.sudo().write(
        {
            'name': '{} {}'.format(nombres, apellidos),
            'nombres': nombres,
            'apellidos': apellidos,
            'tz': 'America/Bogota',
            'partner_id': partner_id,
            'groups_id': [(4, groups_employe.id)],
        })

def create_user(odoo, nombres, apellidos, partner_id, login):
    usuario_obj = odoo.env['res.users']
    groups_employe = odoo.env.ref('base.group_user')
    new_user = usuario_obj.sudo().create(
    {
        'name': '{} {}'.format(nombres, apellidos),
        'nombres': nombres,
        'apellidos': apellidos,
        'login': login,
        'groups_id': [(4,groups_employe.id)],
        'lang': 'es_CO',
        'tz': 'America/Bogota',
        'partner_id': partner_id,
    })
    return new_user

def update_partner(odoo, nombres, apellidos, email, usuario_id, object_partner):
    object_partner.sudo().write({
        'email': email,
        'tipo_persona': 'nat',
        'nombres': nombres,
        'apellidos': apellidos,
        'user_id': usuario_id,
    })

def create_employee(odoo, nombres, apellidos, usuario_id, email, partner_id, area_id):
    empleado_obj = odoo.env['hr.employee']
    partner = empleado_obj.sudo().create({
        'name': '{} {}'.format(nombres, apellidos),
        'user_id': usuario_id,
        'department_id': area_id,
        'work_email': email,
        'address_id': partner_id,
    })
    return partner

def update_employee(odoo, nombres, apellidos, email, area_id, partner_id, object_employee):
    object_employee.sudo().write({
        'name': '{} {}'.format(nombres, apellidos),
        'department_id': area_id,
        'work_email': email,
        'address_id': partner_id,
    })
