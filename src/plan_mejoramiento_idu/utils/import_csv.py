#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

class Import():
    def __init__(self, odoo, _logger):
        self.odoo = odoo
        self._logger = _logger

    def find_area(self, name_area):
        area = self.odoo.model('hr.department').get([('abreviatura','=',name_area.strip())])
        if area is None:
            raise Exception("El Area: '" + name_area + "' no se encuentar definida en la BD")
        return area.id

    def find_user_existing(self, auditor, email=None):
        user = self.odoo.model('res.users').get([('login','=',auditor.strip())])
        if user:
            return True
        else:
            if email:
                user = self.odoo.model('res.users').get([('email','=',email.strip())])
            if user:
                return True
            return False

    def get_user(self, auditor, email=None):
        user = self.odoo.model('res.users').get([('login','=',auditor.strip())])
        if user:
            return user.id
        else:
            if email:
                user = self.odoo.model('res.users').get([('email','=',email.strip())])
            if user:
                return user.id

    def create_user(self, auditor, name_user, email_user, area_user, rol_user):
        # buscar area
        area = self.find_area(area_user)
        # buscar grupo
        if rol_user == '1': # se define 1 en el archivo plan
            grups_oci = self.odoo.model('res.groups').get([('name','=','Auditor OCI')])
        elif rol_user == '2':
            grups_oci = self.odoo.model('res.groups').get([('name','=','Responsable Tareas')])
        # crear usuario
        new_user = self.odoo.model('res.users').create({
            'name': name_user,
            'login': auditor,
            'groups_id': [(4,grups_oci.id)],
            'lang': 'es_CO',
            'tz': 'America/Bogota',
        })
        # actualizar partner_id para correo
        partner = self.odoo.model('res.partner').get([('id','=',new_user.partner_id.id)])
        partner.write({
            'email': email_user,
        })
        # crear empleado
        new_employee = self.odoo.model('hr.employee').create({'name':name_user.strip(), 'user_id': new_user.id, 'department_id': area})
        return new_user.id

    def add_rol_to_user(self, rol_user, auditor):
        # definir grupo
        if rol_user == '1': # se define 1 en el archivo plan
            groups = self.odoo.model('res.groups').get([('name','=','Auditor OCI')])
        elif rol_user == '2':
            groups = self.odoo.model('res.groups').get([('name','=','Responsable Tareas')])
        # buscar usuario
        user = self.odoo.model('res.users').get([('login','=',auditor.strip())])
        # si no tiene el rol lo agrega
        if not groups.id in user.groups_id.id:
            user.write({
                'groups_id': [(4,groups.id)],
            })
