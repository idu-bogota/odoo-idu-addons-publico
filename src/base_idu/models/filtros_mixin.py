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

def adiciona_keywords_en_search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False, xtra=None):
    """Permite adicionar keyworkds en las busquedas que se hagan a través del search,
    sirve para hacer más dinámicos los filtros en la vista tree. Ejemplo

    Extender el modelo:
    from openerp.addons.base_idu.models.filtros_mixin import adiciona_keywords_en_search

    class project_project(models.Model):
        _name = 'project.project'
        _inherit = ['project.project']

        def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False, xtra=None):
            new_args = adiciona_keywords_en_search(self, cr, uid, args, offset, limit, order, context, count, xtra)
            return super(project_project, self).search(cr, uid, new_args, offset, limit, order, context, count)

    Adicionar en la vista:

    <record model="ir.actions.act_window" id="dependencia_admin_project_action">
        <field name="name">Proyectos Dependencia</field>
        <field name="res_model">project.project</field>
        <field name="view_mode">tree,kanban,form</field>
        <field name="domain">[('dependencia_id', '=', 'USER_DEPARTMENT_ID')]</field>
    </record>

    """
    user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
    new_args = []
    for arg in args:
        if type(arg) is not tuple and type(arg) is not list:
            new_args += arg
            continue
        if arg[2] == 'USER_DEPARTMENT_ID':
            new_args += [(arg[0], arg[1], user.department_id.id)]
        elif arg[2] == 'USER_CHILD_DEPARTMENT_IDS':
            department_ids = self.pool.get('hr.department').search(cr, uid, [('id', 'child_of', user.department_id.id)], context=context)
            new_args += [(arg[0], arg[1], department_ids)]
        else:
            new_args += [arg]
    return new_args
