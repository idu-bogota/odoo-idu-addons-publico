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
from openerp.exceptions import Warning
from ..models.project import calcular_fecha_fin, calcular_fecha_inicio, calcular_duracion_en_dias
import logging
_logger = logging.getLogger(__name__)

class project_edt_wizard_reprogramar_tarea(models.TransientModel):
    _name = 'project.edt.wizard.reprogramar_tarea'
    _description = 'Wizard para reprogramar tarea'

    def _default_fecha_inicio(self):
        if self.env.context.get('task_id'):
            task = self.env['project.task'].browse(self.env.context.get('task_id'))
            return task.fecha_inicio

    def _default_fecha_fin(self):
        if self.env.context.get('task_id'):
            task = self.env['project.task'].browse(self.env.context.get('task_id'))
            return task.fecha_inicio

    def _default_duracion_dias(self):
        if self.env.context.get('task_id'):
            task = self.env['project.task'].browse(self.env.context.get('task_id'))
            return task.duracion_dias

    # -------------------
    # Fields
    # -------------------
    task_id = fields.Many2one(
        string='Tarea',
        required=True,
        readonly=True,
        comodel_name='project.task',
        ondelete='restrict',
        default=lambda self: self._context.get('task_id', None),
    )
    tipo_agendamiento = fields.Selection(
        string='Estado',
        required=True,
        selection=[
            ('fecha_inicio', 'Calcular fecha inicial'),
            ('fecha_fin', 'Calcular fecha final'),
            ('duracion_dias', 'Calcular duración en días laborales'),
        ],
        default='fecha_fin',
    )
    fecha_inicio = fields.Date(
        string='Fecha Inicio',
        required=True,
        readonly=False,
        default=_default_fecha_inicio,
    )
    fecha_fin = fields.Date(
        string='Fecha Fin',
        required=True,
        readonly=False,
        default=_default_fecha_fin,
    )
    duracion_dias = fields.Integer(
        string='Duración en Días',
        required=True,
        readonly=False,
        default=_default_duracion_dias,
    )

    @api.multi
    def reprogramar(self):
        self.ensure_one()
        fecha_inicio, fecha_fin, duracion_dias = self._calcular_datos(self.tipo_agendamiento, self.fecha_inicio, self.fecha_fin, self.duracion_dias)
        self.task_id.write({
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'duracion_dias_manual': duracion_dias,
        })
        self.task_id.reprogramar_tarea_button()
        return {'type': 'ir.actions.act_window_close'}

    @api.onchange('fecha_inicio', 'fecha_fin','duracion_dias')
    def _onchange_data(self):
        self.fecha_inicio, self.fecha_fin, self.duracion_dias = self._calcular_datos(self.tipo_agendamiento, self.fecha_inicio, self.fecha_fin, self.duracion_dias)

    def _calcular_datos(self, tipo_agendamiento, fecha_inicio, fecha_fin, duracion_dias):
        if self.tipo_agendamiento == 'fecha_inicio':
            fecha_inicio = calcular_fecha_inicio(fecha_fin, duracion_dias)
            fecha_inicio = fields.Date.to_string(fecha_inicio)
        elif self.tipo_agendamiento == 'fecha_fin':
            fecha_fin = calcular_fecha_fin(fecha_inicio, duracion_dias)
            fecha_fin = fields.Date.to_string(fecha_fin)
        elif self.tipo_agendamiento == 'duracion':
            duracion_dias = calcular_duracion_en_dias(fecha_inicio, fecha_fin)
        return fecha_inicio, fecha_fin, duracion_dias
