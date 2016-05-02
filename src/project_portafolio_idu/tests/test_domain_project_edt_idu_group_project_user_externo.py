# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import AccessError

logging.basicConfig()
_logger = logging.getLogger('TEST')

class test_security_project_edt_idu_group_project_user_externo(common.TransactionCase):
    def test_000_project_edt_idu_group_project_user_externo_search(self):
        """ project_edt_idu.group_project_user_externo Verifica reglas de dominio en operación READ """
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

        # ----------------------------
        # project.meta
        # ----------------------------
        meta_model = self.env['project.meta']
        self.assertEqual(1000, meta_model.sudo(user_group_project_user_externo_01).search_count([]))
        self.assertEqual(1000, meta_model.sudo(user_group_project_user_externo_02).search_count([]))

        # ----------------------------
        # project.meta.tipo
        # ----------------------------
        meta_tipo_model = self.env['project.meta.tipo']
        self.assertEqual(1000, meta_tipo_model.sudo(user_group_project_user_externo_01).search_count([]))
        self.assertEqual(1000, meta_tipo_model.sudo(user_group_project_user_externo_02).search_count([]))

    def test_010_project_edt_idu_group_project_user_externo_create(self):
        """ project_edt_idu.group_project_user_externo Verifica reglas de dominio en operación CREATE """
        user_group_project_user_externo_01 = self.ref('project_portafolio_idu.group_project_user_externo_user_01')
        user_group_project_user_externo_02 = self.ref('project_portafolio_idu.group_project_user_externo_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        # Creación permitida
        vals = {
            'name': "Omnis quo expedita nesciunt totam nam ipsum.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Alias reprehenderit quo eum similique harum.",
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
            'name': "Libero facilis qui quis numquam.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Neque quam est et dolore id.",
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
            'name': "Magnam est sint earum repellat perferendis.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Voluptatem non rerum dolor qui sit unde.",
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
            'name': "Debitis animi praesentium sit quasi consectetur.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Dolorum sint quo nihil aut tenetur voluptate consequatur.",
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
            'name': "Mollitia ut sunt saepe incidunt sed.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "In provident qui sit enim nam nihil eos.",
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
            'name': "Tenetur deserunt vel aut est fugit accusantium.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Tempora dolore molestias molestias perspiciatis rerum iure maiores.",
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
            'res_model': "Ratione vero quidem vitae.",
            'res_id': 99046533,
            'fecha_inicio': "2009-01-14 10:08:45",
            'fecha_fin': "2010-03-17 18:48:44",
            'progreso': 35365177.6823,
            'costo': 77663920.5256,
        }
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'res_model': "Blanditiis quia accusamus suscipit odit ipsa non totam.",
            'res_id': 84324583,
            'fecha_inicio': "1980-07-07 22:49:11",
            'fecha_fin': "1986-02-07 17:21:38",
            'progreso': 96306623.7644,
            'costo': 2528333.818,
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
            'name': "Voluptatem et nemo deleniti at dolor.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'linea_base_reporte_id': self.ref('project_portafolio_idu.linea_base_reporte_id_01'),
            'fecha': "1976-08-15 13:52:12",
            'descripcion': "Molestias nostrum incidunt est suscipit.",
        }
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Qui adipisci dolorem ut.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'linea_base_reporte_id': self.ref('project_portafolio_idu.linea_base_reporte_id_01'),
            'fecha': "2012-01-22 06:44:49",
            'descripcion': "Ut autem aliquid fuga.",
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
            'planned_complete': 31977387.2723,
            'actual_complete': 39751414.6425,
            'bac': 12410852.3802,
            'ac': 92926262.2129,
            'es': 85093700.85,
            'at': 93577255.6961,
        }
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'reporte_id': self.ref('project_portafolio_idu.reporte_id_01'),
            'linea_base_linea_id': self.ref('project_portafolio_idu.linea_base_linea_id_01'),
            'planned_complete': 56807730.3649,
            'actual_complete': 71136485.4817,
            'bac': 35817236.8924,
            'ac': 66094081.6216,
            'es': 8351376.29005,
            'at': 81055818.298,
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
            'proyecto_tipo': "obra_componente",
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
        project = project_model.sudo(user_group_project_user_externo_01).create(vals)

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
            'name': "Corporis ut officia alias amet doloribus atque.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 32021929.9277,
        }
        financiacion = financiacion_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Illo aliquam et fuga magnam in.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 35412594.8993,
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
            'name': "Unde dolor est nisi ullam aliquam.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Repellendus provident ipsum saepe est nemo quis commodi.",
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

        # ----------------------------
        # project.meta
        # ----------------------------
        meta_model = self.env['project.meta']
        # Creación permitida
        vals = {
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'tipo_id': self.ref('project_portafolio_idu.tipo_id_01'),
            'cantidad': 21551255.3999,
        }
        meta = meta_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'tipo_id': self.ref('project_portafolio_idu.tipo_id_01'),
            'cantidad': 93143285.5742,
        }
        try:
            meta = meta_model.sudo(user_group_project_user_externo_01).create(vals)
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
            'name': "Ut id veniam accusamus.",
            'uom_id': self.ref('project_portafolio_idu.uom_id_01'),
        }
        meta_tipo = meta_tipo_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Tenetur ex qui consectetur aut nemo mollitia.",
            'uom_id': self.ref('project_portafolio_idu.uom_id_01'),
        }
        try:
            meta_tipo = meta_tipo_model.sudo(user_group_project_user_externo_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(meta_tipo_model))

    def test_020_project_edt_idu_group_project_user_externo_write(self):
        """ project_edt_idu.group_project_user_externo Verifica reglas de dominio en operación WRITE """
        user_group_project_user_externo_01 = self.ref('project_portafolio_idu.group_project_user_externo_user_01')
        user_group_project_user_externo_02 = self.ref('project_portafolio_idu.group_project_user_externo_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        # Actualización permitida
        vals = {
            'name': "Eos quae ex quaerat aliquid est.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Aut natus quaerat quis.",
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
            'name': "Quidem voluptatem omnis officia fuga ex.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Officia est autem provident vel doloribus consequuntur.",
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
            'name': "Cupiditate animi provident et ut dolores est omnis itaque.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Ut enim quia enim sint.",
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
            'name': "Dolor tempora exercitationem et assumenda qui et voluptas.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Cum labore voluptatem sed id eaque nemo veritatis.",
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
            'name': "Doloribus quibusdam suscipit ad porro.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Veritatis beatae asperiores quos dolorem enim.",
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
            'name': "Error eum molestiae incidunt qui nam.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Alias repellendus expedita adipisci rerum sed quia.",
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
            'res_model': "Officia est cumque porro impedit odit corporis.",
            'res_id': 24514696,
            'fecha_inicio': "2001-12-27 20:39:08",
            'fecha_fin': "1979-10-06 17:01:23",
            'progreso': 26203106.0837,
            'costo': 10076018.4844,
        }
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        linea_base_linea.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'res_model': "Tempore repellat nostrum quam facilis.",
            'res_id': 81205406,
            'fecha_inicio': "1977-06-23 13:37:45",
            'fecha_fin': "1992-07-07 09:57:14",
            'progreso': 91327793.3857,
            'costo': 75680089.9788,
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
            'name': "Possimus delectus tempore corrupti voluptatem minima laboriosam.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'linea_base_reporte_id': self.ref('project_portafolio_idu.linea_base_reporte_id_01'),
            'fecha': "1977-09-05 01:37:46",
            'descripcion': "Nobis magni dolor eius error dolore.",
        }
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        reporte_desempeno.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Atque quisquam laboriosam tempora vitae rerum voluptas.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'linea_base_reporte_id': self.ref('project_portafolio_idu.linea_base_reporte_id_01'),
            'fecha': "1971-07-04 11:46:38",
            'descripcion': "Aspernatur qui ut ad impedit quos ratione et est.",
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
            'planned_complete': 80027974.2461,
            'actual_complete': 28806207.0183,
            'bac': 72687681.8574,
            'ac': 82882302.1282,
            'es': 72001464.4444,
            'at': 9112774.7302,
        }
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        reporte_desempeno_valor_ganado.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'reporte_id': self.ref('project_portafolio_idu.reporte_id_01'),
            'linea_base_linea_id': self.ref('project_portafolio_idu.linea_base_linea_id_01'),
            'planned_complete': 28891198.7628,
            'actual_complete': 58999729.6404,
            'bac': 72919558.6931,
            'ac': 25970041.2768,
            'es': 51747113.487,
            'at': 21767297.304,
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
        project = project_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        project.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
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
            'name': "Magnam vitae quibusdam et quasi.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 86500674.3324,
        }
        financiacion = financiacion_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        financiacion.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Rerum est sed eligendi corrupti.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 14222612.9946,
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
            'name': "Ex ea maiores ducimus.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        solicitud_cambio.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Omnis possimus nostrum et ut voluptatem.",
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

        # ----------------------------
        # project.meta
        # ----------------------------
        meta_model = self.env['project.meta']
        # Actualización permitida
        vals = {
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'tipo_id': self.ref('project_portafolio_idu.tipo_id_01'),
            'cantidad': 64096041.1669,
        }
        meta = meta_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        meta.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'tipo_id': self.ref('project_portafolio_idu.tipo_id_01'),
            'cantidad': 2308741.94529,
        }
        meta = meta_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            meta.sudo(user_group_project_user_externo_01).write(vals)
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
            'name': "Rerum non adipisci nihil molestiae unde nostrum.",
            'uom_id': self.ref('project_portafolio_idu.uom_id_01'),
        }
        meta_tipo = meta_tipo_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        meta_tipo.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Facilis eos officiis dolorum.",
            'uom_id': self.ref('project_portafolio_idu.uom_id_01'),
        }
        meta_tipo = meta_tipo_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            meta_tipo.sudo(user_group_project_user_externo_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(meta_tipo_model))

    def test_030_project_edt_idu_group_project_user_externo_unlink(self):
        """ project_edt_idu.group_project_user_externo Verifica reglas de dominio en operación UNLINK - Delete """
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

        # ----------------------------
        # project.meta
        # ----------------------------
        meta_model = self.env['project.meta']
        # Eliminación permitida
        meta = meta_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        meta.sudo(user_group_project_user_externo_01).unlink()

        # Eliminación NO permitida
        meta = meta_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            meta.sudo(user_group_project_user_externo_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(meta_model))

        # ----------------------------
        # project.meta.tipo
        # ----------------------------
        meta_tipo_model = self.env['project.meta.tipo']
        # Eliminación permitida
        meta_tipo = meta_tipo_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        meta_tipo.sudo(user_group_project_user_externo_01).unlink()

        # Eliminación NO permitida
        meta_tipo = meta_tipo_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            meta_tipo.sudo(user_group_project_user_externo_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(meta_tipo_model))


if __name__ == '__main__':
    unittest2.main()