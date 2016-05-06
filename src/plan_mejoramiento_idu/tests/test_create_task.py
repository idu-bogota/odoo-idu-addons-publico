# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import AccessError, ValidationError
from datetime import *

logging.basicConfig()
_logger = logging.getLogger('TEST')

class TestCreateTask(common.TransactionCase):

    def test_create_task(self):
        _logger.info("***** Inicio test_create_task *****")
        """Creacion de tarea asociado a una accion.
           No se realiza desde el yml por inpedimentos de asociar al campo
           edt_id el edt_raiz_id de la tarea
        """

        admin_id = self.ref('plan_mejoramiento_idu.id_user_admin_01')
        oci_id = self.ref('plan_mejoramiento_idu.id_user_oci')
        oci = self.browse_ref('plan_mejoramiento_idu.id_user_oci')
        jefe_id = self.ref('plan_mejoramiento_idu.id_user_jefe_d01')
        ejecutor_id = self.ref('plan_mejoramiento_idu.id_user_ejecutor_01')
        ejecutor2_id = self.ref('plan_mejoramiento_idu.id_user_ejecutor_02')
        accion = self.browse_ref('plan_mejoramiento_idu.id_acc_01').with_context(no_enviar_mail=True)
        dp_juridica = self.ref('plan_mejoramiento_idu.id_department_juridica')
        jefe_id_juridica =  self.ref('plan_mejoramiento_idu.id_user_jefe_d02')

        # Garantizar que el usuario jefe sea el jefe de la dependencia
        # Fechas
        today = date.today()
        fecha_incio = timedelta(days=10)
        fecha_fin = timedelta(days=11)

        # =====================================================================
        # (1) Estado Inicial
        self.assertEqual(accion.state, 'nuevo', 'WKF ok. Estado Inicial')
        # (2) la OCI lo lleva a por Aprovar
        accion.sudo(oci_id).signal_workflow('wkf_nuevo_a_por_aprobar')
        self.assertEqual(accion.state, 'por_aprobar', 'WKF ok')
        # (3) El jefe del area lo aprueba
        accion.sudo(jefe_id).signal_workflow('wkf_por_aprobar_a_aprobado')
        self.assertEqual(accion.state, 'aprobado', 'WKF ok')
        # (4) El jefe dependencia asigna el Ejecutores a la accion
        accion.sudo(jefe_id).write({
                'ejecutor_id': ejecutor_id
        })
        # (5) Ejecutor Crea Tarea
        # la tarea va ser para el area de juridica campo dependencia_id
        # el usuario proietario de la tarea debe pertenece al area de juridicas campo user_id
        self.assertEqual(len(accion.task_ids), 0) # Estado inicial sin tareas
        self.assertEqual(accion.state, 'aprobado') # Estado inicial
        task = {
            'project_id': accion.hallazgo_id.plan_id.project_id.id,
            'name': 'tarea test',
            'edt_id': accion.hallazgo_id.plan_id.edt_raiz_id.id,
            'dependencia_id': dp_juridica,
            'user_id': jefe_id_juridica,
            'fecha_inicio': today + fecha_incio,
            'fecha_fin': today + fecha_fin,
            'accion_id': accion.id
        }
        # Falla si el estado no es en_progreso
        try:
            accion.sudo(ejecutor_id).write({
                'task_ids': [
                    (0,0, task),
                ]
            })
        except ValidationError, e:
            pass
        else:
            self.fail('No se generó exception de validación cuando el estado no es en ejecución para la acción')
        # estado en progreso requerido
        accion.state = 'en_progreso'
        accion.sudo(ejecutor_id).write({
            'task_ids': [
                (0,0, task),
            ]
        })
        # Probando que un ejecutor diferente no puede crear tarea a la accion
        try:
            accion.sudo(ejecutor2_id).write({
                'task_ids': [
                    (0,0, task),
                ]
            })
        except AccessError, e:
            pass
        else:
            self.fail('No se generó exception de validación al crear una tarea con un ejecutor diferente al de la accion')

        # Verificando la cantidad de tareas creadas
        self.assertEqual(len(accion.task_ids), 1)

        _logger.info("***** Fin test_create_task *****\n")
