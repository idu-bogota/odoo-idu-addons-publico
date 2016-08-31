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
import openerp.tools as tools
import os
import base64
import csv
import json
from datetime import datetime, date
import pytz
import logging
import subprocess
import zipfile
from subprocess import CalledProcessError

_logger = logging.getLogger(__name__)

class project_edt_wizard_importar_mpp(models.TransientModel):
    _name = 'project.edt.wizard.importar_mpp'
    _description = 'Wizard para importar archivos .mpp'

    # -------------------
    # Fields
    # -------------------
    project_id = fields.Many2one(
        string='Proyecto',
        required=True,
        track_visibility='onchange',
        comodel_name='project.project',
        ondelete='restrict',
        default=lambda self: self._context.get('project_id', False),
    )
    metodo = fields.Selection(
        string='¿Como importar las hojas?',
        required=True,
        selection=[
            ('hojas_son_tareas', 'Como tareas'),
            ('hojas_son_paquetes_trabajo', 'Como paquetes de trabajo'),
        ],
        default='hojas_son_tareas',
    )
    asignar_recursos_mpp = fields.Boolean(
        string='Asignar recursos del archivo .mpp?',
        required=False,
        default=True,
        help="Los recursos asignados en el .mpp deben ser asignados utilizando los usuarios del sistema?"
    )
    user_id = fields.Many2one(
        string='Asignar como responsable a:',
        required=False,
        comodel_name='res.users',
        ondelete='restrict',
        help="Se toma solo si en el archivo .mpp no se asignó ninguno"
    )
    programador_id = fields.Many2one(
        string='Asignar como programador a:',
        required=False,
        comodel_name='res.users',
        ondelete='restrict',
        help="Se toma solo si en el archivo .mpp no se asignó ninguno"
    )
    revisor_id = fields.Many2one(
        string='Asignar como revisor de tareas a:',
        required=False,
        comodel_name='res.users',
        ondelete='restrict',
        help="Se toma solo si en el archivo .mpp no se asignó ninguno"
    )
    archivo = fields.Binary(
        required=True,
    )
    archivo_nombre = fields.Char()

    # -------------------
    # methods
    # -------------------
    def _settings(self):
        jython = self.env['ir.config_parameter'].get_param('project.edt.jython_path', default=False)
        mpp2csv_path = self.env['ir.config_parameter'].get_param('project.edt.mpp2csv_path', default=False)
        if not jython or not mpp2csv_path:
            raise Warning('Deben configurarse los parametros jython_path y mpp2csv_path')
        temp_folder = tools.config.filestore(self.env.cr.dbname) + '/project_edt_importar_mpp/'
        try:
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)
        except OSError, e:
            _logger.error('No se pudo crear el directorio: {0}'.format(temp_folder))
            _logger.exception(e)
            raise Warning('No existe el directorio temporal para importar el archivo. Por favor contacte al administrador del sistema.')
        return jython, mpp2csv_path, temp_folder

    def _get_default_stage_id(self, project_id):
        stages = self.env['project.task.type'].search([
            ('project_ids', '=', project_id),
            ('fold', '=', False),
        ])
        if stages:
            return stages[0].id
        return None

    @api.multi
    def importar_mpp(self):
        edt_model = self.env['project.edt']
        task_model = self.env['project.task']
        jython, mpp2csv_path, temp_folder = self._settings()

        for form in self:
            if form.archivo_nombre.lower().endswith('.csv'): # Si es CSV importar directamente
                archivo_csv = '{0}{1}-{2}-{3}'.format(temp_folder, fields.datetime.now(), form.id, form.archivo_nombre) # Se supone que es un archivo válido generado por el comando mpp2csv
                archivo = base64.decodestring(form.archivo)
                binario = open(archivo_csv, 'wb')
                binario.write(archivo)
                binario.close()
                _logger.info('Importando directamente archivo CSV: {0}'.format(archivo_csv))
            else:
                archivo_csv = self.mpp2csv(form, jython, mpp2csv_path, temp_folder)
                _logger.info('Creado archivo {0}'.format(archivo_csv))
            with open(archivo_csv, 'rb') as f:
                recursos = self.get_recursos_asignados(form, csv.DictReader(f))
                f.seek(0)
                datos_edt = self.get_datos_edts(form, csv.DictReader(f), recursos)
                f.seek(0)
                datos_tareas = self.get_datos_tareas(form, csv.DictReader(f), recursos)
                f.seek(0)
                indice_objetos = {}

                ctx = {'carga_masiva': True, 'mail_notrack': True, 'mail_create_nosubscribe': True, 'tracking_disable': True}
                for vals in datos_edt:
                    vals['project_id'] = form.project_id.id
                    if form.user_id and not vals.get('user_id', False):
                        vals['user_id'] = form.user_id.id
                    if form.programador_id and not vals.get('programador_id', False):
                        vals['programador_id'] = form.programador_id.id
                    edt = edt_model.with_context(ctx).create(vals)
                    indice_objetos[vals['ms_project_guid']] = ('e', edt.id, edt)
                    if not form.project_id.edt_raiz_id:
                        form.project_id.edt_raiz_id = edt.id
                _logger.info('{} líneas de EDT creadas'.format(len(indice_objetos)))
                params = {
                    'cnt': 0,
                    'company_id': self.env.user.company_id.id,
                    'stage_id': self._get_default_stage_id(form.project_id.id),
                    'nombre_progreso': unicode('Avance cargado masivamente el {0}'.format(date.today().strftime('%d, %b %Y')),'utf-8'),
                    'fecha_corte': fields.Date.today(),
                }
                for vals in datos_tareas:
                    vals['project_id'] = form.project_id.id
                    if form.user_id and not vals.get('user_id', False):
                        vals['user_id'] = form.user_id.id
                    if form.revisor_id and not vals.get('revisor_id', False):
                        vals['revisor_id'] = form.revisor_id.id
                    if vals.get('raw_edt_id'):
                        vals['edt_id'] = indice_objetos.get(vals['raw_edt_id'])[1]
                        del vals['raw_edt_id']
                    # task = task_model.with_context(ctx).create(vals)
                    params['cnt'] += 1
                    task_id = self.insert_task(vals, form, params)
                    indice_objetos[vals['ms_project_guid']] = ('t', task_id)
                _logger.info('{} Tareas creadas'.format(params['cnt']))
                f.seek(0)
                self.asociar_edts(form, csv.DictReader(f), datos_edt, indice_objetos)
                f.seek(0)
                self.crear_dependencias(form, csv.DictReader(f), indice_objetos)

        return {'type': 'ir.actions.act_window_close'}

    def insert_task(self, vals, form, params):
        """Creado para insertar en BD y mejorar velocidad de carga en archivos grandes"""

        sql_task = """INSERT INTO "project_task"(
            "id", "sequence", "date_last_stage_update",
            "progreso_aprobado", "partner_id", "user_id",
            "progreso", "fecha_planeada_fin", "date_start",
            "company_id", "priority", "fecha_inicio",
            "edt_id", "project_id", "date_assign",
            "kanban_state", "numero", "costo_planeado",
            "fecha_planeada_inicio", "active", "name",
            "stage_id", "progreso_metodo", "ms_project_guid",
            "fecha_fin", "costo", "date_end",
            "revisor_id", "create_uid", "write_uid",
            "create_date", "write_date",
            "duracion_dias","duracion_dias_manual","duracion_planeada_dias"
        )
        VALUES(
            nextval('project_task_id_seq'), %s, (now() at time zone 'UTC'), --"id", "sequence", "date_last_stage_update",
            %s, NULL, %s, -- "progreso_aprobado", "partner_id", "user_id",
            %s, %s, %s, -- "progreso", "fecha_planeada_fin", "date_start",
            %s, '0', %s, -- "company_id", "priority", "fecha_inicio",
            %s, %s, (now() at time zone 'UTC'), -- "edt_id", "project_id", "date_assign",
            'normal', %s, %s, -- "kanban_state", "numero", "costo_planeado",
            %s, true, %s, -- "fecha_planeada_inicio", "active", "name",
            %s, 'manual', %s, -- "stage_id", "progreso_metodo", "ms_project_guid",
            %s, %s, %s, -- "fecha_fin", "costo", "date_end",
            %s, %s, %s, -- "revisor_id", "create_uid", "write_uid",
            (now() at time zone 'UTC'), (now() at time zone 'UTC'), -- "create_date", "write_date"
            %s, %s, %s -- "duracion_dias", "duracion_dias_manual", "duracion_planeada_dias"
        ) RETURNING id"""
        self.env.cr.execute(sql_task, (
            params['cnt'],
            0.0, vals.get('user_id'),
            vals.get('progreso', 0), vals.get('fecha_planeada_fin'), vals.get('date_start'),
            params['company_id'], vals.get('fecha_inicio'),
            vals.get('edt_id'), form.project_id.id,
            vals.get('numero'), vals.get('costo_planeado', 0),
            vals.get('fecha_planeada_inicio'), vals.get('name')[:127],
            params['stage_id'], vals.get('ms_project_guid'),
            vals.get('fecha_fin'), vals.get('costo', 0), vals.get('date_end'),
            vals.get('revisor_id'), self.env.uid, self.env.uid,
            vals.get('duracion_dias'), vals.get('duracion_dias'), vals.get('duracion_dias'),
        ))
        task_id = self.env.cr.fetchone()[0]

        if vals.get('cantidad') or vals.get('costo') or vals.get('progreso'):
            sql_progreso = """INSERT INTO "project_task_registro_progreso"(
                "id", "nivel_alerta", "task_id",
                "name", "cantidad", "fecha",
                "company_id", "costo", "porcentaje",
                "active", "create_uid", "write_uid",
                "create_date", "write_date"
            )
            VALUES(
                nextval('project_task_registro_progreso_id_seq'), 'ninguno', %s, -- "id", "nivel_alerta", "task_id",
                %s, %s, %s, -- "name", "cantidad", "fecha",
                %s, %s, %s, -- "company_id", "costo", "porcentaje",
                true, %s, %s, -- "active", "create_uid", "write_uid",
                (now() at time zone 'UTC'), (now() at time zone 'UTC') -- "create_date", "write_date"
            ) RETURNING id"""

            self.env.cr.execute(sql_progreso, (
                task_id,
                params['nombre_progreso'], vals.get('cantidad',0), params['fecha_corte'],
                params['company_id'], vals.get('costo', 0), vals.get('progreso', 0),
                self.env.uid, self.env.uid,
            ))

        return task_id


    def mpp2csv(self, form, jython, mpp2csv_path, temp_folder):
        archivo_nombre = '{0}{1}-{2}-{3}'.format(temp_folder, fields.datetime.now(), form.id, form.archivo_nombre)
        archivo_nombre = archivo_nombre.replace(' ', '_')
        archivo_mpp = archivo_nombre + '.mpp'
        archivo_csv = archivo_nombre + '.csv'
        archivo = base64.decodestring(form.archivo)
        binario = open(archivo_mpp, 'wb')
        binario.write(archivo)
        binario.close()
        if zipfile.is_zipfile(archivo_mpp):
            _logger.info('ZIP file found')
            zf = zipfile.ZipFile(archivo_mpp)
            filenames = zf.namelist()
            if len(filenames) > 1:
                raise Warning('El archivo ZIP debe contener solo un archivo correspondiente al .mpp a importar')

            for filename in filenames:
                zf.extract(filename, temp_folder)
                archivo_mpp = '{}/{}'.format(temp_folder, filename)
                _logger.info('ZIP file descromprimido a importar {}'.format(archivo_mpp))

        try:
            command = [
                jython,
                '-Dpython.path={0}/mpxj.jar:{0}/poi-3.11-20141221.jar:{0}/rtfparserkit-1.1.0.jar'.format(mpp2csv_path + 'javalib'),
                mpp2csv_path + 'main.py',
                '-f', archivo_mpp,
                '-o', archivo_csv,
            ]
            _logger.info("command to run '{}' ".format(' '.join(command)))
            subprocess.check_output(
                command,
                stderr=subprocess.STDOUT,
                cwd='/tmp/'
            )
        except CalledProcessError, e:
            _logger.error("command '{}' return with error (code {}): {}".format(' '.join(e.cmd), e.returncode, e.output))
            _logger.exception(e)
            raise Warning('Ocurrio un problema al convertir el archivo .mpp a formato .csv')
        return archivo_csv

    def get_recursos_asignados(self, form, archivo_csv):
        """Obtiene un listado consolidado de los usuarios a ser asignados en la carga de EDT/tasks"""
        users_model = self.env['res.users']
        res = {}
        if not form.asignar_recursos_mpp:
            return {}
        for row in archivo_csv:
            recursos = json.loads(row['resources'])
            for r in recursos:
                email = r.get('email', False)
                if email and not email in res:
                    user = users_model.search(['|',('email','=',email),('login','=',email)], order='id DESC')
                    if user:
                        res[email] = user[0].id # Si hay varios ie un pxxx y otro cxxxx toma el usuario más reciente basado en el ID
                    else:
                        e = Warning('No se encontró el usuario "{0}" para ser asignado a la tarea No "{1}"'.format(
                            email, row['outline_number']
                        ))
                        _logger.exception(e)
                        raise e
        return res

    def get_datos_edts(self, form, archivo_csv, indice_recursos):
        """Genera la estructura de datos necesaria para crear project.edt"""
        res = []
        time_zone = self.env.context.get('tz') or 'UTC'
        time_zone = pytz.timezone(time_zone)
        utc = pytz.utc
        fmt_in = '%Y-%m-%d %H:%M:%S'
        fmt_out_time = '%Y-%m-%d %H:%M:%S'
        fmt_out = '%Y-%m-%d'
        incluir_leaves = False
        if form.metodo == 'hojas_son_paquetes_trabajo':
            incluir_leaves = True
        for row in archivo_csv:
            if not incluir_leaves and row['is_leaf'] == 'True':
                continue
            data = {
                'ms_project_guid':row['guid'],
                'numero': row['outline_number'],
                'name': row['name'],
                'progreso': int(float(row['percentage'])),
                'costo_planeado': int(float(row['cost'])),
                'costo': int(float(row['actual_cost'])),
            }
            for k,v in data.iteritems():
                if v == '0.0':
                    data[k] = 0
            if row['date_start']:
                fecha = datetime.strptime(row['date_start'], fmt_in)
                fecha = time_zone.localize(fecha)
                data['fecha_planeada_inicio'] = fecha.astimezone(utc).strftime(fmt_out)
            if row['date_end']:
                fecha = datetime.strptime(row['date_end'], fmt_in)
                fecha = time_zone.localize(fecha)
                data['fecha_planeada_fin'] = fecha.astimezone(utc).strftime(fmt_out)
            if row['actual_date_start']:
                fecha = datetime.strptime(row['actual_date_start'], fmt_in)
                fecha = time_zone.localize(fecha)
                data['fecha_inicio'] = fecha.astimezone(utc).strftime(fmt_out)
                data['date_start'] = fecha.astimezone(utc).strftime(fmt_out_time)
            if row['actual_date_end']:
                fecha = datetime.strptime(row['actual_date_end'], fmt_in)
                fecha = time_zone.localize(fecha)
                data['fecha_fin'] = fecha.astimezone(utc).strftime(fmt_out)
                data['date_end'] = fecha.astimezone(utc).strftime(fmt_out_time)
            else:
                data['fecha_fin'] = data['fecha_planeada_fin']

            if form.asignar_recursos_mpp:
                recursos = json.loads(row['resources'])
                for r in recursos:
                    email = r.get('email')
                    if r.get('tipo', None) in [None, 'responsable']:
                        data['user_id'] = indice_recursos.get(email, False)
                    elif r.get('tipo') == 'programador':
                        data['programador_id'] = indice_recursos.get(email, False)
            res.append(data)
        return res

    def get_datos_tareas(self, form, archivo_csv, indice_recursos):
        """Genera la estructura de datos necesaria para crear project.task"""
        if form.metodo == 'hojas_son_paquetes_trabajo':
            return [] # No hay que crear tasks

        res = []
        time_zone = self.env.context.get('tz') or 'UTC'
        time_zone = pytz.timezone(time_zone)
        utc = pytz.utc
        fmt_in = '%Y-%m-%d %H:%M:%S'
        fmt_out = '%Y-%m-%d %H:%M:%S'
        for row in archivo_csv:
            if row['is_leaf'] == 'False': # Solo las hojas crean tasks
                continue
            data = {
                'ms_project_guid':row['guid'],
                'numero': row['outline_number'],
                'name': unicode(row['name'], 'utf-8'),
                'progreso': int(float(row['percentage'])),
                'costo_planeado': int(float(row['cost'])),
                'costo': int(float(row['actual_cost'])),
                'raw_edt_id': row['parent_id'],
            }
            for k,v in data.iteritems():
                if v == '0.0':
                    data[k] = 0
            if row['date_start']:
                fecha = datetime.strptime(row['date_start'], fmt_in)
                fecha = time_zone.localize(fecha)
                data['fecha_planeada_inicio'] = fecha.astimezone(utc).strftime(fmt_out)
            if row['date_end']:
                fecha = datetime.strptime(row['date_end'], fmt_in)
                fecha = time_zone.localize(fecha)
                data['fecha_planeada_fin'] = fecha.astimezone(utc).strftime(fmt_out)
            if row['actual_date_start']:
                fecha = datetime.strptime(row['actual_date_start'], fmt_in)
                fecha = time_zone.localize(fecha)
                data['fecha_inicio'] = fecha.astimezone(utc).strftime(fmt_out)
            if row['actual_date_end']:
                fecha = datetime.strptime(row['actual_date_end'], fmt_in)
                fecha = time_zone.localize(fecha)
                data['fecha_fin'] = fecha.astimezone(utc).strftime(fmt_out)
            else:
                data['fecha_fin'] = data['fecha_planeada_fin']

            if row['actual_date_end']:
                data['duracion_dias'] = int(float(row.get('actual_duration','0').split('.')[0])) # Valor viene de esta forma: '33.0d' y lo dejamos 33
            else: # Si no hay actual date end se toma la duración planeada, porque de otra forma viene con valor 0 el actual_duration.
                data['duracion_dias'] = int(float(row.get('duration','0').split('.')[0])) # Valor viene de esta forma: '33.0d' y lo dejamos 33

            if form.asignar_recursos_mpp:
                recursos = json.loads(row['resources'])
                for r in recursos:
                    email = r.get('email')
                    if r.get('tipo', None) in [None, 'responsable']:
                        data['user_id'] = indice_recursos.get(email, False)
                    elif r.get('tipo') == 'revisor':
                        data['revisor_id'] = indice_recursos.get(email, False)
            res.append(data)
        return res


    def asociar_edts(self, form, archivo_csv, datos_edt, indice_objetos):
        """Crear las relaciones de agregación entre edts"""
        edt_model = self.env['project.edt']
        incluir_leaves = False
        if form.metodo == 'hojas_son_paquetes_trabajo':
            incluir_leaves = True
        # Padre - Hijo
        by_parent = {}
        for row in archivo_csv:
            if not incluir_leaves and row['is_leaf'] == 'True':
                continue

            edt_id = indice_objetos.get(row['guid'])[1]
            edt_padre_id = indice_objetos.get(row['parent_id'], (None, None))[1]
            if edt_padre_id:
                if not edt_padre_id in by_parent:
                    by_parent[edt_padre_id] = []
                by_parent[edt_padre_id].append(edt_id)
        ctx = {'carga_masiva': True, 'mail_notrack': True, 'mail_create_nosubscribe': True, 'tracking_disable': True}
        for parent_id, children_ids in by_parent.iteritems():
            edt_model.browse(children_ids).with_context(ctx).write({'parent_id': parent_id})

        # Dependencia


    def crear_dependencias(self, form, archivo_csv, indice_objetos):
        """Crear las relaciones de dependencia y agregación para tareas y EDTs"""
        predecesor_model = self.env['project.predecesor']
        edt_error_msg = '''Como buena práctica no deben crearse relaciones de dependencia con paquetes de trabajo,
                           por favor cree relaciones de dependencia solo entre tareas. Debe modificar el archivo en la EDT
                           {} {} y modificar la relación {}'''
        for row in archivo_csv:
            if row['predecesor'] != "[]": # Hay predecesores
                row_model = indice_objetos[row['guid']][0]
                row_id = indice_objetos[row['guid']][1]
                predecesores = json.loads(row['predecesor'])
                for p in predecesores:
                    # p = [{"guid": "5ab07020-0b7d-4f22-b0bf-191a77bf00e9", "tipo": "FS"}]
                    record = indice_objetos[p['guid']]
                    vals = {
                        'origen_res_model': record[0],
                        'origen_res_id': record[1],
                        'destino_res_model': row_model,
                        'destino_res_id': row_id,
                        'tipo': p['tipo'],
                        'lag': p['lag'],
                    }
                    if vals['origen_res_model'] == 'e':
                        edt = record[2]
                        raise Warning(edt_error_msg.format(edt.numero, edt.name, 'sucesora'))
                    if  vals['destino_res_model'] == 'e':
                        edt = indice_objetos[row['guid']][2]
                        raise Warning(edt_error_msg.format(edt.numero, edt.name, 'predecesora'))
                    predecesor_model.create(vals)
