# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import ValidationError

logging.basicConfig()
_logger = logging.getLogger('TEST')

class Test_project_project(common.TransactionCase):
    def test_crud_validaciones(self):
        project_model = self.env['project.project']
        vals = {
            'name': 'Mi proyecto',
            'user_id': self.ref('project_edt_idu.group_project_user_user_01'),
            'programador_id': self.ref('project_edt_idu.group_project_user_user_02'),
            'edt_raiz_id': self.ref('project_edt_idu.project_edt_1'),
        }
        project = project_model.create(vals)


if __name__ == '__main__':
    unittest2.main()