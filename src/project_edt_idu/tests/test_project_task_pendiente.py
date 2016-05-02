# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import ValidationError

logging.basicConfig()
_logger = logging.getLogger('TEST')

class Test_project_task_pendiente(common.TransactionCase):
    def test_crud_validaciones(self):
        task_pendiente_model = self.env['project.task.pendiente']
        vals = {
            'name': "Et velit id repudiandae sit.",
            'sequence': 7,
            'task_id': self.ref('project_edt_idu.project_edt_1_4_1_4_t1'),
            'peso': 1,
            'user_id': self.ref('project_edt_idu.group_project_user_user_01'),
            'fecha_terminacion': "2015-12-09 00:00:00",
            'fecha_aprobacion': "2015-12-19 00:00:00",
        }
        task_pendiente = task_pendiente_model.create(vals)

# TODO: Probar Calculo de Progreso basado pendientes
# TODO: Probar Calculo de Progreso basado pendientes con peso


if __name__ == '__main__':
    unittest2.main()