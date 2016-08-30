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
from openerp import models, fields, api, exceptions
from openerp.exceptions import Warning


class actualizar_responsable_tareas(models.TransientModel):
    _name = 'project_edt.wizard.actualizar_responsable_tareas'

    user_id = fields.Many2one(
        string='Asignar como responsable a:',
        required=True,
        comodel_name='res.users',
        ondelete='restrict',
    )

    @api.multi
    def actualizar(self):
        tareas = self.env['project.task'].browse(self.env.context.get('active_ids'))
        tareas.write({'user_id': self.user_id.id})

