# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import AccessError

logging.basicConfig()
_logger = logging.getLogger('TEST')

class test_security_project_group_project_user(common.TransactionCase):
    def test_000_project_group_project_user_search(self):
        """ project.group_project_user Verifica reglas de dominio en operación READ """
        user_group_project_user_01 = self.ref('project_portafolio_idu.group_project_user_user_01')
        user_group_project_user_02 = self.ref('project_portafolio_idu.group_project_user_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        self.assertEqual(1000, programa_model.sudo(user_group_project_user_01).search_count([]))
        self.assertEqual(1000, programa_model.sudo(user_group_project_user_02).search_count([]))

        # ----------------------------
        # project.portafolio
        # ----------------------------
        portafolio_model = self.env['project.portafolio']
        self.assertEqual(1000, portafolio_model.sudo(user_group_project_user_01).search_count([]))
        self.assertEqual(1000, portafolio_model.sudo(user_group_project_user_02).search_count([]))

        # ----------------------------
        # project.linea_base
        # ----------------------------
        linea_base_model = self.env['project.linea_base']
        self.assertEqual(1000, linea_base_model.sudo(user_group_project_user_01).search_count([]))
        self.assertEqual(1000, linea_base_model.sudo(user_group_project_user_02).search_count([]))

        # ----------------------------
        # project.linea_base.linea
        # ----------------------------
        linea_base_linea_model = self.env['project.linea_base.linea']
        self.assertEqual(1000, linea_base_linea_model.sudo(user_group_project_user_01).search_count([]))
        self.assertEqual(1000, linea_base_linea_model.sudo(user_group_project_user_02).search_count([]))

        # ----------------------------
        # project.reporte_desempeno
        # ----------------------------
        reporte_desempeno_model = self.env['project.reporte_desempeno']
        self.assertEqual(1000, reporte_desempeno_model.sudo(user_group_project_user_01).search_count([]))
        self.assertEqual(1000, reporte_desempeno_model.sudo(user_group_project_user_02).search_count([]))

        # ----------------------------
        # project.reporte_desempeno.valor_ganado
        # ----------------------------
        reporte_desempeno_valor_ganado_model = self.env['project.reporte_desempeno.valor_ganado']
        self.assertEqual(1000, reporte_desempeno_valor_ganado_model.sudo(user_group_project_user_01).search_count([]))
        self.assertEqual(1000, reporte_desempeno_valor_ganado_model.sudo(user_group_project_user_02).search_count([]))

        # ----------------------------
        # project.project
        # ----------------------------
        project_model = self.env['project.project']
        self.assertEqual(1000, project_model.sudo(user_group_project_user_01).search_count([]))
        self.assertEqual(1000, project_model.sudo(user_group_project_user_02).search_count([]))

        # ----------------------------
        # project.financiacion
        # ----------------------------
        financiacion_model = self.env['project.financiacion']
        self.assertEqual(1000, financiacion_model.sudo(user_group_project_user_01).search_count([]))
        self.assertEqual(1000, financiacion_model.sudo(user_group_project_user_02).search_count([]))

        # ----------------------------
        # project.solicitud_cambio
        # ----------------------------
        solicitud_cambio_model = self.env['project.solicitud_cambio']
        self.assertEqual(1000, solicitud_cambio_model.sudo(user_group_project_user_01).search_count([]))
        self.assertEqual(1000, solicitud_cambio_model.sudo(user_group_project_user_02).search_count([]))

        # ----------------------------
        # project.task
        # ----------------------------
        task_model = self.env['project.task']
        self.assertEqual(1000, task_model.sudo(user_group_project_user_01).search_count([]))
        self.assertEqual(1000, task_model.sudo(user_group_project_user_02).search_count([]))

        # ----------------------------
        # project.meta
        # ----------------------------
        meta_model = self.env['project.meta']
        self.assertEqual(1000, meta_model.sudo(user_group_project_user_01).search_count([]))
        self.assertEqual(1000, meta_model.sudo(user_group_project_user_02).search_count([]))

        # ----------------------------
        # project.meta.tipo
        # ----------------------------
        meta_tipo_model = self.env['project.meta.tipo']
        self.assertEqual(1000, meta_tipo_model.sudo(user_group_project_user_01).search_count([]))
        self.assertEqual(1000, meta_tipo_model.sudo(user_group_project_user_02).search_count([]))

    def test_010_project_group_project_user_create(self):
        """ project.group_project_user Verifica reglas de dominio en operación CREATE """
        user_group_project_user_01 = self.ref('project_portafolio_idu.group_project_user_user_01')
        user_group_project_user_02 = self.ref('project_portafolio_idu.group_project_user_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        # Creación permitida
        vals = {
            'name': "Reprehenderit ut ut id accusantium et aliquam.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Perspiciatis eius assumenda consectetur tempore nobis repellat.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        programa = programa_model.sudo(user_group_project_user_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Et voluptas consectetur non nihil repellat et corporis ab.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Quia incidunt rerum perferendis commodi ut quos animi et.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        try:
            programa = programa_model.sudo(user_group_project_user_01).create(vals)
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
            'name': "Qui quae et fuga et ad.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Deserunt vel recusandae recusandae et corrupti et quidem.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        portafolio = portafolio_model.sudo(user_group_project_user_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Voluptates molestias eius rem ea.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Iste laborum qui consectetur et.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        try:
            portafolio = portafolio_model.sudo(user_group_project_user_01).create(vals)
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
            'name': "Laudantium cum inventore cumque voluptas numquam tempora nihil.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Voluptates omnis est harum.",
            'linea_ids': [
                (4, self.ref('project_portafolio_idu.linea_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        linea_base = linea_base_model.sudo(user_group_project_user_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Molestiae voluptatibus est ratione.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Repellat voluptatum modi aliquam fuga quis atque.",
            'linea_ids': [
                (4, self.ref('project_portafolio_idu.linea_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        try:
            linea_base = linea_base_model.sudo(user_group_project_user_01).create(vals)
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
            'res_model': "Minima porro ipsa repudiandae eveniet fugiat id.",
            'res_id': 49358472,
            'fecha_inicio': "1980-03-06 15:40:54",
            'fecha_fin': "1986-05-11 04:30:59",
            'progreso': 287884.098609,
            'costo': 34930836.5328,
        }
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_user_01).create(vals)

        # Creación NO permitida
        vals = {
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'res_model': "Nemo qui id et nostrum quo distinctio.",
            'res_id': 49304652,
            'fecha_inicio': "2012-08-20 23:53:51",
            'fecha_fin': "1998-01-23 22:22:38",
            'progreso': 75657799.4696,
            'costo': 84580797.378,
        }
        try:
            linea_base_linea = linea_base_linea_model.sudo(user_group_project_user_01).create(vals)
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
            'name': "Explicabo corporis quas ut enim dolores officia earum.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'linea_base_reporte_id': self.ref('project_portafolio_idu.linea_base_reporte_id_01'),
            'fecha': "1998-06-09 15:44:09",
            'descripcion': "Occaecati nemo pariatur magnam est fuga ipsa voluptates.",
        }
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_user_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Tenetur a dignissimos esse eum quos officiis aut.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'linea_base_reporte_id': self.ref('project_portafolio_idu.linea_base_reporte_id_01'),
            'fecha': "2004-03-27 11:43:14",
            'descripcion': "Facilis maiores ut quaerat eum.",
        }
        try:
            reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_user_01).create(vals)
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
            'planned_complete': 81779903.915,
            'actual_complete': 64113943.2883,
            'bac': 1470116.80991,
            'ac': 17907701.4485,
            'es': 10340128.1533,
            'at': 5177323.27145,
        }
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_user_01).create(vals)

        # Creación NO permitida
        vals = {
            'reporte_id': self.ref('project_portafolio_idu.reporte_id_01'),
            'linea_base_linea_id': self.ref('project_portafolio_idu.linea_base_linea_id_01'),
            'planned_complete': 90280567.7396,
            'actual_complete': 10273997.2372,
            'bac': 4966082.16064,
            'ac': 23710717.0638,
            'es': 23760437.2662,
            'at': 94125524.8048,
        }
        try:
            reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_user_01).create(vals)
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
        project = project_model.sudo(user_group_project_user_01).create(vals)

        # Creación NO permitida
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
        try:
            project = project_model.sudo(user_group_project_user_01).create(vals)
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
            'name': "Eius quas quaerat minima debitis deleniti.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 63894301.1664,
        }
        financiacion = financiacion_model.sudo(user_group_project_user_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Aut eaque incidunt ut rerum ex quo magni.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 5013153.33654,
        }
        try:
            financiacion = financiacion_model.sudo(user_group_project_user_01).create(vals)
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
            'name': "Molestiae nihil vero veniam modi.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_user_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Cum enim esse eos eum.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        try:
            solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_user_01).create(vals)
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
        task = task_model.sudo(user_group_project_user_01).create(vals)

        # Creación NO permitida
        vals = {
            'dependencia_id': self.ref('project_portafolio_idu.dependencia_id_01'),
        }
        try:
            task = task_model.sudo(user_group_project_user_01).create(vals)
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
            'cantidad': 73609872.7611,
        }
        meta = meta_model.sudo(user_group_project_user_01).create(vals)

        # Creación NO permitida
        vals = {
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'tipo_id': self.ref('project_portafolio_idu.tipo_id_01'),
            'cantidad': 49598996.4871,
        }
        try:
            meta = meta_model.sudo(user_group_project_user_01).create(vals)
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
            'name': "Incidunt qui quas et maxime adipisci illum incidunt sed.",
            'uom_id': self.ref('project_portafolio_idu.uom_id_01'),
        }
        meta_tipo = meta_tipo_model.sudo(user_group_project_user_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Est nesciunt totam quasi necessitatibus et.",
            'uom_id': self.ref('project_portafolio_idu.uom_id_01'),
        }
        try:
            meta_tipo = meta_tipo_model.sudo(user_group_project_user_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(meta_tipo_model))

    def test_020_project_group_project_user_write(self):
        """ project.group_project_user Verifica reglas de dominio en operación WRITE """
        user_group_project_user_01 = self.ref('project_portafolio_idu.group_project_user_user_01')
        user_group_project_user_02 = self.ref('project_portafolio_idu.group_project_user_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        # Actualización permitida
        vals = {
            'name': "Dolorum sit quisquam iure eum blanditiis atque temporibus aut.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Ex ut voluptas quibusdam qui.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        programa = programa_model.sudo(user_group_project_user_01).search([], limit=1)
        programa.sudo(user_group_project_user_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Consequatur nesciunt officia quo ut.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Inventore adipisci iusto aut ut.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        programa = programa_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            programa.sudo(user_group_project_user_01).write(vals)
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
            'name': "Eligendi optio impedit commodi dolorem perspiciatis perspiciatis.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Ab adipisci expedita corrupti quo eos voluptas.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        portafolio = portafolio_model.sudo(user_group_project_user_01).search([], limit=1)
        portafolio.sudo(user_group_project_user_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Laboriosam optio aut est recusandae molestiae modi sit exercitationem.",
            'user_id': self.ref('project_portafolio_idu.user_id_01'),
            'descripcion': "Aperiam veritatis sed omnis qui voluptatibus.",
            'project_ids': [
                (4, self.ref('project_portafolio_idu.project_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        portafolio = portafolio_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            portafolio.sudo(user_group_project_user_01).write(vals)
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
            'name': "Architecto sit molestiae rem corrupti et.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Nulla nam autem quos reiciendis corporis eligendi.",
            'linea_ids': [
                (4, self.ref('project_portafolio_idu.linea_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        linea_base = linea_base_model.sudo(user_group_project_user_01).search([], limit=1)
        linea_base.sudo(user_group_project_user_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Saepe commodi quaerat modi in.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'descripcion': "Placeat necessitatibus vel aut deleniti nesciunt.",
            'linea_ids': [
                (4, self.ref('project_portafolio_idu.linea_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        linea_base = linea_base_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            linea_base.sudo(user_group_project_user_01).write(vals)
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
            'res_model': "Maiores sit minima fuga quibusdam.",
            'res_id': 40693596,
            'fecha_inicio': "1978-04-29 05:38:48",
            'fecha_fin': "1996-04-10 19:29:08",
            'progreso': 66037490.1219,
            'costo': 16130336.4491,
        }
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_user_01).search([], limit=1)
        linea_base_linea.sudo(user_group_project_user_01).write(vals)

        # Actualización NO permitida
        vals = {
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'res_model': "Eum reprehenderit hic architecto quibusdam assumenda et ut.",
            'res_id': 45628742,
            'fecha_inicio': "1980-04-06 20:56:21",
            'fecha_fin': "2011-06-05 07:48:58",
            'progreso': 11196229.0154,
            'costo': 68245582.6602,
        }
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            linea_base_linea.sudo(user_group_project_user_01).write(vals)
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
            'name': "Voluptate qui veritatis delectus in rerum explicabo aut ea.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'linea_base_reporte_id': self.ref('project_portafolio_idu.linea_base_reporte_id_01'),
            'fecha': "1998-01-27 07:21:35",
            'descripcion': "Blanditiis velit repellat voluptas minus.",
        }
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_user_01).search([], limit=1)
        reporte_desempeno.sudo(user_group_project_user_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Et provident aut debitis beatae autem ab sapiente.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'linea_base_id': self.ref('project_portafolio_idu.linea_base_id_01'),
            'linea_base_reporte_id': self.ref('project_portafolio_idu.linea_base_reporte_id_01'),
            'fecha': "1975-02-08 10:18:15",
            'descripcion': "Eum voluptatem delectus qui fugit repudiandae.",
        }
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            reporte_desempeno.sudo(user_group_project_user_01).write(vals)
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
            'planned_complete': 49462141.6815,
            'actual_complete': 15922507.6531,
            'bac': 9466505.03357,
            'ac': 55169612.5377,
            'es': 10005808.3911,
            'at': 76767674.8821,
        }
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_user_01).search([], limit=1)
        reporte_desempeno_valor_ganado.sudo(user_group_project_user_01).write(vals)

        # Actualización NO permitida
        vals = {
            'reporte_id': self.ref('project_portafolio_idu.reporte_id_01'),
            'linea_base_linea_id': self.ref('project_portafolio_idu.linea_base_linea_id_01'),
            'planned_complete': 82319088.0646,
            'actual_complete': 15369887.1024,
            'bac': 41912220.5568,
            'ac': 3073256.39844,
            'es': 66365124.7388,
            'at': 45349369.3148,
        }
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            reporte_desempeno_valor_ganado.sudo(user_group_project_user_01).write(vals)
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
        project = project_model.sudo(user_group_project_user_01).search([], limit=1)
        project.sudo(user_group_project_user_01).write(vals)

        # Actualización NO permitida
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
        project = project_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            project.sudo(user_group_project_user_01).write(vals)
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
            'name': "Sit molestiae explicabo est reiciendis magni minus minus consequuntur.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 65134705.7444,
        }
        financiacion = financiacion_model.sudo(user_group_project_user_01).search([], limit=1)
        financiacion.sudo(user_group_project_user_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Et dicta facere autem ipsum dicta.",
            'company_id': self.ref('project_portafolio_idu.company_id_01'),
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'fuente_financiacion_id': self.ref('project_portafolio_idu.fuente_financiacion_id_01'),
            'valor': 76428113.2856,
        }
        financiacion = financiacion_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            financiacion.sudo(user_group_project_user_01).write(vals)
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
            'name': "Ab ad et eius molestias numquam excepturi explicabo.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_user_01).search([], limit=1)
        solicitud_cambio.sudo(user_group_project_user_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Incidunt et dolore debitis cum expedita aut reiciendis.",
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
        }
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            solicitud_cambio.sudo(user_group_project_user_01).write(vals)
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
        task = task_model.sudo(user_group_project_user_01).search([], limit=1)
        task.sudo(user_group_project_user_01).write(vals)

        # Actualización NO permitida
        vals = {
            'dependencia_id': self.ref('project_portafolio_idu.dependencia_id_01'),
        }
        task = task_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            task.sudo(user_group_project_user_01).write(vals)
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
            'cantidad': 9396696.75741,
        }
        meta = meta_model.sudo(user_group_project_user_01).search([], limit=1)
        meta.sudo(user_group_project_user_01).write(vals)

        # Actualización NO permitida
        vals = {
            'project_id': self.ref('project_portafolio_idu.project_id_01'),
            'tipo_id': self.ref('project_portafolio_idu.tipo_id_01'),
            'cantidad': 42457833.9223,
        }
        meta = meta_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            meta.sudo(user_group_project_user_01).write(vals)
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
            'name': "Veniam rerum quae a eos.",
            'uom_id': self.ref('project_portafolio_idu.uom_id_01'),
        }
        meta_tipo = meta_tipo_model.sudo(user_group_project_user_01).search([], limit=1)
        meta_tipo.sudo(user_group_project_user_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Rerum ad quidem nobis et.",
            'uom_id': self.ref('project_portafolio_idu.uom_id_01'),
        }
        meta_tipo = meta_tipo_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            meta_tipo.sudo(user_group_project_user_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(meta_tipo_model))

    def test_030_project_group_project_user_unlink(self):
        """ project.group_project_user Verifica reglas de dominio en operación UNLINK - Delete """
        user_group_project_user_01 = self.ref('project_portafolio_idu.group_project_user_user_01')
        user_group_project_user_02 = self.ref('project_portafolio_idu.group_project_user_user_02')

        # ----------------------------
        # project.programa
        # ----------------------------
        programa_model = self.env['project.programa']
        # Eliminación permitida
        programa = programa_model.sudo(user_group_project_user_01).search([], limit=1)
        programa.sudo(user_group_project_user_01).unlink()

        # Eliminación NO permitida
        programa = programa_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            programa.sudo(user_group_project_user_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(programa_model))

        # ----------------------------
        # project.portafolio
        # ----------------------------
        portafolio_model = self.env['project.portafolio']
        # Eliminación permitida
        portafolio = portafolio_model.sudo(user_group_project_user_01).search([], limit=1)
        portafolio.sudo(user_group_project_user_01).unlink()

        # Eliminación NO permitida
        portafolio = portafolio_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            portafolio.sudo(user_group_project_user_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(portafolio_model))

        # ----------------------------
        # project.linea_base
        # ----------------------------
        linea_base_model = self.env['project.linea_base']
        # Eliminación permitida
        linea_base = linea_base_model.sudo(user_group_project_user_01).search([], limit=1)
        linea_base.sudo(user_group_project_user_01).unlink()

        # Eliminación NO permitida
        linea_base = linea_base_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            linea_base.sudo(user_group_project_user_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(linea_base_model))

        # ----------------------------
        # project.linea_base.linea
        # ----------------------------
        linea_base_linea_model = self.env['project.linea_base.linea']
        # Eliminación permitida
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_user_01).search([], limit=1)
        linea_base_linea.sudo(user_group_project_user_01).unlink()

        # Eliminación NO permitida
        linea_base_linea = linea_base_linea_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            linea_base_linea.sudo(user_group_project_user_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(linea_base_linea_model))

        # ----------------------------
        # project.reporte_desempeno
        # ----------------------------
        reporte_desempeno_model = self.env['project.reporte_desempeno']
        # Eliminación permitida
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_user_01).search([], limit=1)
        reporte_desempeno.sudo(user_group_project_user_01).unlink()

        # Eliminación NO permitida
        reporte_desempeno = reporte_desempeno_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            reporte_desempeno.sudo(user_group_project_user_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(reporte_desempeno_model))

        # ----------------------------
        # project.reporte_desempeno.valor_ganado
        # ----------------------------
        reporte_desempeno_valor_ganado_model = self.env['project.reporte_desempeno.valor_ganado']
        # Eliminación permitida
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_user_01).search([], limit=1)
        reporte_desempeno_valor_ganado.sudo(user_group_project_user_01).unlink()

        # Eliminación NO permitida
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            reporte_desempeno_valor_ganado.sudo(user_group_project_user_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(reporte_desempeno_valor_ganado_model))

        # ----------------------------
        # project.project
        # ----------------------------
        project_model = self.env['project.project']
        # Eliminación permitida
        project = project_model.sudo(user_group_project_user_01).search([], limit=1)
        project.sudo(user_group_project_user_01).unlink()

        # Eliminación NO permitida
        project = project_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            project.sudo(user_group_project_user_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(project_model))

        # ----------------------------
        # project.financiacion
        # ----------------------------
        financiacion_model = self.env['project.financiacion']
        # Eliminación permitida
        financiacion = financiacion_model.sudo(user_group_project_user_01).search([], limit=1)
        financiacion.sudo(user_group_project_user_01).unlink()

        # Eliminación NO permitida
        financiacion = financiacion_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            financiacion.sudo(user_group_project_user_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(financiacion_model))

        # ----------------------------
        # project.solicitud_cambio
        # ----------------------------
        solicitud_cambio_model = self.env['project.solicitud_cambio']
        # Eliminación permitida
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_user_01).search([], limit=1)
        solicitud_cambio.sudo(user_group_project_user_01).unlink()

        # Eliminación NO permitida
        solicitud_cambio = solicitud_cambio_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            solicitud_cambio.sudo(user_group_project_user_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(solicitud_cambio_model))

        # ----------------------------
        # project.task
        # ----------------------------
        task_model = self.env['project.task']
        # Eliminación permitida
        task = task_model.sudo(user_group_project_user_01).search([], limit=1)
        task.sudo(user_group_project_user_01).unlink()

        # Eliminación NO permitida
        task = task_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            task.sudo(user_group_project_user_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(task_model))

        # ----------------------------
        # project.meta
        # ----------------------------
        meta_model = self.env['project.meta']
        # Eliminación permitida
        meta = meta_model.sudo(user_group_project_user_01).search([], limit=1)
        meta.sudo(user_group_project_user_01).unlink()

        # Eliminación NO permitida
        meta = meta_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            meta.sudo(user_group_project_user_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(meta_model))

        # ----------------------------
        # project.meta.tipo
        # ----------------------------
        meta_tipo_model = self.env['project.meta.tipo']
        # Eliminación permitida
        meta_tipo = meta_tipo_model.sudo(user_group_project_user_01).search([], limit=1)
        meta_tipo.sudo(user_group_project_user_01).unlink()

        # Eliminación NO permitida
        meta_tipo = meta_tipo_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            meta_tipo.sudo(user_group_project_user_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(meta_tipo_model))


if __name__ == '__main__':
    unittest2.main()