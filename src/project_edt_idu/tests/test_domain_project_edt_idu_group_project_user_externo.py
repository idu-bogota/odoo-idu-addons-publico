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
        user_group_project_user_externo_01 = self.ref('project_edt_idu.group_project_user_externo_user_01')
        user_group_project_user_externo_02 = self.ref('project_edt_idu.group_project_user_externo_user_02')

        # ----------------------------
        # project.edt
        # ----------------------------
        edt_model = self.env['project.edt']
        self.assertEqual(1000, edt_model.sudo(user_group_project_user_externo_01).search_count([]))
        self.assertEqual(1000, edt_model.sudo(user_group_project_user_externo_02).search_count([]))

        # ----------------------------
        # project.task
        # ----------------------------
        task_model = self.env['project.task']
        self.assertEqual(1000, task_model.sudo(user_group_project_user_externo_01).search_count([]))
        self.assertEqual(1000, task_model.sudo(user_group_project_user_externo_02).search_count([]))

        # ----------------------------
        # project.project
        # ----------------------------
        project_model = self.env['project.project']
        self.assertEqual(1000, project_model.sudo(user_group_project_user_externo_01).search_count([]))
        self.assertEqual(1000, project_model.sudo(user_group_project_user_externo_02).search_count([]))

        # ----------------------------
        # project.task.registro_progreso
        # ----------------------------
        task_registro_progreso_model = self.env['project.task.registro_progreso']
        self.assertEqual(1000, task_registro_progreso_model.sudo(user_group_project_user_externo_01).search_count([]))
        self.assertEqual(1000, task_registro_progreso_model.sudo(user_group_project_user_externo_02).search_count([]))

        # ----------------------------
        # project.task.pendiente
        # ----------------------------
        task_pendiente_model = self.env['project.task.pendiente']
        self.assertEqual(1000, task_pendiente_model.sudo(user_group_project_user_externo_01).search_count([]))
        self.assertEqual(1000, task_pendiente_model.sudo(user_group_project_user_externo_02).search_count([]))

        # ----------------------------
        # project.predecesor
        # ----------------------------
        predecesor_model = self.env['project.predecesor']
        self.assertEqual(1000, predecesor_model.sudo(user_group_project_user_externo_01).search_count([]))
        self.assertEqual(1000, predecesor_model.sudo(user_group_project_user_externo_02).search_count([]))

        # ----------------------------
        # project.task.reporte_avance
        # ----------------------------
        task_reporte_avance_model = self.env['project.task.reporte_avance']
        self.assertEqual(1000, task_reporte_avance_model.sudo(user_group_project_user_externo_01).search_count([]))
        self.assertEqual(1000, task_reporte_avance_model.sudo(user_group_project_user_externo_02).search_count([]))

    def test_010_project_edt_idu_group_project_user_externo_create(self):
        """ project_edt_idu.group_project_user_externo Verifica reglas de dominio en operación CREATE """
        user_group_project_user_externo_01 = self.ref('project_edt_idu.group_project_user_externo_user_01')
        user_group_project_user_externo_02 = self.ref('project_edt_idu.group_project_user_externo_user_02')

        # ----------------------------
        # project.edt
        # ----------------------------
        edt_model = self.env['project.edt']
        # Creación permitida
        vals = {
            'name': "Occaecati ut repellat vitae quo.",
            'sequence': 11076668,
            'ms_project_guid': "Soluta qui recusandae sit exercitationem harum commodi.",
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "cerrado",
            'fecha_planeada_inicio': "2013-05-16",
            'fecha_planeada_fin': "1986-08-16",
            'fecha_inicio': "2013-03-20",
            'fecha_fin': "1993-05-08",
            'peso': 16985530.7376,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 20282607.844,
            'costo': 64143696.7382,
            'progreso': 93827533.127,
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
            'progreso_aprobado': 14357371.7655,
        }
        edt = edt_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Quis qui illo omnis aspernatur sit sunt.",
            'sequence': 24706033,
            'ms_project_guid': "Et officia sit deleniti tenetur.",
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "cerrado",
            'fecha_planeada_inicio': "1981-09-02",
            'fecha_planeada_fin': "1983-05-07",
            'fecha_inicio': "1970-10-19",
            'fecha_fin': "1972-02-20",
            'peso': 70506069.7855,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 19235463.8008,
            'costo': 22674605.1328,
            'progreso': 27682136.5046,
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
            'progreso_aprobado': 42644591.0003,
        }
        try:
            edt = edt_model.sudo(user_group_project_user_externo_01).create(vals)
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
            'ms_project_guid': "Rerum excepturi pariatur ut amet.",
            'edt_peso': 48684715,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 46606325.918,
            'costo': 16396633.9262,
            'progreso': 94755918.9358,
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'progreso_metodo': "manual",
            'fecha_planeada_inicio': "1988-10-05 18:54:11",
            'fecha_planeada_fin': "2003-10-20 01:03:11",
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
            'progreso_aprobado': 91357132.662,
            'terminado': False,
            'cantidad_planeada': 90718456.7412,
            'cantidad': 15453949.6732,
            'product_id': self.ref('project_edt_idu.product_id_01'),
        }
        task = task_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'edt_id': self.ref('project_edt_idu.edt_id_01'),
            'ms_project_guid': "Non vitae dolores commodi quibusdam.",
            'edt_peso': 17577830,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 2878184.25321,
            'costo': 9085608.29972,
            'progreso': 28888171.5819,
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'progreso_metodo': "manual",
            'fecha_planeada_inicio': "1995-10-02 15:58:49",
            'fecha_planeada_fin': "2012-07-15 19:32:04",
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
            'progreso_aprobado': 35093259.795,
            'terminado': True,
            'cantidad_planeada': 36791647.0945,
            'cantidad': 22798837.5794,
            'product_id': self.ref('project_edt_idu.product_id_01'),
        }
        try:
            task = task_model.sudo(user_group_project_user_externo_01).create(vals)
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
        project = project_model.sudo(user_group_project_user_externo_01).create(vals)

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
            project = project_model.sudo(user_group_project_user_externo_01).create(vals)
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
            'name': "Sit culpa odit labore tempore ut omnis.",
            'fecha': "2001-09-13",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'porcentaje': 83215275,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo': 69796446.5671,
            'fecha_aprobacion': "2012-12-01 20:49:44",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'nivel_alerta': "bajo",
            'novedad': "Expedita occaecati necessitatibus suscipit rerum nisi aut sit.",
            'reporte_avance_id': self.ref('project_edt_idu.reporte_avance_id_01'),
            'cantidad': 90021583.6751,
        }
        task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Harum ut ipsa doloribus et ea.",
            'fecha': "2009-01-23",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'porcentaje': 86449048,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo': 62888475.0963,
            'fecha_aprobacion': "2002-04-23 19:15:20",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'nivel_alerta': "medio",
            'novedad': "Quis id velit quis at.",
            'reporte_avance_id': self.ref('project_edt_idu.reporte_avance_id_01'),
            'cantidad': 606592.752188,
        }
        try:
            task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_user_externo_01).create(vals)
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
            'name': "Quia suscipit et facere quae officia sed.",
            'sequence': 99421629,
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'peso': 2915563,
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'fecha_terminacion': "1983-11-07 09:13:22",
            'fecha_aprobacion': "1975-09-30 05:15:01",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
        }
        task_pendiente = task_pendiente_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Esse ut nulla voluptatem qui.",
            'sequence': 12679709,
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'peso': 67540218,
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'fecha_terminacion': "1990-07-14 08:49:35",
            'fecha_aprobacion': "1970-09-13 11:19:35",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
        }
        try:
            task_pendiente = task_pendiente_model.sudo(user_group_project_user_externo_01).create(vals)
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
            'origen_res_model': "tarea",
            'origen_res_id': 96068957,
            'destino_res_model': "edt",
            'destino_res_id': 262933,
            'tipo': "s_s",
        }
        predecesor = predecesor_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'origen_res_model': "edt",
            'origen_res_id': 59554884,
            'destino_res_model': "tarea",
            'destino_res_id': 93327289,
            'tipo': "s_s",
        }
        try:
            predecesor = predecesor_model.sudo(user_group_project_user_externo_01).create(vals)
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
            'fecha': "1984-06-11",
            'project_id': self.ref('project_edt_idu.project_id_01'),
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "borrador",
            'registro_progreso_ids': [
                (4, self.ref('project_edt_idu.registro_progreso_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        task_reporte_avance = task_reporte_avance_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'fecha': "2006-03-27",
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
            task_reporte_avance = task_reporte_avance_model.sudo(user_group_project_user_externo_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(task_reporte_avance_model))

    def test_020_project_edt_idu_group_project_user_externo_write(self):
        """ project_edt_idu.group_project_user_externo Verifica reglas de dominio en operación WRITE """
        user_group_project_user_externo_01 = self.ref('project_edt_idu.group_project_user_externo_user_01')
        user_group_project_user_externo_02 = self.ref('project_edt_idu.group_project_user_externo_user_02')

        # ----------------------------
        # project.edt
        # ----------------------------
        edt_model = self.env['project.edt']
        # Actualización permitida
        vals = {
            'name': "Quasi explicabo ea consequatur consequatur deleniti.",
            'sequence': 59212905,
            'ms_project_guid': "Iusto quia consequuntur veniam quam.",
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "abierto",
            'fecha_planeada_inicio': "1973-02-05",
            'fecha_planeada_fin': "2003-08-20",
            'fecha_inicio': "1983-07-21",
            'fecha_fin': "1971-01-06",
            'peso': 41772605.3458,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 86726733.1474,
            'costo': 43844888.6975,
            'progreso': 20262596.3016,
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
            'progreso_aprobado': 7818670.30042,
        }
        edt = edt_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        edt.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Molestiae recusandae omnis sit laborum aut.",
            'sequence': 50441288,
            'ms_project_guid': "Voluptatibus nulla omnis repellat qui id eius.",
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "aplazado",
            'fecha_planeada_inicio': "2004-06-09",
            'fecha_planeada_fin': "1976-11-04",
            'fecha_inicio': "2013-11-02",
            'fecha_fin': "1988-09-19",
            'peso': 91115481.3668,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 44341971.8092,
            'costo': 92109934.6452,
            'progreso': 32524719.5389,
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
            'progreso_aprobado': 5734837.46517,
        }
        edt = edt_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            edt.sudo(user_group_project_user_externo_01).write(vals)
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
            'ms_project_guid': "Voluptatem cumque cumque eum ut.",
            'edt_peso': 3619501,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 94631673.2265,
            'costo': 74514367.1247,
            'progreso': 50030067.3627,
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'progreso_metodo': "pendientes",
            'fecha_planeada_inicio': "1973-10-14 16:12:09",
            'fecha_planeada_fin': "1996-07-12 19:07:43",
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
            'progreso_aprobado': 23381539.6309,
            'terminado': True,
            'cantidad_planeada': 39408256.5653,
            'cantidad': 76530084.6343,
            'product_id': self.ref('project_edt_idu.product_id_01'),
        }
        task = task_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        task.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'edt_id': self.ref('project_edt_idu.edt_id_01'),
            'ms_project_guid': "Tempora officia sunt minima vel.",
            'edt_peso': 11540455,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 68030006.9516,
            'costo': 69039583.388,
            'progreso': 81999375.7431,
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'progreso_metodo': "pendientes",
            'fecha_planeada_inicio': "2005-09-09 14:24:16",
            'fecha_planeada_fin': "2006-12-29 16:49:58",
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
            'progreso_aprobado': 85954918.1572,
            'terminado': False,
            'cantidad_planeada': 35586119.6167,
            'cantidad': 29820478.7648,
            'product_id': self.ref('project_edt_idu.product_id_01'),
        }
        task = task_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            task.sudo(user_group_project_user_externo_01).write(vals)
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
        project = project_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        project.sudo(user_group_project_user_externo_01).write(vals)

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
        project = project_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            project.sudo(user_group_project_user_externo_01).write(vals)
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
            'name': "Sit autem voluptatem consequatur sapiente.",
            'fecha': "1974-09-23",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'porcentaje': 62613980,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo': 25351894.6697,
            'fecha_aprobacion': "1971-12-05 12:38:22",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'nivel_alerta': "medio",
            'novedad': "Ea molestiae ab placeat quis natus et in.",
            'reporte_avance_id': self.ref('project_edt_idu.reporte_avance_id_01'),
            'cantidad': 17449630.5961,
        }
        task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        task_registro_progreso.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Aliquid quae qui dolorem.",
            'fecha': "1982-03-03",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'porcentaje': 11719914,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo': 18633039.7523,
            'fecha_aprobacion': "1987-08-14 08:50:40",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'nivel_alerta': "medio",
            'novedad': "Reprehenderit ut dolores dolorum est consectetur ut.",
            'reporte_avance_id': self.ref('project_edt_idu.reporte_avance_id_01'),
            'cantidad': 62755665.0763,
        }
        task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            task_registro_progreso.sudo(user_group_project_user_externo_01).write(vals)
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
            'name': "Quia odit nemo rerum ut.",
            'sequence': 79915288,
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'peso': 67189491,
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'fecha_terminacion': "2010-03-20 23:56:32",
            'fecha_aprobacion': "1998-06-14 13:23:53",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
        }
        task_pendiente = task_pendiente_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        task_pendiente.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Repudiandae saepe officia alias quibusdam quia exercitationem sed.",
            'sequence': 95524354,
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'peso': 34686141,
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'fecha_terminacion': "1977-09-23 23:08:52",
            'fecha_aprobacion': "1980-07-30 11:36:35",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
        }
        task_pendiente = task_pendiente_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            task_pendiente.sudo(user_group_project_user_externo_01).write(vals)
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
            'origen_res_id': 96583343,
            'destino_res_model': "tarea",
            'destino_res_id': 60067855,
            'tipo': "s_e",
        }
        predecesor = predecesor_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        predecesor.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'origen_res_model': "edt",
            'origen_res_id': 67537670,
            'destino_res_model': "edt",
            'destino_res_id': 84090733,
            'tipo': "e_e",
        }
        predecesor = predecesor_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            predecesor.sudo(user_group_project_user_externo_01).write(vals)
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
            'fecha': "1994-04-08",
            'project_id': self.ref('project_edt_idu.project_id_01'),
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "borrador",
            'registro_progreso_ids': [
                (4, self.ref('project_edt_idu.registro_progreso_ids_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
        }
        task_reporte_avance = task_reporte_avance_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        task_reporte_avance.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'fecha': "2000-05-18",
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
        task_reporte_avance = task_reporte_avance_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            task_reporte_avance.sudo(user_group_project_user_externo_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(task_reporte_avance_model))

    def test_030_project_edt_idu_group_project_user_externo_unlink(self):
        """ project_edt_idu.group_project_user_externo Verifica reglas de dominio en operación UNLINK - Delete """
        user_group_project_user_externo_01 = self.ref('project_edt_idu.group_project_user_externo_user_01')
        user_group_project_user_externo_02 = self.ref('project_edt_idu.group_project_user_externo_user_02')

        # ----------------------------
        # project.edt
        # ----------------------------
        edt_model = self.env['project.edt']
        # Eliminación permitida
        edt = edt_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        edt.sudo(user_group_project_user_externo_01).unlink()

        # Eliminación NO permitida
        edt = edt_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            edt.sudo(user_group_project_user_externo_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(edt_model))

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
        # project.task.registro_progreso
        # ----------------------------
        task_registro_progreso_model = self.env['project.task.registro_progreso']
        # Eliminación permitida
        task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        task_registro_progreso.sudo(user_group_project_user_externo_01).unlink()

        # Eliminación NO permitida
        task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            task_registro_progreso.sudo(user_group_project_user_externo_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(task_registro_progreso_model))

        # ----------------------------
        # project.task.pendiente
        # ----------------------------
        task_pendiente_model = self.env['project.task.pendiente']
        # Eliminación permitida
        task_pendiente = task_pendiente_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        task_pendiente.sudo(user_group_project_user_externo_01).unlink()

        # Eliminación NO permitida
        task_pendiente = task_pendiente_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            task_pendiente.sudo(user_group_project_user_externo_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(task_pendiente_model))

        # ----------------------------
        # project.predecesor
        # ----------------------------
        predecesor_model = self.env['project.predecesor']
        # Eliminación permitida
        predecesor = predecesor_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        predecesor.sudo(user_group_project_user_externo_01).unlink()

        # Eliminación NO permitida
        predecesor = predecesor_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            predecesor.sudo(user_group_project_user_externo_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(predecesor_model))

        # ----------------------------
        # project.task.reporte_avance
        # ----------------------------
        task_reporte_avance_model = self.env['project.task.reporte_avance']
        # Eliminación permitida
        task_reporte_avance = task_reporte_avance_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        task_reporte_avance.sudo(user_group_project_user_externo_01).unlink()

        # Eliminación NO permitida
        task_reporte_avance = task_reporte_avance_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            task_reporte_avance.sudo(user_group_project_user_externo_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(task_reporte_avance_model))


if __name__ == '__main__':
    unittest2.main()