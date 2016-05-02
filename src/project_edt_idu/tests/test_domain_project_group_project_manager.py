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
        user_group_project_manager_01 = self.ref('project_edt_idu.group_project_manager_user_01')
        user_group_project_manager_02 = self.ref('project_edt_idu.group_project_manager_user_02')

        # ----------------------------
        # project.edt
        # ----------------------------
        edt_model = self.env['project.edt']
        self.assertEqual(1000, edt_model.sudo(user_group_project_manager_01).search_count([]))
        self.assertEqual(1000, edt_model.sudo(user_group_project_manager_02).search_count([]))

        # ----------------------------
        # project.task
        # ----------------------------
        task_model = self.env['project.task']
        self.assertEqual(1000, task_model.sudo(user_group_project_manager_01).search_count([]))
        self.assertEqual(1000, task_model.sudo(user_group_project_manager_02).search_count([]))

        # ----------------------------
        # project.project
        # ----------------------------
        project_model = self.env['project.project']
        self.assertEqual(1000, project_model.sudo(user_group_project_manager_01).search_count([]))
        self.assertEqual(1000, project_model.sudo(user_group_project_manager_02).search_count([]))

        # ----------------------------
        # project.task.registro_progreso
        # ----------------------------
        task_registro_progreso_model = self.env['project.task.registro_progreso']
        self.assertEqual(1000, task_registro_progreso_model.sudo(user_group_project_manager_01).search_count([]))
        self.assertEqual(1000, task_registro_progreso_model.sudo(user_group_project_manager_02).search_count([]))

        # ----------------------------
        # project.task.pendiente
        # ----------------------------
        task_pendiente_model = self.env['project.task.pendiente']
        self.assertEqual(1000, task_pendiente_model.sudo(user_group_project_manager_01).search_count([]))
        self.assertEqual(1000, task_pendiente_model.sudo(user_group_project_manager_02).search_count([]))

        # ----------------------------
        # project.predecesor
        # ----------------------------
        predecesor_model = self.env['project.predecesor']
        self.assertEqual(1000, predecesor_model.sudo(user_group_project_manager_01).search_count([]))
        self.assertEqual(1000, predecesor_model.sudo(user_group_project_manager_02).search_count([]))

        # ----------------------------
        # project.task.reporte_avance
        # ----------------------------
        task_reporte_avance_model = self.env['project.task.reporte_avance']
        self.assertEqual(1000, task_reporte_avance_model.sudo(user_group_project_manager_01).search_count([]))
        self.assertEqual(1000, task_reporte_avance_model.sudo(user_group_project_manager_02).search_count([]))

    def test_010_project_group_project_manager_create(self):
        """ project.group_project_manager Verifica reglas de dominio en operación CREATE """
        user_group_project_manager_01 = self.ref('project_edt_idu.group_project_manager_user_01')
        user_group_project_manager_02 = self.ref('project_edt_idu.group_project_manager_user_02')

        # ----------------------------
        # project.edt
        # ----------------------------
        edt_model = self.env['project.edt']
        # Creación permitida
        vals = {
            'name': "Voluptatem sit mollitia molestiae odit quod dolores.",
            'sequence': 86328473,
            'ms_project_guid': "Dicta explicabo ex quos dolor.",
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "cerrado",
            'fecha_planeada_inicio': "1998-08-02",
            'fecha_planeada_fin': "1972-07-19",
            'fecha_inicio': "2001-08-14",
            'fecha_fin': "1979-03-31",
            'peso': 52957451.8823,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 69270039.1226,
            'costo': 38401926.4209,
            'progreso': 53819523.7212,
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
            'progreso_aprobado': 41514740.7576,
        }
        edt = edt_model.sudo(user_group_project_manager_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Iste sit praesentium et mollitia.",
            'sequence': 53879144,
            'ms_project_guid': "Voluptas ea incidunt excepturi animi maxime aut atque.",
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "cerrado",
            'fecha_planeada_inicio': "2002-05-07",
            'fecha_planeada_fin': "1993-01-03",
            'fecha_inicio': "1994-12-23",
            'fecha_fin': "1997-08-21",
            'peso': 20764938.8398,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 59907233.2269,
            'costo': 28045759.1098,
            'progreso': 82443027.7765,
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
            'progreso_aprobado': 30511437.1363,
        }
        try:
            edt = edt_model.sudo(user_group_project_manager_01).create(vals)
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
            'ms_project_guid': "Quod molestiae explicabo omnis consequuntur nostrum nam.",
            'edt_peso': 49312186,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 76687286.9724,
            'costo': 35033163.0254,
            'progreso': 75889824.5086,
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'progreso_metodo': "manual",
            'fecha_planeada_inicio': "2010-11-11 05:09:18",
            'fecha_planeada_fin': "2005-06-24 01:10:27",
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
            'progreso_aprobado': 47447000.4824,
            'terminado': False,
            'cantidad_planeada': 70904491.3939,
            'cantidad': 77093726.8999,
            'product_id': self.ref('project_edt_idu.product_id_01'),
        }
        task = task_model.sudo(user_group_project_manager_01).create(vals)

        # Creación NO permitida
        vals = {
            'edt_id': self.ref('project_edt_idu.edt_id_01'),
            'ms_project_guid': "Commodi ut nulla consequatur totam est quod ipsum dolores.",
            'edt_peso': 3013632,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 98465895.7087,
            'costo': 61369379.2772,
            'progreso': 94111913.4548,
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'progreso_metodo': "pendientes",
            'fecha_planeada_inicio': "2005-09-29 10:34:41",
            'fecha_planeada_fin': "2007-01-08 01:57:46",
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
            'progreso_aprobado': 59814272.5556,
            'terminado': True,
            'cantidad_planeada': 20521468.2309,
            'cantidad': 92634409.6181,
            'product_id': self.ref('project_edt_idu.product_id_01'),
        }
        try:
            task = task_model.sudo(user_group_project_manager_01).create(vals)
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
        project = project_model.sudo(user_group_project_manager_01).create(vals)

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
            project = project_model.sudo(user_group_project_manager_01).create(vals)
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
            'name': "Velit esse deleniti beatae est aut illo.",
            'fecha': "1976-03-30",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'porcentaje': 33468381,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo': 79612140.5719,
            'fecha_aprobacion': "1987-10-01 02:42:02",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'nivel_alerta': "bajo",
            'novedad': "Omnis mollitia modi est sit placeat blanditiis culpa.",
            'reporte_avance_id': self.ref('project_edt_idu.reporte_avance_id_01'),
            'cantidad': 82101567.8629,
        }
        task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_manager_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Porro officiis et corrupti.",
            'fecha': "1976-11-06",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'porcentaje': 51903116,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo': 58842723.9526,
            'fecha_aprobacion': "2012-09-10 17:39:36",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'nivel_alerta': "ninguno",
            'novedad': "Eaque officiis qui velit aut saepe.",
            'reporte_avance_id': self.ref('project_edt_idu.reporte_avance_id_01'),
            'cantidad': 71634189.4941,
        }
        try:
            task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_manager_01).create(vals)
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
            'name': "Rerum possimus quia sunt atque esse.",
            'sequence': 7806318,
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'peso': 45733305,
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'fecha_terminacion': "1989-10-05 04:38:11",
            'fecha_aprobacion': "2009-03-07 20:21:26",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
        }
        task_pendiente = task_pendiente_model.sudo(user_group_project_manager_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Distinctio et ut cupiditate iure est.",
            'sequence': 73953168,
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'peso': 58036496,
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'fecha_terminacion': "1988-11-23 00:51:12",
            'fecha_aprobacion': "2010-08-15 05:03:28",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
        }
        try:
            task_pendiente = task_pendiente_model.sudo(user_group_project_manager_01).create(vals)
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
            'origen_res_id': 88965780,
            'destino_res_model': "edt",
            'destino_res_id': 14351673,
            'tipo': "s_s",
        }
        predecesor = predecesor_model.sudo(user_group_project_manager_01).create(vals)

        # Creación NO permitida
        vals = {
            'origen_res_model': "edt",
            'origen_res_id': 2397363,
            'destino_res_model': "tarea",
            'destino_res_id': 401586,
            'tipo': "s_e",
        }
        try:
            predecesor = predecesor_model.sudo(user_group_project_manager_01).create(vals)
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
            'fecha': "2004-09-24",
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
        task_reporte_avance = task_reporte_avance_model.sudo(user_group_project_manager_01).create(vals)

        # Creación NO permitida
        vals = {
            'fecha': "1982-09-30",
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
            task_reporte_avance = task_reporte_avance_model.sudo(user_group_project_manager_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(task_reporte_avance_model))

    def test_020_project_group_project_manager_write(self):
        """ project.group_project_manager Verifica reglas de dominio en operación WRITE """
        user_group_project_manager_01 = self.ref('project_edt_idu.group_project_manager_user_01')
        user_group_project_manager_02 = self.ref('project_edt_idu.group_project_manager_user_02')

        # ----------------------------
        # project.edt
        # ----------------------------
        edt_model = self.env['project.edt']
        # Actualización permitida
        vals = {
            'name': "Repudiandae sapiente quo quisquam sequi minus maiores.",
            'sequence': 74467080,
            'ms_project_guid': "Ut sunt maiores sunt quo.",
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "cerrado",
            'fecha_planeada_inicio': "1977-02-11",
            'fecha_planeada_fin': "2012-01-10",
            'fecha_inicio': "1982-12-22",
            'fecha_fin': "2000-06-02",
            'peso': 62559295.5775,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 20319542.3408,
            'costo': 10782856.0887,
            'progreso': 92455897.7967,
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
            'progreso_aprobado': 72987931.0563,
        }
        edt = edt_model.sudo(user_group_project_manager_01).search([], limit=1)
        edt.sudo(user_group_project_manager_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Facilis consequatur officiis animi libero.",
            'sequence': 82741730,
            'ms_project_guid': "Dolore commodi eum et reprehenderit qui.",
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "abierto",
            'fecha_planeada_inicio': "1988-12-02",
            'fecha_planeada_fin': "1982-12-09",
            'fecha_inicio': "2012-08-20",
            'fecha_fin': "2000-04-27",
            'peso': 70592555.1918,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 72150967.9998,
            'costo': 97498658.7199,
            'progreso': 78489058.8914,
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
            'progreso_aprobado': 97992918.724,
        }
        edt = edt_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            edt.sudo(user_group_project_manager_01).write(vals)
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
            'ms_project_guid': "Corrupti illum repellendus dolorem molestiae.",
            'edt_peso': 16041985,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 88025683.9555,
            'costo': 3875287.94777,
            'progreso': 42216123.8984,
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'progreso_metodo': "manual",
            'fecha_planeada_inicio': "1987-02-03 12:09:18",
            'fecha_planeada_fin': "2011-07-24 21:39:00",
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
            'progreso_aprobado': 61241526.682,
            'terminado': True,
            'cantidad_planeada': 84607066.6618,
            'cantidad': 9064496.79722,
            'product_id': self.ref('project_edt_idu.product_id_01'),
        }
        task = task_model.sudo(user_group_project_manager_01).search([], limit=1)
        task.sudo(user_group_project_manager_01).write(vals)

        # Actualización NO permitida
        vals = {
            'edt_id': self.ref('project_edt_idu.edt_id_01'),
            'ms_project_guid': "Non nulla ut quis voluptatum.",
            'edt_peso': 77176307,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo_planeado': 83905395.3795,
            'costo': 67165757.1693,
            'progreso': 34820756.4228,
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'progreso_metodo': "pendientes",
            'fecha_planeada_inicio': "1994-03-14 23:24:51",
            'fecha_planeada_fin': "1985-03-30 03:50:23",
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
            'progreso_aprobado': 30811239.9131,
            'terminado': False,
            'cantidad_planeada': 88892848.7534,
            'cantidad': 16975551.2306,
            'product_id': self.ref('project_edt_idu.product_id_01'),
        }
        task = task_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            task.sudo(user_group_project_manager_01).write(vals)
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
        project = project_model.sudo(user_group_project_manager_01).search([], limit=1)
        project.sudo(user_group_project_manager_01).write(vals)

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
        project = project_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            project.sudo(user_group_project_manager_01).write(vals)
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
            'name': "Totam libero beatae odio labore.",
            'fecha': "1972-10-27",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'porcentaje': 17534193,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo': 98282856.3003,
            'fecha_aprobacion': "1987-09-26 20:34:08",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'nivel_alerta': "medio",
            'novedad': "Molestias perspiciatis porro nam voluptates ut optio.",
            'reporte_avance_id': self.ref('project_edt_idu.reporte_avance_id_01'),
            'cantidad': 42949804.9753,
        }
        task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_manager_01).search([], limit=1)
        task_registro_progreso.sudo(user_group_project_manager_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Alias in suscipit sit sunt molestiae.",
            'fecha': "2004-06-17",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'porcentaje': 68649153,
            'company_id': self.ref('project_edt_idu.company_id_01'),
            'costo': 6312332.34288,
            'fecha_aprobacion': "1972-08-11 05:46:24",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'nivel_alerta': "alto",
            'novedad': "Dignissimos voluptatem magnam eligendi.",
            'reporte_avance_id': self.ref('project_edt_idu.reporte_avance_id_01'),
            'cantidad': 31085248.8334,
        }
        task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            task_registro_progreso.sudo(user_group_project_manager_01).write(vals)
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
            'name': "Dolore quas ratione et ipsam.",
            'sequence': 34873555,
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'peso': 25713247,
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'fecha_terminacion': "1974-03-15 09:57:44",
            'fecha_aprobacion': "2014-05-09 17:08:39",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
        }
        task_pendiente = task_pendiente_model.sudo(user_group_project_manager_01).search([], limit=1)
        task_pendiente.sudo(user_group_project_manager_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Autem in est quod expedita magnam architecto dicta.",
            'sequence': 44133554,
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'peso': 10948218,
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'fecha_terminacion': "1999-04-01 02:28:05",
            'fecha_aprobacion': "1977-04-08 04:53:40",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
        }
        task_pendiente = task_pendiente_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            task_pendiente.sudo(user_group_project_manager_01).write(vals)
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
            'origen_res_id': 60924633,
            'destino_res_model': "tarea",
            'destino_res_id': 82441294,
            'tipo': "s_e",
        }
        predecesor = predecesor_model.sudo(user_group_project_manager_01).search([], limit=1)
        predecesor.sudo(user_group_project_manager_01).write(vals)

        # Actualización NO permitida
        vals = {
            'origen_res_model': "tarea",
            'origen_res_id': 76245307,
            'destino_res_model': "tarea",
            'destino_res_id': 73722319,
            'tipo': "s_s",
        }
        predecesor = predecesor_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            predecesor.sudo(user_group_project_manager_01).write(vals)
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
            'fecha': "1999-03-15",
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
        task_reporte_avance = task_reporte_avance_model.sudo(user_group_project_manager_01).search([], limit=1)
        task_reporte_avance.sudo(user_group_project_manager_01).write(vals)

        # Actualización NO permitida
        vals = {
            'fecha': "2008-11-03",
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
        task_reporte_avance = task_reporte_avance_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            task_reporte_avance.sudo(user_group_project_manager_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(task_reporte_avance_model))

    def test_030_project_group_project_manager_unlink(self):
        """ project.group_project_manager Verifica reglas de dominio en operación UNLINK - Delete """
        user_group_project_manager_01 = self.ref('project_edt_idu.group_project_manager_user_01')
        user_group_project_manager_02 = self.ref('project_edt_idu.group_project_manager_user_02')

        # ----------------------------
        # project.edt
        # ----------------------------
        edt_model = self.env['project.edt']
        # Eliminación permitida
        edt = edt_model.sudo(user_group_project_manager_01).search([], limit=1)
        edt.sudo(user_group_project_manager_01).unlink()

        # Eliminación NO permitida
        edt = edt_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            edt.sudo(user_group_project_manager_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(edt_model))

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
        # project.task.registro_progreso
        # ----------------------------
        task_registro_progreso_model = self.env['project.task.registro_progreso']
        # Eliminación permitida
        task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_manager_01).search([], limit=1)
        task_registro_progreso.sudo(user_group_project_manager_01).unlink()

        # Eliminación NO permitida
        task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            task_registro_progreso.sudo(user_group_project_manager_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(task_registro_progreso_model))

        # ----------------------------
        # project.task.pendiente
        # ----------------------------
        task_pendiente_model = self.env['project.task.pendiente']
        # Eliminación permitida
        task_pendiente = task_pendiente_model.sudo(user_group_project_manager_01).search([], limit=1)
        task_pendiente.sudo(user_group_project_manager_01).unlink()

        # Eliminación NO permitida
        task_pendiente = task_pendiente_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            task_pendiente.sudo(user_group_project_manager_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(task_pendiente_model))

        # ----------------------------
        # project.predecesor
        # ----------------------------
        predecesor_model = self.env['project.predecesor']
        # Eliminación permitida
        predecesor = predecesor_model.sudo(user_group_project_manager_01).search([], limit=1)
        predecesor.sudo(user_group_project_manager_01).unlink()

        # Eliminación NO permitida
        predecesor = predecesor_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            predecesor.sudo(user_group_project_manager_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(predecesor_model))

        # ----------------------------
        # project.task.reporte_avance
        # ----------------------------
        task_reporte_avance_model = self.env['project.task.reporte_avance']
        # Eliminación permitida
        task_reporte_avance = task_reporte_avance_model.sudo(user_group_project_manager_01).search([], limit=1)
        task_reporte_avance.sudo(user_group_project_manager_01).unlink()

        # Eliminación NO permitida
        task_reporte_avance = task_reporte_avance_model.sudo(user_group_project_manager_01).search([], limit=1)
        try:
            task_reporte_avance.sudo(user_group_project_manager_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format(task_reporte_avance_model))


if __name__ == '__main__':
    unittest2.main()