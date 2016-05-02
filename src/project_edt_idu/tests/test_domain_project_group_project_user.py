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
        user_group_project_user_01 = self.ref('project_edt_idu.group_project_user_user_01')
        user_group_project_user_02 = self.ref('project_edt_idu.group_project_user_user_02')

        # ----------------------------
        # project.edt
        # ----------------------------
        edt_model = self.env['project.edt']
        self.assertEqual(1000, edt_model.sudo(user_group_project_user_01).search_count([]))
        self.assertEqual(1000, edt_model.sudo(user_group_project_user_02).search_count([]))

        # ----------------------------
        # project.task
        # ----------------------------
        task_model = self.env['project.task']
        self.assertEqual(1000, task_model.sudo(user_group_project_user_01).search_count([]))
        self.assertEqual(1000, task_model.sudo(user_group_project_user_02).search_count([]))

        # ----------------------------
        # project.project
        # ----------------------------
        project_model = self.env['project.project']
        self.assertEqual(1000, project_model.sudo(user_group_project_user_01).search_count([]))
        self.assertEqual(1000, project_model.sudo(user_group_project_user_02).search_count([]))

        # ----------------------------
        # project.task.registro_progreso
        # ----------------------------
        task_registro_progreso_model = self.env['project.task.registro_progreso']
        self.assertEqual(1000, task_registro_progreso_model.sudo(user_group_project_user_01).search_count([]))
        self.assertEqual(1000, task_registro_progreso_model.sudo(user_group_project_user_02).search_count([]))

        # ----------------------------
        # project.task.pendiente
        # ----------------------------
        task_pendiente_model = self.env['project.task.pendiente']
        self.assertEqual(1000, task_pendiente_model.sudo(user_group_project_user_01).search_count([]))
        self.assertEqual(1000, task_pendiente_model.sudo(user_group_project_user_02).search_count([]))

        # ----------------------------
        # project.predecesor
        # ----------------------------
        predecesor_model = self.env['project.predecesor']
        self.assertEqual(1000, predecesor_model.sudo(user_group_project_user_01).search_count([]))
        self.assertEqual(1000, predecesor_model.sudo(user_group_project_user_02).search_count([]))

        # ----------------------------
        # project.task.reporte_avance
        # ----------------------------
        task_reporte_avance_model = self.env['project.task.reporte_avance']
        self.assertEqual(1000, task_reporte_avance_model.sudo(user_group_project_user_01).search_count([]))
        self.assertEqual(1000, task_reporte_avance_model.sudo(user_group_project_user_02).search_count([]))

    def test_010_project_group_project_user_create(self):
        """ project.group_project_user Verifica reglas de dominio en operación CREATE """
        user_group_project_user_01 = self.ref('project_edt_idu.group_project_user_user_01')
        user_group_project_user_02 = self.ref('project_edt_idu.group_project_user_user_02')

        # ----------------------------
        # project.edt
        # ----------------------------
        edt_model = self.env['project.edt']
        # Creación permitida
        vals = {
            'name': "Aperiam neque rerum eum quasi dolor vitae.",
            'sequence': 31927799,
            'ms_project_guid': "Ratione itaque sed consequatur incidunt accusantium.",
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "aplazado",
            'fecha_planeada_inicio': "2007-09-14",
            'fecha_planeada_fin': "1998-10-08",
            'fecha_inicio': "1997-05-25",
            'fecha_fin': "1985-10-14",
            'peso': 14912639.9892,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 88125958.6827,
            'costo': 3312963.57805,
            'progreso': 43090233.1423,
            'project_id': self.ref('project_edt_idu.project_id_01'),
            'task_ids': [
                (4, self.ref('project_edt_idu.task_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'parent_id': self.ref('project_edt_idu.parent_id_01'),
            'child_ids': [
                (4, self.ref('project_edt_idu.child_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'programador_id': self.ref('project_edt_idu.programador_id_01'),
            'progreso_aprobado': 89164734.3717,
        }
        edt = edt_model.sudo(user_group_project_user_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Occaecati dolores eius numquam quia eius unde magni.",
            'sequence': 31551922,
            'ms_project_guid': "Similique recusandae numquam fugiat non exercitationem.",
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "aplazado",
            'fecha_planeada_inicio': "1992-04-08",
            'fecha_planeada_fin': "1994-01-17",
            'fecha_inicio': "2011-01-22",
            'fecha_fin': "1970-08-03",
            'peso': 17994322.7574,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 16386228.5617,
            'costo': 98127792.411,
            'progreso': 2647139.32023,
            'project_id': self.ref('project_edt_idu.project_id_01'),
            'task_ids': [
                (4, self.ref('project_edt_idu.task_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'parent_id': self.ref('project_edt_idu.parent_id_01'),
            'child_ids': [
                (4, self.ref('project_edt_idu.child_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'programador_id': self.ref('project_edt_idu.programador_id_01'),
            'progreso_aprobado': 37340684.601,
        }
        try:
            edt = edt_model.sudo(user_group_project_user_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(edt_model))

        # ----------------------------
        # project.task
        # ----------------------------
        task_model = self.env['project.task']
        # Creación permitida
        vals = {
            'edt_id': self.ref('project_edt_idu.edt_id_01'),
            'ms_project_guid': "Eligendi iure itaque sunt quam id ducimus.",
            'edt_peso': 77368687,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 75448344.1609,
            'costo': 39415620.7167,
            'progreso': 33572931.1108,
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'progreso_metodo': "pendientes",
            'fecha_planeada_inicio': "1988-10-17 21:13:32",
            'fecha_planeada_fin': "1981-05-28 19:29:13",
            'pendiente_ids': [
                (4, self.ref('project_edt_idu.pendiente_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'registro_progreso_ids': [
                (4, self.ref('project_edt_idu.registro_progreso_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'progreso_aprobado': 13647885.1674,
            'terminado': True,
            'cantidad_planeada': 82822496.4234,
            'cantidad': 85134266.4001,
            'product_id': self.ref('project_edt_idu.product_id_01'),
        }
        task = task_model.sudo(user_group_project_user_01).create(vals)

        # Creación NO permitida
        vals = {
            'edt_id': self.ref('project_edt_idu.edt_id_01'),
            'ms_project_guid': "Officiis et aspernatur dolor quaerat saepe iusto.",
            'edt_peso': 63163936,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 37690316.9018,
            'costo': 25211576.6812,
            'progreso': 9073949.10435,
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'progreso_metodo': "manual",
            'fecha_planeada_inicio': "2006-08-22 07:52:57",
            'fecha_planeada_fin': "1996-07-29 21:54:01",
            'pendiente_ids': [
                (4, self.ref('project_edt_idu.pendiente_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'registro_progreso_ids': [
                (4, self.ref('project_edt_idu.registro_progreso_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'progreso_aprobado': 36334092.1118,
            'terminado': False,
            'cantidad_planeada': 25849152.7475,
            'cantidad': 20098480.557,
            'product_id': self.ref('project_edt_idu.product_id_01'),
        }
        try:
            task = task_model.sudo(user_group_project_user_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(task_model))

        # ----------------------------
        # project.project
        # ----------------------------
        project_model = self.env['project.project']
        # Creación permitida
        vals = {
            'edt_raiz_id': self.ref('project_edt_idu.edt_raiz_id_01'),
            'edt_ids': [
                (4, self.ref('project_edt_idu.edt_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'programador_id': self.ref('project_edt_idu.programador_id_01'),
        }
        project = project_model.sudo(user_group_project_user_01).create(vals)

        # Creación NO permitida
        vals = {
            'edt_raiz_id': self.ref('project_edt_idu.edt_raiz_id_01'),
            'edt_ids': [
                (4, self.ref('project_edt_idu.edt_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'programador_id': self.ref('project_edt_idu.programador_id_01'),
        }
        try:
            project = project_model.sudo(user_group_project_user_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(project_model))

        # ----------------------------
        # project.task.registro_progreso
        # ----------------------------
        task_registro_progreso_model = self.env['project.task.registro_progreso']
        # Creación permitida
        vals = {
            'name': "Officiis quia consectetur voluptatum aut.",
            'fecha': "1982-02-16",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'porcentaje': 33429336,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo': 74746933.8123,
            'fecha_aprobacion': "1972-11-16 21:59:31",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'nivel_alerta': "bajo",
            'novedad': "Qui nulla temporibus est in.",
            'reporte_avance_id': self.ref('project_edt_idu.reporte_avance_id_01'),
            'cantidad': 94089352.6573,
        }
        task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_user_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Consectetur in culpa amet eum debitis.",
            'fecha': "1978-01-08",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'porcentaje': 85188801,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo': 31608076.7885,
            'fecha_aprobacion': "1987-08-10 02:51:49",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'nivel_alerta': "ninguno",
            'novedad': "Voluptatibus sunt molestiae qui minima repellat earum.",
            'reporte_avance_id': self.ref('project_edt_idu.reporte_avance_id_01'),
            'cantidad': 15167656.8374,
        }
        try:
            task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_user_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(task_registro_progreso_model))

        # ----------------------------
        # project.task.pendiente
        # ----------------------------
        task_pendiente_model = self.env['project.task.pendiente']
        # Creación permitida
        vals = {
            'name': "Eos consectetur illo animi maxime.",
            'sequence': 91173206,
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'peso': 76218775,
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'fecha_terminacion': "1981-10-09 13:12:36",
            'fecha_aprobacion': "2015-02-22 13:59:30",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
        }
        task_pendiente = task_pendiente_model.sudo(user_group_project_user_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Soluta asperiores velit dolores eos pariatur voluptate nulla.",
            'sequence': 32323661,
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'peso': 81832768,
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'fecha_terminacion': "1984-05-31 17:42:31",
            'fecha_aprobacion': "1984-04-08 19:48:40",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
        }
        try:
            task_pendiente = task_pendiente_model.sudo(user_group_project_user_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(task_pendiente_model))

        # ----------------------------
        # project.predecesor
        # ----------------------------
        predecesor_model = self.env['project.predecesor']
        # Creación permitida
        vals = {
            'origen_res_model': "edt",
            'origen_res_id': 28913862,
            'destino_res_model': "edt",
            'destino_res_id': 97521362,
            'tipo': "s_s",
        }
        predecesor = predecesor_model.sudo(user_group_project_user_01).create(vals)

        # Creación NO permitida
        vals = {
            'origen_res_model': "edt",
            'origen_res_id': 30528488,
            'destino_res_model': "edt",
            'destino_res_id': 10293211,
            'tipo': "s_s",
        }
        try:
            predecesor = predecesor_model.sudo(user_group_project_user_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(predecesor_model))

        # ----------------------------
        # project.task.reporte_avance
        # ----------------------------
        task_reporte_avance_model = self.env['project.task.reporte_avance']
        # Creación permitida
        vals = {
            'fecha': "2006-07-19",
            'project_id': self.ref('project_edt_idu.project_id_01'),
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "terminado",
            'registro_progreso_ids': [
                (4, self.ref('project_edt_idu.registro_progreso_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        task_reporte_avance = task_reporte_avance_model.sudo(user_group_project_user_01).create(vals)

        # Creación NO permitida
        vals = {
            'fecha': "1970-12-14",
            'project_id': self.ref('project_edt_idu.project_id_01'),
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "terminado",
            'registro_progreso_ids': [
                (4, self.ref('project_edt_idu.registro_progreso_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        try:
            task_reporte_avance = task_reporte_avance_model.sudo(user_group_project_user_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(task_reporte_avance_model))

    def test_020_project_group_project_user_write(self):
        """ project.group_project_user Verifica reglas de dominio en operación WRITE """
        user_group_project_user_01 = self.ref('project_edt_idu.group_project_user_user_01')
        user_group_project_user_02 = self.ref('project_edt_idu.group_project_user_user_02')

        # ----------------------------
        # project.edt
        # ----------------------------
        edt_model = self.env['project.edt']
        # Actualización permitida
        vals = {
            'name': "Eos ut eum dicta deserunt animi recusandae.",
            'sequence': 87516499,
            'ms_project_guid': "Mollitia quaerat tenetur commodi repellendus.",
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "cancelado",
            'fecha_planeada_inicio': "2001-09-25",
            'fecha_planeada_fin': "1970-02-22",
            'fecha_inicio': "2010-11-21",
            'fecha_fin': "1973-10-30",
            'peso': 85034281.6308,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 92248651.6259,
            'costo': 64767456.6298,
            'progreso': 58126042.4474,
            'project_id': self.ref('project_edt_idu.project_id_01'),
            'task_ids': [
                (4, self.ref('project_edt_idu.task_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'parent_id': self.ref('project_edt_idu.parent_id_01'),
            'child_ids': [
                (4, self.ref('project_edt_idu.child_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'programador_id': self.ref('project_edt_idu.programador_id_01'),
            'progreso_aprobado': 27590979.5995,
        }
        edt = edt_model.sudo(user_group_project_user_01).search([], limit=1)
        edt.sudo(user_group_project_user_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Laboriosam qui eum quia qui numquam expedita laborum.",
            'sequence': 65889415,
            'ms_project_guid': "Quis architecto qui officiis veritatis pariatur est.",
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "aplazado",
            'fecha_planeada_inicio': "2014-11-08",
            'fecha_planeada_fin': "1973-02-19",
            'fecha_inicio': "1991-06-30",
            'fecha_fin': "2007-01-24",
            'peso': 7634751.21428,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 79097313.6267,
            'costo': 75227684.9132,
            'progreso': 2076683.75649,
            'project_id': self.ref('project_edt_idu.project_id_01'),
            'task_ids': [
                (4, self.ref('project_edt_idu.task_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'parent_id': self.ref('project_edt_idu.parent_id_01'),
            'child_ids': [
                (4, self.ref('project_edt_idu.child_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'programador_id': self.ref('project_edt_idu.programador_id_01'),
            'progreso_aprobado': 20725049.1765,
        }
        edt = edt_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            edt.sudo(user_group_project_user_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(edt_model))

        # ----------------------------
        # project.task
        # ----------------------------
        task_model = self.env['project.task']
        # Actualización permitida
        vals = {
            'edt_id': self.ref('project_edt_idu.edt_id_01'),
            'ms_project_guid': "Quis repellendus est quaerat.",
            'edt_peso': 21316073,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 65071839.3281,
            'costo': 29743588.0208,
            'progreso': 8132831.97318,
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'progreso_metodo': "manual",
            'fecha_planeada_inicio': "1998-10-20 22:08:54",
            'fecha_planeada_fin': "1983-07-13 10:52:39",
            'pendiente_ids': [
                (4, self.ref('project_edt_idu.pendiente_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'registro_progreso_ids': [
                (4, self.ref('project_edt_idu.registro_progreso_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'progreso_aprobado': 4191805.92481,
            'terminado': False,
            'cantidad_planeada': 82435269.3249,
            'cantidad': 58463563.7896,
            'product_id': self.ref('project_edt_idu.product_id_01'),
        }
        task = task_model.sudo(user_group_project_user_01).search([], limit=1)
        task.sudo(user_group_project_user_01).write(vals)

        # Actualización NO permitida
        vals = {
            'edt_id': self.ref('project_edt_idu.edt_id_01'),
            'ms_project_guid': "Hic aut quaerat et.",
            'edt_peso': 50260949,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 68496900.0262,
            'costo': 78402153.8662,
            'progreso': 62126004.904,
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'progreso_metodo': "manual",
            'fecha_planeada_inicio': "1995-02-21 17:44:54",
            'fecha_planeada_fin': "1985-07-05 04:38:26",
            'pendiente_ids': [
                (4, self.ref('project_edt_idu.pendiente_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'registro_progreso_ids': [
                (4, self.ref('project_edt_idu.registro_progreso_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'progreso_aprobado': 37969759.679,
            'terminado': False,
            'cantidad_planeada': 2136838.52109,
            'cantidad': 64548961.0161,
            'product_id': self.ref('project_edt_idu.product_id_01'),
        }
        task = task_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            task.sudo(user_group_project_user_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(task_model))

        # ----------------------------
        # project.project
        # ----------------------------
        project_model = self.env['project.project']
        # Actualización permitida
        vals = {
            'edt_raiz_id': self.ref('project_edt_idu.edt_raiz_id_01'),
            'edt_ids': [
                (4, self.ref('project_edt_idu.edt_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'programador_id': self.ref('project_edt_idu.programador_id_01'),
        }
        project = project_model.sudo(user_group_project_user_01).search([], limit=1)
        project.sudo(user_group_project_user_01).write(vals)

        # Actualización NO permitida
        vals = {
            'edt_raiz_id': self.ref('project_edt_idu.edt_raiz_id_01'),
            'edt_ids': [
                (4, self.ref('project_edt_idu.edt_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
            'programador_id': self.ref('project_edt_idu.programador_id_01'),
        }
        project = project_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            project.sudo(user_group_project_user_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(project_model))

        # ----------------------------
        # project.task.registro_progreso
        # ----------------------------
        task_registro_progreso_model = self.env['project.task.registro_progreso']
        # Actualización permitida
        vals = {
            'name': "Sed dicta ad ex et dolores consequatur.",
            'fecha': "1972-07-03",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'porcentaje': 50702233,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo': 26255542.4803,
            'fecha_aprobacion': "2011-08-20 05:35:47",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'nivel_alerta': "ninguno",
            'novedad': "Illo numquam est est dignissimos praesentium.",
            'reporte_avance_id': self.ref('project_edt_idu.reporte_avance_id_01'),
            'cantidad': 16423657.1578,
        }
        task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_user_01).search([], limit=1)
        task_registro_progreso.sudo(user_group_project_user_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Odio quaerat quibusdam minus necessitatibus.",
            'fecha': "1993-04-17",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'porcentaje': 49942721,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo': 22789930.569,
            'fecha_aprobacion': "2014-09-13 13:00:26",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'nivel_alerta': "medio",
            'novedad': "Dolorum cum culpa quos quod voluptas ut ut.",
            'reporte_avance_id': self.ref('project_edt_idu.reporte_avance_id_01'),
            'cantidad': 55816209.7236,
        }
        task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            task_registro_progreso.sudo(user_group_project_user_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(task_registro_progreso_model))

        # ----------------------------
        # project.task.pendiente
        # ----------------------------
        task_pendiente_model = self.env['project.task.pendiente']
        # Actualización permitida
        vals = {
            'name': "Pariatur est ullam voluptatem cum expedita.",
            'sequence': 64163693,
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'peso': 90571224,
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'fecha_terminacion': "2014-03-01 18:33:15",
            'fecha_aprobacion': "1999-11-22 18:40:35",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
        }
        task_pendiente = task_pendiente_model.sudo(user_group_project_user_01).search([], limit=1)
        task_pendiente.sudo(user_group_project_user_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Voluptas corrupti aspernatur quisquam dolorem assumenda non pariatur.",
            'sequence': 8710477,
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'peso': 5818008,
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'fecha_terminacion': "1994-08-17 23:43:21",
            'fecha_aprobacion': "2006-03-23 02:38:25",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
        }
        task_pendiente = task_pendiente_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            task_pendiente.sudo(user_group_project_user_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(task_pendiente_model))

        # ----------------------------
        # project.predecesor
        # ----------------------------
        predecesor_model = self.env['project.predecesor']
        # Actualización permitida
        vals = {
            'origen_res_model': "tarea",
            'origen_res_id': 69027730,
            'destino_res_model': "tarea",
            'destino_res_id': 57240926,
            'tipo': "e_e",
        }
        predecesor = predecesor_model.sudo(user_group_project_user_01).search([], limit=1)
        predecesor.sudo(user_group_project_user_01).write(vals)

        # Actualización NO permitida
        vals = {
            'origen_res_model': "edt",
            'origen_res_id': 4703700,
            'destino_res_model': "tarea",
            'destino_res_id': 80203866,
            'tipo': "e_e",
        }
        predecesor = predecesor_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            predecesor.sudo(user_group_project_user_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(predecesor_model))

        # ----------------------------
        # project.task.reporte_avance
        # ----------------------------
        task_reporte_avance_model = self.env['project.task.reporte_avance']
        # Actualización permitida
        vals = {
            'fecha': "2008-06-06",
            'project_id': self.ref('project_edt_idu.project_id_01'),
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "por_revisar",
            'registro_progreso_ids': [
                (4, self.ref('project_edt_idu.registro_progreso_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        task_reporte_avance = task_reporte_avance_model.sudo(user_group_project_user_01).search([], limit=1)
        task_reporte_avance.sudo(user_group_project_user_01).write(vals)

        # Actualización NO permitida
        vals = {
            'fecha': "1987-10-13",
            'project_id': self.ref('project_edt_idu.project_id_01'),
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "terminado",
            'registro_progreso_ids': [
                (4, self.ref('project_edt_idu.registro_progreso_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        task_reporte_avance = task_reporte_avance_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            task_reporte_avance.sudo(user_group_project_user_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(task_reporte_avance_model))

    def test_030_project_group_project_user_unlink(self):
        """ project.group_project_user Verifica reglas de dominio en operación UNLINK - Delete """
        user_group_project_user_01 = self.ref('project_edt_idu.group_project_user_user_01')
        user_group_project_user_02 = self.ref('project_edt_idu.group_project_user_user_02')

        # ----------------------------
        # project.edt
        # ----------------------------
        edt_model = self.env['project.edt']
        # Eliminación permitida
        edt = edt_model.sudo(user_group_project_user_01).search([], limit=1)
        edt.sudo(user_group_project_user_01).unlink()

        # Eliminación NO permitida
        edt = edt_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            edt.sudo(user_group_project_user_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(edt_model))

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
        # project.task.registro_progreso
        # ----------------------------
        task_registro_progreso_model = self.env['project.task.registro_progreso']
        # Eliminación permitida
        task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_user_01).search([], limit=1)
        task_registro_progreso.sudo(user_group_project_user_01).unlink()

        # Eliminación NO permitida
        task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            task_registro_progreso.sudo(user_group_project_user_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(task_registro_progreso_model))

        # ----------------------------
        # project.task.pendiente
        # ----------------------------
        task_pendiente_model = self.env['project.task.pendiente']
        # Eliminación permitida
        task_pendiente = task_pendiente_model.sudo(user_group_project_user_01).search([], limit=1)
        task_pendiente.sudo(user_group_project_user_01).unlink()

        # Eliminación NO permitida
        task_pendiente = task_pendiente_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            task_pendiente.sudo(user_group_project_user_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(task_pendiente_model))

        # ----------------------------
        # project.predecesor
        # ----------------------------
        predecesor_model = self.env['project.predecesor']
        # Eliminación permitida
        predecesor = predecesor_model.sudo(user_group_project_user_01).search([], limit=1)
        predecesor.sudo(user_group_project_user_01).unlink()

        # Eliminación NO permitida
        predecesor = predecesor_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            predecesor.sudo(user_group_project_user_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(predecesor_model))

        # ----------------------------
        # project.task.reporte_avance
        # ----------------------------
        task_reporte_avance_model = self.env['project.task.reporte_avance']
        # Eliminación permitida
        task_reporte_avance = task_reporte_avance_model.sudo(user_group_project_user_01).search([], limit=1)
        task_reporte_avance.sudo(user_group_project_user_01).unlink()

        # Eliminación NO permitida
        task_reporte_avance = task_reporte_avance_model.sudo(user_group_project_user_01).search([], limit=1)
        try:
            task_reporte_avance.sudo(user_group_project_user_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(task_reporte_avance_model))


if __name__ == '__main__':
    unittest2.main()