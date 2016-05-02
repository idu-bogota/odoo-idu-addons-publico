# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import AccessError
#from heapq import merge
from openerp.exceptions import Warning
from datetime import *

logging.basicConfig()
_logger = logging.getLogger('TEST')

class TestAnalistaDomains(common.TransactionCase):

    def test_group_analista_search(self):
        _logger.info("***** Inicio test_group_analista_search *****")
        """Se valida que el usuario analista solo se listen sus planes"""
        user_analista = self.ref('plan_mejoramiento_idu.id_user_analista_01')
        #PLAN
        planes = self.env['plan_mejoramiento.plan'].sudo(user_analista).search([])
        # Verificar la cantidad de planes retornadas
        self.assertEqual(4, len(planes))
        #HALLAZGO
        hallazgo = self.env['plan_mejoramiento.hallazgo'].sudo(user_analista).search([])
        self.assertEqual(3, len(hallazgo))
        #ACCION
        accion = self.env['plan_mejoramiento.hallazgo'].sudo(user_analista).search([])
        self.assertEqual(3, len(accion))
        #AVANCE
        avance = self.env['plan_mejoramiento.avance'].sudo(user_analista).search([])
        self.assertEqual(3, len(avance))
        _logger.info("***** Fin test_group_analista_search *****\n")

    def test_group_analista_create(self):
        _logger.info("***** Inicio test_group_analista_create *****")
        """Se valida que el usuario analista
            no pueda realizar operacion de crear en el objeto plan. com no
            puede realizar create, esto lanzara una excepcion que se controlará,
            si puede create lanzaremos una excepcion personalizada
        """
        user_analista = self.ref('plan_mejoramiento_idu.id_user_analista_01')
        #PLAN
        try:
            crear_plan = self.env['plan_mejoramiento.plan'].sudo(user_analista).create({})
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad Crando Plan')
        #HALLAZGO
        try:
            crear_hallazgo = self.env['plan_mejoramiento.hallazgo'].sudo(user_analista).create({})
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad Crando Hallazgo')
        #ACCION
        try:
            crear_accion = self.env['plan_mejoramiento.accion'].sudo(user_analista).create({})
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad Crando Accion')
        #AVANCE
        user_admin_plan = self.ref('plan_mejoramiento_idu.id_user_admin_01')
        accion_id = self.ref('plan_mejoramiento_idu.id_acc_04_for_task')
        # Crear Parametros del sistema
        today = date.today()
        wizard = self.env['plan_mejoramiento.wizard.abrir_registro_avance'].sudo(user_admin_plan).create({
                'fecha_inicio': today,
                'fecha_fin': today + timedelta(days=1),
        })
        # Ejecutar wizard para establecer fechas para crear avances
        wizard.action_create()
        # CREAR AVANCE
        try:
            avance = self.env['plan_mejoramiento.avance'].sudo(user_analista).create({
                 'accion_id': accion_id,
                 'state': 'en_progreso',
                 'descripcion': 'Descripcion Unit test de avance 01 de accion perteneciente a oci',
             })
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad Crando Avance')
        _logger.info("***** Fin test_group_analista_create *****\n")

    def test_group_analista_write(self):
        _logger.info("*****Inicio test_model_plan_group_analista_write *****")
        """Se valida que el usuario analista
            no pueda realizar operacion de write en el objeto plan. com no
            puede realizar create, esto lanzara una excepcion que se controlará,
            si puede create lanzaremos una excepcion personalizada
        """
        user_analista = self.ref('plan_mejoramiento_idu.id_user_analista_01')

        planes = self.env['plan_mejoramiento.plan'].sudo(user_analista).search([])
        hallazgo = self.env['plan_mejoramiento.hallazgo'].sudo(user_analista).search([])
        accion = self.env['plan_mejoramiento.accion'].sudo(user_analista).search([])
        avance = self.env['plan_mejoramiento.avance'].sudo(user_analista).search([])

        #PLAN
        try:
            planes[0].sudo(user_analista).write({
                'name': 'Sobreescribiendo Nombre',
            })
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad Sobreescribiendo Plan')
        #HALLAZGO
        try:
            hallazgo[0].sudo(user_analista).write({
                'name': 'Sobreescribiendo Nombre',
            })
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad Sobreescribiendo Hallazgo')
        #ACCION
        try:
            accion[0].sudo(user_analista).write({
                'name': 'Sobreescribiendo Nombre',
            })
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad Sobreescribiendo Accion')
        #AVANCE
        try:
            avance[0].sudo(user_analista).write({
                 'fecha_corte': '2015-06-01',
             })
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad Sobreescribiendo Avance')
        _logger.info("***** Fin test_model_plan_group_analista_write *****\n")