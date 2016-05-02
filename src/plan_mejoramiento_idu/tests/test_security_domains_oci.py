# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import AccessError

logging.basicConfig()
_logger = logging.getLogger('TEST')

class TestOciDomains(common.TransactionCase):

    def test_group_oci_search(self):
        _logger.info("***** Inicio test_group_oci_search *****")
        """Se valida que el usuario user_oci pueda leer todos los planes,
           hallazgos, acciones, avances existentes
        """
        user_oci_id = self.ref('plan_mejoramiento_idu.id_user_oci')
        user_oci_id_02 = self.ref('plan_mejoramiento_idu.id_user_oci_02')

        # PLAN
        planes_internos = self.env['plan_mejoramiento.plan'].sudo(user_oci_id).search([])
        # Verificar la cantidad de planes internos retornadas
        self.assertEqual(4, len(planes_internos))
        # Obtener los IDs de los planes internos para verificar que son las del usuario
        user_ids = list(set([i.user_id.id for i in planes_internos]))
        user_ids.sort()
        self.assertEqual([user_oci_id, user_oci_id_02], user_ids)

        # HALLAZGO
        hallazgo_internos = self.env['plan_mejoramiento.hallazgo'].sudo(user_oci_id).search([])
        # Verificar la cantidad de Hallazgo internos retornadas
        self.assertEqual(3, len(hallazgo_internos))
        # Obtener los IDs de los planes internos para verificar que son las del usuario demo
        user_ids = list(set([i.user_id.id for i in hallazgo_internos]))
        user_ids.sort()
        self.assertEqual([user_oci_id, user_oci_id_02], user_ids)

        # ACCION
        acciones = self.env['plan_mejoramiento.accion'].sudo(user_oci_id).search([])
        # Verificar la cantidad de Hallazgo internos retornadas
        self.assertEqual(4, len(acciones))
        # Obtener los IDs de los planes internos para verificar que son las del usuario demo
        user_ids = list(set([i.user_id.id for i in acciones]))
        user_ids.sort()
        self.assertEqual([user_oci_id, user_oci_id_02], user_ids)

        # AVANCES
        avance = self.env['plan_mejoramiento.avance'].sudo(user_oci_id).search([])
        # Verificar la cantidad de Hallazgo internos retornadas
        self.assertEqual(3, len(avance))
        # Obtener los IDs de los planes internos para verificar que son las del usuario demo
        user_ids = list(set([i.user_id.id for i in avance]))
        user_ids.sort()
        self.assertEqual([user_oci_id, user_oci_id_02], user_ids)
        _logger.info("***** Fin test_group_oci_search *****\n")

    def test_group_oci_create(self):
        _logger.info("***** Inicio test_group_oci_create *****")
        """Se valida que el usuario user_ocio pueda realizar operacion
           de CREATE en el objeto plan, hallazgo, accion.
        """
        user_oci = self.ref('plan_mejoramiento_idu.id_user_oci')
        id_department_juridica = self.ref('plan_mejoramiento_idu.id_department_juridica')
        # PLAN
        crear_plan = self.env['plan_mejoramiento.plan'].sudo(user_oci).create({
            'name': 'Plan M. BOGOTA PMB 02',
            'radicado_orfeo': 'A002',
            'tipo': 'contraloria_bog',
            'dependencia_id': id_department_juridica
        })
        # HALLAZGO
        create_hallazgo = self.env['plan_mejoramiento.hallazgo'].sudo(user_oci).create({
            'plan_id': crear_plan.id,
            'name': 'Hallazgo Test 01',
            'dependencia_id': id_department_juridica,
            'descripcion': 'Descripción de Hallazgo Interno 01',
            'causa': 'Causa de Hallazgo Interno Preventivo 01',
            'state': 'in_progress',
        })

        # ACCIONES
        create_accion = self.env['plan_mejoramiento.accion'].sudo(user_oci).create({
            'name': 'accion Interna 01',
            'state': 'nuevo',
            'hallazgo_id': create_hallazgo.id,
            'dependencia_id': id_department_juridica,
            'accion_tipo': 'preventivo',
            'accion_correctiva': 'Acción Interna Preventiva de ...',
            'objetivo': 'Objetivo de accion Interna',
            'indicador': 'tareas asignadas/tareas resueltas',
            'unidad_medida': 'tareas resueltas',
            'meta': 'lograr realizar...',
            'recurso': 'personal capacitado',
            'fecha_inicio': '2015-05-01',
            'fecha_fin': '2015-05-01',
        })

        # AVANCES
        """ Se valida que el usuario OCI no pueda realizar CREATE en el objeto
            Avance.
        """
        try:
            create_avance = self.env['plan_mejoramiento.avance'].sudo(user_oci).create({
                'accion_id': create_accion.id,
                'state': 'en_progreso',
                'descripcion': 'Descripcion de avance, 01 de accion perteneciente a oci',
                'fecha_corte': '2015-05-01',
            })
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad al Create Avances')
        _logger.info("***** Fin test_group_oci_create *****\n")


    def test_group_oci_write(self):
        _logger.info("***** Inicio test_group_oci_write *****")
        """Se valida que el usuario user_ocio pueda realizar operacion
           de WRITE en el objeto plan, hallazgo, accion, Avances.
        """
        user_oci = self.ref('plan_mejoramiento_idu.id_user_oci')
        jefe_dependencia_id = self.ref('plan_mejoramiento_idu.id_user_jefe_d01')

        # PLAN
        planes = self.env['plan_mejoramiento.plan'].sudo(user_oci).search([])
        planes[0].sudo(user_oci).write({
            'name': 'Sobreescribiendo Nombre',
        })

        # HALLAZGO
        hallazgo = self.env['plan_mejoramiento.hallazgo'].sudo(user_oci).search([])
        hallazgo[0].sudo(user_oci).write({
            'name': 'Sobreescribiendo Nombre',
        })

        # ACCION
        accion = self.env['plan_mejoramiento.accion'].sudo(user_oci).search([])
        accion[0].sudo(user_oci).write({
            'name': 'Sobreescribiendo Nombre',
        })

        # AVANCES
        avance = self.browse_ref('plan_mejoramiento_idu.id_avance1_oci')
        # El jefe dependencia lo aprueba para que el usuario oci pueda calificar
        avance.sudo(jefe_dependencia_id).write({
            'aprobacion_jefe_dependencia': True,
        })
        # Calificar Avance por OCI
        avance.sudo(user_oci).write({
            'porcentaje': 20,
        })
        _logger.info("***** Fin test_group_oci_write *****\n")

if __name__ == '__main__':
    unittest2.main()