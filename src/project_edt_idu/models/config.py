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


class config_settings(models.TransientModel):
    _name = 'project.edt.config'
    _inherit = 'res.config.settings'

    jython_path = fields.Char(
        string="Comando Jython a ejecutar",
        help="Incluir parametros si son necesarios",
    )
    mpp2csv_path = fields.Char(
        string="Ruta del script mpp2csv",
    )

    def set_jython_path(self, cr, uid, ids, context):
        url_ids = self.pool.get('ir.config_parameter').search(cr, uid,
            [('key','=','project.edt.jython_path')],
            context=context,
        )
        for form in self.browse(cr, uid, ids, context=context):
            if not form.jython_path:
                continue

            if len(url_ids):
                self.pool.get('ir.config_parameter').write(cr, uid, url_ids, {
                    'value': form.jython_path,
                })
            else:
                self.pool.get('ir.config_parameter').create(cr, uid, {
                    'key': 'project.edt.jython_path',
                    'value': form.jython_path,
                })

    def get_default_jython_path(self, cr, uid, fields, context):
        value = self.pool.get('ir.config_parameter').get_param(cr, uid, 'project.edt.jython_path', default='', context=context)
        return {'jython_path': value}

    def set_mpp2csv_path(self, cr, uid, ids, context):
        url_ids = self.pool.get('ir.config_parameter').search(cr, uid,
            [('key','=','project.edt.mpp2csv_path')],
            context=context,
        )
        for form in self.browse(cr, uid, ids, context=context):
            if not form.mpp2csv_path:
                continue

            if len(url_ids):
                self.pool.get('ir.config_parameter').write(cr, uid, url_ids, {
                    'value': form.mpp2csv_path,
                })
            else:
                self.pool.get('ir.config_parameter').create(cr, uid, {
                    'key': 'project.edt.mpp2csv_path',
                    'value': form.mpp2csv_path,
                })

    def get_default_mpp2csv_path(self, cr, uid, fields, context):
        value = self.pool.get('ir.config_parameter').get_param(cr, uid, 'project.edt.mpp2csv_path', default='', context=context)
        return {'mpp2csv_path': value}
