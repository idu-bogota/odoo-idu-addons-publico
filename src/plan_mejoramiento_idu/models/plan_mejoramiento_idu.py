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
from openerp.exceptions import Warning, AccessError, ValidationError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp.addons.base_idu.models.filtros_mixin import adiciona_keywords_en_search

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

    # Fields
    name = fields.Char(
        string='Nombre',
        required=True,
        size=255,
    )
    user_id = fields.Many2one(
        'res.users',
        'Auditor',
        default=lambda self: self.env.user,
    )
    descripcion = fields.Text('Descripción')
    causa = fields.Text('Causa')
    efecto = fields.Text('Efecto')
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
        return hallazgo

    @api.one
    def _compute_fechas_min(self):
        for hallazgo in self:
            self.env.cr.execute("""
                        SELECT
                            MIN(fecha_inicio)
                        FROM
                            plan_mejoramiento_accion t
                        WHERE
                            t.hallazgo_id = %s
                     """, (hallazgo.id,))
        date_min = self.env.cr.fetchall()[0][0]
        self.fecha_inicio = date_min

    @api.one
    def _compute_fechas_max(self):
        for hallazgo in self:
            self.env.cr.execute("""
                        SELECT
                            MAX(fecha_fin)
                        FROM
                            plan_mejoramiento_accion t
                        WHERE
                            t.hallazgo_id = %s
                     """, (hallazgo.id,))
        date_max = self.env.cr.fetchall()[0][0]
        self.fecha_fin = date_max

    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False, xtra=None):
        """Se sobreescribe para poder adicionar keyworkds a usar en filtros de la vista"""
        new_args = adiciona_keywords_en_search(self, cr, uid, args, offset, limit, order, context, count, xtra)
        return super(plan_mejoramiento_hallazgo, self).search(cr, uid, new_args, offset, limit, order, context, count)


