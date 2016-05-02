# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import ValidationError

logging.basicConfig()
_logger = logging.getLogger('TEST')

class Test_project_predecesor(common.TransactionCase):
    def test_crud_validaciones(self):
        predecesor_model = self.env['project.predecesor']
        vals = {
            'origen_res_model': "edt",
            'origen_res_id': self.ref('project_edt_idu.project_edt_2_3_1_1'),
            'destino_res_model': "tarea",
            'destino_res_id': self.ref('project_edt_idu.project_edt_2_5_t1'),
            'tipo': "e_s",
        }
        predecesor = predecesor_model.create(vals)

        # Campos computados
        vals_update = {
            'origen_res_id': self.ref('project_edt_idu.project_edt_2_3_1_2'),
        }
        predecesor.write(vals_update)
        self.assertTrue(predecesor.name)
        self.assertTrue(predecesor.progreso)

#TODO: Probar que se envie notificación al terminar una predecesora

if __name__ == '__main__':
    unittest2.main()