# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import ValidationError
from datetime import *

logging.basicConfig()
_logger = logging.getLogger('TEST')

class Test_project_edt(common.TransactionCase):
    def test_crud_validaciones(self):
        edt_model = self.env['project.edt']
        vals = {
            'name': "EDT 1",
            'sequence': 1,
            'ms_project_guid': "ms-project-uuid",
            'user_id': self.ref('project_edt_idu.group_project_manager_user_01'),
            'state': "abierto",
            'fecha_planeada_inicio': "2016-01-01",
            'fecha_planeada_fin': "2016-02-01",
            'fecha_inicio': "2016-01-01",
            'fecha_fin': "2016-02-01",
            'costo': 66927115.92,
        }
        edt = edt_model.create(vals)
        # Verificar fecha_planeada es tomada de la fechas asignadas inicialmente
        self.assertEqual(edt.fecha_planeada_inicio, '2016-01-01')
        self.assertEqual(edt.fecha_planeada_fin, '2016-02-01')
        self.assertEqual(edt.fecha_inicio, '2016-01-01')
        self.assertEqual(edt.fecha_fin, '2016-02-01')
        # Verificar Costo Planeado es tomado del Costo inicial
        self.assertEqual(edt.costo_planeado, 0.0)
        self.assertEqual(edt.costo, 66927115.92)

        vals_update = {
            'fecha_inicio': '2016-01-05',
            'fecha_fin': '2016-02-05',
            'costo': 111,
        }
        edt.write(vals_update)
        # Verificar fecha_planeada es tomada de la fechas asignadas inicialmente
        self.assertEqual(edt.fecha_planeada_inicio, '2016-01-01')
        self.assertEqual(edt.fecha_planeada_fin, '2016-02-01')

        # Campos con api.constrain
        vals_update = {
            'fecha_planeada_inicio': '2016-03-01',
        }
        try:
            edt.write(vals_update)
        except ValidationError, e:
            pass
        else:
            self.fail('No se generó exception de validación para "fecha_planeada_inicio"')

        vals_update = {
            'fecha_planeada_fin': '2014-12-01',
        }
        try:
            edt.write(vals_update)
        except ValidationError, e:
            pass
        else:
            self.fail('No se generó exception de validación para "fecha_planeada_fin"')

        vals_update = {
            'fecha_inicio': '2016-03-01',
        }
        try:
            edt.write(vals_update)
        except ValidationError, e:
            pass
        else:
            self.fail('No se generó exception de validación para "fecha_inicio"')

        vals_update = {
            'fecha_fin': '2014-12-01',
        }
        try:
            edt.write(vals_update)
        except ValidationError, e:
            pass
        else:
            self.fail('No se generó exception de validación para "fecha_fin"')

    def test_calcular_duracion_dias(self):
        from openerp.addons.project_edt_idu.models.project import calcular_duracion_en_dias
        from openerp.addons.project_edt_idu.models.project import calcular_duracion_en_dias_fecha_estado
        self.assertEqual(calcular_duracion_en_dias('2016-01-01', '2016-02-10'), 29)
        self.assertEqual(calcular_duracion_en_dias('2016-01-01', '2016-01-09'), 6) # Sabado
        self.assertEqual(calcular_duracion_en_dias('2016-01-01', '2016-01-10'), 6) # Domingo
        self.assertEqual(calcular_duracion_en_dias('2016-01-01', '2016-01-08'), 6) # Viernes
        self.assertEqual(calcular_duracion_en_dias('2016-01-01', '2016-01-11'), 7) # Lunes
        self.assertEqual(calcular_duracion_en_dias('2016-01-01', '2016-01-12'), 8) # Martes

        self.assertEqual(calcular_duracion_en_dias_fecha_estado('2016-01-01', '2016-01-10'), 6) # Domingo
        self.assertEqual(calcular_duracion_en_dias_fecha_estado('2016-01-01', '2016-01-08'), 5) # Viernes
        self.assertEqual(calcular_duracion_en_dias_fecha_estado('2016-01-01', '2016-01-11'), 6) # Lunes
        self.assertEqual(calcular_duracion_en_dias_fecha_estado('2016-01-01', '2016-01-12'), 7) # Martes

    def test_generacion_numero(self):
        return # FIXME: Ajustar la prueba
        edt_model = self.env['project.edt']

        # Carga de numero en la tarea en importacion masiva
        vals = {
            'numero_manual': '1.2.3',
            'name': 'EDT prueba numero',
        }
        edt = edt_model.create(vals)
        self.assertEqual(edt.numero, '1.2.3')

        edt_p = self.browse_ref('project_edt_idu.project_edt_1')
        edt.parent_id = edt_p.id
        self.assertEqual(edt.numero, '1.5')
        self.assertEqual(0, edt.numero.find(edt_p.numero)) # 0 Indica que se encontró al comienzo, -1 no se encontró

        vals = {
            'name': 'EDT prueba numero 3 nivel',
            'parent_id': edt.id,
            'task_ids': [
                (0,0, {
                    'name': 'Prueba numero',
                })
            ]
        }
        edt_3 = edt_model.with_context({'carga_masiva': True}).create(vals)
        edt_p.numero_manual = 'aaa'
        self.assertEqual('aaa', edt_p.numero)
        self.assertEqual('aaa.5', edt.numero)
        self.assertEqual('aaa.5.1', edt_3.numero)
        self.assertEqual('aaa.5.1.1', edt_3.task_ids.numero)
        edt.parent_id = False
        self.assertEqual('1', edt.numero)

    def test_calculo_progreso(self):
        # Condiciones iniciales
        edt_1 = self.browse_ref('project_edt_idu.project_edt_1')
        edt_1_4 = self.browse_ref('project_edt_idu.project_edt_1_4')
        edt_1_4_1 = self.browse_ref('project_edt_idu.project_edt_1_4_1')
        edt_1_4_1_1 = self.browse_ref('project_edt_idu.project_edt_1_4_1_1')
        edt_1_4_1_2 = self.browse_ref('project_edt_idu.project_edt_1_4_1_2')
        edt_1_4_1_3 = self.browse_ref('project_edt_idu.project_edt_1_4_1_3')
        edt_1_4_1_4 = self.browse_ref('project_edt_idu.project_edt_1_4_1_4')
        task_t1 = self.browse_ref('project_edt_idu.project_edt_1_4_1_4_t1')
        task_registro_progreso_model = self.env['project.task.registro_progreso']
        task = self.browse_ref('project_edt_idu.project_edt_1_4_1_4_t1')
        #print "Revisar datos iniciales"
        #print edt_1.numero, edt_1.progreso
        #print edt_1_4.numero, edt_1_4.progreso
        #print edt_1_4_1.numero, edt_1_4_1.progreso
        #print edt_1_4_1_1.numero, edt_1_4_1_1.progreso
        #print edt_1_4_1_2.numero, edt_1_4_1_2.progreso
        #print edt_1_4_1_3.numero, edt_1_4_1_3.progreso
        #print edt_1_4_1_4.numero, edt_1_4_1_4.progreso
        #print task.numero, task.progreso

        self.assertEqual(edt_1.progreso, 27)
        self.assertEqual(edt_1_4.progreso, 47)
        self.assertEqual(edt_1_4_1.progreso, 35)
        self.assertEqual(edt_1_4_1_1.progreso, 40)
        self.assertEqual(edt_1_4_1_2.progreso, 45)
        self.assertEqual(edt_1_4_1_3.progreso, 50)
        self.assertEqual(edt_1_4_1_4.progreso, 4)
        self.assertEqual(task.progreso, 55)
        # Progreso No 1
        vals = {
            'name': "Aut explicabo quae quaerat pariatur.",
            'fecha': date.today(),
            'task_id': task.id,
            'porcentaje': 100,
            'costo': 100,
        }
        task_registro_progreso = task_registro_progreso_model.create(vals)
        #print "revisar al cambiar progreso"
        #print edt_1.numero, edt_1.progreso
        #print edt_1_4.numero, edt_1_4.progreso
        #print edt_1_4_1.numero, edt_1_4_1.progreso
        #print edt_1_4_1_1.numero, edt_1_4_1_1.progreso
        #print edt_1_4_1_2.numero, edt_1_4_1_2.progreso
        #print edt_1_4_1_3.numero, edt_1_4_1_3.progreso
        #print edt_1_4_1_4.numero, edt_1_4_1_4.progreso
        #print task.numero, task.progreso

        self.assertEqual(edt_1.progreso, 27)
        self.assertEqual(edt_1.costo, 100)
        self.assertEqual(edt_1_4.progreso, 48)
        self.assertEqual(edt_1_4_1.progreso, 36)
        self.assertEqual(edt_1_4_1_1.progreso, 40)
        self.assertEqual(edt_1_4_1_2.progreso, 45)
        self.assertEqual(edt_1_4_1_3.progreso, 50)
        self.assertEqual(edt_1_4_1_3.costo, 0)
        self.assertEqual(edt_1_4_1_4.progreso, 8)
        self.assertEqual(edt_1_4_1_4.costo, 100)
        self.assertEqual(task.progreso, 100)
        self.assertEqual(task.costo, 100)

    def test_calculo_costo_planeado_fecha(self):
        # Condiciones iniciales
        edt_1 = self.browse_ref('project_edt_idu.project_edt_1')
        edt_1_4 = self.browse_ref('project_edt_idu.project_edt_1_4')
        edt_1_4_1 = self.browse_ref('project_edt_idu.project_edt_1_4_1')
        edt_1_4_1_1 = self.browse_ref('project_edt_idu.project_edt_1_4_1_1')
        edt_1_4_1_2 = self.browse_ref('project_edt_idu.project_edt_1_4_1_2')
        edt_1_4_1_3 = self.browse_ref('project_edt_idu.project_edt_1_4_1_3')
        edt_1_4_1_4 = self.browse_ref('project_edt_idu.project_edt_1_4_1_4')
        task_t1 = self.browse_ref('project_edt_idu.project_edt_1_4_1_4_t1')
        task_registro_progreso_model = self.env['project.task.registro_progreso']
        task = self.browse_ref('project_edt_idu.project_edt_1_4_1_4_t1')

        self.assertEqual(edt_1.progreso, 27)
        self.assertEqual(edt_1_4.progreso, 47)
        self.assertEqual(edt_1_4_1.progreso, 35)
        self.assertEqual(edt_1_4_1_1.progreso, 40)
        self.assertEqual(edt_1_4_1_2.progreso, 45)
        self.assertEqual(edt_1_4_1_3.progreso, 50)
        self.assertEqual(edt_1_4_1_4.progreso, 4)
        self.assertEqual(edt_1.costo_planeado, 1000)
        self.assertEqual(edt_1_4.costo_planeado, 1000)
        self.assertEqual(edt_1_4_1.costo_planeado, 1000)
        self.assertEqual(edt_1_4_1_1.costo_planeado, 0)
        self.assertEqual(edt_1_4_1_2.costo_planeado, 0)
        self.assertEqual(edt_1_4_1_3.costo_planeado, 0)
        self.assertEqual(edt_1_4_1_4.costo_planeado, 1000)
        self.assertEqual(task.costo_planeado, 1000)

        # Asignar fecha de estado antes de iniciar proyecto
        fecha_estado = '2015-01-01'
        wizard = self.env['project.edt.wizard.fecha_estado'].create({
            'project_id': edt_1.project_id.id,
            'fecha_estado': fecha_estado,
        })
        wizard.actualizar_fecha_estado()

        self.assertEqual(edt_1.costo_planeado_fecha, 0)
        self.assertEqual(edt_1_4.costo_planeado_fecha, 0)
        self.assertEqual(edt_1_4_1.costo_planeado_fecha, 0)
        self.assertEqual(edt_1_4_1_1.costo_planeado_fecha, 0)
        self.assertEqual(edt_1_4_1_2.costo_planeado_fecha, 0)
        self.assertEqual(edt_1_4_1_3.costo_planeado_fecha, 0)
        self.assertEqual(edt_1_4_1_4.costo_planeado_fecha, 0)
        self.assertEqual(task.costo_planeado_fecha, 0)

        # Asignar fecha de estado luego de finalizar proyecto
        fecha_estado = '2018-01-01'
        wizard = self.env['project.edt.wizard.fecha_estado'].create({
            'project_id': edt_1.project_id.id,
            'fecha_estado': fecha_estado,
        })
        wizard.actualizar_fecha_estado()

        self.assertEqual(edt_1.costo_planeado_fecha, 1000)
        self.assertEqual(edt_1_4.costo_planeado_fecha, 1000)
        self.assertEqual(edt_1_4_1.costo_planeado_fecha, 1000)
        self.assertEqual(edt_1_4_1_1.costo_planeado_fecha, 0)
        self.assertEqual(edt_1_4_1_2.costo_planeado_fecha, 0)
        self.assertEqual(edt_1_4_1_3.costo_planeado_fecha, 0)
        self.assertEqual(edt_1_4_1_4.costo_planeado_fecha, 1000)
        self.assertEqual(task.costo_planeado_fecha, 1000)

        # Asignar fecha de estado cuando tarea ya ha terminado
        fecha_estado = '2016-07-10'
        wizard = self.env['project.edt.wizard.fecha_estado'].create({
            'project_id': edt_1.project_id.id,
            'fecha_estado': fecha_estado,
        })
        wizard.actualizar_fecha_estado()

        self.assertEqual(edt_1.costo_planeado_fecha, 1000)
        self.assertEqual(edt_1_4.costo_planeado_fecha, 1000)
        self.assertEqual(edt_1_4_1.costo_planeado_fecha, 1000)
        self.assertEqual(edt_1_4_1_1.costo_planeado_fecha, 0)
        self.assertEqual(edt_1_4_1_2.costo_planeado_fecha, 0)
        self.assertEqual(edt_1_4_1_3.costo_planeado_fecha, 0)
        self.assertEqual(edt_1_4_1_4.costo_planeado_fecha, 1000)
        self.assertEqual(task.costo_planeado_fecha, 1000)

        # Asignar fecha de estado cuando tarea esta en progreso
        fecha_estado = '2016-01-10'
        wizard = self.env['project.edt.wizard.fecha_estado'].create({
            'project_id': edt_1.project_id.id,
            'fecha_estado': fecha_estado,
        })
        wizard.actualizar_fecha_estado()

        self.assertEqual(edt_1.costo_planeado_fecha, 210)
        self.assertEqual(edt_1_4.costo_planeado_fecha, 210)
        self.assertEqual(edt_1_4_1.costo_planeado_fecha, 210)
        self.assertEqual(edt_1_4_1_1.costo_planeado_fecha, 0)
        self.assertEqual(edt_1_4_1_2.costo_planeado_fecha, 0)
        self.assertEqual(edt_1_4_1_3.costo_planeado_fecha, 0)
        self.assertEqual(edt_1_4_1_4.costo_planeado_fecha, 210)
        self.assertEqual(task.costo_planeado_fecha, 210)

    def test_calculo_retraso(self):
        # Condiciones iniciales
        edt_1 = self.browse_ref('project_edt_idu.project_edt_1')
        edt_1_4 = self.browse_ref('project_edt_idu.project_edt_1_4')
        edt_1_4_1 = self.browse_ref('project_edt_idu.project_edt_1_4_1')
        edt_1_4_1_1 = self.browse_ref('project_edt_idu.project_edt_1_4_1_1')
        edt_1_4_1_2 = self.browse_ref('project_edt_idu.project_edt_1_4_1_2')
        edt_1_4_1_3 = self.browse_ref('project_edt_idu.project_edt_1_4_1_3')
        edt_1_4_1_4 = self.browse_ref('project_edt_idu.project_edt_1_4_1_4')
        task_t1 = self.browse_ref('project_edt_idu.project_edt_1_4_1_4_t1')
        task_registro_progreso_model = self.env['project.task.registro_progreso']
        task = self.browse_ref('project_edt_idu.project_edt_1_4_1_4_t1')

        # Asignar fecha de estado
        fecha_estado = '2016-07-10'
        wizard = self.env['project.edt.wizard.fecha_estado'].create({
            'project_id': edt_1.project_id.id,
            'fecha_estado': fecha_estado,
        })
        wizard.actualizar_fecha_estado()
        # Verificar fecha de estado
        self.env.invalidate_all()
        self.assertEqual(edt_1.fecha_estado, fecha_estado)
        self.assertEqual(edt_1_4.fecha_estado, fecha_estado)
        self.assertEqual(edt_1_4_1.fecha_estado, fecha_estado)
        self.assertEqual(edt_1_4_1_1.fecha_estado, fecha_estado)
        self.assertEqual(edt_1_4_1_2.fecha_estado, fecha_estado)
        self.assertEqual(edt_1_4_1_3.fecha_estado, fecha_estado)
        self.assertEqual(edt_1_4_1_4.fecha_estado, fecha_estado)
        self.assertEqual(task.fecha_estado, fecha_estado)

        # Verificar valores esperados de progreso pre cargados con una BD limpia y recien instalada
        self.assertEqual(edt_1.progreso, 27)
        self.assertEqual(edt_1_4.progreso, 47)
        self.assertEqual(edt_1_4_1.progreso, 35)
        self.assertEqual(edt_1_4_1_1.progreso, 40)
        self.assertEqual(edt_1_4_1_2.progreso, 45)
        self.assertEqual(edt_1_4_1_3.progreso, 50)
        self.assertEqual(edt_1_4_1_4.progreso, 4)
        self.assertEqual(task.progreso, 55)

        # Revisar retraso a la fecha de estado definida
        self.assertEqual(edt_1.retraso, 25)
        self.assertEqual(edt_1_4.retraso, 6)
        self.assertEqual(edt_1_4_1.retraso, 19)
        self.assertEqual(edt_1_4_1_1.retraso, 12)
        self.assertEqual(edt_1_4_1_2.retraso, 7)
        self.assertEqual(edt_1_4_1_3.retraso, 2)
        self.assertEqual(edt_1_4_1_4.retraso, 56)
        self.assertEqual(task.retraso, 45)

        # Asignar fecha de estado cuando tarea esta en progreso
        fecha_estado = '2016-01-10'
        wizard = self.env['project.edt.wizard.fecha_estado'].create({
            'project_id': edt_1.project_id.id,
            'fecha_estado': fecha_estado,
        })
        wizard.actualizar_fecha_estado()
        # FIXME: Los valores no estan comparando si el valor del progreso a la fecha de estado es ese,
        # solo lo compara con el progreso actual registrado en el sistema, asi el registro de avance sea a una
        # fecha posterior a la fecha de estado
        self.assertEqual(edt_1.retraso, -25)
        self.assertEqual(edt_1_4.retraso, -45)
        self.assertEqual(edt_1_4_1.retraso, -33)
        self.assertEqual(edt_1_4_1_1.retraso, -38)
        self.assertEqual(edt_1_4_1_2.retraso, -43)
        self.assertEqual(edt_1_4_1_3.retraso, -48)
        self.assertEqual(edt_1_4_1_4.retraso, -2 )
        self.assertEqual(task.retraso, -34)


    def test_calculo_fechas_duracion(self):
        edt_1 = self.browse_ref('project_edt_idu.project_edt_1')
        edt_1_4 = self.browse_ref('project_edt_idu.project_edt_1_4')
        edt_1_4_1 = self.browse_ref('project_edt_idu.project_edt_1_4_1')
        edt_1_4_1_1 = self.browse_ref('project_edt_idu.project_edt_1_4_1_1')
        edt_1_4_1_2 = self.browse_ref('project_edt_idu.project_edt_1_4_1_2')
        edt_1_4_1_3 = self.browse_ref('project_edt_idu.project_edt_1_4_1_3')
        edt_1_4_1_4 = self.browse_ref('project_edt_idu.project_edt_1_4_1_4')
        task_1_4_1_4_t1 = self.browse_ref('project_edt_idu.project_edt_1_4_1_4_t1')
        task_1_4_1_4_t2 = self.browse_ref('project_edt_idu.project_edt_1_4_1_4_t2')
        task_1_4_1_4_t3 = self.browse_ref('project_edt_idu.project_edt_1_4_1_4_t3')
        task_1_4_1_4_t4 = self.browse_ref('project_edt_idu.project_edt_1_4_1_4_t4')
        task_1_4_1_4_t5 = self.browse_ref('project_edt_idu.project_edt_1_4_1_4_t5')

        self.assertEqual(edt_1.fecha_inicio, '2016-01-01')
        self.assertEqual(edt_1.fecha_fin, '2016-12-31')
        self.assertEqual(edt_1.fecha_planeada_inicio, '2016-01-01')
        self.assertEqual(edt_1.fecha_planeada_fin, '2016-12-31')
        self.assertEqual(edt_1_4_1_4.fecha_inicio, '2016-01-01')
        self.assertEqual(edt_1_4_1_4.fecha_fin, '2016-11-11')
        self.assertEqual(edt_1_4_1_4.fecha_planeada_inicio, '2016-01-01')
        self.assertEqual(edt_1_4_1_4.fecha_planeada_fin, '2016-12-31')
        self.assertEqual(edt_1_4_1_4.duracion_dias, 226)
        self.assertEqual(edt_1_4_1_4.duracion_planeada_dias, 261)
        self.assertEqual(task_1_4_1_4_t1.duracion_dias, 29)
        self.assertEqual(task_1_4_1_4_t1.duracion_planeada_dias, 29)
        self.assertEqual(task_1_4_1_4_t2.duracion_dias, 44)
        self.assertEqual(task_1_4_1_4_t2.duracion_planeada_dias, 44)
        self.assertEqual(task_1_4_1_4_t3.duracion_dias, 14)
        self.assertEqual(task_1_4_1_4_t3.duracion_planeada_dias, 14)
        self.assertEqual(task_1_4_1_4_t4.duracion_dias, 43)
        self.assertEqual(task_1_4_1_4_t4.duracion_planeada_dias, 43)
        self.assertEqual(task_1_4_1_4_t5.duracion_dias, 205)
        self.assertEqual(task_1_4_1_4_t5.duracion_planeada_dias, 205)

        task_1_4_1_4_t4.fecha_fin = '2017-02-01'
        self.assertEqual(edt_1_4_1_4.fecha_inicio, '2016-01-01')
        self.assertEqual(edt_1_4_1_4.fecha_fin, '2017-02-01')
        self.assertEqual(edt_1_4_1_4.fecha_planeada_inicio, '2016-01-01')
        self.assertEqual(edt_1_4_1_4.fecha_planeada_fin, '2016-12-31')
        self.assertEqual(edt_1.fecha_inicio, '2016-01-01')
        self.assertEqual(edt_1.fecha_fin, '2017-02-01')
        self.assertEqual(edt_1.fecha_planeada_inicio, '2016-01-01')
        self.assertEqual(edt_1.fecha_planeada_fin, '2016-12-31')


# TODO: Probar Calculo de Progreso aprobado basado en duración
# TODO: Probar Calculo de Progreso aprobado basado en peso
# TODO: Probar Calculo de Progreso aprobado basado en peso y duración
# TODO: Probar Calculo de Costos


if __name__ == '__main__':
    unittest2.main()