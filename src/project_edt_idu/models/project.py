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
from openerp.exceptions import ValidationError
import datetime
import workdays


def calcular_duracion_en_dias(date1, date2, return_dates=False):
    if not date1 or not date2:
        return 0
    formato = '%Y-%m-%d %H:%M:%S'
    if len(date1) == 10:
        formato = '%Y-%m-%d'
    fecha_inicio = datetime.datetime.strptime(date1, formato)
    fecha_fin = datetime.datetime.strptime(date2, formato)
    duracion = workdays.networkdays(fecha_inicio, fecha_fin)
    if return_dates:
        return fecha_inicio, fecha_fin, duracion
    return duracion

def calcular_duracion_en_dias_fecha_estado(date1, date2):
    """Calculo de duración utilizado para cuando se utiliza una fecha de estado para pronosticar
    valores de progreso y costo a una fecha"""
    fecha_inicio, fecha_fin, duracion = calcular_duracion_en_dias(date1, date2, True)
    if fecha_fin.weekday() < 5: # no es sabado/domingo
        duracion = duracion - 1 # Para ajustarse a como lo hace en ms-project
    return duracion


PROJECT_TASK_REPORTE_AVANCE_NIVEL_ALERTA=[
    ('ninguno', 'Ninguno'),
    ('bajo', 'Bajo'),
    ('medio', 'Medio'),
    ('alto', 'Alto'),
]