class plan_mejoramiento_accion(models.Model):
    _name = 'plan_mejoramiento.accion'
    _description = 'Plan Mejoramiento Accion'
    _inherit = ['mail.thread', 'models.fields.security.mixin']
    _mail_post_access = 'read'

    _write_fields_whitelist = {
        'plan_mejoramiento_idu.group_responsable_tareas': ['state', 'ejecutor_id', 'avances_ids', 'task_ids'],
    }
    _write_fields_blacklist = {
        'plan_mejoramiento_idu.group_oci': ['task_ids', 'avance_ids'],
    }

    # Fields
    name = fields.Char(
        string="Código Accion",
        size=255,
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
    jefe_dependencia_id = fields.Many2one(
        related='dependencia_id.manager_id.user_id',
        readonly=True,
        string='Jefe de Dependencia',
    )
    ejecutor_id = fields.Many2one(
        'res.users',
        'Ejecutor',
        domain="[('department_id','=', dependencia_id)]"
    )
    user_id = fields.Many2one(
        'res.users',
        'Auditor',
        default=lambda self: self.env.user,
    )
    fecha_inicio = fields.Date(
        'Fecha Inicio',
         help="Fecha minima de las acciones asociada a este hallazgo",
    )
    fecha_fin = fields.Date(
        'Fecha Fin',
         help="Fecha maxima de las acciones asociada a este hallazgo",
    )
    task_ids = fields.One2many(
        string='Tareas',
        required=False,
        comodel_name='project.task',
        inverse_name='accion_id',
        ondelete='restrict',
    )

    @api.one
    @api.constrains('fecha_inicio')
    def _check_fecha_inicio(self):
        self._check_fechas()

    @api.one
    @api.constrains('fecha_fin')
    def _check_fecha_fin(self):
        self._check_fechas()
        fecha_inicio = datetime.strptime(self.fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(self.fecha_fin, '%Y-%m-%d')
        year = relativedelta(years=1)
        tope = fecha_inicio + year
        #if fecha_fin > tope:
        #    raise ValidationError('No se permite que la vigencia de una acción sea superior a un año')

    @api.one
    def _check_fechas(self):
        if(self.fecha_inicio and self.fecha_fin and
           self.fecha_inicio > self.fecha_fin
            ):
            raise ValidationError("Fecha de inicio no puede ser posterior a la de finalización")

    @api.model
    def create(self, vals):
        name = self.env['ir.sequence'].next_by_code('name_accion.secuencia')
        vals.update({'name': name})
        accion = super(plan_mejoramiento_accion, self).create(vals)
        accion.task_ids.write({'project_id': self.hallazgo_id.plan_id.project_id.id, 'edt_id': self.hallazgo_id.plan_id.project_id.edt_raiz_id.id, 'revisor_id': accion.ejecutor_id.id, 'accion_id': accion.id})
        return accion

    @api.one
    def write(self, vals):
        if self.state == 'cancelado':
            raise ValidationError('No se puede editar una Acción en estado cancelado')

        if ('task_ids' in vals or 'avances_ids' in vals) and self.state != 'en_progreso':
            raise ValidationError('No se permite adicionar tareas o avances en una Acción que no esta en progreso')

        result = super(plan_mejoramiento_accion, self).write(vals)

        if 'dependencia_id' in vals or 'jefe_dependencia_id' in vals or 'task_ids' in vals:
            self.task_ids.write({'project_id': self.hallazgo_id.plan_id.project_id.id, 'edt_id': self.hallazgo_id.plan_id.project_id.edt_raiz_id.id, 'revisor_id': self.ejecutor_id.id, 'accion_id': self.id})
        return result

    def wkf_por_aprobar(self):
        self.state = 'por_aprobar'
        # buscar los usuarios jefe_dependencia de la accion
        enviar_a = []
        jefe_dependencia = self.dependencia_id.manager_id
        enviar_a.append(jefe_dependencia.user_id.partner_id.id)
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
                partner_ids=[accion.jefe_dependencia_id.partner_id.id, accion.ejecutor_id.partner_id.id]
            )
        return True

    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False, xtra=None):
        """Se sobreescribe para poder adicionar keyworkds a usar en filtros de la vista"""
        new_args = adiciona_keywords_en_search(self, cr, uid, args, offset, limit, order, context, count, xtra)
        return super(plan_mejoramiento_accion, self).search(cr, uid, new_args, offset, limit, order, context, count)


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
    state = fields.Selection(
        related='tipo_calificacion_id.estado',
        readonly=True,
        store=True,
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

        es_jefe_dependencia = self.accion_id.jefe_dependencia_id.id == self.env.uid
        if vals.get('aprobacion_jefe_dependencia', False) and not es_jefe_dependencia:
            raise AccessError('el campo [Aprobación por Jefe de la Dependencia] solo lo puede diligenciar el usuario Jefe de la Dependencia')

        avance = super(plan_mejoramiento_avance, self).create(vals)
        return avance

    @api.one
    def write(self, vals):
        # se valida que los avances ya calificados no sean modificados
        es_responsable_tareas = self.env.user.has_group_v8('plan_mejoramiento_idu.group_responsable_tareas')[0]
        if len(vals) == 1 and self.tipo_calificacion_id and es_responsable_tareas:
            raise AccessError('No se permite modificar un avance que ya ha sido calificado')
        # se valida que solo el jefe_dependencia apruebe el avance
        es_jefe_dependencia = self.accion_id.jefe_dependencia_id.id == self.env.uid
        if 'aprobacion_jefe_dependencia' in vals and not es_jefe_dependencia:
            raise AccessError('el campo [Aprobación por Jefe de la Dependencia] solo lo puede diligenciar el usuario Jefe Dependencia')
        # se valida que el usuario oci solo pueda realizar la calificación una vez este aprobado el avance por el usuario jefe_dependencia
        es_oci = self.env.user.has_group_v8('plan_mejoramiento_idu.group_oci')[0]
        if ('tipo_calificacion_id' in vals or 'porcentaje' in vals) and es_oci and self.aprobacion_jefe_dependencia == False:
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
