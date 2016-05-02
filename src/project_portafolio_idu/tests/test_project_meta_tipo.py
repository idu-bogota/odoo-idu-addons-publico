# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import ValidationError

logging.basicConfig()
_logger = logging.getLogger('TEST')

class Test_project_meta_tipo(common.TransactionCase):
    def test_crud_validaciones(self):
        meta_tipo_model = self.env['project.meta.tipo']
        vals = {
            'name': "Doloribus cum qui voluptas dolorum quia pariatur.",
            'uom_id': self.ref('project_portafolio_idu.uom_id_01'),
        }
        meta_tipo = meta_tipo_model.create(vals)

        # Campos computados

        # Campos con api.constrain


if __name__ == '__main__':
    unittest2.main()