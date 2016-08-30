# -*- encoding: utf-8 -*-
import unittest2
import logging
import base64
import os
import csv
from openerp.tests import common
from openerp.exceptions import ValidationError
from datetime import *

logging.basicConfig()
_logger = logging.getLogger('TEST')

class Test_project_edt_reprogramar(common.TransactionCase):
    def test_wizard_registro_progreso_con_reprogramacion(self):
        project_model = self.env['project.project']
        vals = {
            'name': 'Test Reprogramar',
        }
        self.env['ir.config_parameter'].create({'key':'project.edt.jython_path', 'value': 'x'})
        self.env['ir.config_parameter'].create({'key':'project.edt.mpp2csv_path', 'value': 'y'})
        project = project_model.create(vals)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # Cargar archivo CSV con programación
        with open(dir_path + '/test_dependencias.mpp.csv', "rb") as test_file:
            encoded_file = base64.b64encode(test_file.read())
            wizard = self.env['project.edt.wizard.importar_mpp'].create({
                'project_id': project.id,
                'archivo': encoded_file,
                'archivo_nombre': 'test_dependencias.mpp.csv',
                'metodo': 'hojas_son_tareas',
                'asignar_recursos_mpp': False,
            })
            wizard.importar_mpp()
        # Registrar progreso en tarea para disparar la reprogramación
        tarea = self.env['project.task'].search([
            ('name','=','Inicio test_dependencias'),
            ('project_id', '=', project.id),
        ])
        tarea.ensure_one()
        wizard = self.env['project.edt.wizard.registrar_progreso_tarea'].create({
            'name': 'test',
            'porcentaje':100,
            'task_id': tarea.id,
            'terminado': True,
        })
        wizard.with_context({'fecha_fin': '2016-08-08'}).registrar_progreso()
        # Cargar archivo CSV con RE-programación y comparar con lo reprogramado en la BD
        with open(dir_path + '/test_dependencias.reprogramado.csv', "rb") as f:
            archivo_csv = csv.DictReader(f)
            for row in archivo_csv:
                if row['name'] == 'test_dependencias': # Ignore EDT Raiz
                    continue
                tarea = self.env['project.task'].search([
                    ('name','=',row['name']),
                    ('project_id', '=', project.id),
                ])
                tarea.ensure_one()
                msg = 'Comparando Tarea "{}" de duración "{}" Comparando inicio (calculada vs esperada) {} == {} / fin {} == {}'.format(
                    tarea.name, tarea.duracion_dias,
                    tarea.fecha_inicio, row['fecha_inicio_reprogramada'],
                    tarea.fecha_fin, row['fecha_fin_reprogramada'],
                )
                self.assertEqual(tarea.fecha_inicio, row['fecha_inicio_reprogramada'], msg)
                self.assertEqual(tarea.fecha_fin, row['fecha_fin_reprogramada'], msg)


if __name__ == '__main__':
    unittest2.main()
