#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import erppeek
from import_csv import Import 
from import_avances import ImportAvance

class ImportAccion(Import):
    def __init__(self, odoo, _logger, hallazgo, id_hallazgo_css, options):
        self.odoo = odoo
        self._logger = _logger
        self.hallazgo = hallazgo
        self.id_hallazgo_css = id_hallazgo_css
        self.options = options

    def open_file_accion(self):
        with open(self.options.path_openERP +'plan_mejoramiento.accion.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            cnt = 0
            for row in reader:
                cnt += 1
                if self.id_hallazgo_css == row['hallazgo_id']:
                    self._logger.debug("        ***[{2}] Cargando Accion: [{0}] del Hallazgo: [{1}]***".format(row['accion'], self.hallazgo.name, cnt))
                    # Crear Accion
                    new_accion = self.create_accion(row['tipo'], row['auditor'], row['dependencia'], row['accion'], row['objetivo'], row['indicador'],
                                                    row['unidad_medida'], row['meta'], row['recursos'], row['fecha_inicio'], row['fecha_fin'],
                                                    row['descripcion'], row['denominacion_medida'], self.hallazgo,
                                                    row['ejecutor_login'], row['ejecutor_name'], row['ejecutor_email'], row['ejecutor_rol']
                                                   )
                    # Crear Avance
                    if self.options.avance_openERP == "1": # parametro de la consola para definir si se crena Avances
                        import_avance = ImportAvance(self.odoo, self._logger, new_accion, row['accion_id'], self.options)
                        import_avance.open_file_avance()
                    new_accion._send('wkf_carga_masiva')

    def create_accion(self, tipo, auditor, dependencia, accion, objetivo, indicador, unidad_medida, meta, recurso,
                      fecha_inicio, fecha_fin, descripcion, denominacion_medida, hallazgo,
                      ejecutor_login, ejecutor_name, ejecutor_email, ejecutor_rol):
        if ejecutor_login != '' and ejecutor_name != '' and ejecutor_email != '' and ejecutor_rol != '':
            # Para Ejecutor
            if not self.find_user_existing(ejecutor_login, ejecutor_email):
                # crear
                self.create_user(ejecutor_login, ejecutor_name, ejecutor_email, dependencia, ejecutor_rol)
                # buscar
                ejecutor = self.get_user(ejecutor_login, ejecutor_email)
            else:
                # solo buscar
                ejecutor = self.get_user(ejecutor_login, ejecutor_email)
                # actualizo rol
                self.add_rol_to_user(ejecutor_rol, ejecutor_login)

            new_accion = self.odoo.model('plan_mejoramiento.accion').create({
                'hallazgo_id': hallazgo.id,
                'accion_tipo': tipo,
                'user_id': self.get_user(auditor) or hallazgo.user_id.id,
                'dependencia_id': self.find_area(dependencia),
                'accion_correctiva': accion,
                'objetivo': objetivo,
                'indicador': indicador,
                'unidad_medida': unidad_medida,
                'meta': meta,
                'recurso': recurso,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'descripcion': descripcion,
                'denominacion_medida': denominacion_medida,
                'ejecutor_id': ejecutor
            })
            # Agregar el Auditro y Ejecutor como Seguidor
            new_accion.message_subscribe_users(self.get_user(auditor))
            new_accion.message_subscribe_users(ejecutor)
        else:
            new_accion = self.odoo.model('plan_mejoramiento.accion').create({
                'hallazgo_id': hallazgo.id,
                'accion_tipo': tipo,
                'user_id':self.get_user(auditor) or hallazgo.user_id.id,
                'dependencia_id': self.find_area(dependencia),
                'accion_correctiva': accion,
                'objetivo': objetivo,
                'indicador': indicador,
                'unidad_medida': unidad_medida,
                'meta': meta,
                'recurso': recurso,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'descripcion': descripcion,
                'denominacion_medida': denominacion_medida
            })
            # Agregar el Auditro como Seguidor
            new_accion.message_subscribe_users(self.get_user(auditor))

        if self.options.state_accion_openERP:
            new_accion.write({
                'state': self.options.state_accion_openERP,
            })
        return new_accion