# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from datetime import date, datetime, timedelta

logging.basicConfig()
_logger = logging.getLogger('TEST')


class TestUserExpiracion(common.TransactionCase):
    def test_res_user_expiracion_cuenta(self):
        mail_message_obj = self.env['mail.message']
        users_obj = self.env['res.users']

        _logger.info("=========================================  Inicio prueba Notificación expiración de cuentas ===========================================")
        fecha_1 = date.today() + timedelta(2)
        fecha_2 = date.today() + timedelta(30)

        us_1 = users_obj.create({
            'name': 'Usuario prueba expiracion 1',
            'login': 'exp1@test.com',
            'employee_id': False,
            'fecha_expiracion': fecha_1.strftime('%Y-%m-%d')
        })
        us_2 = users_obj.create({
            'name': 'Usuario prueba expiracion 2',
            'login': 'exp2@test.com',
            'employee_id': False,
            'fecha_expiracion': fecha_2.strftime('%Y-%m-%d')
        })

        users_obj.expiracion_cuenta(8)      # Con 8 dias deberia tomar solo al us_1 para enviar email

        mail_enviado = mail_message_obj.search([('partner_ids','=',us_1.partner_id.id)])[0]
        partner_mail_enviado_id = mail_enviado.partner_ids[0]


        self.assertEqual(
            partner_mail_enviado_id.id,
            us_1.partner_id.id, 
            'El usuario al que le debió llegar la notificación es: {}'.format(us_1.name)
        )


if __name__ == '__main__':
    unittest2.main()