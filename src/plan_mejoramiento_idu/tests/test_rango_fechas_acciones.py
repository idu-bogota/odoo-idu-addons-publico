# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import AccessError, Warning, ValidationError
from datetime import *

logging.basicConfig()
_logger = logging.getLogger('TEST')

class TestRangoFechasAcciones(common.TransactionCase):

    def test_rango_fechas_Acciones(self):
        _logger.info("***** Inicio test_rago_fechas_Acciones *****")
        """Se valida los controles por los check_fecha_inicio, check_fecha_fin
           y los onchange_fecha_inicio,  onchange_fecha_fin
        """
        user_oci_id = self.ref('plan_mejoramiento_idu.id_user_oci')
        id_hallazgo = self.ref('plan_mejoramiento_idu.id_h_01')
        id_department_juridica = self.ref('plan_mejoramiento_idu.id_department_juridica')

        today = date.today()
        # Crear Acción, Fecha_inicio > Fecha_fin
        try:
            create_accion = self.env['plan_mejoramiento.accion'].sudo(user_oci_id).create({
                'name': 'accion Interna 01',
                'state': 'nuevo',
                'hallazgo_id': id_hallazgo,
                'dependencia_id': id_department_juridica,
                'accion_tipo': 'preventivo',
                'accion_correctiva': 'Acción Interna Preventiva de ...',
                'objetivo': 'Objetivo de accion Interna',
                'indicador': 'tareas asignadas/tareas resueltas',
                'unidad_medida': 'tareas resueltas',
                'meta': 'lograr realizar...',
                'recurso': 'personal capacitado',
                'fecha_inicio': today + timedelta(days=10),
                'fecha_fin': today,
            })
        except ValidationError:
            pass
        else:
            self.fail('No se genero Exception de check y onchange (Fecha_inicio > Fecha_fin) al Crear la Acción')
        _logger.info("***** Fin test_rago_fechas_Acciones *****\n")