class project_edt(models.Model):
    _name = 'project.edt'
    _description = 'EDT de Proyecto'
    _inherit = ['models.soft_delete.mixin']
    _order = 'numero ASC'

    # -------------------
    # Fields
    # -------------------
    name = fields.Char(
        string='Nombre',
        required=True,
        size=255,
    )
    sequence = fields.Integer(
        string='Sequencia',
        required=False,
    )
    numero = fields.Char(
        string='Número',
        required=False,
        readonly=True,
        size=64,
        store=True,
        compute='_compute_numero',
        inverse='_compute_numero_inverse',
    )
    numero_manual = fields.Char(
        string='Número (asignado manualmente)',
        help='Asignado en el wizard para importar masivamente y conservarlo como el número a utilizar',
        required=False,
        readonly=True,
        size=64,
    )
    ms_project_guid = fields.Char(
        string='GUID en ms-project',
        required=False,
        size=64,
        index=True,
    )
    user_id = fields.Many2one(
        string='Responsable',
        required=False,
        comodel_name='res.users',
        ondelete='restrict',
        default=lambda self: self._context.get('uid', False),
    )
    state = fields.Selection(
        string='Estado',
        required=True,
        selection=[
            ('abierto', 'abierto'),
            ('cerrado', 'cerrado'),
            ('cancelado', 'cancelado'),
            ('aplazado', 'aplazado'),
        ],
        default='abierto',
    )
    fecha_planeada_inicio = fields.Date(
        string='Fecha Planeada de Inicio',
        required=False,
        readonly=True,
        track_visibility='onchange',
    )
    fecha_planeada_fin = fields.Date(
        string='Fecha Planeada de Finalización',
        required=False,
        readonly=True,
    )
    duracion_planeada_dias = fields.Integer(
        string='Duración Planeada',
        help='Duración Planeada en Días',
        required=False,
        compute='_compute_duracion_planeada',
        store=True,
    )
    fecha_inicio = fields.Date(
        string='Fecha de Inicio',
        required=False,
    )
    fecha_fin = fields.Date(
        string='Fecha de Finalización',
        required=False,
    )
    duracion_dias = fields.Integer(
        string='Duración',
        help='Duración Actual en Días',
        required=False,
        compute='_compute_duracion_dias',
        store=True,
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
    costo_planeado = fields.Monetary(
        string='Costo Planeado',
        help='''El costo planeado es la suma del costo planeado de sus tareas.''',
        required=False,
        readonly=True,
    )
    costo = fields.Monetary(
        string='Costo Ejecutado',
        required=False,
        readonly=True,
    )
    progreso = fields.Integer(
        string='Progreso',
        required=False,
        readonly=True,
        default=0,
    )
    project_id = fields.Many2one(
        string='Proyecto',
        required=False,
        track_visibility='onchange',
        comodel_name='project.project',
        ondelete='restrict',
        default=lambda self: self._context.get('project_id', None),
    )
    task_ids = fields.One2many(
        string='Tareas',
        required=False,
        comodel_name='project.task',
        inverse_name='edt_id',
        ondelete='restrict',
    )
    parent_id = fields.Many2one(
        string='EDT Padre',
        required=False,
        comodel_name='project.edt',
        ondelete='restrict',
        default=lambda self: self._context.get('parent_id', None),
    )
    child_ids = fields.One2many(
        string='EDT Hijas',
        required=False,
        comodel_name='project.edt',
        inverse_name='parent_id',
        ondelete='restrict',
    )
    project_manager_id = fields.Many2one(
        string='Responsable Proyecto',
        required=False,
        related='project_id.user_id',
        comodel_name='res.users',
        ondelete='restrict',
    )
    programador_id = fields.Many2one(
        string='Programador',
        required=False,
        track_visibility='onchange',
        comodel_name='res.users',
        ondelete='restrict',
        default=lambda self: self._context.get('programador_id', None),
    )
    progreso_aprobado = fields.Integer(
        string='Progreso Aprobado',
        required=False,
        readonly=True,
        help='''Indica el progreso registrado y que ha seguido el flujo de aprobación''',
        default=0,
    )
    fecha_estado = fields.Date(
        string='Fecha de Estado',
        help="Indica la fecha sobre la cual se va a calcular el retraso",
        readonly=False,
    )
    retraso = fields.Integer(
        string="Retraso",
        required=False,
        store=True,
        compute="_compute_retraso",
        help='''El retraso es la diferencia entre el progreso actual registrado y 
            el avance planeado esperado para la fecha de estado.''',
    )
    costo_planeado_fecha = fields.Monetary(
        string='Costo Planeado a Fecha',
        required=False,
        readonly=True,
        store=True,
        compute="_compute_retraso",
        help='''Costo planeado a la fecha de estado''',
    )
    # -------------------
    # methods
    # -------------------

    @api.model
    def create(self, vals):
        # print self._name, vals.get('numero'), self.env.context
        es_carga_masiva = self.env.context.get('carga_masiva', False)
        edt = super(project_edt, self).create(vals)
        if not es_carga_masiva and ('fecha_inicio' in vals or 'fecha_fin' in vals):
            # Asignar fechas planeadas de inicio y fin  apartir de las fechas dadas
            # Si no han sido definidas
            upd_vals = {}
            if not edt.fecha_planeada_inicio and vals.get('fecha_inicio', False):
                upd_vals['fecha_planeada_inicio'] = vals['fecha_inicio']
            if not edt.fecha_planeada_fin and vals.get('fecha_fin', False):
                upd_vals['fecha_planeada_fin'] = vals['fecha_fin']
            if upd_vals:
                edt.write(upd_vals)

        if not es_carga_masiva:
            edt.sudo()._subscribe_resources(vals)

        if not es_carga_masiva and ('costo' in vals or 'progreso' in vals):
            self.parent_id.sudo()._compute_progreso()

        if not es_carga_masiva and ('fecha_fin' in vals or 'fecha_inicio' in vals or 'duracion_dias' in vals):
            self.parent_id.sudo()._compute_fechas()

        return edt

    @api.one
    def write(self, vals):
        # print self._name, self.numero, vals, self.env.context
        es_carga_masiva = self.env.context.get('carga_masiva', False)
        if not es_carga_masiva and ('fecha_inicio' in vals or 'fecha_fin' in vals):
            # Asignar fechas planeadas de inicio y fin  apartir de las fechas dadas
            # Si no han sido definidas
            if not self.fecha_planeada_inicio and not vals.get('fecha_planeada_inicio') and vals.get('fecha_inicio'):
                vals['fecha_planeada_inicio'] = vals['fecha_inicio']
            if not self.fecha_planeada_fin and not vals.get('fecha_planeada_fin') and vals.get('fecha_fin'):
                vals['fecha_planeada_fin'] = vals['fecha_fin']

        res = super(project_edt, self).write(vals)
        if not es_carga_masiva:
            self.sudo()._subscribe_resources(vals)

        if not es_carga_masiva and ('costo' in vals or 'progreso' in vals):
            self.parent_id.sudo()._compute_progreso()

        if not es_carga_masiva and ('fecha_fin' in vals or 'fecha_inicio' in vals or 'duracion_dias' in vals):
            self.parent_id.sudo()._compute_fechas()

        return res

    @api.one
    def _subscribe_resources(self, vals):
        """Inscribe a los responsables y programadores como seguidores del proyecto"""
        recurso_fields = ['user_id', 'programador_id']
        user_ids = []
        for field in recurso_fields:
            if vals.get(field):
                user_ids.append(vals.get(field))
        if user_ids and self.project_id:
                self.project_id.message_subscribe_users(user_ids)

    @api.one
    @api.constrains('fecha_planeada_inicio')
    def _check_fecha_planeada_inicio(self):
        self._check_fechas_planeadas()

    @api.one
    @api.constrains('fecha_planeada_fin')
    def _check_fecha_planeada_fin(self):
        self._check_fechas_planeadas()

    @api.one
    def _check_fechas_planeadas(self):
        if(self.fecha_planeada_inicio and self.fecha_planeada_fin and
           self.fecha_planeada_inicio > self.fecha_planeada_fin
            ):
            raise ValidationError("Fecha de inicio no puede ser posterior a la de finalización")

    @api.one
    @api.constrains('fecha_inicio')
    def _check_fecha_inicio(self):
        self._check_fechas()

    @api.one
    @api.constrains('fecha_fin')
    def _check_fecha_fin(self):
        self._check_fechas()

    @api.one
    def _check_fechas(self):
        if(self.fecha_inicio and self.fecha_fin and
           self.fecha_inicio > self.fecha_fin
            ):
            raise ValidationError("Fecha de inicio no puede ser posterior a la de finalización")

    @api.onchange('fecha_planeada_inicio')
    def _onchange_fecha_planeada_inicio(self):
        try:
            self._check_fecha_planeada_inicio()
        except Exception as e:
            return {
                'title': "Error de Validación",
                'warning': {'message': e.name}
            }

    @api.onchange('fecha_planeada_fin')
    def _onchange_fecha_planeada_fin(self):
        try:
            self._check_fecha_planeada_fin()
        except Exception as e:
            return {
                'title': "Error de Validación",
                'warning': {'message': e.name}
            }

    @api.onchange('fecha_inicio')
    def _onchange_fecha_inicio(self):
        try:
            self._check_fecha_inicio()
        except Exception as e:
            return {
                'title': "Error de Validación",
                'warning': {'message': e.name}
            }

    @api.onchange('fecha_fin')
    def _onchange_fecha_fin(self):
        try:
            self._check_fecha_fin()
        except Exception as e:
            return {
                'title': "Error de Validación",
                'warning': {'message': e.name}
            }
    # -------------------
    # Campos Computados
    # -------------------
    @api.one
    @api.depends('parent_id', 'parent_id.sequence', 'parent_id.numero_manual', 'parent_id.child_ids.numero_manual', 'parent_id.child_ids.sequence', 'parent_id.task_ids.numero_manual', 'parent_id.task_ids.sequence', 'numero_manual', 'sequence')
    def _compute_numero(self):
        if self.numero_manual:
            self.numero = self.numero_manual
        elif self.parent_id:
            edt_num = self.parent_id.numero
            children = self.parent_id.child_ids.sorted(key=lambda r: r.sequence).mapped('id')
            try:
                position = children.index(self.id) + 1
            except ValueError, e:
                position = 0
            self.numero = "{0}.{1}".format(edt_num, position)
        else:
            self.numero =  '1'

    def _compute_numero_inverse(self):
        self.numero_manual = self.numero

    @api.one
    def _compute_progreso(self):
        """ Formula para cálculo de progreso en ms-project
        https://support.microsoft.com/en-us/kb/101495

        Name             Outline   Dur   Sch St   Sch Fin  %Comp   Act Dur

        Top Summary           1       8d    1/1/96    1/10/96   23%    1.8d
        Subordinate Summary   1.1     5d    1/1/96    1/5/96    25%    1.25d
          task1              1.1.1   1d    1/1/96    1/1/96    50%    0.5d
          task2              1.1.2   1d    1/5/96    1/5/96     0%      0d
        task3                1.2     1d    1/10/96   1/10/96   10%    0.1d

        Formula Subordinate Summary
          (1d*50%+1d*0%)/2d=25%
          [(task1 dur) * (task1 %Comp) + (task2 dur) * (task2 %Comp)] /
          [(task1 dur) + (task2 dur)]

        Formula Top Summary
          (5d*25%+1d*10%)/6d=22.5% (=23%)
          [(Subordinate Summary dur) * (Subordinate Summary %Comp) + (task3 dur) * (task3 %Comp)] /
          [(Subordinate Summary dur) + (task3 dur)]
        """
        # print '_compute_progreso', self._name, self.id, self.numero
        vals = {
            'costo': 0,
            'progreso': 0,
        }
        costo = 0
        numerador = 0
        denominador = 0
        for edt in self.child_ids:
            numerador += (edt.duracion_dias * edt.progreso)
            denominador += edt.duracion_dias
            costo += edt.costo

        for task in self.task_ids:
            numerador += (task.duracion_dias * task.progreso)
            denominador += task.duracion_dias
            costo += task.costo

        if denominador:
            vals['progreso'] = round(numerador / denominador)
        vals['costo'] = costo
        self.write(vals)

    @api.one
    @api.depends('fecha_planeada_inicio', 'fecha_planeada_fin')
    def _compute_duracion_planeada(self):
        # print '_compute_duracion_planeada', self._name, self.id, self.numero
        self.duracion_planeada_dias = calcular_duracion_en_dias(self.fecha_planeada_inicio, self.fecha_planeada_fin)

    @api.one
    @api.depends('fecha_inicio', 'fecha_fin')
    def _compute_duracion_dias(self):
        # print '_compute_duracion_dias', self._name, self.id, self.numero
        self.duracion_dias = calcular_duracion_en_dias(self.fecha_inicio, self.fecha_fin)

    @api.one
    def _compute_fechas(self):
        # print '_compute_fechas', self._name, self.id, self.numero
        # print 'Calculando {} {} {} {}'.format(self.numero, self.fecha_inicio, self.fecha_fin, self.id)
        vals = {
            'fecha_inicio': False,
            'fecha_fin': False,
            'duracion_dias': 0,
        }
        (edt_inicio, edt_fin) = self._obtener_rango_fecha_edt()
        (task_start, task_end) = self._obtener_rango_fecha_tareas()
        if not edt_inicio and not edt_fin and not task_start and not task_end:
            return
        if task_start and task_end and not edt_inicio and not edt_fin:
            vals['fecha_inicio'] = fields.Date.to_string(task_start)
            vals['fecha_fin'] = fields.Date.to_string(task_end)
        elif edt_inicio and edt_fin and not task_start and not task_end:
            if task_start or edt_inicio:
                vals['fecha_inicio'] = fields.Date.to_string(edt_inicio)
            if task_end or edt_fin:
                vals['fecha_fin'] = fields.Date.to_string(edt_fin)
        else:
            if task_start < edt_inicio:
                vals['fecha_inicio'] = fields.Date.to_string(task_start)
            else:
                vals['fecha_inicio'] = fields.Date.to_string(edt_inicio)
            if task_end > edt_fin:
                vals['fecha_fin'] = fields.Date.to_string(task_end)
            else:
                vals['fecha_fin'] = fields.Date.to_string(edt_fin)

        if vals['fecha_inicio'] and vals['fecha_fin']:
            vals['duracion_dias'] = calcular_duracion_en_dias(vals['fecha_inicio'], vals['fecha_fin'])
        self.write(vals)

    def _obtener_rango_fecha_tareas(self):
        if isinstance(self.id, models.NewId):
            return False, False
        self.ensure_one()
        fecha_inicio = False
        fecha_fin = False
        self.env.cr.execute("""
            SELECT
                MIN(fecha_inicio), MAX(fecha_fin)
            FROM
                project_task
            WHERE
                edt_id = %s
            """, (self.id, )
        )
        result = self.env.cr.fetchall()
        if len(result):
            if result[0][0]:
                fecha_inicio = datetime.datetime.strptime(result[0][0], '%Y-%m-%d').date()
            if result[0][1]:
                fecha_fin = datetime.datetime.strptime(result[0][1], '%Y-%m-%d').date()
        return (fecha_inicio, fecha_fin)

    def _obtener_rango_fecha_edt(self):
        if isinstance(self.id, models.NewId):
            return False, False
        self.ensure_one()
        fecha_inicio = False
        fecha_fin = False
        self.env.cr.execute("""
            SELECT
                MIN(fecha_inicio), MAX(fecha_fin)
            FROM
                project_edt
            WHERE
                parent_id = %s
            """, (self.id,)
        )
        result = self.env.cr.fetchall()
        if len(result):
            if result[0][0]:
                fecha_inicio = datetime.datetime.strptime(result[0][0], '%Y-%m-%d').date()
            if result[0][1]:
                fecha_fin = datetime.datetime.strptime(result[0][1], '%Y-%m-%d').date()
        return (fecha_inicio, fecha_fin)

    @api.one
    @api.depends('progreso', 'fecha_estado', 'fecha_planeada_inicio', 'fecha_planeada_fin', 'costo_planeado')
    def _compute_retraso(self):
        #print '_compute_retraso', self._name, self.id, self.numero, self.fecha_estado, self.duracion_planeada_dias
        if not self.fecha_estado:
            return

        progreso_esperado, costo_planeado_fecha = self._compute_ejecucion_esperada_a_fecha_estado()
        retraso = 0

        if progreso_esperado:
            retraso = progreso_esperado - self.progreso
        self.retraso = retraso
        self.costo_planeado_fecha = costo_planeado_fecha

    def _compute_ejecucion_esperada_a_fecha_estado(self):
        """Calcula el progreso esperado y costo esperado a la fecha de estado,
        tomando como base los valores ya calculados por objeto
        """
        # print '_compute_ejecucion_esperada_a_fecha_estado', self._name, self.id, self.numero
        costo = 0
        costo_planeado_fecha = 0
        progreso_esperado = 0
        progreso_diario = 100/float(self.duracion_planeada_dias)
        dias_esperados = calcular_duracion_en_dias_fecha_estado(self.fecha_planeada_inicio, self.fecha_estado)
        if dias_esperados < 0:
            dias_esperados = 0

        if self.fecha_planeada_inicio > self.fecha_estado:
            progreso_esperado = 0
            costo_planeado_fecha = 0
        elif self.fecha_planeada_fin < self.fecha_estado:
            progreso_esperado = 100
            for task in self.task_ids:
                costo_planeado_fecha += task.costo_planeado_fecha
            for edt in self.child_ids:
                costo_planeado_fecha += edt.costo_planeado_fecha
        else:
            numerador = 0
            denominador = 0
            for task in self.task_ids:
                numerador += float(task.duracion_planeada_dias) * (task.progreso + task.retraso) # Duración por avance esperado
                denominador += float(task.duracion_planeada_dias)
                costo_planeado_fecha += task.costo_planeado_fecha

            for edt in self.child_ids:
                numerador += float(edt.duracion_planeada_dias)*(edt.progreso + edt.retraso) # Duración por avance esperado
                denominador += float(edt.duracion_planeada_dias)
                costo_planeado_fecha += edt.costo_planeado_fecha

            if denominador:
                progreso_esperado = round((numerador / denominador))

        if progreso_esperado > 100:
            progreso_esperado = 100

        return progreso_esperado, costo_planeado_fecha

    def _recorrer_arbol_postorder(self, edt, resultado):
        """ Recorre el árbol EDT/Tareas colocando en el listado resultado primero las hojas y al final la raiz,
        mayores detalles de ordenamiento ver https://en.wikipedia.org/wiki/Tree_traversal"""
        if len(edt.task_ids.ids):
            resultado.append(edt.task_ids)
        if len(edt.child_ids.ids):
            for child in edt.child_ids:
                self._recorrer_arbol_postorder(child, resultado)
        resultado.append(edt)
        return resultado


class project_task(models.Model):
    _name = 'project.task'
    _inherit = ['project.task', 'models.soft_delete.mixin', 'project.recompute_hack']

    # -------------------
    # Fields
    # -------------------
    edt_id = fields.Many2one(
        string='EDT',
        required=False,
        track_visibility='onchange',
        comodel_name='project.edt',
        ondelete='restrict',
        default=lambda self: self._context.get('edt_id', self.env['project.edt'].browse()),
        # Retorna un objeto vacio
        # see https://github.com/odoo/odoo/issues/10906
    )
    ms_project_guid = fields.Char(
        string='ID en ms-project',
        required=False,
        size=64,
        index=True,
    )
    company_id = fields.Many2one(
        string='Compañía',
        required=True,
        readonly=True,
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
    costo_planeado = fields.Monetary(
        string='Costo Planeado',
        required=False,
        readonly=False,
    )
    costo = fields.Monetary(
        string='Costo Ejecutado',
        required=False,
        readonly=True,
    )
    progreso = fields.Integer(
        string='Progreso',
        required=False,
        readonly=True,
    )
    revisor_id = fields.Many2one(
        string='Revisor',
        required=False,
        track_visibility='onchange',
        comodel_name='res.users',
        ondelete='restrict',
    )
    progreso_metodo = fields.Selection(
        string='Forma de cálculo del progreso',
        required=False,
        track_visibility='onchange',
        default='manual',
        help='''- Pendientes: se toman los pendientes para definir el avance.
- Manual: Se registra el progreso manualmente''',
        selection=[
            ('manual', 'manual'),
            ('pendientes', 'pendientes'),
        ],
    )
    fecha_planeada_inicio = fields.Date(
        string='Fecha de Inicio Planeada',
        required=False,
        readonly=True,
        track_visibility='onchange',
    )
    fecha_planeada_fin = fields.Date(
        string='Fecha de Finalización Planeada',
        required=False,
        readonly=True,
        track_visibility='onchange',
    )
    fecha_inicio = fields.Date(
        string='Fecha de Inicio',
        required=True,
        default=fields.Date.today,
    )
    fecha_fin = fields.Date(
        string='Fecha de Finalización',
        required=True,
        default=fields.Date.today,
    )
    duracion_planeada_dias = fields.Integer(
        string='Duración Planeada',
        help='Duración Planeada en Días',
        required=False,
        compute='_compute_duracion_planeada',
        store=True,
    )
    duracion_dias = fields.Integer(
        string='Duración',
        help='Duración Actual en Días',
        required=False,
        compute='_compute_duracion',
        store=True,
    )
    pendiente_ids = fields.One2many(
        string='Lista de Pendientes',
        required=False,
        comodel_name='project.task.pendiente',
        inverse_name='task_id',
        ondelete='restrict',
    )
    registro_progreso_ids = fields.One2many(
        string='Registros de Progreso',
        required=False,
        readonly=True,
        comodel_name='project.task.registro_progreso',
        inverse_name='task_id',
        ondelete='restrict',
        help='''El registro se diligencia automáticamente o manualmente dependiendo del método de cálculo de progreso''',
    )
    numero = fields.Char(
        string='Número',
        required=False,
        readonly=True,
        size=64,
        store=True,
        compute='_compute_numero',
    )
    numero_manual = fields.Char(
        string='Número (asignado manualmente)',
        help='Asignado en el wizard para importar masivamente y conservarlo como el número a utilizar',
        required=False,
        readonly=True,
        size=64,
    )
    progreso_aprobado = fields.Integer(
        string='Progreso Aprobado',
        required=False,
        readonly=True,
        default=0,
    )
    terminado = fields.Boolean(
        string='Terminado',
        required=False,
        track_visibility='onchange',
        help='''La tarea fue marcada como terminada''',
        default=False,
    )
    cantidad_planeada = fields.Float(
        string='Cantidad Planeada',
        required=False,
        track_visibility='onchange',
    )
    cantidad = fields.Float(
        string='Cantidad',
        required=False,
        track_visibility='onchange',
    )
    product_id = fields.Many2one(
        string='Código APU',
        required=False,
        track_visibility='onchange',
        comodel_name='product.product',
        ondelete='restrict',
        help='''Código APU oficial del IDU – Análisis de Precios Unitarios''',
    )
    project_id = fields.Many2one(
      default=lambda self: self._context.get('project_id', None),
    )
    fecha_estado = fields.Date(
        string='Fecha de Estado',
        help="Indica la fecha sobre la cual se va a calcular el retraso",
        readonly=False,
    )
    retraso = fields.Integer(
        string="Retraso",
        required=False,
        store=True,
        compute="_compute_retraso",
        help='''El retraso es la diferencia entre el progreso actual registrado y
            el avance planeado esperado para la fecha de estado.''',
    )
    costo_planeado_fecha = fields.Monetary(
        string='Costo Planeado a la Fecha de Estado',
        required=False,
        store=True,
        compute="_compute_retraso",
        help='''Costo planeado a la fecha de estado.''',
        readonly=True,
    )
    # -------------------
    # methods
    # -------------------
    @api.model
    def create(self, vals):
        # print self._name, vals.get('numero'), self.env.context
        es_carga_masiva = self.env.context.get('carga_masiva', False)
        task = super(project_task, self).create(vals)
        if not es_carga_masiva and ('fecha_inicio' in vals or 'fecha_fin' in vals):
            # Asignar fechas planeadas de inicio y fin  apartir de las fechas dadas
            # Si no han sido definidas
            upd_vals = {}
            if not task.fecha_planeada_inicio and vals.get('fecha_inicio', False):
                upd_vals['fecha_planeada_inicio'] = vals['fecha_inicio']
            if not task.fecha_planeada_fin and vals.get('fecha_fin', False):
                upd_vals['fecha_planeada_fin'] = vals['fecha_fin']
            if upd_vals:
                task.write(upd_vals)

        if not es_carga_masiva and ('fecha_inicio' in vals or 'fecha_fin' in vals):
            # Actualizar fechas del árbol de la EDT
            task.edt_id.sudo()._compute_fechas()

        if not es_carga_masiva and ('progreso' in vals or 'costo' in vals):
            # Solo el progreso y el costo afectan los valores en el árbol EDT
            task.edt_id.sudo()._compute_progreso()

        # Crea registro_progreso
        if ('progreso' in vals or 'cantidad' in vals or 'costo' in vals):
            task._set_progreso(vals)
        if not es_carga_masiva:
            task.sudo()._subscribe_resources(vals)
        return task

    @api.one
    def write(self, vals):
        # print self._name, self.numero, vals, self.env.context
        es_carga_masiva = self.env.context.get('carga_masiva', False)
        if not es_carga_masiva and ('fecha_inicio' in vals or 'fecha_fin' in vals):
            # Asignar fechas planeadas de inicio y fin  apartir de las fechas dadas
            # Si no han sido definidas
            if not self.fecha_planeada_inicio and not vals.get('fecha_planeada_inicio') and vals.get('fecha_inicio'):
                vals['fecha_planeada_inicio'] = vals['fecha_inicio']
            if not self.fecha_planeada_fin and not vals.get('fecha_planeada_fin') and vals.get('fecha_fin'):
                vals['fecha_planeada_fin'] = vals['fecha_fin']

        res = super(project_task, self).write(vals)
        if not es_carga_masiva and ('fecha_inicio' in vals or 'fecha_fin' in vals):
            # Actualizar fechas del árbol de la EDT
            self.edt_id.sudo()._compute_fechas()

        if (not self.env.context.get('no_crear_registro_progreso') and
           ('progreso' in vals or 'cantidad' in vals or 'costo' in vals)
        ):
            self._set_progreso(vals)

        if not es_carga_masiva and ('progreso' in vals or 'costo' in vals):
            # Solo el progreso y el costo afectan los valores en el árbol EDT
            # No calcular cuando es carga masiva
            self.edt_id.sudo()._compute_progreso()

        if not es_carga_masiva:
            # Cuando carga masiva en la creación se realizó la suscripción
            self.sudo()._subscribe_resources(vals)
        return res

    def _store_history(self, cr, uid, ids, context=None):
        # en nuestra versión no utilizamos la historia
        # que viene por defecto en las tareas de odoo
        return True

    @api.one
    def _subscribe_resources(self, vals):
        """Inscribe a los responsables y revisores como seguidores de la Tarea, y del proyecto"""
        recurso_fields = ['user_id', 'revisor_id']
        user_ids = []
        for field in recurso_fields:
            if vals.get(field):
                user_ids.append(vals.get(field))
        if user_ids:
            self.message_subscribe_users(user_ids)
            if self.project_id:
                self.project_id.message_subscribe_users(user_ids)

    @api.one
    @api.constrains('fecha_planeada_inicio')
    def _check_fecha_planeada_inicio(self):
        self._check_fechas_planeadas()

    @api.one
    @api.constrains('fecha_planeada_fin')
    def _check_fecha_planeada_fin(self):
        self._check_fechas_planeadas()

    @api.one
    def _check_fechas_planeadas(self):
        if(self.fecha_planeada_inicio and self.fecha_planeada_fin and
           self.fecha_planeada_inicio > self.fecha_planeada_fin
            ):
            raise ValidationError("Fecha de inicio no puede ser posterior a la de finalización")

    @api.onchange('fecha_planeada_inicio')
    def _onchange_fecha_planeada_inicio(self):
        try:
            self._check_fecha_planeada_inicio()
        except Exception as e:
            return {
                'title': "Error de Validación",
                'warning': {'message': e.name}
            }

    @api.onchange('fecha_planeada_fin')
    def _onchange_fecha_planeada_fin(self):
        try:
            self._check_fecha_planeada_fin()
        except Exception as e:
            return {
                'title': "Error de Validación",
                'warning': {'message': e.name}
            }

    @api.onchange('terminado')
    def _onchange_terminado(self):
        # https://www.odoo.com/documentation/8.0/howtos/backend.html#onchange
        pass

    @api.multi
    def registrar_avance_wizard_button(self):
        view = self.env.ref('project_edt_idu.edt_wizard_registrar_progreso_tarea_form')
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.edt.wizard.registrar_progreso_tarea',
            'context': { 'task_id': self.id },
            'view_id': view.id,
            'target': 'new',
            'views': [(view.id, 'form'),
                    (False, 'form')],
        }

    # -------------------
    # Campos Computados
    # -------------------
    @api.one
    @api.depends('fecha_inicio', 'fecha_fin')
    def _compute_duracion(self):
        # print '_compute_duracion', self._name, self.id, self.numero
        self.duracion_dias = calcular_duracion_en_dias(self.fecha_inicio, self.fecha_fin)

    @api.one
    @api.depends('fecha_planeada_inicio', 'fecha_planeada_fin')
    def _compute_duracion_planeada(self):
        # print '_compute_duracion_planeada', self._name, self.id, self.numero
        self.duracion_planeada_dias = calcular_duracion_en_dias(self.fecha_planeada_inicio, self.fecha_planeada_fin)

    @api.one
    @api.depends('edt_id', 'edt_id.numero_manual', 'numero_manual', 'edt_id.child_ids.numero_manual', 'edt_id.task_ids.numero_manual')
    def _compute_numero(self):
        if self.numero_manual:
            self.numero = self.numero_manual
        elif self.edt_id:
            edt_num = self.edt_id.numero
            cnt_edts = len(self.edt_id.child_ids)
            children = self.edt_id.task_ids.sorted(key=lambda r: r.sequence).mapped('id')
            position = cnt_edts + children.index(self.id) + 1
            self.numero =  "{0}.{1}".format(edt_num, position)
        elif self.project_id:
            children = self.project_id.task_ids.sorted(key=lambda r: r.sequence).mapped('id')
            try:
                position = children.index(self.id) + 1
            except ValueError, e:
                position = 0
            self.numero = position
        else:
            if isinstance(self.id, models.NewId):
                self.numero = 0
            else:
                self.numero =  self.id

    @api.one
    def _compute_progreso(self):
        # print '_compute_progreso', self._name, self.id, self.numero
        vals = {
            'progreso': 0,
            'costo': 0,
            'cantidad': 0,
        }
        if isinstance(self.id, models.NewId):
            return

        # Traer el último project.task.registro_progreso de esta tarea organizado por fecha
        self.env.cr.execute("""
            SELECT porcentaje, costo, cantidad, id, fecha
            FROM project_task_registro_progreso
            WHERE task_id = {0}
            AND active = 't'
            ORDER BY fecha DESC, id DESC
            LIMIT 1""".format(self.id)
        )
        resultados = self.env.cr.fetchall()
        #print 'TAREA', self.id, resultados
        if len(resultados):
            vals['progreso'] = resultados[0][0]
            vals['costo'] = resultados[0][1]
            vals['cantidad'] = resultados[0][2]

        self.with_context({'no_crear_registro_progreso': True}).write(vals)

    @api.one
    def _set_progreso(self, vals):
        # print '_set_progreso', self._name, self.id, self.numero
        # Crear un project.task.registro_progreso con fecha de hoy o que venga del contexto
        datos = {
            'task_id': self.id,
            'name': 'Avance cargado masivamente el {0}'.format(datetime.date.today().strftime('%d, %b %Y')),
        }
        for field_t, field_rp in {'progreso': 'porcentaje', 'costo': 'costo', 'cantidad': 'cantidad'}.iteritems():
            datos[field_rp] = vals.get(field_t, 0)

        ctx = dict(self.env.context)
        ctx.update({'no_actualizar_tarea': True})
        self.env['project.task.registro_progreso'].with_context(ctx).create(datos)

    @api.one
    @api.depends('progreso', 'fecha_estado', 'fecha_planeada_inicio', 'fecha_planeada_fin', 'costo_planeado')
    def _compute_retraso(self):
        #print '_compute_retraso', self._name, self.id, self.numero, self.fecha_estado, self.duracion_planeada_dias
        if not self.fecha_estado:
            return
        progreso_esperado, costo_planeado_fecha = self._compute_progreso_esperado(self.fecha_estado)
        self.retraso = progreso_esperado - self.progreso
        self.costo_planeado_fecha = costo_planeado_fecha

    def _compute_progreso_esperado(self, fecha_estado):
        progreso_esperado = 0
        progreso_diario = 100/float(self.duracion_planeada_dias)
        dias_esperados = calcular_duracion_en_dias_fecha_estado(self.fecha_planeada_inicio, fecha_estado)
        if dias_esperados < 0:
            dias_esperados = 0
        if self.fecha_planeada_inicio > fecha_estado:
            progreso_esperado = 0
        elif self.fecha_planeada_fin < fecha_estado:
            progreso_esperado = 100
        else:
            progreso_esperado = round(dias_esperados * progreso_diario)
        if progreso_esperado > 100:
            progreso_esperado = 100

        costo_planeado_fecha = (progreso_esperado * self.costo_planeado) / 100
        # print '_compute_progreso_esperado', self._name, self.id, self.numero, progreso_esperado, costo_planeado_fecha
        return progreso_esperado, costo_planeado_fecha


class project_project(models.Model):
    _name = 'project.project'
    _inherit = ['project.project', 'models.soft_delete.mixin']

    # -------------------
    # Fields
    # -------------------
    edt_raiz_id = fields.Many2one(
        string='EDT',
        required=False,
        track_visibility='onchange',
        comodel_name='project.edt',
        ondelete='restrict',
    )
    edt_ids = fields.One2many(
        string='EDT Asociadas',
        required=False,
        comodel_name='project.edt',
        inverse_name='project_id',
        ondelete='restrict',
    )
    reporte_avance_tarea_ids = fields.One2many(
        string='Reportes de Avance en Tareas',
        required=False,
        comodel_name='project.task.reporte_avance',
        inverse_name='project_id',
        ondelete='restrict',
    )
    progreso = fields.Integer(
        string='Progreso',
        required=False,
        readonly=True,
        related='edt_raiz_id.progreso',
    )
    fecha_inicio = fields.Date(
        string='Fecha de Inicio',
        required=False,
        readonly=True,
        track_visibility='onchange',
        related='edt_raiz_id.fecha_inicio',
    )
    fecha_fin = fields.Date(
        string='Fecha de Finalización',
        required=False,
        readonly=True,
        track_visibility='onchange',
        related='edt_raiz_id.fecha_fin',
    )
    fecha_planeada_inicio = fields.Date(
        string='Fecha de Inicio Planeada',
        required=False,
        readonly=True,
        track_visibility='onchange',
        related='edt_raiz_id.fecha_planeada_inicio',
    )
    fecha_planeada_fin = fields.Date(
        string='Fecha de Finalización Planeada',
        required=False,
        readonly=True,
        track_visibility='onchange',
        related='edt_raiz_id.fecha_planeada_fin',
    )
    programador_id = fields.Many2one(
        string='Programador del Proyecto',
        required=False,
        track_visibility='onchange',
        comodel_name='res.users',
        ondelete='restrict',
    )
    reportar_costo = fields.Boolean(
        string='En Reporte de Avance incluir Costo de la Tarea',
        required=False,
        default=False,
    )
    reportar_cantidad = fields.Boolean(
        string='En Reporte de Avance incluir Cantidades',
        required=False,
        default=False,
    )

    # -------------------
    # methods
    # -------------------
    @api.multi
    def edt_arbol_view_button(self):
        model, view_id = self.env['ir.model.data'].get_object_reference('project_edt_idu', 'arbol_edt_tree')
        return {
            'name': self.name,
            'res_model': 'project.edt',
            'domain': [('id', '=', self.edt_raiz_id.id)],
            'type': 'ir.actions.act_window',
            'view_id': view_id,
            'view_mode': 'tree',
            'view_type': 'tree',
        }

    @api.multi
    def get_tareas_atrasadas(self):
        self.ensure_one()
        task_model = self.env['project.task']
        return task_model.search([('project_id','=',self.id),('retraso','>',0)])

    @api.multi
    def registrar_fecha_estado_wizard_button(self):
        view = self.env.ref('project_edt_idu.edt_wizard_fecha_estado_form')
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.edt.wizard.fecha_estado',
            'context': { 'project_id': self.id },
            'view_id': view.id,
            'target': 'new',
            'views': [(view.id, 'form'),
                    (False, 'form')],
        }


