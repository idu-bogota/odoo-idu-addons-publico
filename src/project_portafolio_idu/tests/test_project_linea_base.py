# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import ValidationError

logging.basicConfig()
_logger = logging.getLogger('TEST')

class Test_project_linea_base(common.TransactionCase):
    def test_crear_linea_base(self):
        linea_base_model = self.env['project.linea_base']
        linea_base_linea_model = self.env['project.linea_base.linea']
        project = self.browse_ref('project.project_project_data')
        self.assertEqual(len(project.linea_base_ids), 0)
        edt = self.browse_ref('project_edt_idu.project_edt_1_3_2')
        self.assertEqual(len(edt.linea_base_linea_ids), 0)
        task = self.browse_ref('project_edt_idu.project_edt_1_4_1_3_t1')
        self.assertEqual(len(task.linea_base_linea_ids), 0)
        project.crear_linea_base('Prueba')
        # 13 son las tareas que tiene el proyecto por defecto de odoo y que no esta relacionados con la EDT
        cnt_tasks = len(project.task_ids) - 13
        cnt_edt = len(project.edt_ids)
        self.assertEqual(len(project.linea_base_ids), 1)
        self.assertEqual(len(project.snapshot_ids), 0)
        self.assertEqual(project.linea_base_ids.es_snapshot, False)
        self.assertEqual(len(project.linea_base_id.linea_ids), cnt_tasks + cnt_edt)
        edt_lineas = linea_base_linea_model.search([('linea_base_id', '=', project.linea_base_id.id),('res_id','=',edt.id), ('res_model', '=', 'project.edt')])
        self.assertEqual(len(edt_lineas), 1)
        edt.invalidate_cache()
        task.invalidate_cache()
        self.assertEqual(len(edt.linea_base_linea_ids), 1)
        self.assertEqual(edt.progreso_aprobado, edt.linea_base_linea_ids[0].progreso)
        self.assertEqual(len(task.linea_base_linea_ids), 1)
        self.assertEqual(task.progreso_aprobado, task.linea_base_linea_ids[0].progreso)

    def test_crear_snapshot(self):
        linea_base_model = self.env['project.linea_base']
        linea_base_linea_model = self.env['project.linea_base.linea']
        project = self.browse_ref('project.project_project_data')
        self.assertEqual(len(project.linea_base_ids), 0)
        edt = self.browse_ref('project_edt_idu.project_edt_1_3_2')
        self.assertEqual(len(edt.linea_base_linea_ids), 0)
        task = self.browse_ref('project_edt_idu.project_edt_1_4_1_3_t1')
        self.assertEqual(len(task.linea_base_linea_ids), 0)
        project.crear_snapshot('Prueba')
        # 13 son las tareas que tiene el proyecto por defecto de odoo y que no esta relacionados con la EDT
        cnt_tasks = len(project.task_ids) - 13
        cnt_edt = len(project.edt_ids)
        self.assertEqual(len(project.snapshot_ids), 1)
        self.assertEqual(len(project.linea_base_ids), 0)
        self.assertEqual(len(project.snapshot_ids[0].linea_ids), cnt_tasks + cnt_edt)
        edt.invalidate_cache()
        task.invalidate_cache()
        self.assertEqual(len(edt.linea_base_linea_ids), 0)
        self.assertEqual(len(edt.snapshot_linea_ids), 1)
        self.assertEqual(edt.progreso, edt.snapshot_linea_ids[0].progreso)
        self.assertEqual(len(task.linea_base_linea_ids), 0)
        self.assertEqual(len(task.snapshot_linea_ids), 1)
        self.assertEqual(task.progreso, task.snapshot_linea_ids[0].progreso)


if __name__ == '__main__':
    unittest2.main()