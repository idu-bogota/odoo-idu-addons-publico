# -*- encoding: utf-8 -*-

from openerp import models, fields, api, exceptions
from openerp.exceptions import Warning
import subprocess
from subprocess import CalledProcessError
import logging
import cStringIO as StringIO
import xlwt
from base64 import encodestring
from datetime import *
from Style import Style

_logger = logging.getLogger(__name__)

class plan_mejoramiento_wizard_plan_mejoramiento_export_xls(models.TransientModel):
    _name = 'plan_mejoramiento.wizard.plan_mejoramiento_export_xls'

    plan_tipo = fields.Selection(
        selection=[
            ('interno', 'Interno'),
            ('contraloria_bog', 'Contraloría de Bogotá'),
            ('contraloria_gral', 'Contraloría General'),
        ],
        string="Reporte",
        required = True
    )
    tipo_calificacion_id = fields.Many2one(
        'plan_mejoramiento.tipo_calificacion',
        'Tipo Calificación Avance',
        domain="[('tipo_plan','=', plan_tipo)]",
        track_visibility='onchange',
    )
    fecha_inicio = fields.Date('Fecha Inicial Acción')
    fecha_fin = fields.Date('Fecha Final Acción')
    data = fields.Binary('Archivo',readonly=True,filters="xls")
    filename = fields.Char('Nombre del Archivo', size=255, default='Plan_Mejoramiento.xls')
    agrupar = fields.Boolean('Agrupar Reporte')

    @api.multi
    def generar_plan_interno(self, tipo_calificacion_id, plan_tipo, fecha_inicio, fecha_fin, agrupar):
        crear_xml = Style(self.env, fecha_inicio, fecha_fin, tipo_calificacion_id, plan_tipo, agrupar)
        file_interno = crear_xml.style_interno()
        return file_interno

    @api.multi
    def generar_plan_contraloria_bogota(self, tipo_calificacion_id, plan_tipo, fecha_inicio, fecha_fin, agrupar):
        crear_xml = Style(self.env, fecha_inicio, fecha_fin, tipo_calificacion_id, plan_tipo, agrupar)
        file_bogota = crear_xml.style_bogota()
        return file_bogota

    @api.multi
    def generar_plan_contraloria_general(self, tipo_calificacion_id, plan_tipo, fecha_inicio, fecha_fin, agrupar):
        crear_xml = Style(self.env, fecha_inicio, fecha_fin, tipo_calificacion_id, plan_tipo, agrupar)
        file_general = crear_xml.style_general()
        return file_general

    @api.multi
    def generar_xls(self):
        if self.plan_tipo == 'interno':
            reporte = self.generar_plan_interno(self.tipo_calificacion_id, self.plan_tipo, self.fecha_inicio, self.fecha_fin, self.agrupar)
            fname = 'Plan_Mejoramiento_Interno.xls'
        elif self.plan_tipo == 'contraloria_bog':
            reporte = self.generar_plan_contraloria_bogota(self.tipo_calificacion_id, self.plan_tipo, self.fecha_inicio, self.fecha_fin, self.agrupar)
            fname = 'Plan_Mejoramiento_Contraloria_Bogota.xls'
        elif self.plan_tipo == 'contraloria_gral':
            reporte = self.generar_plan_contraloria_general(self.tipo_calificacion_id, self.plan_tipo, self.fecha_inicio, self.fecha_fin, self.agrupar)
            fname = 'Plan_Mejoramiento_Contraloria_General.xls'

        if reporte:
            self.data = reporte
            self.filename = fname
            view_ids = self.env['ir.ui.view'].search([('model','=','plan_mejoramiento.wizard.plan_mejoramiento_export_xls'),
                                                      ('name','=','plan contratacion descargar excel')])
            ids = self.id
            return {
                    'view_type':'form',
                    'view_mode':'form',
                    'res_model':'plan_mejoramiento.wizard.plan_mejoramiento_export_xls',
                    'target':'new',
                    'type':'ir.actions.act_window',
                    'view_id':view_ids.id,
                    'res_id': ids
            }