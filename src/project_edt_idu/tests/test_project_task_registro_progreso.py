# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import ValidationError
from datetime import *

logging.basicConfig()
_logger = logging.getLogger('TEST')

class Test_project_task_registro_progreso(common.TransactionCase):
    def test_crud_validaciones(self):
        task_registro_progreso_model = self.env['project.task.registro_progreso']
        vals = {
            'name': "Aut explicabo quae quaerat pariatur.",
            'fecha': "2016-01-01",
            'task_id': self.ref('project_edt_idu.project_edt_1_4_1_4_t1'),
            'porcentaje': 50,
            'costo': 63022452.0285,
            'nivel_alerta': "bajo",
            'novedad': "Reiciendis occaecati quo veniam voluptatum.",
        }
        task_registro_progreso = task_registro_progreso_model.create(vals)

        # Campos computados

        # Campos con api.constrain
        vals_update = {
            'porcentaje': 101,
        }
        try:
            task_registro_progreso.write(vals_update)
        except ValidationError, e:
            pass
        else:
            self.fail('No se generó exception de validación para "porcentaje"')

        vals_update = {
            'porcentaje': -1,
        }
        try:
            task_registro_progreso.write(vals_update)
        except ValidationError, e:
            pass
        else:
            self.fail('No se generó exception de validación para "porcentaje"')

        vals_update = {
            'costo': -1,
        }
        try:
            task_registro_progreso.write(vals_update)
        except ValidationError, e:
            pass
        else:
            self.fail('No se generó exception de validación para "costo"')

    def test_calculo_progreso(self):
        task_registro_progreso_model = self.env['project.task.registro_progreso']
        # Registro de otra tarea diferente a la que se va a probar
        vals = {
            'name': "Avance a ser ignorado",
            'fecha': "2016-01-01",
            'task_id': self.ref('project_edt_idu.project_edt_2_2_1_t1'),
            'porcentaje': 51,
        }
        task_registro_progreso = task_registro_progreso_model.create(vals)
        # Registro de otra tarea diferente a la que se va a probar
        vals = {
            'name': "Avance a ser ignorado",
            'fecha': "2016-01-01",
            'task_id': self.ref('project_edt_idu.project_edt_2_5_t1'),
            'porcentaje': 52,
            'fecha_aprobacion': '2016-02-01'
        }
        task_registro_progreso = task_registro_progreso_model.create(vals)
        try:
            task_registro_progreso.porcentaje = 10
        except ValidationError, e:
            pass
        else:
            self.fail('No se generó exception de validación al intentar editar un progreso ya aprobado')

        # Tarea para revisar el progreso
        task = self.browse_ref('project_edt_idu.project_edt_1_4_1_4_t1')
        # Progreso No 1
        vals = {
            'name': "Aut explicabo quae quaerat pariatur.",
            'fecha': date.today() + timedelta(days=1),
            'task_id': task.id,
            'porcentaje': 50,
        }
        task_registro_progreso = task_registro_progreso_model.create(vals)
        self.assertEqual(task.progreso, 50)
        self.assertEqual(len(task.registro_progreso_ids), 2)

        # Progreso No 2
        vals = {
            'name': "Aut explicabo quae quaerat pariatur.",
            'fecha': date.today() + timedelta(days=1),
            'task_id': task.id,
            'porcentaje': 40,
        }

        task_registro_progreso_2 = task_registro_progreso_model.create(vals)
        self.assertEqual(task.progreso, 40)
        self.assertEqual(len(task.registro_progreso_ids), 3)

        # Progreso No 3 con fecha en el pasado, deberia ser ignorado
        vals = {
            'name': "Aut explicabo quae quaerat pariatur.",
            'fecha': "2015-12-31",
            'task_id': task.id,
            'porcentaje': 100,
        }
        task_registro_progreso = task_registro_progreso_model.create(vals)
        self.assertEqual(task.progreso, 40)
        self.assertEqual(len(task.registro_progreso_ids), 4)
        # Eliminando el progreso No 2, deberia tomar el progreso No 1
        task_registro_progreso_2.unlink()
        self.assertEqual(task.progreso, 50)
        self.assertEqual(len(task.registro_progreso_ids), 3)

        # Probar colocando el progreso en la tarea
        task.write({'progreso': 90})
        self.assertEqual(task.progreso, 90)
        self.assertEqual(len(task.registro_progreso_ids), 4)


if __name__ == '__main__':
    unittest2.main()