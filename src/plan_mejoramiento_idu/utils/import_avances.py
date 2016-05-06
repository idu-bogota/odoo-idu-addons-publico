#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import erppeek
from import_csv import Import

class ImportAvance(Import):
    def __init__(self, odoo, _logger, accion, id_accion_css, options):
        self.odoo = odoo
        self._logger = _logger
        self.accion = accion
        self.id_accion_css = id_accion_css
        self.options = options

    def open_file_avance(self):
        with open(self.options.path_openERP + 'plan_mejoramiento.avance.csv') as csvfile:
            cnt = 0
            reader = csv.DictReader(csvfile)
            for row in reader:
                cnt += 1
                if self.id_accion_css == row['accion_id']:
                    self._logger.debug("            ***[{2}] Cargando Avance: [{0}] del Hallazgo: [{1}]***".format(row['descripcion'], self.accion.name, cnt))
                    # Crear Avance
                    self.create_avance(self.accion, row['descripcion'], row['fecha_corte'], row['porcentaje'], row['tipo_calificacion'],)

    def create_avance(self, accion, descripcion, fecha_corte, porcentaje, tipo_calificacion):
        new_avance = self.odoo.model('plan_mejoramiento.avance').create({
            'accion_id': accion.id,
            'descripcion': descripcion,
            'fecha_corte': fecha_corte,
            'porcentaje': porcentaje,
            'tipo_calificacion_id': None if tipo_calificacion == '' else self.find_tipo_calificacion(tipo_calificacion, accion.plan_tipo)
        })
        #Si tiene Ejecutor Agregarlo como Seguidor al avance
        if new_avance.accion_id.ejecutor_id:
            new_avance.message_subscribe_users(new_avance.accion_id.ejecutor_id.id)
        #Auditor OCI Agregar el Auditro como Seguidor al avance
        if new_avance.accion_id.user_id:
            new_avance.message_subscribe_users(new_avance.accion_id.user_id.id)
        return new_avance

    def find_tipo_calificacion(self, name, tipo_plan):
        calificacion = self.odoo.model('plan_mejoramiento.tipo_calificacion').get([('name','=',name), ('tipo_plan', '=', tipo_plan)])
        if calificacion is None:
            print 'El Tipo Calificacion {0} no Existe'.format(name)
            self._logger.error("El Tipo Calificacion '{0}' no Existe ".format(name))
            raise Exception('No Se Encontro El Tipo Calificacion Especificada')
        return calificacion.id