# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import ValidationError
from datetime import *

logging.basicConfig()
_logger = logging.getLogger('TEST')

class Test_project_task(common.TransactionCase):
    def test_crud_validaciones(self):
        task_model = self.env['project.task']
        vals = {
            'name': 'Tarea Prueba',
            'edt_id': self.ref('project_edt_idu.project_edt_1'),
            'ms_project_guid': "ms-project-uuid-task",
            'costo': 35191515.05,
            'progreso_metodo': "manual",
            'fecha_planeada_inicio': "2016-01-01",
            'fecha_planeada_fin': "2016-02-01",
            'fecha_inicio': "2016-01-01",
            'fecha_fin': "2016-02-01",
            'cantidad': 280851,
        }
        task = task_model.with_context({'carga_masiva': True}).create(vals)
        self.assertEqual(task.fecha_planeada_inicio, '2016-01-01')
        self.assertEqual(task.fecha_planeada_fin, '2016-02-01')
        self.assertEqual(task.costo_planeado, 0)
        self.assertEqual(task.cantidad_planeada, 0)

        vals_update = {
            'fecha_inicio': '2016-01-05',
            'fecha_fin': '2016-02-05',
            'costo': 111,
            'cantidad': 23454,
        }
        task.write(vals_update)

        # Campos con api.constrain
        vals_update = {
            'fecha_planeada_inicio': '2016-05-01',
        }
        try:
            task.write(vals_update)
        except ValidationError, e:
            pass
        else:
            self.fail('No se generó exception de validación para "fecha_planeada_inicio"')

        vals_update = {
            'fecha_planeada_fin': '2015-05-01',
        }
        try:
            task.write(vals_update)
        except ValidationError, e:
            pass
        else:
            self.fail('No se generó exception de validación para "fecha_planeada_fin"')


    def test_generacion_numero(self):
        return # FIXME: Corregir prueba
        task_model = self.env['project.task']

        # Carga de numero en la tarea en importacion masiva
        vals = {
            'numero': '1.2.3',
            'name': 'Tarea prueba numero',
        }
        task = task_model.with_context({'carga_masiva': True, 'numero': '1.4.1'}).create(vals)
        self.assertEqual(task.numero, '1.4.1') # el valor en la creación lo ignora NPI
        task.numero = '123'
        self.assertEqual(task.numero, '123')

        edt = self.browse_ref('project_edt_idu.project_edt_1')
        task.edt_id = edt.id
        self.assertEqual(0, task.numero.find(edt.numero)) # 0 Indica que se encontró al comienzo, -1 no se encontró
        task.with_context({}).edt_id = False # Se limpia el contexto que se adicionó al crear la tarea
        self.assertEqual(str(task.id), task.numero)

    def test_calculo_retraso(self):
        task_model = self.env['project.task']
        vals = {
            'name': 'Tarea en progreso',
            'fecha_planeada_inicio': '2016-02-01',
            'fecha_planeada_fin': '2016-02-15',
            'fecha_estado': '2016-02-01',
            'progreso': 10,
        }
        task = task_model.create(vals)
        self.assertEqual(task.progreso, 10)
        self.assertEqual(task.retraso, -10)

        vals = {
            'name': 'Tarea en progreso',
            'fecha_planeada_inicio': '2016-02-01',
            'fecha_planeada_fin': '2016-02-15',
            'fecha_estado': '2016-02-10',
            'progreso': 10,
        }
        task = task_model.create(vals)
        self.assertEqual(task.progreso, 10)
        self.assertEqual(task.retraso, 54)

        vals = {
            'name': 'Tarea deberia estar terminada',
            'fecha_planeada_inicio': '2016-01-01',
            'fecha_planeada_fin': '2016-01-05',
            'fecha_estado': '2016-02-10',
            'progreso': 10,
        }
        task = task_model.create(vals)
        self.assertEqual(task.retraso, 90)

        vals = {
            'name': 'Tarea no deberia haber iniciado',
            'fecha_planeada_inicio': '2016-03-01',
            'fecha_planeada_fin': '2016-03-15',
            'fecha_estado': '2016-02-15',
            'progreso': 10,
        }
        task = task_model.create(vals)
        self.assertEqual(task.retraso, -10)


if __name__ == '__main__':
    unittest2.main()