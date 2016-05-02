# -*- coding: utf-8 -*-
##############################################################################
#
#    Grupo I+D+I
#    Subdirección Técnica de Recursos Tecnológicos
#    Instituto de Desarrollo Urbano - IDU - Bogotá - Colombia
#    Copyright (C) IDU (<http://www.idu.gov.co>)
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

from openerp import models, fields, api, exceptions
from openerp.exceptions import Warning, AccessError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

TIPO_PLAN_MEJORAMIENTO = [
    ('interno', 'Interno'),
    ('contraloria_bog', 'Contraloría de Bogotá'),
    ('contraloria_gral', 'Contraloría General'),
]

class plan_mejoramiento_origen(models.Model):
    _name = 'plan_mejoramiento.origen'
    _description = 'Plan Mejoramiento Origen'

    name = fields.Char('Nombre')
    active = fields.Boolean('Habilitado en el sistema?', default=True)
    parent_id = fields.Many2one('plan_mejoramiento.origen', 'Padre')

class plan_mejoramiento_proceso(models.Model):
    _name = 'plan_mejoramiento.proceso'
    _description = 'Plan Mejoramiento Proceso'

    name = fields.Char('Nombre')
    active = fields.Boolean('Habilitado en el sistema?', default=True)


class plan_mejoramiento_plan(models.Model):
    _name = 'plan_mejoramiento.plan'
    _description = 'Plan Mejoramiento Plan'
    _inherits = {
        'project.project': 'project_id',
    }

    # Fields
    active = fields.Boolean('Habilitado en el sistema?', default=True)
    origen_id = fields.Many2one(
        'plan_mejoramiento.origen',
        'Origen Plan de Mejoramiento',
        domain="[('parent_id','=',False)]",
    )
    sub_origen_id = fields.Many2one(
        'plan_mejoramiento.origen',
        'Sub Origen Plan de Mejoramiento',
        domain="[('parent_id','=',origen_id)]",
    )
    proceso_id = fields.Many2one(
        'plan_mejoramiento.proceso',
        'Proceso Origen Plan de Mejoramiento'
    )
    radicado_orfeo = fields.Char('Radicado Orfeo')
    tipo = fields.Selection(
        TIPO_PLAN_MEJORAMIENTO,
        'Tipo',
        required=True,
    )
    project_id = fields.Many2one('project.project', 'Proyecto',
         required=True,
         ondelete='restrict'
    )
    dependencia_id = fields.Many2one(
        'hr.department', 'Dependencia',
         required=True
    )
    hallazgo_ids = fields.One2many(
        'plan_mejoramiento.hallazgo',
        'plan_id',
        'Hallazgos'
    )
    fecha_creacion = fields.Date(
        'Fecha Creación'
    )

    @api.model
    def create(self, vals):
        plan = super(plan_mejoramiento_plan, self).create(vals)
        plan.project_id.proyecto_tipo = 'plan_mejoramiento'
        plan.project_id.edt_raiz_id = self.env['project.edt'].create({
          'name': plan.project_id.name,
          'user_id': plan.project_id.user_id.id,
        })
        return plan

    @api.one
    def write(self, vals):
        res = super(plan_mejoramiento_plan, self).write(vals)
        if vals.get('user_id', False):
            self.project_id.edt_raiz_id.write({
                'user_id': vals.get('user_id'),
            })
        return res


