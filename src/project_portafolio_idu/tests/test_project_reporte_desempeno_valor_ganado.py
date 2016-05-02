# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import ValidationError

logging.basicConfig()
_logger = logging.getLogger('TEST')

class Test_project_reporte_desempeno_valor_ganado(common.TransactionCase):
    def test_crud_validaciones(self):
        # Datos basicos del reporte de Desempeño
        reporte_model = self.env['project.reporte_desempeno']
        name = 'Reporte Desempeño de prueba'
        project = self.browse_ref('project.project_project_data')
        project.crear_linea_base('Prueba')
        snapshot = project.crear_snapshot(name)
        vals = {
            'name': name,
            'project_id': project.id,
            'linea_base_id': project.linea_base_id.id,
            'linea_base_reporte_id': snapshot.id,
        }
        reporte_desempeno = reporte_model.create(vals)
        # Creación de cálculo del valores ganados para una linea del reporte de desempeño
        reporte_desempeno_valor_ganado_model = self.env['project.reporte_desempeno.valor_ganado']
        vals = {
            'reporte_id': reporte_desempeno.id,
            'linea_base_linea_id': project.linea_base_id.linea_ids[0].id, # Tomar una línea cualquiera de la linea base
            'planned_complete': 0.8095238,
            'actual_complete': 0.751923085714,
            'bac': 35000000,
            'ac': 26750800,
#             'es': 19843210.878,
#             'at': 26934438.374,
        }
        reporte_desempeno_valor_ganado = reporte_desempeno_valor_ganado_model.create(vals)

        # Revisión de valores calculados en el momento de la creación
        self.assertEqual(reporte_desempeno_valor_ganado.pv, 28333333)
        self.assertEqual(reporte_desempeno_valor_ganado.ev, 26317308)
        self.assertEqual(reporte_desempeno_valor_ganado.cv, -433492)
        self.assertEqual(reporte_desempeno_valor_ganado.sv, -2016025)
        self.assertEqual(reporte_desempeno_valor_ganado.cpi, 0.9837951762)
        self.assertEqual(reporte_desempeno_valor_ganado.spi, 0.93)
        self.assertEqual(reporte_desempeno_valor_ganado.eac_t, 35576511.09)
        self.assertEqual(reporte_desempeno_valor_ganado.eac_a, 35433492)
        self.assertEqual(reporte_desempeno_valor_ganado.etc_t, 8825711.09)
        self.assertEqual(reporte_desempeno_valor_ganado.etc_a, 8682692)
        self.assertEqual(reporte_desempeno_valor_ganado.vac_t, -576511.09)
        self.assertEqual(reporte_desempeno_valor_ganado.vac_a, -433492)
        self.assertEqual(reporte_desempeno_valor_ganado.tcpi_act, 1.05)
        self.assertEqual(reporte_desempeno_valor_ganado.tcpi_t, 0.98)
        self.assertEqual(reporte_desempeno_valor_ganado.tcpi_a, 1.00)
#         self.assertEqual(reporte_desempeno_valor_ganado.sv_t, 'Valor Esperado')
#         self.assertEqual(reporte_desempeno_valor_ganado.spi_t, 'Valor Esperado')

        # Revisión de valores calculados en el momento de la actualización
        vals_update = {
            'planned_complete': 0.7456140263,
            'actual_complete': 0.6925607368,
            'ac': 26750800,
            'bac': 38000000,
        }
        reporte_desempeno_valor_ganado.write(vals_update)
        self.assertEqual(reporte_desempeno_valor_ganado.pv, 28333333)
        self.assertEqual(reporte_desempeno_valor_ganado.ev, 26317308)
        self.assertEqual(reporte_desempeno_valor_ganado.cv, -433492)
        self.assertEqual(reporte_desempeno_valor_ganado.sv, -2016025)
        self.assertEqual(reporte_desempeno_valor_ganado.cpi, 0.9837951762)
        self.assertEqual(reporte_desempeno_valor_ganado.spi, 0.93)
        self.assertEqual(reporte_desempeno_valor_ganado.eac_t, 38625926.33)
        self.assertEqual(reporte_desempeno_valor_ganado.eac_a, 38433492)
        self.assertEqual(reporte_desempeno_valor_ganado.etc_t, 11875126.33)
        self.assertEqual(reporte_desempeno_valor_ganado.etc_a, 11682692)
        self.assertEqual(reporte_desempeno_valor_ganado.vac_t, -625926.33)
        self.assertEqual(reporte_desempeno_valor_ganado.vac_a, -433492)
        self.assertEqual(reporte_desempeno_valor_ganado.tcpi_act, 1.04)
        self.assertEqual(reporte_desempeno_valor_ganado.tcpi_t, 0.98)
        self.assertEqual(reporte_desempeno_valor_ganado.tcpi_a, 1.00)
#         vals_update = {
#             'es': 'Valor a usarse para calculo',
#             'at': 'Valor a usarse para calculo',
#         }
#         reporte_desempeno_valor_ganado.write(vals_update)
#         self.assertEqual(reporte_desempeno_valor_ganado.sv_t, 'Valor Esperado')
#         vals_update = {
#             'es': 'Valor a usarse para calculo',
#             'at': 'Valor a usarse para calculo',
#         }
#         reporte_desempeno_valor_ganado.write(vals_update)
#         self.assertEqual(reporte_desempeno_valor_ganado.spi_t, 'Valor Esperado')


if __name__ == '__main__':
    unittest2.main()