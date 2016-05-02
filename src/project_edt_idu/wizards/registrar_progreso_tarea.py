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
from ..models.project import PROJECT_TASK_REPORTE_AVANCE_NIVEL_ALERTA

class project_edt_wizard_registrar_progreso_tarea(models.TransientModel):
    _name = 'project.edt.wizard.registrar_progreso_tarea'
    _description = 'Wizard para registrar progreso de tarea'

    def _default_progreso(self):
        if self.env.context.get('task_id'):
            task = self.env['project.task'].browse(self.env.context.get('task_id'))
            return task.progreso

    def _default_costo(self):
        if self.env.context.get('task_id'):
            task = self.env['project.task'].browse(self.env.context.get('task_id'))
            return task.costo

    def _default_cantidad(self):
        if self.env.context.get('task_id'):
            task = self.env['project.task'].browse(self.env.context.get('task_id'))
            return task.cantidad

    # -------------------
    # Fields
    # -------------------
    name = fields.Char(
        string='Resumen',
        required=True,
        track_visibility='onchange',
        size=255,
    )
    fecha = fields.Date(
        string='Fecha',
        required=True,
        readonly=True,
        default=fields.Date.today,
    )
    task_id = fields.Many2one(
        string='Tarea',
        required=True,
        readonly=True,
        comodel_name='project.task',
        ondelete='restrict',
        default=lambda self: self._context.get('task_id', None),
    )
    project_id = fields.Many2one(
        string='Proyecto',
        readonly=True,
        related='task_id.project_id',
    )
    project_reportar_costo = fields.Boolean(
        string='En Reporte de Avance incluir Costo de la Tarea',
        related='task_id.project_id.reportar_costo',
        readonly=True,
        default=False,
    )
    project_reportar_cantidad = fields.Boolean(
        string='En Reporte de Avance incluir Cantidades',
        related='task_id.project_id.reportar_cantidad',
        readonly=True,
        default=False,
    )
    porcentaje = fields.Integer(
        string='Porcentaje',
        required=True,
        default=_default_progreso,
    )
    cantidad = fields.Float(
        string='Cantidad',
        required=False,
        default=_default_cantidad,
    )
    uom_id = fields.Many2one(
        string='Unidad',
        comodel_name='product.uom',
        related='task_id.product_id.uom_id',
        readonly=True,
    )
    company_id = fields.Many2one(
        string='Compañía',
        required=True,
        comodel_name='res.company',
        ondelete='restrict',
        default=lambda self: self.env.user.company_id,
    )
    currency_id = fields.Many2one(
        string='Moneda',
        required=False,
        readonly=True,
        related='company_id.currency_id',
        comodel_name='res.currency',
        ondelete='restrict',
    )
    costo = fields.Monetary(
        string='Costo',
        required=False,
        default=_default_costo,
    )
    nivel_alerta = fields.Selection(
        string='Nivel de Alerta',
        required=False,
        selection=PROJECT_TASK_REPORTE_AVANCE_NIVEL_ALERTA,
        default='ninguno',
    )
    novedad = fields.Text(
        string='Novedad',
        required=False,
    )

    @api.multi
    def registrar_progreso(self):
        self.ensure_one()
        progreso_model = self.env['project.task.registro_progreso']
        fields = ['fecha', 'name', 'porcentaje', 'costo', 'nivel_alerta', 'novedad']
        vals = {
            'task_id': self.task_id.id,
        }
        for field in fields:
            value = getattr(self, field)
            if value:
                vals[field] = value

        progreso_model.create(vals)
        return {'type': 'ir.actions.act_window_close'}
