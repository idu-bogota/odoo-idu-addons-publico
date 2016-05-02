# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import AccessError, Warning, ValidationError
from datetime import *

logging.basicConfig()
_logger = logging.getLogger('TEST')

class TestDateMaxMinAcciones(common.TransactionCase):

    def test_date_max_min_acciones(self):
        _logger.info("***** Inicio test_date_max_min_acciones *****")
        """Se valida que el usuario user_oci pueda leer todos los planes,
           hallazgos, acciones, avances existentes
        """
        user_oci_id = self.ref('plan_mejoramiento_idu.id_user_oci')
        id_plan = self.ref('plan_mejoramiento_idu.id_pmi_01')
        id_department_juridica = self.ref('plan_mejoramiento_idu.id_department_juridica')
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

        #Creación de hallazgo
        hallazgo = self.env['plan_mejoramiento.hallazgo'].sudo(user_oci_id).create({
            'plan_id': id_plan,
            'name': 'Hallazgo Test 01',
            'dependencia_id': id_department_juridica,
            'descripcion': 'Descripción de Hallazgo Interno 01',
            'causa': 'Causa de Hallazgo Interno Preventivo 01',
            'state': 'in_progress',
        })
        # Creacion de acciones
        accion_01 = self.env['plan_mejoramiento.accion'].sudo(user_oci_id).create({
            'name': 'accion Interna 01',
            'state': 'nuevo',
            'hallazgo_id': hallazgo.id,
            'dependencia_id': id_department_juridica,
            'accion_tipo': 'preventivo',
            'accion_correctiva': 'Acción Interna Preventiva de 01...',
            'objetivo': 'Objetivo de accion Interna 01',
            'indicador': 'tareas asignadas/tareas resueltas 01',
            'unidad_medida': 'tareas resueltas 01',
            'meta': 'lograr realizar 01...',
            'recurso': 'personal capacitado 01',
            'fecha_inicio': today - timedelta(days=10),
            'fecha_fin': today + timedelta(days=10),
        })
        accion_02 = self.env['plan_mejoramiento.accion'].sudo(user_oci_id).create({
            'name': 'accion Interna 03',
            'state': 'nuevo',
            'hallazgo_id': hallazgo.id,
            'dependencia_id': id_department_juridica,
            'accion_tipo': 'preventivo',
            'accion_correctiva': 'Acción Interna Preventiva de 02...',
            'objetivo': 'Objetivo de accion Interna 02',
            'indicador': 'tareas asignadas/tareas resueltas 02',
            'unidad_medida': 'tareas resueltas 02',
            'meta': 'lograr realizar 02...',
            'recurso': 'personal capacitado 02',
            'fecha_inicio': today - timedelta(days=20),
            'fecha_fin': today + timedelta(days=20),
        })
        accion_03 = self.env['plan_mejoramiento.accion'].sudo(user_oci_id).create({
            'name': 'accion Interna 03',
            'state': 'nuevo',
            'hallazgo_id': hallazgo.id,
            'dependencia_id': id_department_juridica,
            'accion_tipo': 'preventivo',
            'accion_correctiva': 'Acción Interna Preventiva de 03...',
            'objetivo': 'Objetivo de accion Interna 03',
            'indicador': 'tareas asignadas/tareas resueltas 03',
            'unidad_medida': 'tareas resueltas 03',
            'meta': 'lograr realizar 03...',
            'recurso': 'personal capacitado 03',
            'fecha_inicio': today - timedelta(days=30),
            'fecha_fin': today + timedelta(days=30),
        })
        fecha_inicio = datetime.strptime(hallazgo.fecha_inicio,'%Y-%m-%d')
        fecha_fin  = datetime.strptime(hallazgo.fecha_fin,'%Y-%m-%d')
        date_min = today - timedelta(days=30)
        date_max = today + timedelta(days=30)

        if fecha_inicio != date_min or fecha_fin != date_max:
            self.fail('Error en la fecha Maxima y Minima del Hallazgo')
        _logger.info("***** Fin test_date_max_min_acciones *****\n")