# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import ValidationError

logging.basicConfig()
_logger = logging.getLogger('TEST')

class Test_project_task_reporte_avance(common.TransactionCase):
    def test_crud_validaciones(self):
        task_reporte_avance_model = self.env['project.task.reporte_avance']
        vals = {
            'fecha': "1990-06-08",
            'project_id': self.ref('project_edt_idu.project_id_01'),
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "borrador",
            'registro_progreso_ids': [
                (4, self.ref('project_edt_idu.registro_progreso_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        task_reporte_avance = task_reporte_avance_model.create(vals)

        # Campos computados
        vals_update = {
            'fecha': 'Valor a usarse para calculo',
            'user_id': 'Valor a usarse para calculo',
        }
        task_reporte_avance.write(vals_update)
        self.assertEqual(task_reporte_avance.name, 'Valor Esperado')
        vals_update = {
            'registro_progreso_ids': 'Valor a usarse para calculo',
        }
        task_reporte_avance.write(vals_update)
        self.assertEqual(task_reporte_avance.avances_por_revisar, 'Valor Esperado')
        vals_update = {
            'registro_progreso_ids': 'Valor a usarse para calculo',
        }
        task_reporte_avance.write(vals_update)
        self.assertEqual(task_reporte_avance.avances_rechazados, 'Valor Esperado')
        vals_update = {
            'registro_progreso_ids': 'Valor a usarse para calculo',
        }
        task_reporte_avance.write(vals_update)
        self.assertEqual(task_reporte_avance.avances_aprobados, 'Valor Esperado')

        # Campos con api.constrain
        vals_update = {
            'fecha': 'Valor a usarse para romper la validación',
        }
        try:
            task_reporte_avance.write(vals_update)
        except ValidationError, e:
            pass
        else:
            self.fail('No se generó exception de validación para "fecha"')


if __name__ == '__main__':
    unittest2.main()