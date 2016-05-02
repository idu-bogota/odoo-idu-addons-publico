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
from openerp.exceptions import ValidationError


class hr_department(models.Model):
    _inherit = 'hr.department'

    # -------------------
    # Fields
    # -------------------
    proyecto_gerente_id = fields.Many2one(
        string='Coordinador de Proyectos',
        required=False,
        track_visibility='onchange',
        comodel_name='res.users',
        ondelete='restrict',
        help='''Tiene permisos de administración de los proyectos, EDT y tareas para la dependencia''',
    )
    proyecto_programador_id = fields.Many2one(
        string='Programador de Proyectos',
        required=False,
        track_visibility='onchange',
        comodel_name='res.users',
        ondelete='restrict',
    )

    # -------------------
    # methods
    # -------------------
