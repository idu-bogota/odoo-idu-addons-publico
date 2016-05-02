# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import AccessError

logging.basicConfig()
_logger = logging.getLogger('TEST')

class test_security_project_group_project_admin(common.TransactionCase):
    def test_000_project_group_project_admin_search(self):
        """ project.group_project_admin Verifica reglas de dominio en operación READ """
        user_group_project_admin_01 = self.ref('project_portafolio_idu.group_project_admin_user_01')
        user_group_project_admin_02 = self.ref('project_portafolio_idu.group_project_admin_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        self.assertEqual(1000, programa_model.sudo(user_group_project_admin_01).search_count([]))
        self.assertEqual(1000, programa_model.sudo(user_group_project_admin_02).search_count([]))

        # ----------------------------
        # project.portafolio
        # ----------------------------
        portafolio_model = self.env['project.portafolio']
        self.assertEqual(1000, portafolio_model.sudo(user_group_project_admin_01).search_count([]))
        self.assertEqual(1000, portafolio_model.sudo(user_group_project_admin_02).search_count([]))

        # ----------------------------
        # project.linea_base
        # ----------------------------
        linea_base_model = self.env['project.linea_base']
        self.assertEqual(1000, linea_base_model.sudo(user_group_project_admin_01).search_count([]))
        self.assertEqual(1000, linea_base_model.sudo(user_group_project_admin_02).search_count([]))

        # ----------------------------
        # project.linea_base.linea
        # ----------------------------
        linea_base_linea_model = self.env['project.linea_base.linea']
        self.assertEqual(1000, linea_base_linea_model.sudo(user_group_project_admin_01).search_count([]))
        self.assertEqual(1000, linea_base_linea_model.sudo(user_group_project_admin_02).search_count([]))

        # ----------------------------
        # project.reporte_desempeno
        # ----------------------------
        reporte_desempeno_model = self.env['project.reporte_desempeno']
        self.assertEqual(1000, reporte_desempeno_model.sudo(user_group_project_admin_01).search_count([]))
        self.assertEqual(1000, reporte_desempeno_model.sudo(user_group_project_admin_02).search_count([]))

        # ----------------------------
        # project.reporte_desempeno.valor_ganado
        # ----------------------------
        reporte_desempeno_valor_ganado_model = self.env['project.reporte_desempeno.valor_ganado']
        self.assertEqual(1000, reporte_desempeno_valor_ganado_model.sudo(user_group_project_admin_01).search_count([]))
        self.assertEqual(1000, reporte_desempeno_valor_ganado_model.sudo(user_group_project_admin_02).search_count([]))

        # ----------------------------
        # project.project
        # ----------------------------
        project_model = self.env['project.project']
        self.assertEqual(1000, project_model.sudo(user_group_project_admin_01).search_count([]))
        self.assertEqual(1000, project_model.sudo(user_group_project_admin_02).search_count([]))

        # ----------------------------
        # project.financiacion
        # ----------------------------
        financiacion_model = self.env['project.financiacion']
        self.assertEqual(1000, financiacion_model.sudo(user_group_project_admin_01).search_count([]))
        self.assertEqual(1000, financiacion_model.sudo(user_group_project_admin_02).search_count([]))

        # ----------------------------
        # project.solicitud_cambio
        # ----------------------------
        solicitud_cambio_model = self.env['project.solicitud_cambio']
        self.assertEqual(1000, solicitud_cambio_model.sudo(user_group_project_admin_01).search_count([]))
        self.assertEqual(1000, solicitud_cambio_model.sudo(user_group_project_admin_02).search_count([]))

        # ----------------------------
        # project.task
        # ----------------------------
        task_model = self.env['project.task']
        self.assertEqual(1000, task_model.sudo(user_group_project_admin_01).search_count([]))
        self.assertEqual(1000, task_model.sudo(user_group_project_admin_02).search_count([]))

    def test_010_project_group_project_admin_create(self):
        """ project.group_project_admin Verifica reglas de dominio en operación CREATE """
        user_group_project_admin_01 = self.ref('project_portafolio_idu.group_project_admin_user_01')
        user_group_project_admin_02 = self.ref('project_portafolio_idu.group_project_admin_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        # Creación permitida
        vals = {
            'name': "Architecto neque aut molestiae placeat voluptatem architecto.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Voluptas et nesciunt aliquam nobis quasi sunt.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        programa = programa_model.sudo(user_group_project_admin_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Maxime repellendus rerum minus.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Est nam molestias sunt maxime.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        try:
            programa = programa_model.sudo(user_group_project_admin_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(programa_model))

        # ----------------------------
        # project.portafolio
        # ----------------------------
        portafolio_model = self.env['project.portafolio']
        # Creación permitida
        vals = {
            'name': "Quis cupiditate nisi totam dolore dolorem.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Eum et id culpa ab rem expedita recusandae.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        portafolio = portafolio_model.sudo(user_group_project_admin_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Et eos molestiae molestias quod dolores.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Et ut architecto sed labore qui magni.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        try:
            portafolio = portafolio_model.sudo(user_group_project_admin_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(portafolio_model))

        # ----------------------------
        # project.linea_base
        # ----------------------------
        linea_base_model = self.env['project.linea_base']
        # Creación permitida
        vals = {
            'name': "Dolorem et enim soluta sint illo voluptatem vitae.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Quidem tempore vel est nobis.",
            'active': True,
            'linea_ids': [
                (4, self.ref('project_portafolio_idu.linea_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        linea_base = linea_base_model.sudo(user_group_project_admin_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Odio id sequi provident quis veniam sit.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Quia reiciendis enim doloribus aut placeat ad.",
            'active': True,
            'linea_ids': [
                (4, self.ref('project_portafolio_idu.linea_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        try:
            linea_base = linea_base_model.sudo(user_group_project_admin_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(linea_base_model))

        # ----------------------------
        # project.linea_base.linea
        # ----------------------------
        linea_base_linea_model = self.env['project.linea_base.linea']
        # Creación permitida
        vals = {
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'res_model': "Voluptas nihil consequuntur eum ipsa in.",
            'res_id': 32931853,
            'fecha_inicio': "1991-10-10 20:10:37",
            'fecha_fin': "1971-12-13 17:11:27",
            'progreso': 89652774.5182,
            'costo': 53760552.099,
        }
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_admin_01).create(vals)

        # Creación NO permitida
        vals = {
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'res_model': "Doloremque amet necessitatibus voluptatibus voluptas esse.",
            'res_id': 22766389,
            'fecha_inicio': "1996-01-31 02:07:36",
            'fecha_fin': "1977-01-08 11:19:26",
            'progreso': 66860293.9078,
            'costo': 99154930.7318,
        }
        try:
            linea_base_linea = linea_base_linea_model.sudo(user_group_project_admin_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(linea_base_linea_model))

        # ----------------------------
        # project.reporte_desempeno
        # ----------------------------
        reporte_desempeno_model = self.env['project.reporte_desempeno']
        # Creación permitida
        vals = {
            'name': "Ut atque consequatur fuga consectetur quia quis rerum.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'baseline_id': self.ref('project_portafolio_idu.baseline_id_01'),
            'active': True,
            'fecha': "1971-11-17 21:55:27",
            'descripcion': "Hic fuga vel mollitia eius quidem ut atque.",
        }
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_admin_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Sed sint nihil facilis ut et.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'baseline_id': self.ref('project_portafolio_idu.baseline_id_01'),
            'active': False,
            'fecha': "2001-08-13 19:01:35",
            'descripcion': "Velit possimus sint tempore commodi ullam.",
        }
        try:
            reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_admin_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(reporte_desempeno_model))

        # ----------------------------
        # project.reporte_desempeno.valor_ganado
        # ----------------------------
        reporte_desempeno_valor_ganado_model = self.env['project.reporte_desempeno.valor_ganado']
        # Creación permitida
        vals = {
            'reporte_id': self.ref('project_portafolio_idu.reporte_id_01'),
            'linea_base_linea_id': self.ref('project_portafolio_idu.linea_base_linea_id_01'),
            'planned_complete': 45314731.9276,
            'actual_complete': 49406017.9348,
            'bac': 69155517.0591,
            'ac': 82498546.9208,
            'es': 2069009.40243,
            'at': 26278059.3852,
        }
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_admin_01).create(vals)

        # Creación NO permitida
        vals = {
            'reporte_id': self.ref('project_portafolio_idu.reporte_id_01'),
            'linea_base_linea_id': self.ref('project_portafolio_idu.linea_base_linea_id_01'),
            'planned_complete': 71687777.6952,
            'actual_complete': 14762757.6967,
            'bac': 91564198.2466,
            'ac': 3562166.43178,
            'es': 83507349.1436,
            'at': 32403778.8758,
        }
        try:
            reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_admin_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(reporte_desempeno_valor_ganado_model))

        # ----------------------------
        # project.project
        # ----------------------------
        project_model = self.env['project.project']
        # Creación permitida
        vals = {
            'dependencia_id': self.ref('project_portafolio_idu.dependencia_id_01'),
            'proyecto_tipo': "obra_componente",
        }
        project = project_model.sudo(user_group_project_admin_01).create(vals)

        # Creación NO permitida
        vals = {
            'dependencia_id': self.ref('project_portafolio_idu.dependencia_id_01'),
            'proyecto_tipo': "obra",
        }
        try:
            project = project_model.sudo(user_group_project_admin_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(project_model))

        # ----------------------------
        # project.financiacion
        # ----------------------------
        financiacion_model = self.env['project.financiacion']
        # Creación permitida
        vals = {
            'name': "Aperiam error nesciunt est maiores quas dolor.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 93625167.216,
        }
        financiacion = financiacion_model.sudo(user_group_project_admin_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Ea sed porro neque dolor unde repudiandae.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 64425800.4671,
        }
        try:
            financiacion = financiacion_model.sudo(user_group_project_admin_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(financiacion_model))

        # ----------------------------
        # project.solicitud_cambio
        # ----------------------------
        solicitud_cambio_model = self.env['project.solicitud_cambio']
        # Creación permitida
        vals = {
            'name': "Et expedita et dicta nesciunt.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_admin_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Et officia et nesciunt vero.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        try:
            solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_admin_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(solicitud_cambio_model))

        # ----------------------------
        # project.task
        # ----------------------------
        task_model = self.env['project.task']
        # Creación permitida
        vals = {
            'dependencia_id': self.ref('project_portafolio_idu.dependencia_id_01'),
        }
        task = task_model.sudo(user_group_project_admin_01).create(vals)

        # Creación NO permitida
        vals = {
            'dependencia_id': self.ref('project_portafolio_idu.dependencia_id_01'),
        }
        try:
            task = task_model.sudo(user_group_project_admin_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(task_model))

    def test_020_project_group_project_admin_write(self):
        """ project.group_project_admin Verifica reglas de dominio en operación WRITE """
        user_group_project_admin_01 = self.ref('project_portafolio_idu.group_project_admin_user_01')
        user_group_project_admin_02 = self.ref('project_portafolio_idu.group_project_admin_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        # Actualización permitida
        vals = {
            'name': "Voluptatum quia quia dolorem fugiat.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Est incidunt distinctio tempore aspernatur.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        programa = programa_model.sudo(user_group_project_admin_01).search([], limit=1)
        programa.sudo(user_group_project_admin_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Illo expedita ipsa autem eius.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Ea non et labore qui.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        programa = programa_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            programa.sudo(user_group_project_admin_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(programa_model))

        # ----------------------------
        # project.portafolio
        # ----------------------------
        portafolio_model = self.env['project.portafolio']
        # Actualización permitida
        vals = {
            'name': "Dolorum molestiae nam ad alias.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Et fuga sit soluta est.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        portafolio = portafolio_model.sudo(user_group_project_admin_01).search([], limit=1)
        portafolio.sudo(user_group_project_admin_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Dolor aspernatur qui qui at.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Non aut animi sit autem ut.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        portafolio = portafolio_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            portafolio.sudo(user_group_project_admin_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(portafolio_model))

        # ----------------------------
        # project.linea_base
        # ----------------------------
        linea_base_model = self.env['project.linea_base']
        # Actualización permitida
        vals = {
            'name': "Velit enim animi aut itaque quod eos nihil.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Distinctio dolorem sunt atque temporibus aut eos.",
            'active': False,
            'linea_ids': [
                (4, self.ref('project_portafolio_idu.linea_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        linea_base = linea_base_model.sudo(user_group_project_admin_01).search([], limit=1)
        linea_base.sudo(user_group_project_admin_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Quasi sit nesciunt eligendi soluta distinctio.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Corporis qui qui consequatur iste eos culpa.",
            'active': False,
            'linea_ids': [
                (4, self.ref('project_portafolio_idu.linea_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        linea_base = linea_base_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            linea_base.sudo(user_group_project_admin_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(linea_base_model))

        # ----------------------------
        # project.linea_base.linea
        # ----------------------------
        linea_base_linea_model = self.env['project.linea_base.linea']
        # Actualización permitida
        vals = {
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'res_model': "Consectetur nisi voluptatem sed et aut voluptatem.",
            'res_id': 34478271,
            'fecha_inicio': "1974-07-27 00:10:16",
            'fecha_fin': "2010-11-20 20:58:07",
            'progreso': 53334668.5763,
            'costo': 88922502.2238,
        }
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_admin_01).search([], limit=1)
        linea_base_linea.sudo(user_group_project_admin_01).write(vals)

        # Actualización NO permitida
        vals = {
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'res_model': "Consequatur at sint voluptatum quis.",
            'res_id': 43289984,
            'fecha_inicio': "2010-12-04 06:05:51",
            'fecha_fin': "1979-05-09 18:21:10",
            'progreso': 34563246.5583,
            'costo': 85545378.0221,
        }
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            linea_base_linea.sudo(user_group_project_admin_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(linea_base_linea_model))

        # ----------------------------
        # project.reporte_desempeno
        # ----------------------------
        reporte_desempeno_model = self.env['project.reporte_desempeno']
        # Actualización permitida
        vals = {
            'name': "Molestias hic itaque eos iure nisi.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'baseline_id': self.ref('project_portafolio_idu.baseline_id_01'),
            'active': False,
            'fecha': "1978-04-09 14:24:10",
            'descripcion': "Iste fuga accusantium reprehenderit suscipit quam dolores harum.",
        }
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_admin_01).search([], limit=1)
        reporte_desempeno.sudo(user_group_project_admin_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Et quos deserunt dolorem praesentium ut voluptas aut qui.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'baseline_id': self.ref('project_portafolio_idu.baseline_id_01'),
            'active': True,
            'fecha': "1999-01-22 16:11:11",
            'descripcion': "Consequuntur id eum nostrum qui accusamus quo.",
        }
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            reporte_desempeno.sudo(user_group_project_admin_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(reporte_desempeno_model))

        # ----------------------------
        # project.reporte_desempeno.valor_ganado
        # ----------------------------
        reporte_desempeno_valor_ganado_model = self.env['project.reporte_desempeno.valor_ganado']
        # Actualización permitida
        vals = {
            'reporte_id': self.ref('project_portafolio_idu.reporte_id_01'),
            'linea_base_linea_id': self.ref('project_portafolio_idu.linea_base_linea_id_01'),
            'planned_complete': 80617470.8482,
            'actual_complete': 68005425.0228,
            'bac': 25865840.0793,
            'ac': 23054086.2573,
            'es': 69900220.0088,
            'at': 95096955.7001,
        }
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_admin_01).search([], limit=1)
        reporte_desempeno_valor_ganado.sudo(user_group_project_admin_01).write(vals)

        # Actualización NO permitida
        vals = {
            'reporte_id': self.ref('project_portafolio_idu.reporte_id_01'),
            'linea_base_linea_id': self.ref('project_portafolio_idu.linea_base_linea_id_01'),
            'planned_complete': 95766478.9324,
            'actual_complete': 8085731.49334,
            'bac': 64735666.6553,
            'ac': 29995634.7792,
            'es': 17161369.8829,
            'at': 79979440.9624,
        }
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            reporte_desempeno_valor_ganado.sudo(user_group_project_admin_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(reporte_desempeno_valor_ganado_model))

        # ----------------------------
        # project.project
        # ----------------------------
        project_model = self.env['project.project']
        # Actualización permitida
        vals = {
            'dependencia_id': self.ref('project_portafolio_idu.dependencia_id_01'),
            'proyecto_tipo': "plan_mejoramiento",
        }
        project = project_model.sudo(user_group_project_admin_01).search([], limit=1)
        project.sudo(user_group_project_admin_01).write(vals)

        # Actualización NO permitida
        vals = {
            'dependencia_id': self.ref('project_portafolio_idu.dependencia_id_01'),
            'proyecto_tipo': "obra_componente",
        }
        project = project_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            project.sudo(user_group_project_admin_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(project_model))

        # ----------------------------
        # project.financiacion
        # ----------------------------
        financiacion_model = self.env['project.financiacion']
        # Actualización permitida
        vals = {
            'name': "Rerum ut sunt fugit magni sunt iusto laborum.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 69264528.7197,
        }
        financiacion = financiacion_model.sudo(user_group_project_admin_01).search([], limit=1)
        financiacion.sudo(user_group_project_admin_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Quod iure voluptatem explicabo neque qui tempore sed.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 7438811.22551,
        }
        financiacion = financiacion_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            financiacion.sudo(user_group_project_admin_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(financiacion_model))

        # ----------------------------
        # project.solicitud_cambio
        # ----------------------------
        solicitud_cambio_model = self.env['project.solicitud_cambio']
        # Actualización permitida
        vals = {
            'name': "Suscipit explicabo iste provident vero optio voluptatem odio.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_admin_01).search([], limit=1)
        solicitud_cambio.sudo(user_group_project_admin_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Minima perspiciatis dolor mollitia reprehenderit.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            solicitud_cambio.sudo(user_group_project_admin_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(solicitud_cambio_model))

        # ----------------------------
        # project.task
        # ----------------------------
        task_model = self.env['project.task']
        # Actualización permitida
        vals = {
            'dependencia_id': self.ref('project_portafolio_idu.dependencia_id_01'),
        }
        task = task_model.sudo(user_group_project_admin_01).search([], limit=1)
        task.sudo(user_group_project_admin_01).write(vals)

        # Actualización NO permitida
        vals = {
            'dependencia_id': self.ref('project_portafolio_idu.dependencia_id_01'),
        }
        task = task_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            task.sudo(user_group_project_admin_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(task_model))

    def test_030_project_group_project_admin_unlink(self):
        """ project.group_project_admin Verifica reglas de dominio en operación UNLINK - Delete """
        user_group_project_admin_01 = self.ref('project_portafolio_idu.group_project_admin_user_01')
        user_group_project_admin_02 = self.ref('project_portafolio_idu.group_project_admin_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        # Eliminación permitida
        programa = programa_model.sudo(user_group_project_admin_01).search([], limit=1)
        programa.sudo(user_group_project_admin_01).unlink()

        # Eliminación NO permitida
        programa = programa_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            programa.sudo(user_group_project_admin_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(programa_model))

        # ----------------------------
        # project.portafolio
        # ----------------------------
        portafolio_model = self.env['project.portafolio']
        # Eliminación permitida
        portafolio = portafolio_model.sudo(user_group_project_admin_01).search([], limit=1)
        portafolio.sudo(user_group_project_admin_01).unlink()

        # Eliminación NO permitida
        portafolio = portafolio_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            portafolio.sudo(user_group_project_admin_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(portafolio_model))

        # ----------------------------
        # project.linea_base
        # ----------------------------
        linea_base_model = self.env['project.linea_base']
        # Eliminación permitida
        linea_base = linea_base_model.sudo(user_group_project_admin_01).search([], limit=1)
        linea_base.sudo(user_group_project_admin_01).unlink()

        # Eliminación NO permitida
        linea_base = linea_base_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            linea_base.sudo(user_group_project_admin_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(linea_base_model))

        # ----------------------------
        # project.linea_base.linea
        # ----------------------------
        linea_base_linea_model = self.env['project.linea_base.linea']
        # Eliminación permitida
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_admin_01).search([], limit=1)
        linea_base_linea.sudo(user_group_project_admin_01).unlink()

        # Eliminación NO permitida
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            linea_base_linea.sudo(user_group_project_admin_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(linea_base_linea_model))

        # ----------------------------
        # project.reporte_desempeno
        # ----------------------------
        reporte_desempeno_model = self.env['project.reporte_desempeno']
        # Eliminación permitida
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_admin_01).search([], limit=1)
        reporte_desempeno.sudo(user_group_project_admin_01).unlink()

        # Eliminación NO permitida
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            reporte_desempeno.sudo(user_group_project_admin_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(reporte_desempeno_model))

        # ----------------------------
        # project.reporte_desempeno.valor_ganado
        # ----------------------------
        reporte_desempeno_valor_ganado_model = self.env['project.reporte_desempeno.valor_ganado']
        # Eliminación permitida
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_admin_01).search([], limit=1)
        reporte_desempeno_valor_ganado.sudo(user_group_project_admin_01).unlink()

        # Eliminación NO permitida
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            reporte_desempeno_valor_ganado.sudo(user_group_project_admin_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(reporte_desempeno_valor_ganado_model))

        # ----------------------------
        # project.project
        # ----------------------------
        project_model = self.env['project.project']
        # Eliminación permitida
        project = project_model.sudo(user_group_project_admin_01).search([], limit=1)
        project.sudo(user_group_project_admin_01).unlink()

        # Eliminación NO permitida
        project = project_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            project.sudo(user_group_project_admin_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(project_model))

        # ----------------------------
        # project.financiacion
        # ----------------------------
        financiacion_model = self.env['project.financiacion']
        # Eliminación permitida
        financiacion = financiacion_model.sudo(user_group_project_admin_01).search([], limit=1)
        financiacion.sudo(user_group_project_admin_01).unlink()

        # Eliminación NO permitida
        financiacion = financiacion_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            financiacion.sudo(user_group_project_admin_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(financiacion_model))

        # ----------------------------
        # project.solicitud_cambio
        # ----------------------------
        solicitud_cambio_model = self.env['project.solicitud_cambio']
        # Eliminación permitida
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_admin_01).search([], limit=1)
        solicitud_cambio.sudo(user_group_project_admin_01).unlink()

        # Eliminación NO permitida
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            solicitud_cambio.sudo(user_group_project_admin_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(solicitud_cambio_model))

        # ----------------------------
        # project.task
        # ----------------------------
        task_model = self.env['project.task']
        # Eliminación permitida
        task = task_model.sudo(user_group_project_admin_01).search([], limit=1)
        task.sudo(user_group_project_admin_01).unlink()

        # Eliminación NO permitida
        task = task_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            task.sudo(user_group_project_admin_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(task_model))


if __name__ == '__main__':
    unittest2.main()