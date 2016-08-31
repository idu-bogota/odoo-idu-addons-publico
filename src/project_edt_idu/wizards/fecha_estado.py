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
from openerp.tools import config as odoo_config
from openerp.exceptions import Warning, ValidationError
from openerp import SUPERUSER_ID

class project_edt_wizard_fecha_estado(models.TransientModel):
    _name = 'project.edt.wizard.fecha_estado'
    _description = 'Wizard para registrar fecha de estado'

    project_id = fields.Many2one(
        string='Proyecto',
        required=True,
        readonly=True,
        comodel_name='project.project',
        ondelete='restrict',
        default=lambda self: self._context.get('project_id', None),
    )
    fecha_estado = fields.Date(
        string='Fecha de Estado',
        help="Indica la fecha sobre la cual se va a calcular el retraso",
        readonly=False,
        required=True,
        default=fields.Date.context_today,
    )

    @api.one
    @api.constrains('fecha_estado')
    def check_fecha_estado(self):
        if odoo_config['test_enable']:
            return True
        hoy = fields.Date.context_today(self)
        if self.fecha_estado and self.fecha_estado < hoy:
            raise ValidationError('La fecha de estado debe ser mayor o igual a la fecha de hoy')
        return True

    @api.multi
    def actualizar_fecha_estado(self):
        self.ensure_one()
        if not self.project_id.usuario_actual_actua_como_gerente() and self.env.user.id != SUPERUSER_ID:
            raise Warning('No tiene permisos para ejecutar esta acción')

        if self.project_id.edt_raiz_id:
            # Quita la fecha de estado para dejar los valores nulos
            edt_model = self.env['project.edt']
            task_model = self.env['project.task']
            edts = edt_model.search([('id', 'child_of', self.project_id.edt_raiz_id.id)])
            tasks = task_model.search([('edt_id', 'in', edts.ids)])
            tasks.write({
                'fecha_estado': False,
            })
            edts.write({
                'fecha_estado': False,
            })
            # Asigna recursivamente de hojas a raiz la fecha de estado para que los cálculos
            # se hagan de manera correcta, ya que los valores dependen de valores calculados
            # en los elementos hijos
            for obj in edt_model._recorrer_arbol_postorder(self.project_id.edt_raiz_id, []):
                obj.write({
                    'fecha_estado': self.fecha_estado,
                })

        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def actualizar_fecha_estado_open_projects(self):
        project_model = self.env['project.project']
        wizard_model = self.env['project.edt.wizard.fecha_estado']
        for p in project_model.search([('state','=','open')]):
            try:
                wizard_model.with_context(tracking_disable=True).create({'project_id': p.id}).actualizar_fecha_estado()
            except Exception:
                pass
        return True
