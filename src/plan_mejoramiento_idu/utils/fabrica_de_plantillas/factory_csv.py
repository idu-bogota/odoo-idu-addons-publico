#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

class FactoryCSV():
    def __init__(self):
        self.file_plan = 'plan_mejoramiento.plan.csv'
        self.file_hallazgo = 'plan_mejoramiento.hallazgo.csv'
        self.file_accion = 'plan_mejoramiento.accion.csv'
        self.file_avance = 'plan_mejoramiento.avance.csv'
        self.id_plan = 0
        self.id_hallazgo = 0
        self.id_accion = 0
        self.id_avance = 0

    def create_file_csv(self):
        # Plan
        with open('plan_interno/' + self.file_plan, 'w') as csvfile_p:
            fieldnames = ['id', 'nombre', 'tipo', 'radicado_orfeo', 'fecha_creacion',
                'dependencia', 'Auditor', 'origen', 'sub_origen', 'proceso_origen', 
                'name_user', 'email_user', 'area_user','rol_user']
            writer = csv.DictWriter(csvfile_p, fieldnames=fieldnames)
            writer.writeheader()

        # Hallazgo
        with open('plan_interno/' + self.file_hallazgo, 'w') as csvfile_h:
            fieldnames = ['hallazgo_id', 'plan_id', 'auditor', 'name_hallazgo',
                'capitulo', 'dependencia', 'descripcion', 'causa', 'efecto']
            writer = csv.DictWriter(csvfile_h, fieldnames=fieldnames)
            writer.writeheader()

        # Acciones
        with open('plan_interno/' + self.file_accion, 'w') as csvfile_a:
            fieldnames = ['accion_id', 'hallazgo_id', 'tipo', 'auditor', 'dependencia',
                'accion', 'objetivo', 'indicador', 'unidad_medida', 'meta', 'recursos',
                'fecha_inicio', 'fecha_fin', 'descripcion', 'denominacion_medida',
                'ejecutor_login', 'ejecutor_name', 'ejecutor_email', 'ejecutor_rol']
            writer = csv.DictWriter(csvfile_a, fieldnames=fieldnames)
            writer.writeheader()

        # Avance
        with open('plan_interno/' + self.file_avance, 'w') as csvfile_av:
            fieldnames = ['avances_id', 'accion_id', 'descripcion', 'fecha_corte',
                'estado', 'porcentaje', 'tipo_calificacion']
            writer = csv.DictWriter(csvfile_av, fieldnames=fieldnames)
            writer.writeheader()

    def add_line_template_plan(self, nombre, tipo, radicado_orfeo,
        fecha_creacion, dependencia, Auditor, origen, sub_origen, proceso_origen,
        name_user, email_user, area_user, rol_user):
        self.id_plan += 1
        with open('plan_interno/' + self.file_plan, 'a') as csvfile_p:
            fieldnames = ['id', 'nombre', 'tipo', 'radicado_orfeo', 'fecha_creacion',
                'dependencia', 'Auditor', 'origen', 'sub_origen', 'proceso_origen', 
                'name_user', 'email_user', 'area_user','rol_user']
            writer = csv.DictWriter(csvfile_p, fieldnames=fieldnames)
            writer.writerow({'id': self.id_plan, 'nombre': nombre, 'tipo': tipo,
                'radicado_orfeo': radicado_orfeo, 'fecha_creacion': fecha_creacion,
                'dependencia': dependencia, 'Auditor': Auditor, 'origen': origen,
                'sub_origen': sub_origen, 'proceso_origen': proceso_origen,
                'name_user': name_user, 'email_user': email_user, 'area_user': area_user,
                'rol_user': rol_user
            })

    def find_existing_plan(self, name_plan):
        with open('plan_interno/' + self.file_plan) as csvfile:
            reader = csv.DictReader(csvfile)
            contador = 0
            for row in reader:
                if row['nombre'] == name_plan:
                    contador += 1
            if contador > 0:
                return True
            else:
                return False

    def get_id_plan(self, name_plan):
        with open('plan_interno/' + self.file_plan) as csvfile:
            reader = csv.DictReader(csvfile)
            id = 0
            for row in reader:
                if row['nombre'] == name_plan:
                    id = row['id']
                    break
            return id

    def add_line_template_hallazgo(self, plan_id, auditor, name_hallazgo,
        dependencia, descripcion, causa):
        self.id_hallazgo += 1
        with open('plan_interno/' + self.file_hallazgo, 'a') as csvfile_h:
            fieldnames = ['hallazgo_id', 'plan_id', 'auditor', 'name_hallazgo',
                'capitulo', 'dependencia', 'descripcion', 'causa', 'efecto']
            writer = csv.DictWriter(csvfile_h, fieldnames=fieldnames)

            writer.writerow({'hallazgo_id': self.id_hallazgo, 'plan_id': plan_id,
                'auditor': auditor, 'name_hallazgo': name_hallazgo,
                'dependencia': dependencia, 'descripcion': descripcion,
                'causa': causa
            })
    def find_existing_hallazgo(self, descripcion_hallazgo):
        with open('plan_interno/' + self.file_hallazgo) as csvfile:
            reader = csv.DictReader(csvfile)
            contador = 0
            for row in reader:
                if row['descripcion'] == descripcion_hallazgo:
                    contador += 1
            if contador > 0:
                return True
            else:
                return False

    def get_id_hallazgo(self, descripcion_hallazgo):
        with open('plan_interno/' + self.file_hallazgo) as csvfile:
            reader = csv.DictReader(csvfile)
            id_hallazgo = 0
            for row in reader:
                if row['descripcion'] == descripcion_hallazgo:
                    id_hallazgo = row['hallazgo_id']
                    break
            return id_hallazgo

    def add_line_template_accion(self, hallazgo_id, tipo, auditor, dependencia,
        accion, objetivo, indicador, unidad_medida, meta, recursos,
        fecha_inicio, fecha_fin, ejecutor_login, ejecutor_name, ejecutor_email, ejecutor_rol):
        self.id_accion += 1
        with open('plan_interno/' + self.file_accion, 'a') as csvfile_a:
            fieldnames = ['accion_id', 'hallazgo_id', 'tipo', 'auditor', 'dependencia',
                'accion', 'objetivo', 'indicador', 'unidad_medida', 'meta', 'recursos',
                'fecha_inicio', 'fecha_fin', 'descripcion', 'denominacion_medida',
                'ejecutor_login', 'ejecutor_name', 'ejecutor_email', 'ejecutor_rol']
            writer = csv.DictWriter(csvfile_a, fieldnames=fieldnames)

            writer.writerow({'accion_id': self.id_accion, 'hallazgo_id': hallazgo_id,
                'tipo': tipo, 'auditor': auditor, 'dependencia': dependencia,
                'accion': accion, 'objetivo': objetivo, 'indicador': indicador,
                'unidad_medida': unidad_medida, 'meta': meta,
                'recursos': recursos, 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin,
                'ejecutor_login': ejecutor_login, 'ejecutor_name': ejecutor_name,
                'ejecutor_email': ejecutor_email, 'ejecutor_rol': ejecutor_rol
            })
    def find_existing_accion(self, accion):
        with open('plan_interno/' + self.file_accion) as csvfile:
            reader = csv.DictReader(csvfile)
            contador = 0
            for row in reader:
                if row['accion'] == accion:
                    contador += 1
            if contador > 0:
                return True
            else:
                return False

    def get_id_accion(self, accion):
        with open('plan_interno/' + self.file_accion) as csvfile:
            reader = csv.DictReader(csvfile)
            id_accion = 0
            for row in reader:
                if row['accion'] == accion:
                    id_accion = row['accion_id']
                    break
            return id_accion

    def add_line_template_avances(self, accion_id, descripcion, fecha_corte,
        estado, porcentaje, tipo_calificacion):
        self.id_avance += 1
        with open('plan_interno/' + self.file_avance, 'a') as csvfile_av:
            fieldnames = ['avances_id', 'accion_id', 'descripcion', 'fecha_corte',
                'estado', 'porcentaje', 'tipo_calificacion']
            writer = csv.DictWriter(csvfile_av, fieldnames=fieldnames)

            writer.writerow({'avances_id':self.id_avance , 'accion_id': accion_id,
                'descripcion': descripcion, 'fecha_corte': fecha_corte, 'estado': estado,
                'porcentaje': porcentaje, 'tipo_calificacion': tipo_calificacion
            })
    def get_tipo_calificacion_avances_internos(self, cumplida, no_cumplida, a_tiempo):
        calificacion = []
        if cumplida:
            calificacion.append('terminado') # estado
            calificacion.append('Cumplida')  # mombre
            calificacion.append(100)         # %
        elif no_cumplida:
            calificacion.append('en_progreso')
            calificacion.append('No Cumplida')
            calificacion.append(50)
        elif a_tiempo:
            calificacion.append('terminado')
            calificacion.append('En Tiempo')
            calificacion.append(100)
        return calificacion
