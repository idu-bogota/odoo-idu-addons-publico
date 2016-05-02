# -*- coding: utf-8 -*-

from openerp import models, fields, api

# Para el uso del wizard se debe enviar en el contexto los valores de:
# id del registro donde se registra la nota, campo 'registro_id'
# Titulo que quiera que este en la ventana para registrar el mensaje, campo 'titulo'
# si esta trabajando con workflow puede añadir la señal, campo 'signal'
# ej. context="{'registro_id': id, 'signal': 'wkf_por_aprobar__rechazado', 'titulo':'No se aprueba el cambio'}"


class base_idu_wizard_registrar_mensaje(models.TransientModel):
    _name = 'base_idu.wizard.registrar_mensaje'
    _inherit = ['mail.thread',]

    # Fields
    mensaje = fields.Text(
        required=True
    )
    titulo = fields.Char(
        required=True,
        readonly=True,
        default=lambda self: self._context.get('titulo', None),
    )

    @api.multi
    def action_create(self, context):
        print context
        self.env['mail.message'].create({
            'res_id': context.get('registro_id'),
            'model': context.get('active_model'),
            'subject': self.titulo,
            'type': 'comment',
            'body': self.mensaje,
        }).id
        record = self.env[context.get('active_model')].browse(context.get('registro_id'))
        if context.get('signal'):
            record.signal_workflow(context.get('signal'))
        return {'type': 'ir.actions.act_window_close'}
