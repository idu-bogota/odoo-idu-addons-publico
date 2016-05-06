# -*- coding: utf-8 -*-
##############################################################################
#
#    Grupo de Investigación, Desarrollo e Innovación I+D+I
#    Subdirección de Recursos Tecnológicos - STRT
#    INSTITUTO DE DESARROLLO URBANO - BOGOTA (COLOMBIA)
#    Copyright (C) 2015 IDU STRT I+D+I (http://www.idu.gov.co/)
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

from openerp import models, fields, api

class actualizar_responsables_dependencias(models.TransientModel):
    _name = 'base_idu.wizard.actualizar_responsables_dependencias'
    _description = 'Wizard para actualizar los permisos a los responsables de las dependencias'

    @api.multi
    def procesar(self):
        self.ensure_one()
        grp_jefe_dependencia = self.env.ref('base_idu.group_jefe_dependencia')
        # Asignar permisos jefe de dependencia a todos los hr.department->manager_id
        user_ids = self.env['hr.department'].search([]).mapped('manager_id.user_id.id')
        if user_ids:
            grp_jefe_dependencia.write({
                'users': [(6, 0, user_ids)]
            })
        return {'type': 'ir.actions.act_window_close'}
