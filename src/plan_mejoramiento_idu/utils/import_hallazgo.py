#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import sys
import erppeek
from import_csv import Import
from import_accion import ImportAccion

class ImportHallazgo(Import):
    def __init__(self, odoo, _logger, plan, id_plan_css , options):
        self.odoo = odoo
        self._logger = _logger
        self.plan = plan
        self.id_plan_css = id_plan_css
        self.options = options

    def open_file_hallazgo(self):
        with open(self.options.path_openERP +'plan_mejoramiento.hallazgo.csv') as csvfile:
            cnt = 0
            reader = csv.DictReader(csvfile)
            for row in reader:
                cnt += 1
                if self.id_plan_css == row['plan_id']:
                    self._logger.debug("    ***[{2}] Cargando Hallazgo: [{0}] del Plan: [{1}]***".format(row['name_hallazgo'], self.plan.name, cnt))
                    # Crear hallazgo
                    hallazgo = self.create_hallazgo(row['auditor'], row['name_hallazgo'], row['dependencia'], row['descripcion'], row['causa'], row['efecto'], self.plan, row['capitulo'])
                    if not hallazgo:
                        raise Exception('No se creó el hallazgo')
                    # Crear Accion
                    import_accion = ImportAccion(self.odoo, self._logger, hallazgo, row['hallazgo_id'], self.options)
                    import_accion.open_file_accion()

    def create_hallazgo(self, auditor, name_hallazgo, dependencia, descripcion, causa, efecto, plan, capitulo):
        if auditor != '' and self.find_user_existing(auditor):
            auditor_id = self.get_user(auditor)
        else:
            raise Exception('Hallazgo, no se encuentra usuario: {}'.format(auditor))
            return
            sys.exit("ERROR:DESCRIPTION:EL usuario: " + auditor + " No se encuentar definida en la BD")

        dependencia_id = self.find_area(dependencia)

        new_hallazgo = self.odoo.model('plan_mejoramiento.hallazgo').create({
            'plan_id': plan.id,
            'name': name_hallazgo,
            'user_id': auditor_id,
            'dependencia_id': dependencia_id,
            'descripcion': descripcion,
            'causa': causa,
            'efecto': efecto,
            'capitulo': capitulo
        })
        return new_hallazgo