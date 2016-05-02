# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import AccessError

logging.basicConfig()
_logger = logging.getLogger('TEST')

class test_security_project_group_project_user_externo(common.TransactionCase):
    def test_000_project_group_project_user_externo_search(self):
        """ project.group_project_user_externo Verifica reglas de dominio en operación READ """
        user_group_project_user_externo_01 = self.ref('project_portafolio_idu.group_project_user_externo_user_01')
        user_group_project_user_externo_02 = self.ref('project_portafolio_idu.group_project_user_externo_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        self.assertEqual(1000, programa_model.sudo(user_group_project_user_externo_01).search_count([]))
        self.assertEqual(1000, programa_model.sudo(user_group_project_user_externo_02).search_count([]))

        # ----------------------------
        # project.portafolio
        # ----------------------------
        portafolio_model = self.env['project.portafolio']
        self.assertEqual(1000, portafolio_model.sudo(user_group_project_user_externo_01).search_count([]))
        self.assertEqual(1000, portafolio_model.sudo(user_group_project_user_externo_02).search_count([]))

        # ----------------------------
        # project.linea_base
        # ----------------------------
        linea_base_model = self.env['project.linea_base']
        self.assertEqual(1000, linea_base_model.sudo(user_group_project_user_externo_01).search_count([]))
        self.assertEqual(1000, linea_base_model.sudo(user_group_project_user_externo_02).search_count([]))

        # ----------------------------
        # project.linea_base.linea
        # ----------------------------
        linea_base_linea_model = self.env['project.linea_base.linea']
        self.assertEqual(1000, linea_base_linea_model.sudo(user_group_project_user_externo_01).search_count([]))
        self.assertEqual(1000, linea_base_linea_model.sudo(user_group_project_user_externo_02).search_count([]))

        # ----------------------------
        # project.reporte_desempeno
        # ----------------------------
        reporte_desempeno_model = self.env['project.reporte_desempeno']
        self.assertEqual(1000, reporte_desempeno_model.sudo(user_group_project_user_externo_01).search_count([]))
        self.assertEqual(1000, reporte_desempeno_model.sudo(user_group_project_user_externo_02).search_count([]))

        # ----------------------------
        # project.reporte_desempeno.valor_ganado
        # ----------------------------
        reporte_desempeno_valor_ganado_model = self.env['project.reporte_desempeno.valor_ganado']
        self.assertEqual(1000, reporte_desempeno_valor_ganado_model.sudo(user_group_project_user_externo_01).search_count([]))
        self.assertEqual(1000, reporte_desempeno_valor_ganado_model.sudo(user_group_project_user_externo_02).search_count([]))

        # ----------------------------
        # project.project
        # ----------------------------
        project_model = self.env['project.project']
        self.assertEqual(1000, project_model.sudo(user_group_project_user_externo_01).search_count([]))
        self.assertEqual(1000, project_model.sudo(user_group_project_user_externo_02).search_count([]))

        # ----------------------------
        # project.financiacion
        # ----------------------------
        financiacion_model = self.env['project.financiacion']
        self.assertEqual(1000, financiacion_model.sudo(user_group_project_user_externo_01).search_count([]))
        self.assertEqual(1000, financiacion_model.sudo(user_group_project_user_externo_02).search_count([]))

        # ----------------------------
        # project.solicitud_cambio
        # ----------------------------
        solicitud_cambio_model = self.env['project.solicitud_cambio']
        self.assertEqual(1000, solicitud_cambio_model.sudo(user_group_project_user_externo_01).search_count([]))
        self.assertEqual(1000, solicitud_cambio_model.sudo(user_group_project_user_externo_02).search_count([]))

        # ----------------------------
        # project.task
        # ----------------------------
        task_model = self.env['project.task']
        self.assertEqual(1000, task_model.sudo(user_group_project_user_externo_01).search_count([]))
        self.assertEqual(1000, task_model.sudo(user_group_project_user_externo_02).search_count([]))

    def test_010_project_group_project_user_externo_create(self):
        """ project.group_project_user_externo Verifica reglas de dominio en operación CREATE """
        user_group_project_user_externo_01 = self.ref('project_portafolio_idu.group_project_user_externo_user_01')
        user_group_project_user_externo_02 = self.ref('project_portafolio_idu.group_project_user_externo_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        # Creación permitida
        vals = {
            'name': "Iste odit facilis eum enim.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Repellendus nemo voluptatibus voluptatem voluptatibus.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        programa = programa_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Explicabo quaerat facilis ipsam maxime laboriosam laborum ullam.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Molestiae sed sint harum et.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        try:
            programa = programa_model.sudo(user_group_project_user_externo_01).create(vals)
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
            'name': "Officia magni et laboriosam vero autem.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Aut possimus voluptatem aut animi fugit.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        portafolio = portafolio_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Velit eos aut quaerat doloribus consequatur ut magni.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Sequi non non inventore tempora aut esse.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        try:
            portafolio = portafolio_model.sudo(user_group_project_user_externo_01).create(vals)
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
            'name': "Aut nam aliquam culpa soluta rerum.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Dolores incidunt ut quia necessitatibus nihil expedita.",
            'active': False,
            'linea_ids': [
                (4, self.ref('project_portafolio_idu.linea_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        linea_base = linea_base_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Tenetur aut et reprehenderit alias accusamus.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Voluptatem aut at sit dolorum repellat.",
            'active': True,
            'linea_ids': [
                (4, self.ref('project_portafolio_idu.linea_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        try:
            linea_base = linea_base_model.sudo(user_group_project_user_externo_01).create(vals)
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
            'res_model': "Et voluptates velit et quis eveniet inventore.",
            'res_id': 70043057,
            'fecha_inicio': "1984-10-05 02:19:09",
            'fecha_fin': "2005-11-13 22:58:39",
            'progreso': 91418132.2769,
            'costo': 89379767.4794,
        }
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'res_model': "Rerum est vel odit voluptates.",
            'res_id': 56678265,
            'fecha_inicio': "2006-10-20 21:57:20",
            'fecha_fin': "1987-01-23 09:00:48",
            'progreso': 53634973.9849,
            'costo': 11572003.7052,
        }
        try:
            linea_base_linea = linea_base_linea_model.sudo(user_group_project_user_externo_01).create(vals)
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
            'name': "Modi ipsum beatae est in a libero.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'baseline_id': self.ref('project_portafolio_idu.baseline_id_01'),
            'active': True,
            'fecha': "1984-03-16 09:03:06",
            'descripcion': "Nisi ea ullam omnis non libero.",
        }
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Est vitae aspernatur quos quas qui.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'baseline_id': self.ref('project_portafolio_idu.baseline_id_01'),
            'active': False,
            'fecha': "1990-07-22 13:20:07",
            'descripcion': "Doloribus nesciunt dignissimos autem consequuntur dolorem sit.",
        }
        try:
            reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_user_externo_01).create(vals)
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
            'planned_complete': 71825601.8629,
            'actual_complete': 90919567.5645,
            'bac': 26185823.6141,
            'ac': 10302610.2482,
            'es': 31975585.1292,
            'at': 88217567.7997,
        }
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'reporte_id': self.ref('project_portafolio_idu.reporte_id_01'),
            'linea_base_linea_id': self.ref('project_portafolio_idu.linea_base_linea_id_01'),
            'planned_complete': 44161214.7288,
            'actual_complete': 36654667.2779,
            'bac': 9731882.32718,
            'ac': 83404960.7965,
            'es': 85906708.3894,
            'at': 73319166.0167,
        }
        try:
            reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_user_externo_01).create(vals)
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
            'proyecto_tipo': "obra",
        }
        project = project_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'dependencia_id': self.ref('project_portafolio_idu.dependencia_id_01'),
            'proyecto_tipo': "plan_mejoramiento",
        }
        try:
            project = project_model.sudo(user_group_project_user_externo_01).create(vals)
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
            'name': "Et nobis eligendi accusantium cupiditate.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 71893224.876,
        }
        financiacion = financiacion_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "In ex quos et quidem enim adipisci.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 70324954.6234,
        }
        try:
            financiacion = financiacion_model.sudo(user_group_project_user_externo_01).create(vals)
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
            'name': "Ad et molestiae ducimus nemo non rem dolorem.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Laudantium animi vitae corporis est eveniet porro suscipit.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        try:
            solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_user_externo_01).create(vals)
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
        task = task_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'dependencia_id': self.ref('project_portafolio_idu.dependencia_id_01'),
        }
        try:
            task = task_model.sudo(user_group_project_user_externo_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(task_model))

    def test_020_project_group_project_user_externo_write(self):
        """ project.group_project_user_externo Verifica reglas de dominio en operación WRITE """
        user_group_project_user_externo_01 = self.ref('project_portafolio_idu.group_project_user_externo_user_01')
        user_group_project_user_externo_02 = self.ref('project_portafolio_idu.group_project_user_externo_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        # Actualización permitida
        vals = {
            'name': "Non unde non voluptatem est in dolores nesciunt.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Consectetur hic mollitia quia dolorum quam unde aperiam sint.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        programa = programa_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        programa.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Libero magni adipisci qui officiis ducimus.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Consequatur voluptas et excepturi rem sapiente.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        programa = programa_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            programa.sudo(user_group_project_user_externo_01).write(vals)
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
            'name': "Ratione hic blanditiis reiciendis.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Sed aspernatur expedita iste qui.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        portafolio = portafolio_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        portafolio.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Esse reprehenderit aut recusandae dicta quis ullam ut.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "A et esse ut vitae suscipit ullam suscipit.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        portafolio = portafolio_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            portafolio.sudo(user_group_project_user_externo_01).write(vals)
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
            'name': "Officiis impedit quos aut odio.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Soluta dolores delectus numquam occaecati quisquam.",
            'active': False,
            'linea_ids': [
                (4, self.ref('project_portafolio_idu.linea_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        linea_base = linea_base_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        linea_base.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Sunt aperiam et ullam quia mollitia consectetur esse blanditiis.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Est tempore dolorem eum occaecati ad.",
            'active': True,
            'linea_ids': [
                (4, self.ref('project_portafolio_idu.linea_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        linea_base = linea_base_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            linea_base.sudo(user_group_project_user_externo_01).write(vals)
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
            'res_model': "Doloribus tempora consequatur quo ea aspernatur velit.",
            'res_id': 14738394,
            'fecha_inicio': "1995-06-15 13:01:53",
            'fecha_fin': "1978-11-16 11:22:17",
            'progreso': 37214552.0731,
            'costo': 30277433.0564,
        }
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        linea_base_linea.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'res_model': "Dolorem eum quis dolorem omnis et.",
            'res_id': 95394615,
            'fecha_inicio': "2015-09-02 00:15:36",
            'fecha_fin': "2014-06-03 18:32:09",
            'progreso': 2883014.72626,
            'costo': 60060088.4289,
        }
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            linea_base_linea.sudo(user_group_project_user_externo_01).write(vals)
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
            'name': "Iste illo aut nihil non.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'baseline_id': self.ref('project_portafolio_idu.baseline_id_01'),
            'active': True,
            'fecha': "1974-05-28 23:39:07",
            'descripcion': "Error et quia qui et exercitationem quasi voluptas.",
        }
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        reporte_desempeno.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Veniam perferendis qui maiores.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'baseline_id': self.ref('project_portafolio_idu.baseline_id_01'),
            'active': True,
            'fecha': "1970-11-21 23:05:55",
            'descripcion': "Harum voluptatem ab placeat.",
        }
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            reporte_desempeno.sudo(user_group_project_user_externo_01).write(vals)
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
            'planned_complete': 67857288.751,
            'actual_complete': 99237762.2006,
            'bac': 81761515.8449,
            'ac': 34400135.6066,
            'es': 7723185.43876,
            'at': 86304129.2765,
        }
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        reporte_desempeno_valor_ganado.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'reporte_id': self.ref('project_portafolio_idu.reporte_id_01'),
            'linea_base_linea_id': self.ref('project_portafolio_idu.linea_base_linea_id_01'),
            'planned_complete': 4773614.04444,
            'actual_complete': 58241286.9807,
            'bac': 90539676.2344,
            'ac': 24161584.6642,
            'es': 42142227.7695,
            'at': 83125783.7239,
        }
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            reporte_desempeno_valor_ganado.sudo(user_group_project_user_externo_01).write(vals)
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
            'proyecto_tipo': "obra_etapa",
        }
        project = project_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        project.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'dependencia_id': self.ref('project_portafolio_idu.dependencia_id_01'),
            'proyecto_tipo': "obra",
        }
        project = project_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            project.sudo(user_group_project_user_externo_01).write(vals)
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
            'name': "Et asperiores quibusdam qui cum delectus sit.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 88014305.5842,
        }
        financiacion = financiacion_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        financiacion.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Vel eum excepturi animi sint adipisci.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 37654720.9972,
        }
        financiacion = financiacion_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            financiacion.sudo(user_group_project_user_externo_01).write(vals)
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
            'name': "Voluptas voluptas reprehenderit ut voluptatem et.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        solicitud_cambio.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Pariatur porro eveniet iste.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            solicitud_cambio.sudo(user_group_project_user_externo_01).write(vals)
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
        task = task_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        task.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'dependencia_id': self.ref('project_portafolio_idu.dependencia_id_01'),
        }
        task = task_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            task.sudo(user_group_project_user_externo_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(task_model))

    def test_030_project_group_project_user_externo_unlink(self):
        """ project.group_project_user_externo Verifica reglas de dominio en operación UNLINK - Delete """
        user_group_project_user_externo_01 = self.ref('project_portafolio_idu.group_project_user_externo_user_01')
        user_group_project_user_externo_02 = self.ref('project_portafolio_idu.group_project_user_externo_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        # Eliminación permitida
        programa = programa_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        programa.sudo(user_group_project_user_externo_01).unlink()

        # Eliminación NO permitida
        programa = programa_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            programa.sudo(user_group_project_user_externo_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(programa_model))

        # ----------------------------
        # project.portafolio
        # ----------------------------
        portafolio_model = self.env['project.portafolio']
        # Eliminación permitida
        portafolio = portafolio_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        portafolio.sudo(user_group_project_user_externo_01).unlink()

        # Eliminación NO permitida
        portafolio = portafolio_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            portafolio.sudo(user_group_project_user_externo_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(portafolio_model))

        # ----------------------------
        # project.linea_base
        # ----------------------------
        linea_base_model = self.env['project.linea_base']
        # Eliminación permitida
        linea_base = linea_base_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        linea_base.sudo(user_group_project_user_externo_01).unlink()

        # Eliminación NO permitida
        linea_base = linea_base_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            linea_base.sudo(user_group_project_user_externo_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(linea_base_model))

        # ----------------------------
        # project.linea_base.linea
        # ----------------------------
        linea_base_linea_model = self.env['project.linea_base.linea']
        # Eliminación permitida
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        linea_base_linea.sudo(user_group_project_user_externo_01).unlink()

        # Eliminación NO permitida
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            linea_base_linea.sudo(user_group_project_user_externo_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(linea_base_linea_model))

        # ----------------------------
        # project.reporte_desempeno
        # ----------------------------
        reporte_desempeno_model = self.env['project.reporte_desempeno']
        # Eliminación permitida
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        reporte_desempeno.sudo(user_group_project_user_externo_01).unlink()

        # Eliminación NO permitida
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            reporte_desempeno.sudo(user_group_project_user_externo_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(reporte_desempeno_model))

        # ----------------------------
        # project.reporte_desempeno.valor_ganado
        # ----------------------------
        reporte_desempeno_valor_ganado_model = self.env['project.reporte_desempeno.valor_ganado']
        # Eliminación permitida
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        reporte_desempeno_valor_ganado.sudo(user_group_project_user_externo_01).unlink()

        # Eliminación NO permitida
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            reporte_desempeno_valor_ganado.sudo(user_group_project_user_externo_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(reporte_desempeno_valor_ganado_model))

        # ----------------------------
        # project.project
        # ----------------------------
        project_model = self.env['project.project']
        # Eliminación permitida
        project = project_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        project.sudo(user_group_project_user_externo_01).unlink()

        # Eliminación NO permitida
        project = project_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            project.sudo(user_group_project_user_externo_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(project_model))

        # ----------------------------
        # project.financiacion
        # ----------------------------
        financiacion_model = self.env['project.financiacion']
        # Eliminación permitida
        financiacion = financiacion_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        financiacion.sudo(user_group_project_user_externo_01).unlink()

        # Eliminación NO permitida
        financiacion = financiacion_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            financiacion.sudo(user_group_project_user_externo_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(financiacion_model))

        # ----------------------------
        # project.solicitud_cambio
        # ----------------------------
        solicitud_cambio_model = self.env['project.solicitud_cambio']
        # Eliminación permitida
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        solicitud_cambio.sudo(user_group_project_user_externo_01).unlink()

        # Eliminación NO permitida
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            solicitud_cambio.sudo(user_group_project_user_externo_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(solicitud_cambio_model))

        # ----------------------------
        # project.task
        # ----------------------------
        task_model = self.env['project.task']
        # Eliminación permitida
        task = task_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        task.sudo(user_group_project_user_externo_01).unlink()

        # Eliminación NO permitida
        task = task_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            task.sudo(user_group_project_user_externo_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(task_model))


if __name__ == '__main__':
    unittest2.main()