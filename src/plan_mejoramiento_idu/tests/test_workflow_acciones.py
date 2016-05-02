# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import AccessError

logging.basicConfig()
_logger = logging.getLogger('TEST')

class TestWorkflowAcciones(common.TransactionCase):

    def test_workflow_acciones(self):
        _logger.info("***** Inicio test_workflow_acciones *****")
        """ Estas Pruebas ejecutan funciones que envian correos electronicos.
            Para no tener inconvenientes instalar un servidor MSTP. Asi:
                sudo apt-get install postfix
            Se verifica el flujo completo de acciones
        """
        admin_id = self.ref('plan_mejoramiento_idu.id_user_admin_01')
        oci_id = self.ref('plan_mejoramiento_idu.id_user_oci')
        oci = self.browse_ref('plan_mejoramiento_idu.id_user_oci')
        jefe_id = self.ref('plan_mejoramiento_idu.id_user_jefe_d01')
        accion = self.browse_ref('plan_mejoramiento_idu.id_acc_01').with_context(no_enviar_mail=True)

        # =====================================================================
        # (1) Estado Inicial
        self.assertEqual(accion.state, 'nuevo', 'WKF ok. Estado Inicial')
        accion.sudo(jefe_id).signal_workflow('wkf_nuevo_a_por_aprobar')
        self.assertEqual(accion.state, 'nuevo', 'WKF no cambia por el jefe dependencia')
        accion.sudo(oci_id).signal_workflow('wkf_nuevo_a_por_aprobar')
        self.assertEqual(accion.state, 'por_aprobar', 'WKF ok')

        """Se valida que el jefe dependencia no puede modificar la accion en estado por_aprobar """
        accion_jd01 = self.env['plan_mejoramiento.accion'].sudo(jefe_id).search([])
        try:
            accion_jd01[0].sudo(jefe_id).write({
                'name': "Sobreescribiendo Nombre"
            })
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad Sobreescribir Accion')

        """Se valida que el jefe dependencia no pueda crear tareas cuando la accion se encuentra en el estado por_aprobar"""
#         try:
#             task = self.env['project.task'].sudo(jefe_id).create({
#                 'name': 'tarea test',
#                 'edt_id': accion_jd01.edt_raiz_id.id,
#                 'user_id': jefe_id,
#                 'reviewer_id': jefe_id,
#              })
#         except AccessError:
#             pass
#         else:
#             self.fail('No se genero Exception de Seguridad Sobreescribir Accion')

        # =====================================================================
        # (2) Estados. de pro_aprobar a rechazar
        accion.sudo(oci_id).signal_workflow('wkf_por_aprobar_a_rechazado')
        self.assertEqual(accion.state, 'por_aprobar', 'WKF no cambia por el OCI')
        accion.sudo(jefe_id).signal_workflow('wkf_por_aprobar_a_rechazado')
        self.assertEqual(accion.state, 'rechazado', 'WKF ok')
        """Se valida que el jefe dependencia no puede modificar la accion en estado rechazado """
        accion_jd01 = self.env['plan_mejoramiento.accion'].sudo(jefe_id).search([])
        try:
            accion_jd01[0].sudo(jefe_id).write({
                'name': "Sobreescribiendo Nombre"
            })
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad Sobreescribir Accion')

        """Se valida que el jefe dependencia no pueda crear tareas cuando la accion se encuentra en el estado rechazado"""
#         try:
#             task = self.env['project.task'].sudo(jefe_id).create({
#                 'name': 'tarea test',
#                 'edt_id': accion_jd01.edt_raiz_id.id,
#                 'user_id': jefe_id,
#                 'reviewer_id': jefe_id,
#              })
#         except AccessError:
#             pass
#         else:
#             self.fail('No se genero Exception de Seguridad Sobreescribir Accion')

        # =====================================================================
        # (3) Estados. de rechazar a pro_aprobar
        accion.sudo(jefe_id).signal_workflow('wkf_rechazado_a_por_aprobar')
        self.assertEqual(accion.state, 'rechazado', 'WKF no cambia por el jefe dependencia')
        accion.sudo(oci_id).signal_workflow('wkf_rechazado_a_por_aprobar')
        self.assertEqual(accion.state, 'por_aprobar', 'WKF ok')
        """Se valida que el jefe dependencia no puede modificar la accion en estado por_aprobar """
        accion_jd01 = self.env['plan_mejoramiento.accion'].sudo(jefe_id).search([])
        try:
            accion_jd01[0].sudo(jefe_id).write({
                'name': "Sobreescribiendo Nombre"
            })
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad Sobreescribir Accion')

        """Se valida que el jefe dependencia no pueda crear tareas cuando la accion se encuentra en el estado por_aprobar"""
