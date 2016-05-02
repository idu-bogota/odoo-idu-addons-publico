from openerp import models, fields, api, exceptions
from openerp.exceptions import Warning

class plan_mejoramiento_wizard_plan_mejoramiento_crear_tarea(models.TransientModel):
    _name = 'plan_mejoramiento.wizard.plan_mejoramiento_crear_tarea'

    # -------------------
    # Fields
    # -------------------
    name = fields.Char(
        string='Resumen',
        required=True,
        size=255,
    )
    fecha = fields.Date(
        string='Fecha',
        required=True,
        default=fields.Date.today,
    )
    porcentaje = fields.Integer(
        string='Porcentaje',
        required=True,
    )

    @api.multi
    def crear_progreso(self):
        task_id = self.env.context.get('active_id')
        object_task = self.env['project.task'].search([
             ('id', '=', task_id),
        ])

        if self.env.user.id == object_task.user_id.id:
            progreso = self.env['project.task.registro_progreso'].create({
              'name': self.name,
              'fecha': self.fecha,
              'porcentaje': self.porcentaje,
              'task_id': task_id,
            })
        else:
            raise Warning('Solo el usuario asignado(a) a esta tarea puede adicionar progresos.')
