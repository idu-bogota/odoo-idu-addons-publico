#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import erppeek
import sys
from import_hallazgo import ImportHallazgo
from import_csv import Import

class ImportPlan(Import):
    def __init__(self, odoo, _logger, options):
        self.odoo = odoo
        self._logger = _logger
        self.options = options

    def open_file_plan(self):
        with open(self.options.path_openERP +'plan_mejoramiento.plan.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    self._logger.debug("***Cargando Plan: {0} ***".format(row['nombre']))
                    # buscar existencia del auditor
                    if not self.find_user_existing(row['Auditor'], row['email_user']):
                        # crear
                        self.create_user(row['Auditor'], row['name_user'], row['email_user'], row['area_user'], row['rol_user'])
                        # buscar
                        auditor = self.get_user(row['Auditor'], row['email_user'])
                    else:
                        # solo buscar
                        auditor = self.get_user(row['Auditor'], row['email_user'])
                        # actualizo rol
                        self.add_rol_to_user(row['rol_user'], row['Auditor'])
                    dependencia = self.find_area(row['dependencia'])
                    if row['tipo'] == 'interno':
                        origen = self.find_origen(row['origen'])
                        sub_origen = self.find_sub_origen(origen,row['sub_origen'])
                        proceso = self.find_proceso(row['proceso_origen'])
                        # Crear plan interno
                        plan_int = self.create_plan(row['nombre'], row['radicado_orfeo'], row['fecha_creacion'], dependencia, auditor, row['tipo'], origen, sub_origen, proceso)
                        # hallazgo
                        import_hallazgo = ImportHallazgo(self.odoo, self._logger, plan_int, row['id'], self.options)
                        import_hallazgo.open_file_hallazgo()
                    else:
                        #Crear plan  Ext
                        plan_ext = self.create_plan_ext(row['nombre'], row['radicado_orfeo'], row['fecha_creacion'], dependencia, auditor, row['tipo'])
                        import_hallazgo = ImportHallazgo(self.odoo, self._logger, plan_ext, row['id'], self.options)
                        import_hallazgo.open_file_hallazgo()
                except Exception as e:
                    self._logger.error('*******************')
                    self._logger.exception(e)

    def find_origen(self, name_origen):
        origen = self.odoo.model('plan_mejoramiento.origen').get([('name','=',name_origen)])
        if origen is None:
            #crear origen
            new_origen = self.odoo.model('plan_mejoramiento.origen').create({'name':name_origen})
            return new_origen.id
        else:
            return origen.id

    def find_sub_origen(self, name_origen, name_sub_origen):
        sub_origen = self.odoo.model('plan_mejoramiento.origen').get([('name','=',name_sub_origen), ('parent_id','=',name_origen) ])
        if sub_origen is None:
            #crear sub-origen
            new_sub_origen = self.odoo.model('plan_mejoramiento.origen').create({'name':name_sub_origen, 'parent_id':name_origen})
            return new_sub_origen
        else:
            return sub_origen.id

    def find_proceso(self, name_proceso):
        proceso = self.odoo.model('plan_mejoramiento.proceso').get([('name','=',name_proceso)])
        if proceso is None:
            #crear proceso
            new_proceso = self.odoo.model('plan_mejoramiento.proceso').create({'name':name_proceso})
            return new_proceso
        else:
            return proceso.id

    def create_plan(self, nombre, radicado_orfeo, fecha_creacion, dependencia, auditor, tipo, origen, sub_origen, proceso):
        new_plan = self.odoo.model('plan_mejoramiento.plan').create({
            'name': nombre,
            'radicado_orfeo':radicado_orfeo,
            'fecha_creacion': fecha_creacion,
            'dependencia_id': dependencia,
            'user_id': auditor,
            'tipo': tipo,
            'origen_id': origen,
            'sub_origen_id': sub_origen,
            'proceso_id': proceso
        })
        return new_plan

    def create_plan_ext(self, nombre, radicado_orfeo, fecha_creacion, dependencia, auditor, tipo):
        new_plan = self.odoo.model('plan_mejoramiento.plan').create({
            'name': nombre,
            'radicado_orfeo':radicado_orfeo,
#            'fecha_creacion': fecha_creacion,
            'dependencia_id': dependencia,
            'user_id': auditor,
            'tipo': tipo,
        })
        return new_plan