class project_task_registro_progreso(models.Model):
    _name = 'project.task.registro_progreso'
    _description = 'Registro de Progreso de Tarea'
    _inherit = ['mail.thread', 'models.soft_delete.mixin', 'project.recompute_hack']
    _order = 'fecha DESC, id DESC'

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
        track_visibility='onchange',
        default=fields.Date.today,
    )
    task_id = fields.Many2one(
        string='Tarea',
        required=True,
        track_visibility='onchange',
        comodel_name='project.task',
        ondelete='restrict',
        default=lambda self: self._context.get('task_id', None),
    )
    task_revisor_id = fields.Many2one(
        string='Revisor de la Tarea',
        required=False,
        readonly=True,
        related='task_id.revisor_id',
        comodel_name='res.users',
        ondelete='restrict',
    )
    porcentaje = fields.Integer(
        string='Porcentaje',
        required=True,
        track_visibility='onchange',
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
        track_visibility='onchange',
    )
    fecha_aprobacion = fields.Datetime(
        string='Fecha de Aprobación',
        required=False,
        track_visibility='onchange',
    )
    revisor_id = fields.Many2one(
        string='Aprobado por',
        required=False,
        track_visibility='onchange',
        comodel_name='res.users',
        ondelete='restrict',
    )
    nivel_alerta = fields.Selection(
        string='Nivel de Alerta',
        required=False,
        track_visibility='onchange',
        selection=PROJECT_TASK_REPORTE_AVANCE_NIVEL_ALERTA,
        default='ninguno',
    )
    novedad = fields.Text(
        string='Novedad',
        required=False,
        track_visibility='onchange',
    )
    reporte_avance_id = fields.Many2one(
        string='Reporte de Avance',
        required=False,
        track_visibility='onchange',
        comodel_name='project.task.reporte_avance',
        ondelete='restrict',
    )
    cantidad = fields.Float(
        string='Cantidad',
        required=False,
        track_visibility='onchange',
    )

    # -------------------
    # methods
    # -------------------
    @api.model
    def create(self, vals):
        # print self._name, vals, self.env.context
        record = super(project_task_registro_progreso, self).create(vals)
        if not self.env.context.get('no_actualizar_tarea', False):
            record.task_id._compute_progreso()
        return record

    @api.one
    def write(self, vals):
        # print self._name, vals, self.env.context
        if self.fecha_aprobacion:
            raise ValidationError('No puede ser editado un registro ya aprobado')
        res = super(project_task_registro_progreso, self).write(vals)
        if ('costo' in vals or 'porcentaje' in vals or 'cantidad' in vals or 'fecha' in vals):
            self.task_id._compute_progreso()
        return res

    @api.multi
    def unlink(self):
        super(project_task_registro_progreso, self).unlink()
        self.task_id._compute_progreso()

    @api.one
    @api.constrains('fecha_aprobacion')
    def _check_fecha_aprobacion(self):
        if self.fecha_aprobacion and self.fecha_aprobacion < self.fecha:
            raise ValidationError('La fecha de aprobación no puede ser anterior a la fecha de corte del progreso')


    @api.one
    @api.constrains('task_id')
    def _check_task_id(self):
        if self.task_id and self.task_id.terminado:
            raise ValidationError('La tarea ya ha sido marcada como terminada no puede adicionar o editar registros de progreso')

    @api.one
    @api.constrains('porcentaje')
    def _check_porcentaje(self):
        if self.porcentaje > 100 or self.porcentaje < 0:
            raise ValidationError("Porcentaje debe ser un número positivo no mayor de 100")

    @api.one
    @api.constrains('costo')
    def _check_costo(self):
        if self.costo < 0:
            raise ValidationError('El costo debe ser un valor positivo')

    @api.onchange('porcentaje')
    def _onchange_porcentaje(self):
        try:
            self._check_porcentaje()
        except Exception as e:
            return {
                'title': "Error de Validación",
                'warning': {'message': e.name}
            }

    @api.onchange('costo')
    def _onchange_costo(self):
        try:
            self._check_costo()
        except Exception as e:
            return {
                'title': "Error de Validación",
                'warning': {'message': e.name}
            }

