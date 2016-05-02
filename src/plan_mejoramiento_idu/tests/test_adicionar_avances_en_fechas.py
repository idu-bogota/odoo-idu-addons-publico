# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import Warning
from datetime import *

logging.basicConfig()
_logger = logging.getLogger('TEST')

class TestDateWizard(common.TransactionCase):

    def test_wizard_fuera_rango(self):
        _logger.info("***** Inicio test_wizard furea de rango*****")
        """Se valida que el usuario jefe_dependencia No pueda crear avances 
           fuera del rango de fechas establecidas para el sistema con el wizard
        """
        user_admin_plan = self.ref('plan_mejoramiento_idu.id_user_admin_01')
        jefe_d_id = self.ref('plan_mejoramiento_idu.id_user_jefe_d01')
        accion_id = self.ref('plan_mejoramiento_idu.id_acc_04_for_task')

        # Crear Parametros del sistema
        today = date.today()
        fecha_incio = timedelta(days=10)
        fecha_fin = timedelta(days=11)

        wizard = self.env['plan_mejoramiento.wizard.abrir_registro_avance'].sudo(user_admin_plan).create({
                'fecha_inicio': today + fecha_incio,
                'fecha_fin': today + fecha_fin,
        })
        # Ejecutar wizard para establecer fechas para crear avances
        wizard.action_create()
        # Crear Avance Fuera del rango para crear
        try:
            avance = self.env['plan_mejoramiento.avance'].sudo(jefe_d_id).create({
                 'accion_id': accion_id,
                 'state': 'en_progreso',
                 'descripcion': 'Descripcion Unit test de avance 01 de accion perteneciente a oci',
                 'fecha_corte': today,
            })
        except Warning:
            pass
        else:
            self.fail('No se genero Exception de Seguridad al Create Avances')
        _logger.info("***** Fin test_wizard furea de rango*****\n")

    def test_wizard_en_rango(self):
        _logger.info("***** Inicio test_wizard en rango*****")
        """Se valida que el usuario jefe_dependencia  pueda crear avances
           en el rango de fechas establecidas para el sistema con el wizard
        """
        user_admin_plan = self.ref('plan_mejoramiento_idu.id_user_admin_01')
        jefe_d_id = self.ref('plan_mejoramiento_idu.id_user_jefe_d01')
        accion_id = self.ref('plan_mejoramiento_idu.id_acc_04_for_task')

        # Crear Parametros del sistema
        today = date.today()
        fecha_fin = timedelta(days=11)

        wizard = self.env['plan_mejoramiento.wizard.abrir_registro_avance'].sudo(user_admin_plan).create({
                'fecha_inicio': today,
                'fecha_fin': today + fecha_fin,
        })
        # Ejecutar wizard para establecer fechas para crear avances
        wizard.action_create()
        # Crear Avance en rango de fechas permitidas para crear
        avance_02 = self.env['plan_mejoramiento.avance'].sudo(jefe_d_id).create({
            'accion_id': accion_id,
            'state': 'en_progreso',
            'descripcion': 'Descripcion Unit test de avance 01 de accion perteneciente a oci',
            'fecha_corte': today,
        })
        _logger.info("***** Fin test_wizard en rango*****\n")