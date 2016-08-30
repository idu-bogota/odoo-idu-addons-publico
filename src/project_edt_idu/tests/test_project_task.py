# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp import fields
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

    def test_funciones_calculo_fechas_duracion(self):
        from ..models.project import calcular_fecha_fin, calcular_fecha_inicio, calcular_duracion_en_dias
        # Calcular la fecha final para una duración de 10 días
        datos_calculo_fecha_final = {
            ('2016-01-22','2016-02-04'), # vie
            ('2016-01-23','2016-02-04'), # sab
            ('2016-01-24','2016-02-04'), # dom
            ('2016-01-09','2016-01-22'), # sab
            ('2016-01-10','2016-01-22'), # dom
            ('2016-01-11','2016-01-22'), # lun festivo
            ('2016-01-12','2016-01-25'), # mar
            ('2016-01-01','2016-01-15'), # vie festivo
        }
        for i in datos_calculo_fecha_final:
            calculado = fields.Date.to_string(calcular_fecha_fin(i[0], 10))
            self.assertEqual(
                calculado, i[1],
                'fecha inicio: {}, fecha fin calculada: {}, fecha fin esperada: {}, duracion: 10d'.format(
                    i[0], calculado, i[1]
                )
            )
            duracion = calcular_duracion_en_dias(i[0], i[1])
            self.assertEqual(duracion, 10,
                'fecha inicio: {}, fecha fin: {}, duracion esperada: 10d, duracion calculada: {}'.format(
                    i[0], i[1], duracion
                )
            )
        ## Calcular fecha inicial para duración de 10d
        datos_calculo_fecha_inicial = {
            ('2015-12-28','2016-01-09'), # sab
            ('2015-12-28','2016-01-10'), # dom
            ('2015-12-28','2016-01-11'), # lun festivo
            ('2015-12-28','2016-01-12'), # mar
            ('2015-12-29','2016-01-13'), # mie
        }
        for i in datos_calculo_fecha_inicial:
            calculado = fields.Date.to_string(calcular_fecha_inicio(i[1], 10))
            self.assertEqual(
                calculado, i[0],
                'fecha fin: {}, fecha inicio calculada: {}, fecha inicio esperada: {}, duracion: 10d'.format(
                    i[1], calculado, i[0]
                )
            )
            duracion = calcular_duracion_en_dias(i[0], i[1])
            self.assertEqual(duracion, 10,
                'fecha inicio: {}, fecha fin: {}, duracion esperada: 10d, duracion calculada: {}'.format(
                    i[0], i[1], duracion
                )
            )
        # Inicio y fin festivo
        duracion = calcular_duracion_en_dias('2016-01-01', '2016-01-11')
        self.assertEqual(duracion, 7)


if __name__ == '__main__':
    unittest2.main()