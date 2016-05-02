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

class project_portafolio_crear_proyecto_funcionamiento(models.TransientModel):
    _name = 'project.portafolio.wizard.crear_proyecto_funcionamiento'
    _inherit = 'project.edt.wizard.importar_mpp'
    _description = 'Wizard para crear proyectos de funcionamiento'

    # -------------------
    # Fields
    # -------------------
    name = fields.Char(
        string='Nombre del Proyecto',
        required=True,
    )
    project_id = fields.Many2one(
        required=False,
    )
    user_id = fields.Many2one(
        required=True,
    )
    programador_id = fields.Many2one(
        required=True,
    )

    @api.multi
    def crear_proyecto(self):
        project_model = self.env['project.project']
        for form in self:
            vals = {
                'name': form.name,
                'user_id': form.user_id.id,
                'programador_id': form.programador_id.id,
                'dependencia_id': self.env.user.department_id.id,
                'proyecto_tipo': 'funcionamiento',
            }
            project = project_model.sudo().create(vals)
            form.project_id = project.id
            form.importar_mpp()

        return {'type': 'ir.actions.act_window_close'}
