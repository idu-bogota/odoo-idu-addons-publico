# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import AccessError

logging.basicConfig()
_logger = logging.getLogger('TEST')

class test_workflow_reporte_desempeno(common.TransactionCase):
    def test_000_reporte_desempeno_01(self):
        """ reporte_desempeno verifica flujo de trabajo"""
        user_project_group_project_user = self.ref('project_portafolio_idu.group_project_user_user_01')
        user_project_edt_idu_group_project_user_externo = self.ref('project_portafolio_idu.group_project_user_externo_user_01')
        user_project_group_project_manager = self.ref('project_portafolio_idu.group_project_manager_user_01')
        user_project_portafolio_idu_group_project_admin = self.ref('project_portafolio_idu.group_project_admin_user_01')
        reporte_desempeno_model = self.env['project.reporte_desempeno']
        reporte_desempeno = reporte_desempeno_model.search([], limit=1)

        # ----------------------------
        # [nuevo] -> [por_revisar]
        # ----------------------------
        self.assertEqual(reporte_desempeno.state, 'nuevo')
        reporte_desempeno.signal_workflow('wkf_nuevo__por_revisar')
        self.assertEqual(reporte_desempeno.state, 'por_revisar')
        self.assertEqual(reporte_desempeno.nombre_campo, 'valor esperado al cambiar de estado')

        # ----------------------------
        # [por_revisar] -> [devuelto]
        # ----------------------------
        self.assertEqual(reporte_desempeno.state, 'por_revisar')
        reporte_desempeno.sudo(GRUPO_SIN_PERMISO).signal_workflow('wkf_por_revisar__devuelto')
        self.assertEqual(reporte_desempeno.state, 'por_revisar')
        reporte_desempeno.sudo(user_project_group_project_manager).signal_workflow('wkf_por_revisar__devuelto')
        self.assertEqual(reporte_desempeno.state, 'devuelto')
        self.assertEqual(reporte_desempeno.nombre_campo, 'valor esperado al cambiar de estado')

        # ----------------------------
        # [devuelto] -> [por_revisar]
        # ----------------------------
        self.assertEqual(reporte_desempeno.state, 'devuelto')
        reporte_desempeno.signal_workflow('wkf_devuelto__por_revisar')
        self.assertEqual(reporte_desempeno.state, 'por_revisar')
        self.assertEqual(reporte_desempeno.nombre_campo, 'valor esperado al cambiar de estado')

        # ----------------------------
        # [por_revisar] -> [aprobado]
        # ----------------------------
        self.assertEqual(reporte_desempeno.state, 'por_revisar')
        reporte_desempeno.sudo(GRUPO_SIN_PERMISO).signal_workflow('wkf_por_revisar__aprobado')
        self.assertEqual(reporte_desempeno.state, 'por_revisar')
        reporte_desempeno.sudo(user_project_group_project_manager).signal_workflow('wkf_por_revisar__aprobado')
        self.assertEqual(reporte_desempeno.state, 'aprobado')
        self.assertEqual(reporte_desempeno.nombre_campo, 'valor esperado al cambiar de estado')


if __name__ == '__main__':
    unittest2.main()