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

    def test_010_project_group_project_user_externo_create(self):
        """ project.group_project_user_externo Verifica reglas de dominio en operación CREATE """
        user_group_project_user_externo_01 = self.ref('project_edt_idu.group_project_user_externo_user_01')
        user_group_project_user_externo_02 = self.ref('project_edt_idu.group_project_user_externo_user_02')

        # ----------------------------
        # project.edt
        # ----------------------------
        edt_model = self.env['project.edt']
        # Creación permitida
        vals = {
            'name': "Ut et sit eligendi molestiae in voluptatum qui.",
            'numero': "Cupiditate similique voluptas fuga pariatur eum quis.",
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "cerrado",
            'fecha_planeada_inicio': "1989-06-15",
            'fecha_planeada_fin': "1986-08-29",
            'fecha_inicio': "1996-12-17",
            'fecha_fin': "1972-11-29",
            'peso': 3571253.14343,
            'progreso': 85051298.2341,
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
            'progreso_aprobado': 25631078.2414,
        }
        edt = edt_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Placeat quia sint quaerat voluptates quibusdam dolorem impedit.",
            'numero': "Deleniti illum impedit et sed.",
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "aplazado",
            'fecha_planeada_inicio': "1998-08-26",
            'fecha_planeada_fin': "1970-03-29",
            'fecha_inicio': "2008-06-27",
            'fecha_fin': "1984-05-20",
            'peso': 90370814.4911,
            'progreso': 69075604.9915,
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
            'progreso_aprobado': 80468022.5292,
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
            'edt_peso': 96078545,
            'progreso': 37920451.1541,
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'calcular_progreso_con_pendientes': False,
            'fecha_planeada_inicio': "1977-07-30 13:30:41",
            'fecha_planeada_fin': "1973-07-10 04:07:31",
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
            'numero': "Natus exercitationem occaecati ut.",
            'progreso_aprobado': 80218357.4815,
        }
        task = task_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'edt_id': self.ref('project_edt_idu.edt_id_01'),
            'edt_peso': 13189097,
            'progreso': 18439245.6162,
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'calcular_progreso_con_pendientes': False,
            'fecha_planeada_inicio': "2010-07-12 16:52:26",
            'fecha_planeada_fin': "1978-10-06 12:53:20",
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
            'numero': "Dolorum unde tempora voluptatem nesciunt totam maxime id est.",
            'progreso_aprobado': 66832280.0357,
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
            'name': "Sunt rerum maiores eum ipsa fugiat dolore.",
            'fecha': "2008-01-15",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'porcentaje': 90048512,
            'aprobado': False,
            'fecha_aprobacion': "2006-12-01 20:24:39",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'nivel_alerta': "medio",
        }
        task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Suscipit repudiandae voluptates aut ut sit nostrum odit esse.",
            'fecha': "2002-04-21",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'porcentaje': 81491991,
            'aprobado': False,
            'fecha_aprobacion': "1994-04-06 22:10:31",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'nivel_alerta': "bajo",
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
            'name': "Enim rerum et dicta veritatis ut explicabo.",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'peso': 20833975,
            'fecha_terminacion': "1990-04-18 02:35:17",
        }
        task_pendiente = task_pendiente_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'name': "Repellat modi veniam explicabo deleniti.",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'peso': 78092000,
            'fecha_terminacion': "1991-05-03 12:59:34",
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
            'origen_res_model': "edt",
            'origen_res_id': 30970673,
            'destino_res_model': "tarea",
            'destino_res_id': 66413495,
            'tipo': "e_e",
        }
        predecesor = predecesor_model.sudo(user_group_project_user_externo_01).create(vals)

        # Creación NO permitida
        vals = {
            'origen_res_model': "edt",
            'origen_res_id': 98090274,
            'destino_res_model': "edt",
            'destino_res_id': 71924081,
            'tipo': "e_s",
        }
        try:
            predecesor = predecesor_model.sudo(user_group_project_user_externo_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format(predecesor_model))

    def test_020_project_group_project_user_externo_write(self):
        """ project.group_project_user_externo Verifica reglas de dominio en operación WRITE """
        user_group_project_user_externo_01 = self.ref('project_edt_idu.group_project_user_externo_user_01')
        user_group_project_user_externo_02 = self.ref('project_edt_idu.group_project_user_externo_user_02')

        # ----------------------------
        # project.edt
        # ----------------------------
        edt_model = self.env['project.edt']
        # Actualización permitida
        vals = {
            'name': "Magnam laborum dolor harum aut.",
            'numero': "Et dolorem nemo quia sunt rerum quas.",
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "abierto",
            'fecha_planeada_inicio': "1991-03-01",
            'fecha_planeada_fin': "1986-05-23",
            'fecha_inicio': "1998-07-12",
            'fecha_fin': "1972-02-08",
            'peso': 43572848.1724,
            'progreso': 13979994.7098,
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
            'progreso_aprobado': 26482926.8257,
        }
        edt = edt_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        edt.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Pariatur voluptate minima quisquam tempora.",
            'numero': "Voluptas voluptatibus suscipit omnis quidem ab quia rem.",
            'user_id': self.ref('project_edt_idu.user_id_01'),
            'state': "cerrado",
            'fecha_planeada_inicio': "2008-08-17",
            'fecha_planeada_fin': "2002-01-07",
            'fecha_inicio': "1976-05-09",
            'fecha_fin': "2000-12-15",
            'peso': 91900085.8214,
            'progreso': 48651918.7235,
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
            'progreso_aprobado': 27384236.4911,
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
            'edt_peso': 9371816,
            'progreso': 55588302.4861,
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'calcular_progreso_con_pendientes': True,
            'fecha_planeada_inicio': "1999-03-28 18:34:26",
            'fecha_planeada_fin': "2003-01-13 23:13:27",
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
            'numero': "Laboriosam error et ducimus velit id id.",
            'progreso_aprobado': 78572349.6842,
        }
        task = task_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        task.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'edt_id': self.ref('project_edt_idu.edt_id_01'),
            'edt_peso': 31518207,
            'progreso': 7761018.21217,
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'calcular_progreso_con_pendientes': False,
            'fecha_planeada_inicio': "2003-02-27 14:51:46",
            'fecha_planeada_fin': "1991-07-21 03:52:26",
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
            'numero': "Quae sint rem id tenetur quia quisquam.",
            'progreso_aprobado': 71387836.8615,
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
            'name': "Quis non et labore quidem rerum quia.",
            'fecha': "1991-12-05",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'porcentaje': 11308305,
            'aprobado': False,
            'fecha_aprobacion': "2007-02-09 22:17:14",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'nivel_alerta': "bajo",
        }
        task_registro_progreso = task_registro_progreso_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        task_registro_progreso.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Quis repudiandae velit alias sint ea aut error.",
            'fecha': "1982-02-12",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'porcentaje': 39629567,
            'aprobado': True,
            'fecha_aprobacion': "1993-01-27 10:54:00",
            'revisor_id': self.ref('project_edt_idu.revisor_id_01'),
            'nivel_alerta': "bajo",
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
            'name': "Facere sapiente porro quos fugiat earum molestiae dolores sunt.",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'peso': 86076029,
            'fecha_terminacion': "1974-02-28 14:44:43",
        }
        task_pendiente = task_pendiente_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        task_pendiente.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'name': "Molestias aut suscipit animi consequuntur nemo harum.",
            'task_id': self.ref('project_edt_idu.task_id_01'),
            'peso': 14866716,
            'fecha_terminacion': "1978-08-25 12:48:38",
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
            'origen_res_id': 71480162,
            'destino_res_model': "edt",
            'destino_res_id': 82493200,
            'tipo': "e_e",
        }
        predecesor = predecesor_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        predecesor.sudo(user_group_project_user_externo_01).write(vals)

        # Actualización NO permitida
        vals = {
            'origen_res_model': "tarea",
            'origen_res_id': 71981676,
            'destino_res_model': "edt",
            'destino_res_id': 46171765,
            'tipo': "s_e",
        }
        predecesor = predecesor_model.sudo(user_group_project_user_externo_01).search([], limit=1)
        try:
            predecesor.sudo(user_group_project_user_externo_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format(predecesor_model))

    def test_030_project_group_project_user_externo_unlink(self):
        """ project.group_project_user_externo Verifica reglas de dominio en operación UNLINK - Delete """
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


if __name__ == '__main__':
    unittest2.main()