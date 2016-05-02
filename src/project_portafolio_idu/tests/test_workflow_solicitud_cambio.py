# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import AccessError

logging.basicConfig()
_logger = logging.getLogger('TEST')

class test_workflow_solicitud_cambio(common.TransactionCase):
    def test_000_solicitud_cambio_01(self):
        """ solicitud_cambio verifica flujo de trabajo"""
        user_project_group_project_user = self.ref('project_portafolio_idu.group_project_user_user_01')
        user_project_edt_idu_group_project_user_externo = self.ref('project_portafolio_idu.group_project_user_externo_user_01')
        user_project_group_project_manager = self.ref('project_portafolio_idu.group_project_manager_user_01')
        user_project_portafolio_idu_group_project_admin = self.ref('project_portafolio_idu.group_project_admin_user_01')
        solicitud_cambio_model = self.env['project.solicitud_cambio']
        solicitud_cambio = solicitud_cambio_model.search([], limit=1)

        # ----------------------------
        # [nuevo] -> [por_revisar]
        # ----------------------------
        self.assertEqual(solicitud_cambio.state, 'nuevo')
        solicitud_cambio.signal_workflow('wkf_nuevo__por_revisar')
        self.assertEqual(solicitud_cambio.state, 'por_revisar')
        self.assertEqual(solicitud_cambio.nombre_campo, 'valor esperado al cambiar de estado')

        # ----------------------------
        # [por_revisar] -> [devuelto]
        # ----------------------------
        self.assertEqual(solicitud_cambio.state, 'por_revisar')
        solicitud_cambio.sudo(GRUPO_SIN_PERMISO).signal_workflow('wkf_por_revisar__devuelto')
        self.assertEqual(solicitud_cambio.state, 'por_revisar')
        solicitud_cambio.sudo(user_project_group_project_manager).signal_workflow('wkf_por_revisar__devuelto')
        self.assertEqual(solicitud_cambio.state, 'devuelto')
        self.assertEqual(solicitud_cambio.nombre_campo, 'valor esperado al cambiar de estado')

        # ----------------------------
        # [devuelto] -> [por_revisar]
        # ----------------------------
        self.assertEqual(solicitud_cambio.state, 'devuelto')
        solicitud_cambio.signal_workflow('wkf_devuelto__por_revisar')
        self.assertEqual(solicitud_cambio.state, 'por_revisar')
        self.assertEqual(solicitud_cambio.nombre_campo, 'valor esperado al cambiar de estado')

        # ----------------------------
        # [por_revisar] -> [aprobado]
        # ----------------------------
        self.assertEqual(solicitud_cambio.state, 'por_revisar')
        solicitud_cambio.sudo(GRUPO_SIN_PERMISO).signal_workflow('wkf_por_revisar__aprobado')
        self.assertEqual(solicitud_cambio.state, 'por_revisar')
        solicitud_cambio.sudo(user_project_group_project_manager).signal_workflow('wkf_por_revisar__aprobado')
        self.assertEqual(solicitud_cambio.state, 'aprobado')
        self.assertEqual(solicitud_cambio.nombre_campo, 'valor esperado al cambiar de estado')


if __name__ == '__main__':
    unittest2.main()