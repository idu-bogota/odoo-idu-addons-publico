# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common

logging.basicConfig()
_logger = logging.getLogger('TEST')


class TestHrEmployee(common.TransactionCase):
    def test_empleado_asignado_a_usuario(self):
        usuario_1 = self.env['res.users'].create({
            'name': 'Josefina Cardenas',
            'login': 'josefina@test.com',
            'employee_id': False,
        })
        self.assertEqual(usuario_1.employee_id.id, False, 'Empleado no asignado')
        empleado_1 = self.env['hr.employee'].create({
            'name': 'Josefina Cardenas',
            'user_id': usuario_1.id,
        })
        self.assertEqual(len(usuario_1.employee_ids), 1, 'Empleado asignado')
        self.assertEqual(usuario_1.employee_id.id, empleado_1.id, 'Empleado asignado')
        empleado_2 = self.env['hr.employee'].create({
            'name': 'Perencejo Perez',
            'user_id': usuario_1.id,
        })
        self.assertEqual(len(usuario_1.employee_ids), 2, 'Empleado asignado')
        self.assertEqual(usuario_1.employee_id.id, empleado_1.id, 'Empleado no debe cambiar')
        try:
            usuario_1.write({
                'employee_id': self.ref('hr.employee')
            })
            raise Exception('Debe lanzarse una excepción, porque solo se permite asignar empleados que estan referenciando al usuario actual')
        except:
            pass
        usuario_1.write({'employee_id': empleado_2.id})
        self.assertEqual(usuario_1.employee_id.id, empleado_2.id, 'Empleado asignado directamente en usuario OK')
        demo_user_id = self.ref('base.user_demo')
        empleado_2.write({'user_id': demo_user_id})
        self.assertEqual(len(usuario_1.employee_ids), 1, 'Empleado des-asignado')
        self.assertEqual(usuario_1.employee_id.id, empleado_1.id, 'Empleado disponible asignado')
        empleado_1.write({'user_id': demo_user_id})
        self.assertEqual(len(usuario_1.employee_ids), 0, 'Empleado des-asignado')
        self.assertEqual(usuario_1.employee_id.id, False, 'No Empleado disponible')
        demo_user = self.browse_ref('base.user_demo')
        self.assertEqual(demo_user.employee_id.id, empleado_2.id, 'Demo user tiene asignado el primer empleado que lo tomó')


if __name__ == '__main__':
    unittest2.main()