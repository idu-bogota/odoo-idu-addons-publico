# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import AccessError

logging.basicConfig()
_logger = logging.getLogger('TEST')

class test_security_project_group_project_manager(common.TransactionCase):
    def test_000_project_group_project_manager_search(self):
        """ project.group_project_manager Verifica reglas de dominio en operación READ """
        user_group_project_manager_01 = self.ref('project_portafolio_idu.group_project_manager_user_01')
        user_group_project_manager_02 = self.ref('project_portafolio_idu.group_project_manager_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        self.assertEqual(1000, programa_model.sudo(user_group_project_manager_01).search_count([]))
        self.assertEqual(1000, programa_model.sudo(user_group_project_manager_02).search_count([]))

        # ----------------------------
        # project.portafolio
        # ----------------------------
        portafolio_model = self.env['project.portafolio']
        self.assertEqual(1000, portafolio_model.sudo(user_group_project_manager_01).search_count([]))
        self.assertEqual(1000, portafolio_model.sudo(user_group_project_manager_02).search_count([]))

        # ----------------------------
        # project.linea_base
        # ----------------------------
        linea_base_model = self.env['project.linea_base']
        self.assertEqual(1000, linea_base_model.sudo(user_group_project_manager_01).search_count([]))
        self.assertEqual(1000, linea_base_model.sudo(user_group_project_manager_02).search_count([]))

        # ----------------------------
        # project.linea_base.linea
        # ----------------------------
        linea_base_linea_model = self.env['project.linea_base.linea']
        self.assertEqual(1000, linea_base_linea_model.sudo(user_group_project_manager_01).search_count([]))
        self.assertEqual(1000, linea_base_linea_model.sudo(user_group_project_manager_02).search_count([]))

        # ----------------------------
        # project.reporte_desempeno
        # ----------------------------
        reporte_desempeno_model = self.env['project.reporte_desempeno']
        self.assertEqual(1000, reporte_desempeno_model.sudo(user_group_project_manager_01).search_count([]))
        self.assertEqual(1000, reporte_desempeno_model.sudo(user_group_project_manager_02).search_count([]))

        # ----------------------------
        # project.reporte_desempeno.valor_ganado
        # ----------------------------
        reporte_desempeno_valor_ganado_model = self.env['project.reporte_desempeno.valor_ganado']
        self.assertEqual(1000, reporte_desempeno_valor_ganado_model.sudo(user_group_project_manager_01).search_count([]))
        self.assertEqual(1000, reporte_desempeno_valor_ganado_model.sudo(user_group_project_manager_02).search_count([]))

        # ----------------------------
        # project.project
        # ----------------------------
        project_model = self.env['project.project']
        self.assertEqual(1000, project_model.sudo(user_group_project_manager_01).search_count([]))
        self.assertEqual(1000, project_model.sudo(user_group_project_manager_02).search_count([]))

        # ----------------------------
        # project.financiacion
        # ----------------------------
        financiacion_model = self.env['project.financiacion']
        self.assertEqual(1000, financiacion_model.sudo(user_group_project_manager_01).search_count([]))
        self.assertEqual(1000, financiacion_model.sudo(user_group_project_manager_02).search_count([]))

        # ----------------------------
        # project.solicitud_cambio
        # ----------------------------
        solicitud_cambio_model = self.env['project.solicitud_cambio']
        self.assertEqual(1000, solicitud_cambio_model.sudo(user_group_project_manager_01).search_count([]))
        self.assertEqual(1000, solicitud_cambio_model.sudo(user_group_project_manager_02).search_count([]))

        # ----------------------------
        # project.task
        # ----------------------------
        task_model = self.env['project.task']
        self.assertEqual(1000, task_model.sudo(user_group_project_manager_01).search_count([]))
        self.assertEqual(1000, task_model.sudo(user_group_project_manager_02).search_count([]))

        # ----------------------------
        # project.meta
        # ----------------------------
        meta_model = self.env['project.meta']
        self.assertEqual(1000, meta_model.sudo(user_group_project_manager_01).search_count([]))
        self.assertEqual(1000, meta_model.sudo(user_group_project_manager_02).search_count([]))

        # ----------------------------
        # project.meta.tipo
        # ----------------------------
        meta_tipo_model = self.env['project.meta.tipo']
        self.assertEqual(1000, meta_tipo_model.sudo(user_group_project_manager_01).search_count([]))
        self.assertEqual(1000, meta_tipo_model.sudo(user_group_project_manager_02).search_count([]))

    def test_010_project_group_project_manager_create(self):
        """ project.group_project_manager Verifica reglas de dominio en operación CREATE """
        user_group_project_manager_01 = self.ref('project_portafolio_idu.group_project_manager_user_01')
        user_group_project_manager_02 = self.ref('project_portafolio_idu.group_project_manager_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        # Creación permitida
        vals = {
            'name': "Labore iure debitis tenetur recusandae.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Vero animi non et vitae culpa.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        programa = programa_model.sudo(user_group_project_manager_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Perspiciatis non minus aut voluptates.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Sunt consequuntur quaerat totam illo alias aut.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        try:
            programa = programa_model.sudo(user_group_project_manager_01).create(vals)
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
            'name': "Explicabo quasi id molestias aut qui.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Id molestias dolor omnis earum et aut rerum.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        portafolio = portafolio_model.sudo(user_group_project_manager_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Earum ad et quas eius quas omnis.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Commodi dignissimos et repudiandae laudantium.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        try:
            portafolio = portafolio_model.sudo(user_group_project_manager_01).create(vals)
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
            'name': "Veritatis ut placeat dolorum consequuntur architecto sapiente.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Sunt architecto autem est.",
            'linea_ids': [
                (4, self.ref('project_portafolio_idu.linea_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        linea_base = linea_base_model.sudo(user_group_project_manager_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Qui voluptatem quis expedita adipisci.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Consectetur cum voluptatem fuga necessitatibus et.",
            'linea_ids': [
                (4, self.ref('project_portafolio_idu.linea_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        try:
            linea_base = linea_base_model.sudo(user_group_project_manager_01).create(vals)
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
            'res_model': "Veniam ea nesciunt et.",
            'res_id': 72094582,
            'fecha_inicio': "1987-01-24 15:36:20",
            'fecha_fin': "1990-04-11 20:03:54",
            'progreso': 86124568.9528,
            'costo': 16004619.698,
        }
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_manager_01).create(vals)

        # Creación NO permitida
        vals = {
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'res_model': "Laboriosam dolorum sunt et illum sunt.",
            'res_id': 33200492,
            'fecha_inicio': "1988-02-01 17:36:53",
            'fecha_fin': "1989-11-24 17:56:12",
            'progreso': 5890205.66306,
            'costo': 27470791.3012,
        }
        try:
            linea_base_linea = linea_base_linea_model.sudo(user_group_project_manager_01).create(vals)
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
            'name': "Incidunt reprehenderit sunt fugit quaerat.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'linea_base_reporte_id': self.ref('project_portafolio_idu.linea_base_reporte_id_01'),
            'fecha': "1974-03-15 22:59:24",
            'descripcion': "Id dicta quos et vero mollitia id non.",
        }
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_manager_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Ex qui sed officia earum et repellendus pariatur repellat.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'linea_base_reporte_id': self.ref('project_portafolio_idu.linea_base_reporte_id_01'),
            'fecha': "1971-09-18 06:56:53",
            'descripcion': "Reiciendis beatae et sed reiciendis deleniti vero.",
        }
        try:
            reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_manager_01).create(vals)
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
            'planned_complete': 50251563.4137,
            'actual_complete': 85284324.6743,
            'bac': 38908117.2006,
            'ac': 50752649.8216,
            'es': 70120339.142,
            'at': 69035050.8488,
        }
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_manager_01).create(vals)

        # Creación NO permitida
        vals = {
            'reporte_id': self.ref('project_portafolio_idu.reporte_id_01'),
            'linea_base_linea_id': self.ref('project_portafolio_idu.linea_base_linea_id_01'),
            'planned_complete': 68563378.8468,
            'actual_complete': 25505404.1686,
            'bac': 6616631.09327,
            'ac': 45843824.8675,
            'es': 39135198.0296,
            'at': 98153899.5719,
        }
        try:
            reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_manager_01).create(vals)
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
            'proyecto_tipo': "funcionamiento",
            'financiacion_ids': [
                (4, self.ref('project_portafolio_idu.financiacion_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'meta_ids': [
                (4, self.ref('project_portafolio_idu.meta_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        project = project_model.sudo(user_group_project_manager_01).create(vals)

        # Creación NO permitida
        vals = {
            'dependencia_id': self.ref('project_portafolio_idu.dependencia_id_01'),
            'proyecto_tipo': "obra_etapa",
            'financiacion_ids': [
                (4, self.ref('project_portafolio_idu.financiacion_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'meta_ids': [
                (4, self.ref('project_portafolio_idu.meta_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        try:
            project = project_model.sudo(user_group_project_manager_01).create(vals)
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
            'name': "Maxime ipsum sint harum omnis sit laborum.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 10521177.9972,
        }
        financiacion = financiacion_model.sudo(user_group_project_manager_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Omnis dolorem debitis in ut ut exercitationem natus tempora.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 68676257.6568,
        }
        try:
            financiacion = financiacion_model.sudo(user_group_project_manager_01).create(vals)
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
            'name': "Quisquam laborum est et eum assumenda consequatur quasi.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_manager_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Nemo eum temporibus ut esse ut sint ullam.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        try:
            solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_manager_01).create(vals)
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
        task = task_model.sudo(user_group_project_manager_01).create(vals)

        # Creación NO permitida
        vals = {
            'dependencia_id': self.ref('project_portafolio_idu.dependencia_id_01'),
        }
        try:
            task = task_model.sudo(user_group_project_manager_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(task_model))

        # ----------------------------
        # project.meta
        # ----------------------------
        meta_model = self.env['project.meta']
        # Creación permitida
        vals = {
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'tipo_id': self.ref('project_portafolio_idu.tipo_id_01'),
            'cantidad': 37588824.2543,
        }
        meta = meta_model.sudo(user_group_project_manager_01).create(vals)

        # Creación NO permitida
        vals = {
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'tipo_id': self.ref('project_portafolio_idu.tipo_id_01'),
            'cantidad': 64384412.6008,
        }
        try:
            meta = meta_model.sudo(user_group_project_manager_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(meta_model))

        # ----------------------------
        # project.meta.tipo
        # ----------------------------
        meta_tipo_model = self.env['project.meta.tipo']
        # Creación permitida
        vals = {
            'name': "Possimus dolore voluptas adipisci.",
            'uom_id': self.ref('project_portafolio_idu.uom_id_01'),
        }
        meta_tipo = meta_tipo_model.sudo(user_group_project_manager_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Quam ut labore quibusdam aliquam.",
            'uom_id': self.ref('project_portafolio_idu.uom_id_01'),
        }
        try:
            meta_tipo = meta_tipo_model.sudo(user_group_project_manager_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(meta_tipo_model))

    def test_020_project_group_project_manager_write(self):
        """ project.group_project_manager Verifica reglas de dominio en operación WRITE """
        user_group_project_manager_01 = self.ref('project_portafolio_idu.group_project_manager_user_01')
        user_group_project_manager_02 = self.ref('project_portafolio_idu.group_project_manager_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        # Actualización permitida
        vals = {
            'name': "Non assumenda sunt culpa cupiditate maiores ut enim.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Rem nam numquam ut.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        programa = programa_model.sudo(user_group_project_manager_01).search([], limit=1)
        programa.sudo(user_group_project_manager_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Eos inventore placeat similique.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Dolorum iure et quia vitae nihil.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        programa = programa_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            programa.sudo(user_group_project_manager_01).write(vals)
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
            'name': "Pariatur similique sit dolore et et similique ad et.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Reprehenderit et sint et autem.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        portafolio = portafolio_model.sudo(user_group_project_manager_01).search([], limit=1)
        portafolio.sudo(user_group_project_manager_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Labore eveniet similique iusto.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Dignissimos beatae sed nostrum ut.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        portafolio = portafolio_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            portafolio.sudo(user_group_project_manager_01).write(vals)
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
            'name': "Quaerat libero rerum sit veritatis exercitationem omnis.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Consectetur voluptatem a architecto sint facere quis aut.",
            'linea_ids': [
                (4, self.ref('project_portafolio_idu.linea_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        linea_base = linea_base_model.sudo(user_group_project_manager_01).search([], limit=1)
        linea_base.sudo(user_group_project_manager_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Aut quia quibusdam amet pariatur neque.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Vitae ut iure iure exercitationem et facilis eius.",
            'linea_ids': [
                (4, self.ref('project_portafolio_idu.linea_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        linea_base = linea_base_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            linea_base.sudo(user_group_project_manager_01).write(vals)
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
            'res_model': "Ducimus sunt incidunt fugiat sint dolores amet.",
            'res_id': 3830139,
            'fecha_inicio': "2015-03-23 19:28:42",
            'fecha_fin': "1998-11-01 21:39:04",
            'progreso': 2181663.05316,
            'costo': 99757420.0334,
        }
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_manager_01).search([], limit=1)
        linea_base_linea.sudo(user_group_project_manager_01).write(vals)

        # Actualización NO permitida
        vals = {
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'res_model': "Voluptatem optio eos autem alias dolore.",
            'res_id': 93811460,
            'fecha_inicio': "1996-02-06 16:37:19",
            'fecha_fin': "1990-06-09 08:47:21",
            'progreso': 87643809.6661,
            'costo': 31824597.2607,
        }
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            linea_base_linea.sudo(user_group_project_manager_01).write(vals)
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
            'name': "Fuga laborum dicta ipsa in quae.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'linea_base_reporte_id': self.ref('project_portafolio_idu.linea_base_reporte_id_01'),
            'fecha': "1989-05-09 13:27:04",
            'descripcion': "Facilis aliquid sed iusto qui.",
        }
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_manager_01).search([], limit=1)
        reporte_desempeno.sudo(user_group_project_manager_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Dolor occaecati qui alias et voluptatem.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'linea_base_reporte_id': self.ref('project_portafolio_idu.linea_base_reporte_id_01'),
            'fecha': "2011-06-06 05:30:44",
            'descripcion': "Et nesciunt consequatur quis numquam quia.",
        }
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            reporte_desempeno.sudo(user_group_project_manager_01).write(vals)
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
            'planned_complete': 24844099.4371,
            'actual_complete': 29794715.209,
            'bac': 84732796.3211,
            'ac': 32311408.8824,
            'es': 28022876.7669,
            'at': 22777228.6694,
        }
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_manager_01).search([], limit=1)
        reporte_desempeno_valor_ganado.sudo(user_group_project_manager_01).write(vals)

        # Actualización NO permitida
        vals = {
            'reporte_id': self.ref('project_portafolio_idu.reporte_id_01'),
            'linea_base_linea_id': self.ref('project_portafolio_idu.linea_base_linea_id_01'),
            'planned_complete': 2309755.05621,
            'actual_complete': 546804.97668,
            'bac': 78910355.1843,
            'ac': 37192709.0578,
            'es': 51238887.1984,
            'at': 56620190.1734,
        }
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            reporte_desempeno_valor_ganado.sudo(user_group_project_manager_01).write(vals)
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
            'proyecto_tipo': "obra",
            'financiacion_ids': [
                (4, self.ref('project_portafolio_idu.financiacion_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'meta_ids': [
                (4, self.ref('project_portafolio_idu.meta_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        project = project_model.sudo(user_group_project_manager_01).search([], limit=1)
        project.sudo(user_group_project_manager_01).write(vals)

        # Actualización NO permitida
        vals = {
            'dependencia_id': self.ref('project_portafolio_idu.dependencia_id_01'),
            'proyecto_tipo': "plan_accion",
            'financiacion_ids': [
                (4, self.ref('project_portafolio_idu.financiacion_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'meta_ids': [
                (4, self.ref('project_portafolio_idu.meta_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        project = project_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            project.sudo(user_group_project_manager_01).write(vals)
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
            'name': "Quod reprehenderit placeat qui eos eos.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 93366917.3549,
        }
        financiacion = financiacion_model.sudo(user_group_project_manager_01).search([], limit=1)
        financiacion.sudo(user_group_project_manager_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Qui corrupti laudantium magni maxime est beatae.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 52968572.3171,
        }
        financiacion = financiacion_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            financiacion.sudo(user_group_project_manager_01).write(vals)
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
            'name': "Sunt et totam error illo cum voluptas.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_manager_01).search([], limit=1)
        solicitud_cambio.sudo(user_group_project_manager_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Et unde rerum ipsum alias repellendus.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            solicitud_cambio.sudo(user_group_project_manager_01).write(vals)
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
        task = task_model.sudo(user_group_project_manager_01).search([], limit=1)
        task.sudo(user_group_project_manager_01).write(vals)

        # Actualización NO permitida
        vals = {
            'dependencia_id': self.ref('project_portafolio_idu.dependencia_id_01'),
        }
        task = task_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            task.sudo(user_group_project_manager_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(task_model))

        # ----------------------------
        # project.meta
        # ----------------------------
        meta_model = self.env['project.meta']
        # Actualización permitida
        vals = {
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'tipo_id': self.ref('project_portafolio_idu.tipo_id_01'),
            'cantidad': 53808637.6127,
        }
        meta = meta_model.sudo(user_group_project_manager_01).search([], limit=1)
        meta.sudo(user_group_project_manager_01).write(vals)

        # Actualización NO permitida
        vals = {
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'tipo_id': self.ref('project_portafolio_idu.tipo_id_01'),
            'cantidad': 14966362.6576,
        }
        meta = meta_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            meta.sudo(user_group_project_manager_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(meta_model))

        # ----------------------------
        # project.meta.tipo
        # ----------------------------
        meta_tipo_model = self.env['project.meta.tipo']
        # Actualización permitida
        vals = {
            'name': "Ut iure blanditiis vero repudiandae rerum cum.",
            'uom_id': self.ref('project_portafolio_idu.uom_id_01'),
        }
        meta_tipo = meta_tipo_model.sudo(user_group_project_manager_01).search([], limit=1)
        meta_tipo.sudo(user_group_project_manager_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Qui rerum quis sint totam rerum non voluptatem.",
            'uom_id': self.ref('project_portafolio_idu.uom_id_01'),
        }
        meta_tipo = meta_tipo_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            meta_tipo.sudo(user_group_project_manager_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(meta_tipo_model))

    def test_030_project_group_project_manager_unlink(self):
        """ project.group_project_manager Verifica reglas de dominio en operación UNLINK - Delete """
        user_group_project_manager_01 = self.ref('project_portafolio_idu.group_project_manager_user_01')
        user_group_project_manager_02 = self.ref('project_portafolio_idu.group_project_manager_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        # Eliminación permitida
        programa = programa_model.sudo(user_group_project_manager_01).search([], limit=1)
        programa.sudo(user_group_project_manager_01).unlink()

        # Eliminación NO permitida
        programa = programa_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            programa.sudo(user_group_project_manager_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(programa_model))

        # ----------------------------
        # project.portafolio
        # ----------------------------
        portafolio_model = self.env['project.portafolio']
        # Eliminación permitida
        portafolio = portafolio_model.sudo(user_group_project_manager_01).search([], limit=1)
        portafolio.sudo(user_group_project_manager_01).unlink()

        # Eliminación NO permitida
        portafolio = portafolio_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            portafolio.sudo(user_group_project_manager_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(portafolio_model))

        # ----------------------------
        # project.linea_base
        # ----------------------------
        linea_base_model = self.env['project.linea_base']
        # Eliminación permitida
        linea_base = linea_base_model.sudo(user_group_project_manager_01).search([], limit=1)
        linea_base.sudo(user_group_project_manager_01).unlink()

        # Eliminación NO permitida
        linea_base = linea_base_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            linea_base.sudo(user_group_project_manager_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(linea_base_model))

        # ----------------------------
        # project.linea_base.linea
        # ----------------------------
        linea_base_linea_model = self.env['project.linea_base.linea']
        # Eliminación permitida
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_manager_01).search([], limit=1)
        linea_base_linea.sudo(user_group_project_manager_01).unlink()

        # Eliminación NO permitida
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            linea_base_linea.sudo(user_group_project_manager_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(linea_base_linea_model))

        # ----------------------------
        # project.reporte_desempeno
        # ----------------------------
        reporte_desempeno_model = self.env['project.reporte_desempeno']
        # Eliminación permitida
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_manager_01).search([], limit=1)
        reporte_desempeno.sudo(user_group_project_manager_01).unlink()

        # Eliminación NO permitida
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            reporte_desempeno.sudo(user_group_project_manager_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(reporte_desempeno_model))

        # ----------------------------
        # project.reporte_desempeno.valor_ganado
        # ----------------------------
        reporte_desempeno_valor_ganado_model = self.env['project.reporte_desempeno.valor_ganado']
        # Eliminación permitida
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_manager_01).search([], limit=1)
        reporte_desempeno_valor_ganado.sudo(user_group_project_manager_01).unlink()

        # Eliminación NO permitida
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            reporte_desempeno_valor_ganado.sudo(user_group_project_manager_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(reporte_desempeno_valor_ganado_model))

        # ----------------------------
        # project.project
        # ----------------------------
        project_model = self.env['project.project']
        # Eliminación permitida
        project = project_model.sudo(user_group_project_manager_01).search([], limit=1)
        project.sudo(user_group_project_manager_01).unlink()

        # Eliminación NO permitida
        project = project_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            project.sudo(user_group_project_manager_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(project_model))

        # ----------------------------
        # project.financiacion
        # ----------------------------
        financiacion_model = self.env['project.financiacion']
        # Eliminación permitida
        financiacion = financiacion_model.sudo(user_group_project_manager_01).search([], limit=1)
        financiacion.sudo(user_group_project_manager_01).unlink()

        # Eliminación NO permitida
        financiacion = financiacion_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            financiacion.sudo(user_group_project_manager_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(financiacion_model))

        # ----------------------------
        # project.solicitud_cambio
        # ----------------------------
        solicitud_cambio_model = self.env['project.solicitud_cambio']
        # Eliminación permitida
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_manager_01).search([], limit=1)
        solicitud_cambio.sudo(user_group_project_manager_01).unlink()

        # Eliminación NO permitida
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            solicitud_cambio.sudo(user_group_project_manager_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(solicitud_cambio_model))

        # ----------------------------
        # project.task
        # ----------------------------
        task_model = self.env['project.task']
        # Eliminación permitida
        task = task_model.sudo(user_group_project_manager_01).search([], limit=1)
        task.sudo(user_group_project_manager_01).unlink()

        # Eliminación NO permitida
        task = task_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            task.sudo(user_group_project_manager_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(task_model))

        # ----------------------------
        # project.meta
        # ----------------------------
        meta_model = self.env['project.meta']
        # Eliminación permitida
        meta = meta_model.sudo(user_group_project_manager_01).search([], limit=1)
        meta.sudo(user_group_project_manager_01).unlink()

        # Eliminación NO permitida
        meta = meta_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            meta.sudo(user_group_project_manager_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(meta_model))

        # ----------------------------
        # project.meta.tipo
        # ----------------------------
        meta_tipo_model = self.env['project.meta.tipo']
        # Eliminación permitida
        meta_tipo = meta_tipo_model.sudo(user_group_project_manager_01).search([], limit=1)
        meta_tipo.sudo(user_group_project_manager_01).unlink()

        # Eliminación NO permitida
        meta_tipo = meta_tipo_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            meta_tipo.sudo(user_group_project_manager_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(meta_tipo_model))


if __name__ == '__main__':
    unittest2.main()