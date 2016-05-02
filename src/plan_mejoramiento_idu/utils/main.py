#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import logging
import erppeek
from optparse import OptionParser
from erppeek_connection import Connection
from import_plam import ImportPlan
from openerp import models, fields, api


logging.basicConfig()
_logger = logging.getLogger('IMPORT')

def main():

    usage = "import file csv to Odoo: %prog [options]"
    parser = OptionParser(usage)

    parser.add_option("-N", "--db_name", dest="db_name", help="OpenERP database name")
    parser.add_option("-U", "--db_user",dest="db_user",help="OpenERP database user")
    parser.add_option("-P", "--db_password", dest="db_password", help="OpenERP database password")
    parser.add_option("-H", "--host_openERP", dest="host_openERP", help="OpenERP server host", default="http://localhost")
    parser.add_option("-K", "--port_openERP", dest="port_openERP", help="OpenERP server port", default="8069")
    parser.add_option("-p", "--path_openERP", dest="path_openERP", help="path of file for uploading", default="plan_contraloria_bogota/")
    parser.add_option("-a", "--avance_openERP", dest="avance_openERP", help="tiene avance el conjunto de script. valores 1 para verdadero 0 para falso", default="1")
    parser.add_option("-b", "--state_accion_openERP", dest="state_accion_openERP", help="state for acción")
    parser.add_option("-d", "--debug", dest="debug", help="Mostrar mensajes de debug utilize 10", default=10)

    (options, args) = parser.parse_args()
    _logger.setLevel(int(options.debug))

    if not options.db_name:
        parser.error('Parametro db_name no especificado')
    if not options.db_user:
        parser.error('Parametro db_user no especificado') 
    if not options.db_password:
        parser.error('Parametro db_password no especificado')
    if not options.host_openERP:
        parser.error('Parametro model_openERP no especificadon')

    # Inicio del scrip
    connect = Connection(options)
    odoo = connect.get_connection()

    # Crear Parametros del sistema para poder crear avances
    today = fields.Datetime.now()
    wizard = odoo.model('plan_mejoramiento.wizard.abrir_registro_avance').create({
        'fecha_inicio': today,
        'fecha_fin': today,
    })
    wizard.action_create()

    _logger.debug('**********************************')
    _logger.debug('*** Inicio Script Cargue Masivo ***')
    _logger.debug('**********************************')
    _logger.debug('\n')

    # Plan
    import_plan = ImportPlan(odoo, _logger, options)
    import_plan.open_file_plan()

    _logger.debug('\n')
    _logger.debug('**********************************')
    _logger.debug('*** Fin Script Cargue Masivo ***')
    _logger.debug('**********************************')

if __name__ == '__main__':
    main()