from openerp import models, fields, api, exceptions
from openerp.exceptions import Warning
import datetime

class project_plan_abrir_registro_avance(models.TransientModel):
    _name = 'plan_mejoramiento.wizard.abrir_registro_avance'

    def _default_fecha_inicio(self):
        return self.env['ir.config_parameter'].get_param('plan_mejoramiento.activar_avances.fecha_inicio')

    def _default_fecha_fin(self):
        return self.env['ir.config_parameter'].get_param('plan_mejoramiento.activar_avances.fecha_fin')

    # Fields
    fecha_inicio = fields.Date(required=True, default=_default_fecha_inicio)
    fecha_fin = fields.Date(required=True, default=_default_fecha_fin)

    @api.constrains('fecha_inicio')
    def check_fecha_inicio(self):
        hoy = fields.Date.today()
        if self.fecha_inicio < hoy:
            raise Warning('No se permite guardar una fecha menor a la actual para el campo Fecha Inicio')

    @api.constrains('fecha_fin')
    def check_fecha_fin(self):
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_fin < self.fecha_inicio:
                raise Warning('No se permite que el valor del campo Fecha Inicio sea mayor al valor del campo Fecha Fin')

    @api.multi
    def action_create(self):
        fecha_inicial = self.env['ir.config_parameter'].search(
            [('key','=','plan_mejoramiento.activar_avances.fecha_inicio')],
        )
        fecha_fin = self.env['ir.config_parameter'].search(
            [('key','=','plan_mejoramiento.activar_avances.fecha_fin')],
        )
        for formulario in self:
            if not fecha_inicial:
                self.env['ir.config_parameter'].create({
                    'key': 'plan_mejoramiento.activar_avances.fecha_inicio',
                    'value': formulario.fecha_inicio,
                })
            else:
                fecha_inicial.write({
                    'value': formulario.fecha_inicio,
                })
            if not fecha_fin:
                self.env['ir.config_parameter'].create({
                    'key': 'plan_mejoramiento.activar_avances.fecha_fin',
                    'value': formulario.fecha_fin,
                })
            else:
                fecha_fin.write({
                    'value': formulario.fecha_fin,
                })

        return {'type': 'ir.actions.act_window_close'}
