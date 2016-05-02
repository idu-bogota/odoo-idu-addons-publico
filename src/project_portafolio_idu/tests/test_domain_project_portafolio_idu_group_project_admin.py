# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import AccessError

logging.basicConfig()
_logger = logging.getLogger('TEST')

class test_security_project_portafolio_idu_group_project_admin(common.TransactionCase):
    def test_000_project_portafolio_idu_group_project_admin_search(self):
        """ project_portafolio_idu.group_project_admin Verifica reglas de dominio en operación READ """
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

        # ----------------------------
        # project.meta
        # ----------------------------
        meta_model = self.env['project.meta']
        self.assertEqual(1000, meta_model.sudo(user_group_project_admin_01).search_count([]))
        self.assertEqual(1000, meta_model.sudo(user_group_project_admin_02).search_count([]))

        # ----------------------------
        # project.meta.tipo
        # ----------------------------
        meta_tipo_model = self.env['project.meta.tipo']
        self.assertEqual(1000, meta_tipo_model.sudo(user_group_project_admin_01).search_count([]))
        self.assertEqual(1000, meta_tipo_model.sudo(user_group_project_admin_02).search_count([]))

    def test_010_project_portafolio_idu_group_project_admin_create(self):
        """ project_portafolio_idu.group_project_admin Verifica reglas de dominio en operación CREATE """
        user_group_project_admin_01 = self.ref('project_portafolio_idu.group_project_admin_user_01')
        user_group_project_admin_02 = self.ref('project_portafolio_idu.group_project_admin_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        # Creación permitida
        vals = {
            'name': "Et enim illo rem asperiores aut voluptatibus nihil et.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Dolorem iusto architecto voluptas dolores ipsum qui.",
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
            'name': "Eaque et quasi sit natus quaerat.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Rerum et officiis magnam quas deserunt autem ea dolor.",
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
            'name': "Eum itaque sint nesciunt quis aut ipsam iusto.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Aspernatur cupiditate voluptatem optio eligendi.",
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
            'name': "Aperiam voluptatem incidunt reiciendis necessitatibus accusamus animi aperiam.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Non ut nobis odio quia quia eos id.",
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
            'name': "Atque enim impedit quos dolores saepe ex.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Quos modi voluptatum quia quod quam.",
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
            'name': "Tenetur ex quo vitae quam eaque non nihil.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Cum reiciendis nihil fugit placeat non.",
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
            'res_model': "Numquam sit dolor iusto cupiditate nisi.",
            'res_id': 92243254,
            'fecha_inicio': "1981-11-27 23:22:07",
            'fecha_fin': "1973-07-14 15:17:29",
            'progreso': 88881523.9097,
            'costo': 19450015.5242,
        }
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_admin_01).create(vals)

        # Creación NO permitida
        vals = {
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'res_model': "Iste provident consectetur eos ut maxime.",
            'res_id': 49007925,
            'fecha_inicio': "1986-04-23 08:27:21",
            'fecha_fin': "2007-03-13 01:46:49",
            'progreso': 11308253.098,
            'costo': 31667055.9421,
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
            'name': "Dolorem dolor omnis ipsa repudiandae velit hic libero natus.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'linea_base_reporte_id': self.ref('project_portafolio_idu.linea_base_reporte_id_01'),
            'fecha': "1993-05-30 14:56:27",
            'descripcion': "Voluptate esse reprehenderit alias voluptas reprehenderit ullam eum.",
        }
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_admin_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Corporis reprehenderit ipsa veniam labore necessitatibus.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'linea_base_reporte_id': self.ref('project_portafolio_idu.linea_base_reporte_id_01'),
            'fecha': "2004-02-11 23:47:23",
            'descripcion': "Est est tenetur tenetur.",
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
            'planned_complete': 73147589.6017,
            'actual_complete': 86509194.0051,
            'bac': 39603799.3473,
            'ac': 61153098.1429,
            'es': 60863232.3055,
            'at': 12206644.6674,
        }
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_admin_01).create(vals)

        # Creación NO permitida
        vals = {
            'reporte_id': self.ref('project_portafolio_idu.reporte_id_01'),
            'linea_base_linea_id': self.ref('project_portafolio_idu.linea_base_linea_id_01'),
            'planned_complete': 94779690.0636,
            'actual_complete': 83580151.1754,
            'bac': 62248246.4945,
            'ac': 11312803.4741,
            'es': 18588364.877,
            'at': 21275470.6035,
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
        project = project_model.sudo(user_group_project_admin_01).create(vals)

        # Creación NO permitida
        vals = {
            'dependencia_id': self.ref('project_portafolio_idu.dependencia_id_01'),
            'proyecto_tipo': "plan_mejoramiento",
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
            'name': "Nobis architecto vel natus necessitatibus aut numquam.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 26654289.1557,
        }
        financiacion = financiacion_model.sudo(user_group_project_admin_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Id provident temporibus harum assumenda sunt eos ea ipsa.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 18930748.714,
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
            'name': "Sed esse et et ipsum similique consequatur architecto.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_admin_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Ipsam voluptatem et voluptas.",
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

        # ----------------------------
        # project.meta
        # ----------------------------
        meta_model = self.env['project.meta']
        # Creación permitida
        vals = {
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'tipo_id': self.ref('project_portafolio_idu.tipo_id_01'),
            'cantidad': 66646507.8996,
        }
        meta = meta_model.sudo(user_group_project_admin_01).create(vals)

        # Creación NO permitida
        vals = {
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'tipo_id': self.ref('project_portafolio_idu.tipo_id_01'),
            'cantidad': 29207281.1889,
        }
        try:
            meta = meta_model.sudo(user_group_project_admin_01).create(vals)
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
            'name': "Reprehenderit vel inventore suscipit nulla sint.",
            'uom_id': self.ref('project_portafolio_idu.uom_id_01'),
        }
        meta_tipo = meta_tipo_model.sudo(user_group_project_admin_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Nesciunt delectus eos rerum.",
            'uom_id': self.ref('project_portafolio_idu.uom_id_01'),
        }
        try:
            meta_tipo = meta_tipo_model.sudo(user_group_project_admin_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(meta_tipo_model))

    def test_020_project_portafolio_idu_group_project_admin_write(self):
        """ project_portafolio_idu.group_project_admin Verifica reglas de dominio en operación WRITE """
        user_group_project_admin_01 = self.ref('project_portafolio_idu.group_project_admin_user_01')
        user_group_project_admin_02 = self.ref('project_portafolio_idu.group_project_admin_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        # Actualización permitida
        vals = {
            'name': "Nostrum in dolorum aspernatur qui.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Qui voluptatem ex consequatur necessitatibus.",
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
            'name': "Laboriosam eos consequatur pariatur quasi assumenda cumque ut laboriosam.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Delectus repellendus pariatur ad ipsam.",
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
            'name': "Quia laboriosam nobis eius consequatur.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Velit cupiditate a consectetur vero ipsum esse repudiandae ut.",
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
            'name': "Necessitatibus deserunt possimus praesentium.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Impedit in voluptatem nihil enim aperiam.",
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
            'name': "Eveniet hic deleniti asperiores et.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Consequuntur debitis ipsa aut culpa.",
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
            'name': "In quia delectus velit maxime occaecati sit.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Laboriosam magni atque delectus quia omnis aut eos.",
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
            'res_model': "Molestias veniam distinctio ut delectus est aliquid.",
            'res_id': 97843027,
            'fecha_inicio': "1982-08-15 00:42:49",
            'fecha_fin': "1986-11-27 20:10:07",
            'progreso': 90016536.5932,
            'costo': 5841595.69517,
        }
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_admin_01).search([], limit=1)
        linea_base_linea.sudo(user_group_project_admin_01).write(vals)

        # Actualización NO permitida
        vals = {
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'res_model': "Et soluta veniam tempora doloremque doloremque odit.",
            'res_id': 45451706,
            'fecha_inicio': "1979-05-12 15:50:26",
            'fecha_fin': "1993-07-19 14:13:24",
            'progreso': 61729535.9718,
            'costo': 86648389.4829,
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
            'name': "Quae accusamus sit at blanditiis libero eligendi eos.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'linea_base_reporte_id': self.ref('project_portafolio_idu.linea_base_reporte_id_01'),
            'fecha': "1972-08-18 09:30:47",
            'descripcion': "Eius ut non ratione voluptatem dolor.",
        }
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_admin_01).search([], limit=1)
        reporte_desempeno.sudo(user_group_project_admin_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Necessitatibus illum eum commodi veritatis in ut voluptas.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'linea_base_reporte_id': self.ref('project_portafolio_idu.linea_base_reporte_id_01'),
            'fecha': "2009-07-29 23:48:03",
            'descripcion': "Laudantium placeat sunt officia est aut.",
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
            'planned_complete': 66311516.7455,
            'actual_complete': 24872976.848,
            'bac': 66603402.6886,
            'ac': 81916045.5276,
            'es': 50653012.7016,
            'at': 94182179.9187,
        }
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_admin_01).search([], limit=1)
        reporte_desempeno_valor_ganado.sudo(user_group_project_admin_01).write(vals)

        # Actualización NO permitida
        vals = {
            'reporte_id': self.ref('project_portafolio_idu.reporte_id_01'),
            'linea_base_linea_id': self.ref('project_portafolio_idu.linea_base_linea_id_01'),
            'planned_complete': 18466010.7185,
            'actual_complete': 7508765.80637,
            'bac': 65997722.9851,
            'ac': 34426079.7842,
            'es': 13769946.8042,
            'at': 31632647.7348,
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
        project = project_model.sudo(user_group_project_admin_01).search([], limit=1)
        project.sudo(user_group_project_admin_01).write(vals)

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
            'name': "Quibusdam ullam culpa fugiat ut exercitationem ut temporibus.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 60018431.1593,
        }
        financiacion = financiacion_model.sudo(user_group_project_admin_01).search([], limit=1)
        financiacion.sudo(user_group_project_admin_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Ad enim error dolores atque dolores odit.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 21234066.8828,
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
            'name': "Quis nulla earum eligendi blanditiis.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_admin_01).search([], limit=1)
        solicitud_cambio.sudo(user_group_project_admin_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Natus occaecati dolor et dignissimos itaque.",
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

        # ----------------------------
        # project.meta
        # ----------------------------
        meta_model = self.env['project.meta']
        # Actualización permitida
        vals = {
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'tipo_id': self.ref('project_portafolio_idu.tipo_id_01'),
            'cantidad': 22301583.8899,
        }
        meta = meta_model.sudo(user_group_project_admin_01).search([], limit=1)
        meta.sudo(user_group_project_admin_01).write(vals)

        # Actualización NO permitida
        vals = {
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'tipo_id': self.ref('project_portafolio_idu.tipo_id_01'),
            'cantidad': 89099862.1478,
        }
        meta = meta_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            meta.sudo(user_group_project_admin_01).write(vals)
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
            'name': "Quos vel et tempora.",
            'uom_id': self.ref('project_portafolio_idu.uom_id_01'),
        }
        meta_tipo = meta_tipo_model.sudo(user_group_project_admin_01).search([], limit=1)
        meta_tipo.sudo(user_group_project_admin_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Dolores commodi corporis exercitationem dolor cupiditate doloribus labore.",
            'uom_id': self.ref('project_portafolio_idu.uom_id_01'),
        }
        meta_tipo = meta_tipo_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            meta_tipo.sudo(user_group_project_admin_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(meta_tipo_model))

    def test_030_project_portafolio_idu_group_project_admin_unlink(self):
        """ project_portafolio_idu.group_project_admin Verifica reglas de dominio en operación UNLINK - Delete """
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

        # ----------------------------
        # project.meta
        # ----------------------------
        meta_model = self.env['project.meta']
        # Eliminación permitida
        meta = meta_model.sudo(user_group_project_admin_01).search([], limit=1)
        meta.sudo(user_group_project_admin_01).unlink()

        # Eliminación NO permitida
        meta = meta_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            meta.sudo(user_group_project_admin_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(meta_model))

        # ----------------------------
        # project.meta.tipo
        # ----------------------------
        meta_tipo_model = self.env['project.meta.tipo']
        # Eliminación permitida
        meta_tipo = meta_tipo_model.sudo(user_group_project_admin_01).search([], limit=1)
        meta_tipo.sudo(user_group_project_admin_01).unlink()

        # Eliminación NO permitida
        meta_tipo = meta_tipo_model.sudo(user_group_project_admin_01).search([], limit=1)
        try:
            meta_tipo.sudo(user_group_project_admin_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(meta_tipo_model))


if __name__ == '__main__':
    unittest2.main()