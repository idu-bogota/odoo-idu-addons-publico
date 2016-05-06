# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import AccessError, ValidationError
from heapq import merge
from datetime import *

logging.basicConfig()
_logger = logging.getLogger('TEST')

class TestJefeDomains(common.TransactionCase):

    def test_group_jefe_dependencia_search(self):
        _logger.info("***** Inicio test_group_jefe_dependencia_search *****")
        """Se valida que el usuario jefe_dependencia solo pueda leer los planes,
           hallazgos, avances, accion que coinciden con su area.
        """
        jefe_d01 = self.browse_ref('plan_mejoramiento_idu.id_user_jefe_d01')
        jefe_d02 = self.browse_ref('plan_mejoramiento_idu.id_user_jefe_d02')

        # PAN
        planes_jd01 = self.env['plan_mejoramiento.plan'].sudo(jefe_d01.id).search([])
        planes_jd02 = self.env['plan_mejoramiento.plan'].sudo(jefe_d02.id).search([])
        # Verificar la cantidad de planes internos retornadas
        self.assertEqual(4, len(planes_jd01))
        self.assertEqual(4, len(planes_jd02))

        # HALLAZGO
        hallazgo_jd01 = self.env['plan_mejoramiento.hallazgo'].sudo(jefe_d01.id).search([])
        hallazgo_jd02 = self.env['plan_mejoramiento.hallazgo'].sudo(jefe_d02.id).search([])
        # Verificar la cantidad de planes internos retornadas
        self.assertEqual(3, len(hallazgo_jd01))
        self.assertEqual(3, len(hallazgo_jd02))

        #ACCION
        accion_jd01 = self.env['plan_mejoramiento.accion'].sudo(jefe_d01.id).search([])
        accion_jd02 = self.env['plan_mejoramiento.accion'].sudo(jefe_d02.id).search([])
        # Verificar la cantidad de planes internos retornadas
        self.assertEqual(4, len(accion_jd01))
        self.assertEqual(4, len(accion_jd02))
        # Obtener los IDs de los departamentos asociados a los planes para verificar que son las del usuario
        department_ids_jd01 = list(set([i.dependencia_id.id for i in accion_jd01]))
        department_ids_jd01.sort()
        #self.assertEqual([jefe_d01.department_id.id], department_ids_jd01)

        #AVANCE
        avance_jd01 = self.env['plan_mejoramiento.avance'].sudo(jefe_d01.id).search([])
        avance_jd02 = self.env['plan_mejoramiento.avance'].sudo(jefe_d02.id).search([])
        # Verificar la cantidad de planes internos retornadas
        self.assertEqual(1, len(avance_jd01))
        self.assertEqual(0, len(avance_jd02))
        # Obtener los IDs de los departamentos asociados a los planes para verificar que son las del usuario
        department_ids_jd01 = list(set([i.dependencia_id.id for i in avance_jd01]))
        department_ids_jd01.sort()
        self.assertEqual([jefe_d01.department_id.id], department_ids_jd01)
        _logger.info("***** Fin test_group_jefe_dependencia_search *****\n")


    def test_group_jefe_dependencia_create(self):
        _logger.info("***** Inicio test_group_jefe_dependencia_create *****")
        """Se valida que el usuario jefe_dependencia no pueda realizar operacion
           de CREATE en el objeto plan, hallazgo, accion. como no
           puede realizar CREATE, esto lanzara una excepcion que se controlará.
           Si puede create (alertaremos que esta mal la prueba), lanzaremos
           una excepcion personalizada.
        """
        jefe_d01 = self.ref('plan_mejoramiento_idu.id_user_jefe_d01')
        # PLAN
        try:
            crear_plan = self.env['plan_mejoramiento.plan'].sudo(jefe_d01).create({})
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad al Crear Plan')
        # HALLAZGO
        try:
            crear_hallazgo = self.env['plan_mejoramiento.hallazgo'].sudo(jefe_d01).create({})
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad al Crear Hallazgo')
        # ACCION
        try:
            crear_accion = self.env['plan_mejoramiento.accion'].sudo(jefe_d01).create({})
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad al Crear Accion')
        # AVANCE
        """Se valida que el usuario jefe_dependencia
            pueda crear avances que pertenescan a su area
        """
        jefe_d01 = self.browse_ref('plan_mejoramiento_idu.id_user_jefe_d01')
        accion_id = self.browse_ref('plan_mejoramiento_idu.id_acc_04_for_task')

        avance = self.env['plan_mejoramiento.avance'].sudo(jefe_d01.id).create({
             'accion_id': accion_id.id,
             'state': 'en_progreso',
             'descripcion': 'Descripcion Unit test de avance 01 de accion perteneciente a oci',
             'fecha_corte': '2015-05-01',
         })
        _logger.info("***** Fin test_group_jefe_dependencia_create *****\n")


    def test_group_jefe_dependencia_write(self):
        _logger.info("***** Inicio test_group_jefe_dependencia_write *****")
        """Se valida que el usuario jefe_dependencia no pueda realizar operacion
           de WRITE en el objeto plan, hallazgo, accion. como no
           puede realizar WRITE, esto lanzara una excepcion que se controlará.
           Si puede create (alertaremos que esta mal la prueba), lanzaremos
           una excepcion personalizada.
        """
        jefe_d01 = self.browse_ref('plan_mejoramiento_idu.id_user_jefe_d01')
        jefe_d02 = self.browse_ref('plan_mejoramiento_idu.id_user_jefe_d02')
        result = self.browse_ref('plan_mejoramiento_idu.id_user_jefe_d01').has_group_v8('base_idu.group_jefe_dependencia')
        self.assertTrue(result, 'has_group funciona')

        # PLAN
        planes_jd01 = self.env['plan_mejoramiento.plan'].sudo(jefe_d01.id).search([])
        try:
            planes_jd01[0].sudo(jefe_d01).write({
                'name': 'Sobreescribiendo Nombre',
            })
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad al Sobreescribir Plan')

        # HALLAZGO
        hallazgo_jd01 = self.env['plan_mejoramiento.hallazgo'].sudo(jefe_d01.id).search([])
        try:
            hallazgo_jd01[0].sudo(jefe_d01).write({
                'name': 'Sobreescribiendo Nombre'
            })
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad al Sobreescribir Hallazgo')

        # ACCION
        """El Jefe_dependencia solo prodra Actualizar el Estado, en este caso se Captura la Ecepción"""
        accion_jd01 = self.env['plan_mejoramiento.accion'].sudo(jefe_d01.id).search([])
        try:
            accion_jd01[0].sudo(jefe_d01).write({
                'name': "Sobreescribiendo Nombre"
            })
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad Sobreescribir Accion')

        """El Jefe_dependnecia debe poder actualizar el estado unicamente"""
        accion_jd01[0].sudo(jefe_d01).write({
            'state': "terminado"
        })

        # AVANCE
        """Se valida que el usuario jefe_dependencia pueda realizar operacion
           de WRITE en el objeto avance.
        """
        avances_jd01 = self.env['plan_mejoramiento.avance'].sudo(jefe_d01.id).search([])
        avances_jd01[0].sudo(jefe_d01).write({
            'fecha_corte': '2015-12-01',
        })
        """ Se valida que el usuario jefe_dependencia perteneciente a un area
            distintas al del avance se pueda editar. se controla la excepción
            y en caso de no pasar por la excepcion alertamos con una excepción
            personalizada
        """
        try:
            avances_jd01[0].sudo(jefe_d02.id).write({
                 'fecha_corte': '2015-06-01',
            })
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad al Sobreescribir Avance otro jefe_dependencia')
        _logger.info("***** Fin test_group_jefe_dependencia_write *****\n")