class plan_mejoramiento_hallazgo(models.Model):
    _name = 'plan_mejoramiento.hallazgo'
    _description = 'Plan Mejoramiento Hallazgo'
    _inherits = {
        'project.edt': 'edt_raiz_id',
    }
    # Fields
    descripcion = fields.Text('Descripción')
    causa = fields.Text('Causa')
    efecto = fields.Text('Efecto')
    edt_raiz_id = fields.Many2one('project.edt', 'EDT',
         required=True,
         ondelete='restrict'
    )
    plan_id = fields.Many2one(
        'plan_mejoramiento.plan',
        'Plan_id',
        default=lambda self: self._context.get('plan_id', None),
    )
    plan_tipo = fields.Selection(
        related='plan_id.tipo',
        readonly=True,
        store=True,
    )
    dependencia_id = fields.Many2one(
        'hr.department',
        'Dependencia',
         required=True,
         default=lambda self: self._context.get('plan_dependencia_id', None),
    )
    accion_ids = fields.One2many(
        'plan_mejoramiento.accion',
        'hallazgo_id',
        'Acciones'
    )
    fecha_inicio = fields.Date(
        'Fecha Inicio',
         compute="_compute_fechas_min",
         help="Fecha minima de las acciones asociada a este hallazgo",
    )
    fecha_fin = fields.Date(
        'Fecha Fin',
         compute="_compute_fechas_max",
         help="Fecha maxima de las acciones asociada a este hallazgo",
    )
    capitulo = fields.Char('Capitulo')
    state = fields.Selection(
        [
           ('draft', 'Borrado'),
           ('in_progress', 'En Progreso'),
           ('done', 'Terminado'),
           ('cancel', 'Cancelado'),
        ],
        default="in_progress",
    )

    @api.model
    def create(self, vals):
        hallazgo = super(plan_mejoramiento_hallazgo, self).create(vals)
        # Asocia el EDT del hallazgo con el EDT del plan
        hallazgo.parent_id = hallazgo.plan_id.edt_raiz_id.id
        hallazgo.project_id = hallazgo.plan_id.project_id.id
        return hallazgo

    @api.one
    def _compute_fechas_min(self):
        for hallazgo in self:
            self.env.cr.execute("""
                        SELECT
                            MIN(fecha_inicio)
                        FROM
                            project_edt t
                        WHERE
                            t.parent_id = %s
                     """, (hallazgo.edt_raiz_id.id,))
        date_min = self.env.cr.fetchall()[0][0]
        self.fecha_inicio = date_min

    @api.one
    def _compute_fechas_max(self):
        for hallazgo in self:
            self.env.cr.execute("""
                        SELECT
                            MAX(fecha_fin)
                        FROM
                            project_edt t
                        WHERE
                            t.parent_id = %s
                     """, (hallazgo.edt_raiz_id.id,))
        date_max = self.env.cr.fetchall()[0][0]
        self.fecha_fin = date_max

