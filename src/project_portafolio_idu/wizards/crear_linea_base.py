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

class project_portafolio_crear_linea_base(models.TransientModel):
    _name = 'project.portafolio.wizard.crear_linea_base'
    _description = 'Wizard para crear linea base de un proyecto'

    # -------------------
    # Fields
    # -------------------
    name = fields.Char(
        string='Nombre para la línea base',
        required=True,
        default=fields.Date.context_today,
    )
    project_id = fields.Many2one(
        string='Proyecto',
        required=True,
        readonly=True,
        comodel_name='project.project',
        ondelete='restrict',
        default=lambda self: self._context.get('project_id', False),
    )

    @api.multi
    def crear_linea_base(self):
        edt_model = self.env['project.edt']
        task_model = self.env['project.task']
        for form in self:
            if not form.project_id.usuario_actual_actua_como_gerente():
                raise Warning('No tiene permisos para ejecutar esta acción')

            edt_error_cnt = edt_model.search_count([
                ('project_id','=',form.project_id.id),
                '|',
                    ('fecha_planeada_inicio','=',False),
                    ('fecha_planeada_fin','=',False),
            ])
            task_error_cnt = task_model.search_count([
                ('project_id','=',form.project_id.id),
                '|',
                    ('fecha_planeada_inicio','=',False),
                    ('fecha_planeada_fin','=',False),
            ])
            if task_error_cnt or edt_error_cnt:
                raise Warning(
                    'No se puede crear una línea base ya que hay {} sin fechas planeadas asignadas'.format(
                        (edt_error_cnt and '{} EDT'.format(edt_error_cnt)) or
                        (task_error_cnt and  '{} Tarea(s)'.format(task_error_cnt))
                    )
                )
            form.project_id.crear_linea_base(form.name)

        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def crear_snapshot(self):
        for form in self:
            if not form.project_id.usuario_actual_actua_como_gerente():
                raise Warning('No tiene permisos para ejecutar esta acción')

            form.project_id.crear_snapshot(form.name)

        return {'type': 'ir.actions.act_window_close'}