class project_task_pendiente(models.Model):
    _name = 'project.task.pendiente'
    _description = 'Lista de Chequeo en Tarea'
    _inherit = ['mail.thread', 'models.soft_delete.mixin']

    # -------------------
    # Fields
    # -------------------
    name = fields.Char(
        string='Asunto',
        required=True,
        track_visibility='onchange',
        size=255,
    )
    sequence = fields.Integer(
        string='Sequencia',
        required=False,
    )
    task_id = fields.Many2one(
        string='Tarea',
        required=True,
        track_visibility='onchange',
        comodel_name='project.task',
        ondelete='restrict',
        default=lambda self: self._context.get('task_id', None),
    )
    task_revisor_id = fields.Many2one(
        string='Revisor de la Tarea',
        required=False,
        related='task_id.revisor_id',
        comodel_name='res.users',
        ondelete='restrict',
    )
    peso = fields.Integer(
        string='Peso',
        required=True,
        track_visibility='onchange',
        default=1,
    )
    user_id = fields.Many2one(
        string='Responsable',
        required=True,
        track_visibility='onchange',
        comodel_name='res.users',
        ondelete='restrict',
        default=lambda self: self._context.get('uid', False),
    )
    fecha_limite = fields.Date(
        string='Fecha Límite',
        required=False,
        default=lambda self: self._context.get('fecha_limite', False),
    )
    fecha_terminacion = fields.Datetime(
        string='Fecha de terminación',
        required=False,
        track_visibility='onchange',
    )
    fecha_aprobacion = fields.Datetime(
        string='Fecha de Aprobación',
        required=False,
        track_visibility='onchange',
    )
    revisor_id = fields.Many2one(
        string='Aprobado por',
        required=False,
        track_visibility='onchange',
        comodel_name='res.users',
        ondelete='restrict',
    )

    # -------------------
    # methods
    # -------------------

    @api.one
    @api.constrains('fecha_limite')
    def _check_fecha_limite(self):
        if self.fecha_limite and self.task_id and self.task_id.fecha_planeada_fin and self.fecha_limite > self.task_id.fecha_planeada_fin:
            raise ValidationError(
                "La fecha límite no puede ser mayor a la fecha planeada de terminación de la tarea ({0})".format(self.task_id.fecha_planeada_fin)
            )

    @api.onchange('fecha_limite')
    def _onchange_fecha_limite(self):
        try:
            self._check_fecha_limite()
        except Exception as e:
            return {
                'title': "Error de Validación",
                'warning': {'message': e.name}
            }

    @api.one
    def marcar_terminado_button(self):
        if not self.fecha_terminacion:
            self.fecha_terminacion = fields.Datetime.now()

