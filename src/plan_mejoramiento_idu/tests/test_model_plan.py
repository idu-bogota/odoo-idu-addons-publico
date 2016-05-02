# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common

logging.basicConfig()
_logger = logging.getLogger('TEST')

class TestPlanMejoramiento(common.SingleTransactionCase):

    def test_usuario_asignado_ok_al_crear(self):
        _logger.info("Ejecutando test_usuario_asignado_ok_al_crear")
        plan_model = self.env['plan_mejoramiento.plan']
        user_oci_id = self.ref('plan_mejoramiento_idu.id_user_oci')
        vals = {
            'name': 'Plan Interno',
            'radicado_orfeo': '00000',
            'tipo': 'interno',
            'dependencia_id': self.ref('plan_mejoramiento_idu.id_department_strt'),
            'origen_id': self.ref('plan_mejoramiento_idu.id_origen_01'),
            'proceso_id': self.ref('plan_mejoramiento_idu.id_proceso_01'),
            'user_id': user_oci_id,
        }
        plan = plan_model.create(vals)
        self.assertEqual(
            user_oci_id,
            plan.user_id.id,
            'Usuario del Plan no es el asignado'
        )
        self.assertEqual(
            user_oci_id,
            plan.edt_raiz_id.user_id.id,
            'Usuario del Plan.edt_raiz_id no es el asignado'
        )
        self.assertEqual(
            user_oci_id,
            plan.project_id.user_id.id,
            'Usuario del Plan.project_id no es el asignado'
        )


if __name__ == '__main__':
    unittest2.main()