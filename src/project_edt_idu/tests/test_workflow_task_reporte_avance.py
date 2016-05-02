# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import AccessError

logging.basicConfig()
_logger = logging.getLogger('TEST')

class test_workflow_task_reporte_avance(common.TransactionCase):
    def test_000_task_reporte_avance_01(self):
        """ task_reporte_avance verifica flujo de trabajo"""
        user_project_group_project_user = self.ref('project_edt_idu.group_project_user_user_01')
        user_project_edt_idu_group_project_user_externo = self.ref('project_edt_idu.group_project_user_externo_user_01')
        user_project_group_project_manager = self.ref('project_edt_idu.group_project_manager_user_01')
        task_reporte_avance_model = self.env['project.task.reporte_avance']
        task_reporte_avance = task_reporte_avance_model.search([], limit=1)

        # ----------------------------
        # [borrador] -> [por_revisar]
        # ----------------------------
        self.assertEqual(task_reporte_avance.state, 'borrador')
        task_reporte_avance.sudo(GRUPO_SIN_PERMISO).signal_workflow('wkf_borrador__por_revisar')
        self.assertEqual(task_reporte_avance.state, 'borrador')
        task_reporte_avance.sudo(user_project_group_project_user).signal_workflow('wkf_borrador__por_revisar')
        self.assertEqual(task_reporte_avance.state, 'por_revisar')
        self.assertEqual(task_reporte_avance.nombre_campo, 'valor esperado al cambiar de estado')

        # ----------------------------
        # [por_revisar] -> [terminado]
        # ----------------------------
        self.assertEqual(task_reporte_avance.state, 'por_revisar')
        task_reporte_avance.sudo(GRUPO_SIN_PERMISO).signal_workflow('wkf_por_revisar__terminado')
        self.assertEqual(task_reporte_avance.state, 'por_revisar')
        task_reporte_avance.sudo(user_project_group_project_user).signal_workflow('wkf_por_revisar__terminado')
        self.assertEqual(task_reporte_avance.state, 'terminado')
        self.assertEqual(task_reporte_avance.nombre_campo, 'valor esperado al cambiar de estado')


if __name__ == '__main__':
    unittest2.main()