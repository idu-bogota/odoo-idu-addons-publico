# -*- coding: utf-8 -*-
##############################################################################
#
#    Grupo de Investigación, Desarrollo e Innovación I+D+I
#    Subdirección de Recursos Tecnológicos - STRT
#    INSTITUTO DE DESARROLLO URBANO - BOGOTA (COLOMBIA)
#    Copyright (C) 2015 IDU STRT I+D+I (http://www.idu.gov.co/)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
from openerp.exceptions import Warning, ValidationError
from datetime import timedelta
from ..models.project import PROJECT_TASK_REPORTE_AVANCE_NIVEL_ALERTA
import logging
_logger = logging.getLogger(__name__)

class project_edt_wizard_registrar_progreso_tarea(models.TransientModel):
    _name = 'project.edt.wizard.registrar_progreso_tarea'
    _description = 'Wizard para registrar progreso de tarea'

    def _default_progreso(self):
        if self.env.context.get('task_id'):
            task = self.env['project.task'].browse(self.env.context.get('task_id'))
            return task.progreso

    def _default_costo(self):
        if self.env.context.get('task_id'):
            task = self.env['project.task'].browse(self.env.context.get('task_id'))
            return task.costo

    def _default_cantidad(self):
        if self.env.context.get('task_id'):
            task = self.env['project.task'].browse(self.env.context.get('task_id'))
            return task.cantidad

    def _default_fecha_inicio_real(self):
        if self.env.context.get('task_id'):
            task = self.env['project.task'].browse(self.env.context.get('task_id'))
            return task.fecha_inicio

    def _default_fecha_fin_real(self):
        if self.env.context.get('task_id'):
            task = self.env['project.task'].browse(self.env.context.get('task_id'))
            return task.fecha_fin
    # -------------------
    # Fields
    # -------------------
    name = fields.Char(
        string='Resumen',
        required=True,
        track_visibility='onchange',
        size=255,
    )
    fecha = fields.Date(
        string='Fecha',
        required=True,
        readonly=True,
        default=fields.Date.context_today,
    )
    task_id = fields.Many2one(
        string='Tarea',
        required=True,
        readonly=True,
        comodel_name='project.task',
        ondelete='restrict',
        default=lambda self: self._context.get('task_id', None),
    )
    task_requiere_adjunto = fields.Boolean(
        string='Es requerido adjunto para finalizar tarea',
        related='task_id.requiere_adjunto',
        readonly=True,
        default=False,
    )
    project_id = fields.Many2one(
        string='Proyecto',
        readonly=True,
        related='task_id.project_id',
    )
    project_reportar_costo = fields.Boolean(
        string='En Reporte de Avance incluir Costo de la Tarea',
        related='task_id.project_id.reportar_costo',
        readonly=True,
        default=False,
    )
    project_reportar_cantidad = fields.Boolean(
        string='En Reporte de Avance incluir Cantidades',
        related='task_id.project_id.reportar_cantidad',
        readonly=True,
        default=False,
    )
    porcentaje = fields.Integer(
        string='Porcentaje Acumulado',
        required=True,
        default=_default_progreso,
        help="Porcentaje acumulado al día del reporte",
    )
    cantidad = fields.Float(
        string='Cantidad',
        required=False,
        default=_default_cantidad,
    )
    uom_id = fields.Many2one(
        string='Unidad',
        comodel_name='product.uom',
        related='task_id.product_id.uom_id',
        readonly=True,
    )
    company_id = fields.Many2one(
        string='Compañía',
        required=True,
        comodel_name='res.company',
        ondelete='restrict',
        default=lambda self: self.env.user.company_id,
    )
    currency_id = fields.Many2one(
        string='Moneda',
        required=False,
        readonly=True,
        related='company_id.currency_id',
        comodel_name='res.currency',
        ondelete='restrict',
    )
    costo = fields.Monetary(
        string='Costo',
        required=False,
        default=_default_costo,
    )
    nivel_alerta = fields.Selection(
        string='Nivel de Alerta',
        required=False,
        selection=PROJECT_TASK_REPORTE_AVANCE_NIVEL_ALERTA,
        default='ninguno',
    )
    novedad = fields.Text(
        string='Novedad',
        required=False,
    )
    fecha_inicio = fields.Date(
        string='Fecha Inicio Real',
        required=False,
        readonly=False,
        default=_default_fecha_inicio_real,
    )
    fecha_fin = fields.Date(
        string='Fecha Fin Real',
        required=False,
        readonly=False,
        default=_default_fecha_fin_real,
    )
    terminado = fields.Boolean(
        string='Terminado',
        required=False,
        track_visibility='onchange',
        help='''La tarea fue marcada como terminada''',
        default=False,
    )
    adjunto = fields.Binary(
        string='Archivo Final Producto de la Tarea',
        required=False,
        readonly=False,
    )
    adjunto_nombre = fields.Char('Nombre Archivo Adjunto')

    @api.multi
    def registrar_progreso(self):
        self.ensure_one()
        progreso_model = self.env['project.task.registro_progreso']
        record_fields = [
            'fecha', 'name', 'porcentaje', 'costo', 'nivel_alerta',
            'novedad', 'terminado',
            #'fecha_inicio', 'fecha_fin',
        ]
        vals = {
            'task_id': self.task_id.id,
        }
        for field in record_fields:
            value = getattr(self, field)
            vals[field] = value

        if self.terminado:
            # Se marca el dia actual como la fecha de fin a menos que se envie por contexto una fecha (usada para testing)
            # FIXME: Esto deberia tomar el valor fecha_fin del formulario o el valor de hoy basado en un parametro del proyecto
            vals['fecha_fin'] = self.env.context.get('fecha_fin', False) or fields.Date.context_today(self)
            fechahora_fin = fields.Datetime.now()
            if self.env.context.get('fecha_fin', False):
                fechahora_fin = vals['fecha_fin'] + ' 23:59:59'
            self.task_id.write({
                'duracion_dias_manual': False, # Para obligar a que se recalcule la duración en días basado en la fecha final
                'fecha_fin': vals['fecha_fin'],
                'date_end': fechahora_fin,
            })
            if self.project_id.reprogramar_tareas_automaticamente:
                self.task_id.reprogramar_tarea_button()
            template = self.env.ref('project_edt_idu.notificacion_tarea_puede_iniciar')
            sucesor_ids = self.task_id.sucesor_ids.filtered(lambda x: x.destino_res_model == 't').mapped('destino_res_id')
            sucesoras = self.env['project.task'].browse(sucesor_ids)
            try:
                if sucesoras:
                    sucesoras.message_post_with_template(template.id, notify=True, composition_mode='mass_mail')
            except Exception as e:
                _logger.error('No se pudo enviar email de sucesora')
                _logger.exception(e)

        if self.nivel_alerta != 'ninguno':
            partner_ids = []
            if self.task_id.project_id.user_id.email:
                partner_ids.append(self.task_id.project_id.user_id.partner_id.id)
            if self.task_id.project_id.programador_id.email:
                partner_ids.append(self.task_id.project_id.programador_id.partner_id.id)
            if self.task_id.revisor_id.email:
                partner_ids.append(self.task_id.revisor_id.partner_id.id)
            mensaje = """
            Cordial Saludo,<br/>
            Se registra la siguiente novedad para la tarea <strong>{} {}</strong> parte del proyecto <strong>{}</strong>:<br />
            <strong>Nivel de Alerta:</strong> {}<br />
            <strong>Novedad:</strong>: {}<br />
            """.format(
                self.task_id.numero, self.task_id.name, self.task_id.project_id.name,
                self.nivel_alerta, self.novedad,
            )

            self.task_id.message_post(
                subject='[ZIPA][Alerta {}] Novedad en: {} {}'.format(self.nivel_alerta, self.task_id.numero, self.task_id.name),
                type="email",
                body=mensaje,
                partner_ids=partner_ids
            )


        record = progreso_model.create(vals)
        if self.adjunto:
            self.env['ir.attachment'].create({
                'res_model': record._name,
                'res_id': record.id,
                'datas': self.adjunto,
                'datas_fname': self.adjunto_nombre,
                'name': 'Adjunto Registro de Progreso/Avance en Tarea {}'.format(self.adjunto_nombre),
            })
        return {'type': 'ir.actions.act_window_close'}

    @api.onchange('terminado')
    def _onchange_terminado(self):
        if self.terminado:
            self.porcentaje = 100

    @api.onchange('porcentaje')
    def _onchange_porcentaje(self):
        if self.porcentaje < 0 and self.porcentaje > 100:
            return {
                'title': "Error de Validación",
                'warning': {'message': 'Progreso debe ser un valor entero entre 0 y 100'}
            }
        if self.porcentaje == 100 and not self.terminado:
            self.terminado = True
        elif self.terminado and self.porcentaje != 100:
            self.terminado = False

    @api.one
    @api.constrains('porcentaje')
    def _check_porcentaje(self):
        if self.porcentaje > 100 or self.porcentaje < 0:
            raise ValidationError("Porcentaje debe ser un valor entero entre 0 y 100")
        if self.porcentaje == 100 and not self.terminado:
            raise ValidationError("Si el porcentaje es 100 se debe marcar la tarea como terminada")

    @api.one
    @api.constrains('terminado')
    def _check_terminado(self):
        if self.porcentaje != 100 and self.terminado:
            raise ValidationError("El porcentaje para una tarea marcada como terminada debe ser 100")