class plan_mejoramiento_accion(models.Model):
    _name = 'plan_mejoramiento.accion'
    _description = 'Plan Mejoramiento Accion'
    _inherit = ['mail.thread',]
    _inherits = {
        'project.edt': 'edt_raiz_id',
    }
    _mail_post_access = 'read'

    # Fields
    edt_raiz_id = fields.Many2one('project.edt', 'EDT',
         required=True,
         ondelete='restrict'
    )
    edt_raiz_id_name = fields.Char(
        related='edt_raiz_id.name',
        store=True,
    )
    accion_tipo = fields.Selection(
        [
            ('preventivo', 'Acción Preventivo'),
            ('correctivo', 'Acción Correctivo'),
            ('mejoramiento', 'Acción de Mejoramiento'),
            ('correccion', 'Corrección')
        ],
        'Tipo',
    )
    state = fields.Selection(
        [
           ('nuevo', 'Nuevo'),
           ('por_aprobar', 'Por Aprobar'),
           ('rechazado', 'Rechazada'),
           ('aprobado', 'Aprobada'),
           ('en_progreso', 'En Progreso'),
           ('terminado', 'Terminada'),
           ('cancelado', 'Cancelada'),
        ],
        default="nuevo",
    )

    accion_correctiva = fields.Text('Acción')
    objetivo = fields.Text('Objetivo')
    descripcion = fields.Text('Descripción de la Actividad')
    indicador = fields.Char("Indicador")
    denominacion_medida = fields.Char('Denominación de Medida')
    unidad_medida = fields.Char('Unidad de Medida')
    meta = fields.Char('Meta')
    recurso = fields.Char('Recursos')
    dependencia_id = fields.Many2one(
        'hr.department',
        'Dependencia',
         required=True,
         default=lambda self: self._context.get('dependencia_id', None),
    )
    hallazgo_id = fields.Many2one(
        'plan_mejoramiento.hallazgo',
        'hallazgo_id',
        default=lambda self: self._context.get('hallazgo_id', None),
    )
    hallazgo_dependencia_id = fields.Many2one(
         related='hallazgo_id.dependencia_id',
         readonly=True,
         store=True,
    )
    plan_tipo = fields.Selection(
        related='hallazgo_id.plan_tipo',
        readonly=True,
        store=True,
    )
    plan_id = fields.Many2one(
        'plan_mejoramiento.plan',
        related='hallazgo_id.plan_id',
        readonly=True,
        store=True,
    )
    avances_ids = fields.One2many(
        'plan_mejoramiento.avance',
        'accion_id',
        'Avances_ids'
    )
    ejecutor_id = fields.Many2one(
        'res.users',
        'Ejecutor',
        domain="[('department_id','=', dependencia_id)]"
    )

    @api.onchange('fecha_fin')
    def onchange_fecha_fin_year(self):
        if not self.fecha_fin:
            return
        fecha_inicio = datetime.strptime(self.fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(self.fecha_fin, '%Y-%m-%d')
        year = relativedelta(years=1)
        tope = fecha_inicio + year
        if fecha_fin > tope:
            return {
                'warning': {'message': 'No se permite que la vigencia de una acción sea superior a un año'}
            }

    @api.constrains('fecha_fin')
    def check_fecha_fin_year(self):
        fecha_inicio = datetime.strptime(self.fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(self.fecha_fin, '%Y-%m-%d')
        year = relativedelta(years=1)
        tope = fecha_inicio + year
        if fecha_fin > tope:
            raise Warning('No se permite que la vigencia de una acción sea superior a un año')

    @api.model
    def create(self, vals):
        name = self.env['ir.sequence'].next_by_code('name_accion.secuencia')
        vals.update({'name': name})
        accion = super(plan_mejoramiento_accion, self).create(vals)
        accion.parent_id = accion.hallazgo_id.edt_raiz_id.id
        accion.project_id = accion.hallazgo_id.project_id.id
        accion.programador_id = self.get_jefe_dependencia(vals['dependencia_id'])
        accion.task_ids.write({'project_id': self.project_id.id, 'revisor_id': accion.programador_id.id, 'accion_id': accion.id})
        return accion

    @api.one
    def write(self, vals):
        if self.state == 'cancelado':
            raise AccessError('No se puede editar una Acción en estado cancelado')

        es_responsable_tareas = self.env.user.has_group_v8('plan_mejoramiento_idu.group_responsable_tareas')[0]
        if es_responsable_tareas and (self.ejecutor_id.id == self.env.user.id or self.programador_id.id == self.env.user.id):
            if len(vals) == 1 and 'state' in vals:
                pass
            elif len(vals) == 1 and ('ejecutor_id' in vals or 'programador_id' in vals):
                pass
            elif len(vals) == 1 and 'task_ids' in vals:
                if self.state != 'en_progreso':
                    raise AccessError('No se permite adicionar tareas en una Acción que no esta en progreso')
            elif len(vals) == 1 and 'avances_ids' in vals:
                if self.state != 'en_progreso':
                    raise AccessError('No se permite adicionar avances en una Acción que no esta en progreso')
            else:
                raise AccessError('No tiene permisos para editar valores en la acción')

        if 'dependencia_id' in vals:
            self.programador_id = self.get_jefe_dependencia(vals['dependencia_id'])
        result = super(plan_mejoramiento_accion, self).write(vals)
        if 'project_id' in vals or 'revisor_id' in vals or 'task_ids' in vals:
            self.task_ids.write({'project_id': self.project_id.id, 'revisor_id': self.programador_id.id, 'accion_id': self.id})
        return result

    def wkf_por_aprobar(self):
        self.state = 'por_aprobar'
        # buscar los usuarios jefe_dependencia de la accion
        enviar_a = []
        empleados = self.env['hr.employee'].search([('department_id', '=', self.dependencia_id.id)])
        for empleado in empleados:
            if len(empleado.user_id) >= 1:
                # Tiene usuario asociado
                grupos = self.env['res.groups'].search([('users', '=', empleado.user_id.id)])
                for grupo in grupos:
                    if grupo.name == 'Jefe Dependencia':
                        enviar_a.append(empleado.user_id.partner_id.id)
        # enviar Correo
        self.message_post(
            type="notification",
            body="Se acaba de asignar una Acción al área " + self.dependencia_id.name + ", su estado actual es (Por_Aprobar)",
            partner_ids=enviar_a
        )

    def wkf_rechazado(self):
        self.state = 'rechazado'
        # enviar Correo
        self.message_post(
            type="notification",
            body="Ha sido rechazada la Acción (" + self.name  + ") del área " + self.dependencia_id.name + ", su estado actual es (Rechazada)",
            partner_ids=[self.user_id.partner_id.id]
        )

    def wkf_aprobado(self):
        self.state = 'aprobado'

    def wkf_en_progreso(self):
        self.state = 'en_progreso'

    def wkf_terminado(self):
        self.state = 'terminado'

    def wkf_cancelado(self):
        self.state = 'cancelado'

    def acciones_a_vencerse(self, cr, uid, p_dias, context=None):
        dias =  timedelta(days=p_dias)
        hoy = fields.Date.today()
        fecha_venciminto = datetime.strptime(hoy, '%Y-%m-%d') + dias
        accion_ids = self.search(cr, uid, [('fecha_fin', '=',fecha_venciminto)])
        acciones = self.browse(cr, uid, accion_ids)
        for accion in acciones:
            # enviar Correo
            self.message_post(
                cr, uid, accion.id, context=None,
                type="notification",
                body="Se le informa que la acción (" + accion.accion_correctiva + ") con Código: " + accion.name + " del área " + accion.dependencia_id.name +" está a " + str(p_dias) + " días de vencerse",
                partner_ids=[accion.programador_id.partner_id.id, accion.ejecutor_id.partner_id.id]
            )
        return True

    def get_jefe_dependencia(self, dependencia_id):
        jefe_depen_groups_id = self.env['res.groups'].search([
            ('name','=','Encargado en Planes de Mejoramiento como Jefe Dependencia')
        ])
        user = self.env['res.users'].search([
            ('department_id','=',dependencia_id),
            ('groups_id', 'in', jefe_depen_groups_id.id)
        ])
        if len(user) > 1:
            print ""
            raise AccessError("""Existen más de dos Jefes Dependencia para esta Área.
                Por favor Comuniquese Con El administrador para corregir esta irregularidad.""")
        else:
            return user.id

class plan_mejoramiento_avance(models.Model):
    _name = 'plan_mejoramiento.avance'
    _description = 'Plan Mejoramiento Avance'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _rec_name = 'state'

    _track = {
        'tipo_calificacion_id': {
            'plan_mejoramiento_idu.notificacion_calificacion': lambda self, cr, uid, obj, ctx=None:
                True,
        },
        'porcentaje': {
            'plan_mejoramiento_idu.notificacion_calificacion': lambda self, cr, uid, obj, ctx=None:
                True,
        },
    }
    _mail_post_access = 'read'

    # Fields
    active = fields.Boolean('Habilitado en el sistema?', default=True)
    state = fields.Selection(
        [
           ('sin_iniciar', 'Sin Iniciar'),
           ('en_progreso', 'En Progreso'),
           ('bloqueado', 'Bloqueado'),
           ('terminado', 'Terminado'),
           ('terminado_con_retrazo', 'Terminado Con Retrazo'),
        ],
    )
    descripcion = fields.Text('Descripción', track_visibility='onchange')
    fecha_corte = fields.Date('Fecha de Corte',
        default=lambda self: self.env['ir.config_parameter'].get_param('plan_mejoramiento.activar_avances.fecha_inicio'),
    )
    porcentaje = fields.Integer('% de Avance', track_visibility='onchange')
    accion_id = fields.Many2one(
        'plan_mejoramiento.accion',
        'Código Acción',
        default=lambda self: self._context.get('accion_id', None),
        domain="[('state','=', 'en_progreso')]",
    )
    user_id = fields.Many2one(
         related='accion_id.user_id',
         string="Auditor",
         readonly=True,
         store=False,
    )
    dependencia_id = fields.Many2one(
         related='accion_id.dependencia_id',
         readonly=True,
         store=True,
    )
    accion_correctiva = fields.Text(
         related='accion_id.accion_correctiva',
         readonly=True,
         store=True,
    )
    plan_tipo = fields.Selection(
         related='accion_id.plan_tipo',
         readonly=True,
         store=True,
    )
    tipo_calificacion_id = fields.Many2one(
        'plan_mejoramiento.tipo_calificacion',
        'Tipo Calificación',
        domain="[('tipo_plan','=', plan_tipo)]",
        track_visibility='onchange',
    )
    aprobacion_jefe_dependencia = fields.Boolean(
        'Aprobación por Jefe de la Dependencia',
    )

    @api.onchange('porcentaje')
    def onchange_porcentaje(self):
        if self.porcentaje and (self.porcentaje < 0 or self.porcentaje > 100):
            return {
                'warning': {'message': 'Valor Fuera del Rango Permitido'}
            }

    @api.constrains('porcentaje')
    def check_porcentaje(self):
        if self.porcentaje < 0 or self.porcentaje > 100:
            raise Warning('No se Permite Guardar un Valor Mayor a 100 y Menor a 0 para el Porcentaje de Avance')

    @api.model
    def create(self, vals):
        hoy = fields.Date.today()
        fecha_inicio = self.env['ir.config_parameter'].get_param('plan_mejoramiento.activar_avances.fecha_inicio')
        fecha_fin = self.env['ir.config_parameter'].get_param('plan_mejoramiento.activar_avances.fecha_fin')

        if not fecha_inicio or not fecha_fin:
            raise Warning('No se ha definido fechas para el registro de avances')

        if fecha_inicio and fecha_fin and not (fecha_inicio <= hoy <= fecha_fin):
            raise Warning('Aún no se ha habilitado las fechas para realizar avances')

        if fecha_inicio and fecha_fin:
            self.env.cr.execute("""
                        SELECT
                             count(id)
                        FROM plan_mejoramiento_avance
                        WHERE fecha_corte BETWEEN  '{0}'  and '{1}'
                        AND accion_id = {2}""".format(fecha_inicio, fecha_fin, vals['accion_id'])
            )
            count_avances = self.env.cr.fetchall()[0][0]
            if count_avances >= 1:
                raise Warning('Solo se permite un avance por mes')

        es_responsable_tareas = self.env.user.has_group_v8('plan_mejoramiento_idu.group_responsable_tareas')[0]
        if es_responsable_tareas and vals.get('aprobacion_jefe_dependencia', False):
            raise AccessError('el campo [Aprobación por Jefe de la Dependencia] solo lo puede diligenciar el usuario Jefe Dependencia')

        avance = super(plan_mejoramiento_avance, self).create(vals)
        return avance

    @api.one
    def write(self, vals):
        # se valida que los avances ya calificados no sean modificados
        es_responsable_tareas = self.env.user.has_group_v8('plan_mejoramiento_idu.group_responsable_tareas')[0]
        if len(vals) == 1 and self.tipo_calificacion_id and es_responsable_tareas:
            raise AccessError('No se permite modificar un avance que ya ha sido calificado')
        # se valida que solo el jefe_dependencia apruebe el avance
        es_jefe_dependencia = self.env.user.has_group_v8('plan_mejoramiento_idu.group_jefe_dependencia')[0]
        if 'aprobacion_jefe_dependencia' in vals and not es_jefe_dependencia:
            raise AccessError('el campo [Aprobación por Jefe de la Dependencia] solo lo puede diligenciar el usuario Jefe Dependencia')
        # se valida que el usuario oci solo pueda realizar la calificación una vez este aprobado el avance por el usuario jefe_dependencia
        es_oci = self.env.user.has_group_v8('plan_mejoramiento_idu.group_oci')[0]
        if ('tipo_calificacion_id' in vals or 'porcentaje'in vals) and es_oci and self.aprobacion_jefe_dependencia == False:
            raise AccessError('Se podrá calificar este avance hasta que el usuario Jefe Depedencia lo apruebe')
        result = super(plan_mejoramiento_avance, self).write(vals)
        return result

class plan_mejoramiento_tipo_calificacion(models.Model):
    _name = 'plan_mejoramiento.tipo_calificacion'
    _description = 'Plan Mejoramiento Tipo Calificacion'

    # Fields
    name = fields.Char('Nombre')
    estado = fields.Selection(
        [
           ('sin_iniciar', 'Sin Iniciar'),
           ('en_progreso', 'En Progreso'),
           ('bloqueado', 'Bloqueado'),
           ('terminado', 'Terminado'),
           ('terminado_con_retrazo', 'Terminado Con Retraso'),
        ],
        'Estado',
        required=True,
    )
    tipo_plan = fields.Selection(
        TIPO_PLAN_MEJORAMIENTO,
        'Tipo de Plan al que Aplica',
        required=True,
    )