class project_predecesor(models.Model):
    _name = 'project.predecesor'
    _description = 'Relacion de Precedencia entre Tarea/EDT'

    # -------------------
    # Fields
    # -------------------
    name = fields.Char(
        string='Nombre',
        required=True,
        size=255,
        compute='_compute_name',
    )
    progreso = fields.Integer(
        string='Progreso',
        required=False,
        compute='_compute_progreso',
    )
    origen_res_model = fields.Selection(
        string='Origen Modelo',
        required=True,
        selection=[
            ('tarea', 'tarea'),
            ('edt', 'edt'),
        ],
    )
    origen_res_id = fields.Integer(
        string='Origen ID',
        required=True,
    )
    destino_res_model = fields.Selection(
        string='Destino Modelo',
        required=True,
        selection=[
            ('tarea', 'tarea'),
            ('edt', 'edt'),
        ],
    )
    destino_res_id = fields.Integer(
        string='Destino ID',
        required=True,
    )
    tipo = fields.Selection(
        string='Tipo',
        required=True,
        selection=[
            ('e_s', 'e_s'),
            ('s_s', 's_s'),
            ('e_e', 'e_e'),
            ('s_e', 's_e'),
        ],
        default='e_s',
    )

    # -------------------
    # methods
    # -------------------

    @api.one
    @api.depends('origen_res_id', 'origen_res_model')
    def _compute_name(self):
        self.name = "Nulla quasi qui autem id."

    @api.one
    def _compute_progreso(self):
        self.progreso = 48482016.1052