#         try:
#             task = self.env['project.task'].sudo(jefe_id).create({
#                 'name': 'tarea test',
#                 'edt_id': accion_jd01.edt_raiz_id.id,
#                 'user_id': jefe_id,
#                 'reviewer_id': jefe_id,
#              })
#         except AccessError:
#             pass
#         else:
#             self.fail('No se genero Exception de Seguridad Sobreescribir Accion')

        # =====================================================================
        # (4) Estados. de pro_aprobar a aprobar
        accion.sudo(oci_id).signal_workflow('wkf_por_aprobar_a_aprobado')
        self.assertEqual(accion.state, 'por_aprobar', 'WKF no cambia por el OCI')
        accion.sudo(jefe_id).signal_workflow('wkf_por_aprobar_a_aprobado')
        self.assertEqual(accion.state, 'aprobado', 'WKF ok')
        """Se valida que el jefe dependencia no puede modificar la accion en estado aprobado """
        accion_jd01 = self.env['plan_mejoramiento.accion'].sudo(jefe_id).search([])
        try:
            accion_jd01[0].sudo(jefe_id).write({
                'name': "Sobreescribiendo Nombre"
            })
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad Sobreescribir Accion')

        """Se valida que el jefe dependencia no pueda crear tareas cuando la accion se encuentra en el estado aprobado"""
#         try:
#             task = self.env['project.task'].sudo(jefe_id).create({
#                 'name': 'tarea test',
#                 'edt_id': accion_jd01.edt_raiz_id.id,
#                 'user_id': jefe_id,
#                 'reviewer_id': jefe_id,
#              })
#         except AccessError:
#             pass
#         else:
#             self.fail('No se genero Exception de Seguridad Sobreescribir Accion')

        # =====================================================================
        # (5) Estados. de aprobado a en_progreso
        accion.sudo(oci).signal_workflow('wkf_aprobado_a_en_progreso')
        self.assertEqual(accion.state, 'aprobado', 'WKF o cambia por el OCI')
        accion.sudo(jefe_id).signal_workflow('wkf_aprobado_a_en_progreso')
        self.assertEqual(accion.state, 'en_progreso', 'WKF ok')
        """Se valida que el jefe dependencia no puede modificar la accion en estado en_progreso """
        accion_jd01 = self.env['plan_mejoramiento.accion'].sudo(jefe_id).search([])
        try:
            accion_jd01[0].sudo(jefe_id).write({
                'name': "Sobreescribiendo Nombre"
            })
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad Sobreescribir Accion')

        """Se valida que el jefe dependencia PUEDA crear tareas cuando la accion se encuentra en el estado en_progreso"""
# FIXME: CMM Revisar porque no deja crear
#         task = self.env['project.task'].sudo(jefe_id).create({
#             'name': 'tarea test',
#             'edt_id': accion_jd01.edt_raiz_id.id,
#             'user_id': jefe_id,
#             'reviewer_id': jefe_id,
#          })

        # =====================================================================
        # (6) Estados. de en_progreso a terminado
        accion.sudo(jefe_id).signal_workflow('wkf_en_progreso_a_terminado')
        self.assertEqual(accion.state, 'en_progreso', 'WKF no cambia por el jefe')
        accion.sudo(oci_id).signal_workflow('wkf_en_progreso_a_terminado')
        self.assertEqual(accion.state, 'terminado', 'WKF ok')
        """Se valida que el jefe dependencia no puede modificar la accion en estado terminado """
        accion_jd01 = self.env['plan_mejoramiento.accion'].sudo(jefe_id).search([])
        try:
            accion_jd01[0].sudo(jefe_id).write({
                'name': "Sobreescribiendo Nombre"
            })
        except AccessError:
            pass
        else:
            self.fail('No se genero Exception de Seguridad Sobreescribir Accion')

        """Se valida que el jefe dependencia no pueda crear tareas cuando la accion se encuentra en el estado terminado"""
#         try:
#             task = self.env['project.task'].sudo(jefe_id).create({
#                 'name': 'tarea test',
#                 'edt_id': accion_jd01.edt_raiz_id.id,
#                 'user_id': jefe_id,
#                 'reviewer_id': jefe_id,
#              })
#         except AccessError:
#             pass
#         else:
#             self.fail('No se genero Exception de Seguridad Sobreescribir Accion')

        _logger.info("***** Fin test_workflow_acciones *****\n")

if __name__ == '__main__':
    unittest2.main()