class project_task_reporte_avance(models.Model):
    _name = 'project.task.reporte_avance'
    _description = 'Reporte de Avance de Tareas'
    _inherit = ['mail.thread', 'models.soft_delete.mixin']

    # -------------------
    # Fields
    # -------------------
    name = fields.Char(
        string='Nombre',
        required=False,
        size=255,
        compute='_compute_name',
    )
    fecha = fields.Date(
        string='Fecha de Corte',
        required=True,
        readonly=True,
        track_visibility='onchange',
        default=fields.Date.today,
    )
    project_id = fields.Many2one(
        string='Proyecto',
        required=True,
        track_visibility='onchange',
        comodel_name='project.project',
        ondelete='restrict',
        readonly=True,
        states={
            'borrador': [('readonly', False)]
        },
    )
    user_id = fields.Many2one(
        string='Usuario',
        required=True,
        readonly=True,
        track_visibility='onchange',
        comodel_name='res.users',
        ondelete='restrict',
        default=lambda self: self._context.get('uid', False),
    )
    state = fields.Selection(
        string='Estado',
        required=True,
        track_visibility='onchange',
        selection=[
            ('borrador', 'borrador'),
            ('por_revisar', 'por_revisar'),
            ('terminado', 'terminado'),
        ],
        default='borrador',
    )
    avances_por_revisar = fields.Integer(
        string='Avances Requieren Revisión',
        required=False,
        compute='_compute_conteo_avances',
        help='''Conteo de avances cuyas tareas deben ser revisadas''',
    )
    avances_aprobados = fields.Integer(
        string='Avances Aprobados',
        required=False,
        compute='_compute_conteo_avances',
        help='''Conteo de Tareas que requieren ser revisadas y ya fueron aprobados los avances''',
    )
    registro_progreso_ids = fields.One2many(
        string='Avances en Tareas',
        required=False,
        comodel_name='project.task.registro_progreso',
        inverse_name='reporte_avance_id',
        ondelete='restrict',
        readonly=True,
        states={
            'borrador': [('readonly', False)]
        },
    )

    # -------------------
    # methods
    # -------------------
    @api.model
    def dominio_tareas_a_reportar(self, project_id, user_id):
      return [
          ('project_id', '=', project_id),
          ('user_id', '=', user_id),
          ('progreso_metodo', '=','manual'),
          ('terminado', '=', False),
          ('fecha_inicio','<',fields.Date.today())
      ]

    @api.model
    def create(self, vals):
        task_reporte_avance = super(project_task_reporte_avance, self).create(vals)
        tasks = self.env['project.task'].search(
            self.dominio_tareas_a_reportar(task_reporte_avance.project_id.id, task_reporte_avance.user_id.id)
        )
        if not len(tasks):
            raise ValidationError('No tiene asignadas tareas en este proyecto, no puede generar un reporte de avance, por favor seleccione otro proyecto')
        avance_model = self.env['project.task.registro_progreso']
        for task in tasks:
            avance_model.with_context({'no_actualizar_tarea': True}).create({
                'name': 'Describa el avance',
                'porcentaje': task.progreso,
                'task_id': task.id,
                'fecha': task_reporte_avance.fecha,
                'reporte_avance_id': task_reporte_avance.id,
            })
        return task_reporte_avance

    @api.one
    @api.depends('fecha', 'user_id', 'project_id')
    def _compute_name(self):
        self.name = 'Reporte a fecha del {0} por {1}'.format(self.fecha, self.user_id.name)

    @api.one
    @api.depends('registro_progreso_ids')
    def _compute_conteo_avances(self):
        self.avances_por_revisar = len(self.registro_progreso_ids.filtered(lambda r: r.task_revisor_id and not r.fecha_aprobacion))
        self.avances_aprobados = len(self.registro_progreso_ids.filtered(lambda r: r.task_revisor_id and r.fecha_aprobacion))

    @api.one
    @api.constrains('fecha')
    def _check_fecha(self):
        if self.fecha == 'Condición de Validation':
            raise ValidationError("MENSAJE DE ERROR DE VALIDACIÓN")

    # -------------------
    # Workflow methods
    # -------------------
    def wkf_borrador(self):
        self.state = 'borrador'

    def wkf_terminado(self):
        self.state = 'terminado'
        self.registro_progreso_ids.write({
            'fecha_aprobacion': fields.Date.today(),
            'revisor_id': self.env.uid,
        })

    def wkf_por_revisar(self):
        self.state = 'por_revisar'
