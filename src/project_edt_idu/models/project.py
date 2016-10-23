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
from openerp.osv import fields as fields_v7
from openerp.exceptions import ValidationError
from datetime import datetime, timedelta, date
from workalendar.america import Colombia
import workdays
from collections import deque


def calcular_fecha_fin(fecha_inicio, duracion):
    cal = Colombia()
    if isinstance(fecha_inicio, basestring):
        fecha_inicio = fields.Date.from_string(fecha_inicio)
    holidays = listado_festivos(fecha_inicio.year)
    duracion -= 1 # el parametro inicial se incluye como dia laborable y se descuenta
    return cal.add_working_days(fecha_inicio, duracion, holidays) # suma dias sin incluir fecha inicial, por eso se resta uno

def calcular_fecha_inicio(fecha_fin, duracion):
    cal = Colombia()
    if isinstance(fecha_fin, basestring):
        fecha_fin = fields.Date.from_string(fecha_fin)
    holidays = listado_festivos(fecha_fin.year)
    duracion -= 1 # el parametro inicial se incluye como dia laborable y se descuenta
    return cal.sub_working_days(fecha_fin, duracion, holidays) # suma dias sin incluir fecha inicial, por eso se resta uno

def listado_festivos(*years):
    years = list(set(years))
    cal = Colombia()
    holidays = []
    for year in years:
        # Festivos de colombia por año retornados en formato:
        # [ (datetime.date(2015, 1, 1), 'New year'), ..., (datetime.date(2015, 11, 16), u"Cartagena's Independence")]
        holidays += cal.get_calendar_holidays(year)
    min_time = datetime.min.time()
    holidays = [datetime.combine(i[0], min_time) for i in holidays] # Genera listado con solo las fechas (convertidas a datetime) sin el nombre del festivo
    return list(set(holidays)) # Elimina redundancias

def calcular_duracion_en_dias(date1, date2, return_dates=False):
    if not date1 or not date2:
        return 0
    formato = '%Y-%m-%d %H:%M:%S'
    if len(date1) == 10:
        formato = '%Y-%m-%d'
    fecha_inicio = datetime.strptime(date1, formato)
    fecha_fin = datetime.strptime(date2, formato)
    holidays = listado_festivos(fecha_inicio.year, fecha_fin.year)
    if date1 == date2:
        if return_dates:
            return fecha_inicio, fecha_fin, 0, holidays
        return 0
    duracion = workdays.networkdays(fecha_inicio, fecha_fin, holidays)
    if fecha_inicio.weekday() >= 5 or fecha_inicio in holidays : # no es dia laboral (no sabado/domingo, ni festivo)
        duracion += 1 # como se ignoró en workdays.networkdays, entonces lo sumamos como lo hace project en fechas manuales
    if fecha_fin.weekday() >= 5 or fecha_fin in holidays : # no es dia laboral (no sabado/domingo, ni festivo)
        duracion += 1 # como se ignoró en workdays.networkdays, entonces lo sumamos como lo hace project en fechas manuales

    if return_dates:
        return fecha_inicio, fecha_fin, duracion, holidays
    return duracion

def calcular_duracion_en_dias_fecha_estado(date1, date2):
    """Calculo de duración utilizado para cuando se utiliza una fecha de estado para pronosticar
    valores de progreso y costo a una fecha"""
    fecha_inicio, fecha_fin, duracion, holidays = calcular_duracion_en_dias(date1, date2, True)
    duracion -= 1 # Toma la fecha final con hora inicio de jornada, osea que no cuenta como dia completo de trabajo
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
        string='Fecha Planeada de Inicio (Línea Base)',
        required=False,
        readonly=True,
        track_visibility='onchange',
    )
    fecha_planeada_fin = fields.Date(
        string='Fecha Planeada de Finalización (Línea Base)',
        required=False,
        readonly=True,
    )
    duracion_planeada_dias = fields.Integer(
        string='Duración Planeada (Línea Base)',
        help='Duración Planeada en Días',
        required=False,
        compute='_compute_duracion_planeada',
        store=True,
    )
    fecha_inicio = fields.Date(
        string='Fecha de Inicio',
        required=False,
        help="Se asigna basado en las fechas de las tareas y EDT hijas",
    )
    fecha_fin = fields.Date(
        string='Fecha de Finalización',
        required=False,
        help="Se asigna basado en las fechas de las tareas y EDT hijas",
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
        default=lambda self: self._context.get('programador_id', self._context.get('uid')),
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
    predecesor_ids = fields.One2many(
        string="Predecesoras",
        comodel_name='project.predecesor',
        inverse_name='destino_res_id',
        domain=lambda self: [('destino_res_model', '=', 'e')],
    )
    sucesor_ids = fields.One2many(
        string="Sucesoras",
        comodel_name='project.predecesor',
        inverse_name='origen_res_id',
        domain=lambda self: [('origen_res_model', '=', 'e')],
    )
    usuario_actual_puede_reprogramar = fields.Boolean(
        string="",
        compute='_compute_usuario_actual_puede_reprogramar',
        default=True,
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
            raise ValidationError("Fecha de inicio no puede ser posterior a la de finalización {} {}".format(self.numero, self.name))

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
            raise ValidationError("Fecha de inicio no puede ser posterior a la de finalización {} {}".format(self.numero, self.name))

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

    def compute_duracion_planeada(self):
        # print '_compute_duracion_planeada', self._name, self.id, self.numero
        self.duracion_planeada_dias = calcular_duracion_en_dias(self.fecha_planeada_inicio, self.fecha_planeada_fin)

    @api.one
    @api.depends('fecha_inicio', 'fecha_fin')
    def _compute_duracion_dias(self):
        # print '_compute_duracion_dias', self._name, self.id, self.numero
        self.duracion_dias = calcular_duracion_en_dias(self.fecha_inicio, self.fecha_fin)

    def _compute_fechas_helper(self, planeadas):
        (edt_inicio, edt_fin) = self._obtener_rango_fecha_edt(planeadas)
        (task_start, task_end) = self._obtener_rango_fecha_tareas(planeadas)
        if not edt_inicio and not edt_fin and not task_start and not task_end:
            return self.fecha_planeada_inicio, self.fecha_planeada_fin, calcular_duracion_en_dias(self.fecha_planeada_inicio, self.fecha_planeada_fin)
        fecha_inicio = False
        fecha_fin = False
        duracion_dias = 0

        if task_start and task_end and not edt_inicio and not edt_fin:
            fecha_inicio = fields.Date.to_string(task_start)
            fecha_fin = fields.Date.to_string(task_end)
        elif edt_inicio and edt_fin and not task_start and not task_end:
            if task_start or edt_inicio:
                fecha_inicio = fields.Date.to_string(edt_inicio)
            if task_end or edt_fin:
                fecha_fin = fields.Date.to_string(edt_fin)
        else:
            if task_start < edt_inicio:
                fecha_inicio = fields.Date.to_string(task_start)
            else:
                fecha_inicio = fields.Date.to_string(edt_inicio)
            if task_end > edt_fin:
                fecha_fin = fields.Date.to_string(task_end)
            else:
                fecha_fin = fields.Date.to_string(edt_fin)

        if fecha_inicio and fecha_fin:
            duracion_dias = calcular_duracion_en_dias(fecha_inicio, fecha_fin)
        return fecha_inicio, fecha_fin, duracion_dias

    @api.one
    def _compute_fechas(self):
        # print '_compute_fechas', self._name, self.id, self.numero
        # print 'Calculando {} {} {} {}'.format(self.numero, self.fecha_inicio, self.fecha_fin, self.id)
        fecha_inicio, fecha_fin, duracion_dias = self._compute_fechas_helper(False)
        vals = {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'duracion_dias': duracion_dias,
        }
        self.write(vals)

    @api.one
    def _compute_fechas_planeadas(self):
        print self.id
        fecha_inicio, fecha_fin, duracion_dias = self._compute_fechas_helper(True)
        vals = {
            'fecha_planeada_inicio': fecha_inicio,
            'fecha_planeada_fin': fecha_fin,
            'duracion_planeada_dias': duracion_dias,
        }
        self.write(vals)

    def _obtener_rango_fecha_tareas(self, planeadas=False):
        if isinstance(self.id, models.NewId):
            return False, False
        self.ensure_one()
        fecha_inicio = False
        fecha_fin = False
        if planeadas:
            self.env.cr.execute("""
                SELECT
                    MIN(fecha_planeada_inicio), MAX(fecha_planeada_fin)
                FROM
                    project_task
                WHERE
                    edt_id = %s
                """, (self.id, )
            )
        else:
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
                fecha_inicio = datetime.strptime(result[0][0], '%Y-%m-%d').date()
            if result[0][1]:
                fecha_fin = datetime.strptime(result[0][1], '%Y-%m-%d').date()
        return (fecha_inicio, fecha_fin)

    def _obtener_rango_fecha_edt(self, planeadas=False):
        if isinstance(self.id, models.NewId):
            return False, False
        self.ensure_one()
        fecha_inicio = False
        fecha_fin = False
        if planeadas:
            self.env.cr.execute("""
                SELECT
                    MIN(fecha_planeada_inicio), MAX(fecha_planeada_fin)
                FROM
                    project_edt
                WHERE
                    parent_id = %s
                """, (self.id,)
            )
        else:
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
                fecha_inicio = datetime.strptime(result[0][0], '%Y-%m-%d').date()
            if result[0][1]:
                fecha_fin = datetime.strptime(result[0][1], '%Y-%m-%d').date()
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
        progreso_diario = None
        if not self.duracion_planeada_dias:
            progreso_diario = 100
        else:
            progreso_diario = 100/float(self.duracion_planeada_dias)
        dias_esperados = 0
        if self.fecha_planeada_inicio:
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

    @api.one
    def _compute_usuario_actual_puede_reprogramar(self):
        res = False
        if self.project_id and self.project_id.usuario_actual_actua_como_gerente():
            res = True
        else:
            user_id = self.env.user.id
            autorizado_ids = [1]# superadmin
            autorizado_ids.append(self.user_id.id)
            autorizado_ids.append(self.programador_id.id)
            parent = self.parent_id
            while parent:
                autorizado_ids.append(parent.programador_id.id)
                autorizado_ids.append(parent.user_id.id)
                parent = parent.parent_id
            if user_id and user_id in autorizado_ids:
                res = True
        self.usuario_actual_puede_reprogramar = res


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
        string='Fecha de Inicio Planeada (Línea Base)',
        required=False,
        readonly=True,
        track_visibility='onchange',
    )
    fecha_planeada_fin = fields.Date(
        string='Fecha de Finalización Planeada (Línea Base)',
        required=False,
        readonly=True,
        track_visibility='onchange',
    )
    date_start = fields.Datetime(
        string='Fecha y Hora Real de Inicio',
        readonly=False,
    )
    date_end = fields.Datetime(
        string='Fecha y Hora Real de Finalización',
        readonly=False,
    )
    fecha_inicio = fields.Date(
        string='Fecha de Inicio',
        required=True,
        default=fields.Date.context_today,
        help='Fecha de inicio proyectada',
        track_visibility='onchange',
    )
    fecha_fin = fields.Date(
        string='Fecha de Finalización',
        required=True,
        default=fields.Date.context_today,
        track_visibility='onchange',
        help='Fecha de finalización proyectada basado en fecha inicial y duración en días',
    )
    duracion_planeada_dias = fields.Integer(
        string='Duración Planeada (Línea Base)',
        help='Duración Planeada en Días',
        required=False,
        compute='_compute_duracion_planeada',
        store=True,
    )
    duracion_dias = fields.Integer(
        string='Duración',
        help='Duración Actual en Días',
        required=False,
        compute='_compute_duracion_dias',
        inverse='_compute_duracion_dias_inverse',
        store=True,
    )
    duracion_dias_manual = fields.Integer(
        string='Duración (asignada manualmente)',
        help='Asignado para importar masivamente y conservarlo como el número a utilizar en los cálculos',
        required=False,
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
    requiere_adjunto = fields.Boolean(
        string='Requiere Adjunto para Finalizar',
        required=False,
        track_visibility='onchange',
        help='''Si activo esta tarea requiere que se adicione un adjunto para poder marcar la tarea como terminada''',
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
    predecesor_ids = fields.One2many(
        string="Predecesoras",
        comodel_name='project.predecesor',
        inverse_name='destino_res_id',
        domain=lambda self: [('destino_res_model', '=', 't')],
    )
    sucesor_ids = fields.One2many(
        string="Sucesoras",
        comodel_name='project.predecesor',
        inverse_name='origen_res_id',
        domain=lambda self: [('origen_res_model', '=', 't')],
    )
    usuario_actual_puede_reprogramar = fields.Boolean(
        string="",
        compute='_compute_usuario_actual_puede_reprogramar',
        default=True,
    )

    # -------------------
    # methods
    # -------------------
    @api.model
    def create(self, vals):
        # print self._name, vals.get('numero'), self.env.context
        es_carga_masiva = self.env.context.get('carga_masiva', False)
        if not es_carga_masiva and vals.get('date_start'):
            vals['date_start'] = False # Solo así pude quitar el valor por defecto del campo.

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
            raise ValidationError("Fecha de inicio no puede ser posterior a la de finalización {} {}".format(self.numero, self.name))

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
            raise ValidationError("Fecha de inicio no puede ser posterior a la de finalización {} {}".format(self.numero, self.name))

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

    @api.one
    def reprogramar_tarea_button(self):
        self.sudo().reprogramar_fechas_reales_sucesoras()
        self.message_post(
            type="note",
            body="Reprogramación de tareas a partir de fechas inicial {}, final {} y {} días de duración".format(
                self.fecha_inicio, self.fecha_fin, self.duracion_dias
            ),
        )

    @api.one
    def ajustar_planeado_button(self):
        self.write({
            'fecha_planeada_fin': self.fecha_fin,
            'fecha_planeada_inicio': self.fecha_inicio,
        })
        self._compute_progreso()
        return True

    @api.multi
    def reprogramar_tarea_wizard_button(self):
        view = self.env.ref('project_edt_idu.edt_wizard_reprogramar_tarea_form')
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.edt.wizard.reprogramar_tarea',
            'context': { 'task_id': self.id },
            'view_id': view.id,
            'target': 'new',
            'views': [(view.id, 'form'),
                    (False, 'form')],
        }

    @api.one
    def registrar_hoy_inicio_tarea_button(self):
        hoy = fields.Date.from_string(fields.Date.context_today(self))
        cal = Colombia()
        fecha_fin = calcular_fecha_fin(hoy, self.duracion_dias)
        self.write({
            'date_start': fields.Datetime.to_string(datetime.now()),
            'fecha_inicio': hoy,
            'fecha_fin': fields.Date.to_string(fecha_fin),
        })
        progreso_model = self.env['project.task.registro_progreso']
        record = progreso_model.create({
            'name': 'Se registra el inicio de ejecución de la tarea',
            'fecha_inicio': hoy,
            'task_id': self.id,
            'porcentaje': 0,
        })
        if self.project_id.reprogramar_tareas_automaticamente:
            self.reprogramar_tarea_button()

    @api.one
    def reprogramar_fechas_reales_sucesoras(self):
        sucesora_model = self.env['project.predecesor']
        all_tasks = { self.id: self } # Mantiene el listado de todas las tareas a ser reprogramadas
        visited_tasks = { self.id: True } # Mantiene el listado de tareas visitadas
        tasks = deque([ self.id ]) # Mantiene la cola de tareas a ir procesando recorriendo el arbol en anchura
        # Generar el listado de todas las tareas recorriendo el arbol de sucesoras
        while tasks:
            task_id = tasks.popleft()
            sucesoras = sucesora_model.search([
                ('origen_res_model','=','t'),
                ('destino_res_model','=','t'),
                ('origen_res_id','=',task_id),
            ])
            siguiente_nivel_sucesoras = { x: None for x in sucesoras.mapped('destino_res_id') if x not in all_tasks }
            all_tasks.update(siguiente_nivel_sucesoras)
            for x in siguiente_nivel_sucesoras.keys():
                tasks.append(x) # adiciona las sucesoras para ser procesadas en el while
        # Cargar todas las tareas:
        for t in self.browse(all_tasks.keys()):
            all_tasks[t.id] = t
        # Recorrer el arbol para reprogramar
        def ya_esta_en_cola(elemento, cola):
            # Indica si el elemento ya esta en cola
            # Si al adicionarse al set el elemento, el set no crece, es porque ya esta en la cola
            elementos = set(cola)
            _elemento = set([elemento])
            return _elemento.issubset(elementos)

        tasks = deque([ self.id ])
        while tasks:
            task_id = tasks.popleft()
            task = all_tasks[task_id]
            if task.reprogramar(visited_tasks, all_tasks):
                visited_tasks[task_id] = True
                for sucesora_task_id in task.sucesor_ids.filtered(lambda x: x.destino_res_model == 't').mapped('destino_res_id'):
                    if not ya_esta_en_cola(sucesora_task_id, tasks):
                        tasks.append(sucesora_task_id) # adiciona las sucesoras para ser procesadas en el while
            else:
                if not ya_esta_en_cola(task_id, tasks):
                    tasks.append(task_id) # Dependencia pendiente de ser reprogramada, intentar posteriormente

    def reprogramar(self, visited_tasks, all_tasks):
        fechas = (None, None)
        if visited_tasks.get(self.id):
            return True
        for p in self.predecesor_ids.filtered(lambda x: x.origen_res_model == 't'):
            # Revisa si la predecesora va a ser reprogramada (all_tasks) y si ya fue reprograda
            tarea_id = p.origen_res_id
            if all_tasks.get(tarea_id, False) and not visited_tasks.get(tarea_id, False):
                return False # si no es así se ignora la tarea por el momento, para que sea tomada más adelante
            tarea_origen = all_tasks.get(tarea_id)
            if not tarea_origen:
                tarea_origen = p.get_origen_object()
            fecha_inicio, fecha_final = p.get_fechas_reprogramacion_sucesora(tarea_origen, self)
            if fechas[1] == None or fecha_final > fechas[1]: # Tome la fecha que retraza más el cronograma
                fechas = (fecha_inicio, fecha_final)
        self.write({
            'fecha_inicio': fields.Date.to_string(fechas[0]),
            'fecha_fin': fields.Date.to_string(fechas[1]),
        })
        return True

    # Sobreescribir comportamiento de módulo original de odoo
    # No enviar notificaciones para cambio de estado, de dueño, etc
    # Solo guardar cambio de valor
    def _track_subtype(self, cr, uid, ids, init_values, context=None):
        return False

    # -------------------
    # Campos Computados
    # -------------------
    @api.one
    @api.depends('fecha_inicio', 'fecha_fin')
    def _compute_duracion_dias(self):
        # print '_compute_duracion', self._name, self.id, self.numero
        if self.duracion_dias_manual:
            self.duracion_dias = self.duracion_dias_manual
        else:
            self.duracion_dias = calcular_duracion_en_dias(self.fecha_inicio, self.fecha_fin)

    def _compute_duracion_dias_inverse(self):
        self.duracion_dias_manual = self.duracion_dias

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
            try:
                position = cnt_edts + children.index(self.id) + 1
            except:
                position = cnt_edts + len(children) + 1

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
            SELECT porcentaje, costo, cantidad, fecha_inicio, fecha_fin, terminado, id, fecha
            FROM project_task_registro_progreso
            WHERE task_id = {0}
            AND active = 't'
            ORDER BY fecha DESC, id DESC
            LIMIT 1""".format(self.id)
        )
        resultados = self.env.cr.fetchall()
        #print 'TAREA', self.id, resultados
        if len(resultados):
            vals['progreso'] = resultados[0][0] if not resultados[0][5] else 100
            vals['costo'] = resultados[0][1]
            vals['cantidad'] = resultados[0][2]
            if resultados[0][3]:
                vals['fecha_inicio'] = resultados[0][3]
            if resultados[0][4]:
                vals['fecha_fin'] = resultados[0][4]
            if resultados[0][5]: # terminado
                vals['date_end'] = vals['fecha_fin'] + ' 23:59:59' if resultados[0][4] else fiels.Datetime.to_string(fields.Datetime.now())

        self.with_context({'no_crear_registro_progreso': True}).write(vals)

    @api.one
    def _set_progreso(self, vals):
        # print '_set_progreso', self._name, self.id, self.numero
        # Crear un project.task.registro_progreso con fecha de hoy o que venga del contexto
        datos = {
            'task_id': self.id,
            'name': 'Avance cargado masivamente el {0}'.format(date.today().strftime('%d, %b %Y')),
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
        progreso_diario = None
        if not self.duracion_planeada_dias:
            progreso_diario = 100
        else:
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

    @api.one
    def _compute_usuario_actual_puede_reprogramar(self):
        res = False
        if self.project_id and self.project_id.usuario_actual_actua_como_gerente():
            res = True
        elif (self.edt_id and
            self.edt_id.usuario_actual_puede_reprogramar or
            (self.edt_id.project_id and self.edt_id.project_id.usuario_actual_actua_como_gerente())
        ):
            res = True
        elif not self.project_id and not self.edt_id:
            res = True
        self.usuario_actual_puede_reprogramar = res


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
    fecha_estado = fields.Date(
        related='edt_raiz_id.fecha_estado',
        readonly=True,
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
    reprogramar_tareas_automaticamente = fields.Boolean(
        string='Reprogramar Tareas Automáticamente',
        help='Al registrar el avance de una tarea y marcarla como terminada, las tareas sucesoras se reprograman utilizando el día actual como fecha de finalización real',
        required=False,
        default=True,
    )
    # -------------------
    # Sobreescribe campos y metodos de modulo original del odoo
    # -------------------
    def _get_attached_docs(self, cr, uid, ids, field_name, arg, context):
        res = {}
        attachment = self.pool.get('ir.attachment')
        for id in ids:
            res[id] = attachment.search(cr, uid, self._get_document_domain(cr, uid, ids, context), context=context, count=True)
        return res

    _columns = {
        'doc_count': fields_v7.function(
            _get_attached_docs, string="Number of documents attached", type='integer'
        )
    }

    # -------------------
    # methods
    # -------------------
    @api.multi
    def edt_arbol_view_button(self):
        model, view_id = self.env['ir.model.data'].get_object_reference('project_edt_idu', 'arbol_edt_tree')
        return {
            'name': 'EDTs',
            'res_model': 'project.edt',
            'domain': [('id', '=', self.edt_raiz_id.id)],
            'type': 'ir.actions.act_window',
            'view_id': view_id,
            'view_mode': 'tree',
            'view_type': 'tree',
        }

    @api.multi
    def get_tareas_atrasadas(self,criteria):
        self.ensure_one()
        task_model = self.env['project.task']
        if criteria == 1:
            return task_model.search([('project_id','=',self.id),('retraso','>',0)])
        else:
            return task_model.search([('project_id','=',self.id),('retraso','>',0),('user_id','=',self._context.get('uid',False))])

    @api.multi
    def get_tareas_semana_actual(self):
        self.ensure_one()
        task_model = self.env['project.task']
        start_week =  format(datetime.now() - timedelta(days=datetime.now().weekday()),'%Y-%m-%d')
        end_week = format(datetime.strptime(start_week, '%Y-%m-%d') + timedelta(days=6),'%Y-%m-%d')
        return task_model.search([
            ('project_id','=',self.id),
            ('fecha_planeada_inicio','<=',end_week),
            ('fecha_planeada_fin','>=',start_week),
        ])

    @api.multi
    def get_tareas_semana_siguiente(self):
        self.ensure_one()
        task_model = self.env['project.task']
        start_week =  format((datetime.now() - timedelta(days=datetime.now().weekday())) + timedelta(days=7),'%Y-%m-%d')
        end_week = format(datetime.strptime(start_week, '%Y-%m-%d') + timedelta(days=6),'%Y-%m-%d')
        return task_model.search([
            ('project_id','=',self.id),
            ('fecha_planeada_inicio','<=',end_week),
            ('fecha_planeada_fin','>=',start_week),
        ])

    @api.multi
    def usuario_actual_actua_como_gerente(self):
        """Retorna True a los usuarios que pueden acceder a las funcionalidades que requieren un perfil de gerente para el proyecto"""
        if self.env.user.has_group('project.group_project_manager'):
            return True

        self.ensure_one()
        autorizado_ids = []
        user_id = self.env.user.id
        autorizado_ids.append(1) # superadmin
        autorizado_ids.append(self.user_id.id)
        autorizado_ids.append(self.programador_id.id)
        if user_id and user_id in autorizado_ids:
            return True
        return False

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

    def _get_document_domain(self, cr, uid, ids, context):
        task_ids = self.pool.get('project.task').search(cr, uid, [('project_id', 'in', ids)])
        registro_ids = self.pool.get('project.task.registro_progreso').search(cr, uid, [('task_id', 'in', task_ids)])
        edt_ids = self.pool.get('project.edt').search(cr, uid, [('project_id', 'in', ids)])
        return [
             '|','|','|',
             '&', ('res_model', '=', 'project.project'), ('res_id', 'in', ids),
             '&', ('res_model', '=', 'project.task'), ('res_id', 'in', task_ids),
             '&', ('res_model', '=', 'project.edt'), ('res_id', 'in', edt_ids),
             '&', ('res_model', '=', 'project.task.registro_progreso'), ('res_id', 'in', registro_ids),
        ]

    # Sobreescribe el método en el modulo project original de odoo
    def attachment_tree_view(self, cr, uid, ids, context):
        domain = self._get_document_domain(cr, uid, ids, context)
        res_id = ids and ids[0] or False
        return {
            'name': 'Adjuntos',
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': '''<p class="oe_view_nocontent_create">
                        Se listan Documentos que son parte de las tareas y EDTs del proyecto.
                    </p>''',
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, res_id)
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
        default=fields.Date.context_today,
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
        string='Porcentaje Acumulado',
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
    fecha_inicio = fields.Date(
        string='Fecha Inicio Real',
        required=False,
        readonly=False,
    )
    fecha_fin = fields.Date(
        string='Fecha Fin Real',
        required=False,
        readonly=False,
    )
    terminado = fields.Boolean(
        string='Terminado',
        required=False,
        track_visibility='onchange',
        help='''La tarea fue marcada como terminada''',
        default=False,
    )
    attachment_ids = fields.One2many(
        string="Adjuntos",
        comodel_name='ir.attachment',
        inverse_name='res_id',
        domain=lambda self: [('res_model', '=', self._name)],
        auto_join=True,
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
    _map_model = {'t': 'project.task', 'e': 'project.edt'}

    # -------------------
    # Fields
    # -------------------
    name = fields.Char(
        string='Nombre',
        required=False,
        size=255,
        compute='_compute_name',
        store=True,
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
            ('t', 'Tarea'),
            ('e', 'EDT'),
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
            ('t', 'Tarea'),
            ('e', 'EDT'),
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
            ('FS', 'Fin -> Inicio'),
            ('SS', 'Inicio -> Inicio'),
            ('FF', 'Fin -> Fin'),
            ('SF', 'Inicio -> Fin'),
        ],
        default='FS',
    )
    lag = fields.Char(
        string='Lag',
        required=False,
        size=50,
    )

    # -------------------
    # methods
    # -------------------

    @api.one
    @api.depends('destino_res_id', 'origen_res_id', 'tipo','destino_res_model', 'origen_res_model')
    def _compute_name(self):
        if self.origen_res_model and self.destino_res_model:
            map_model = self._map_model
            origen = self.env[map_model[self.origen_res_model]].browse(self.origen_res_id)
            destino = self.env[map_model[self.destino_res_model]].browse(self.destino_res_id)
            self.name = "{0} {1} -> {2} {3} ({4} - {5})".format(
                origen.numero, origen.name,
                destino.numero, destino.name,
                self.tipo, self.lag,
            )
        else:
            self.name = 'por definir'

    @api.one
    def _compute_progreso(self):
        map_model = self._map_model
        if self.origen_res_id and self.origen_res_model:
            origen = self.env[map_model[self.origen_res_model]].browse(self.origen_res_id)
            self.progreso = origen.progreso
        else:
            self.progreso = 0

    def get_fechas_reprogramacion_sucesora(relacion, tarea_origen=None, tarea=None):
        """Retorna las fechas para reprogramar la 'tarea' sucesora basado en los datos de la 'tarea origen' (predecesora) y la 'relacion'(project.predecesor)'
        FS -> fecha_final (+1 si la siguiente no es milestone - duración 0) es colocada como fecha inicial de la tarea relacionada y se calcula fecha final
        SS -> Fecha Inicial es colocada como fecha inicial de la tarea relacionada y se calcula la fecha final
        FF -> Fecha Final es Colocada como Fecha Final y se calcula la fecha Inicial
        SF -> Fecha Inicial es Colocada como fecha Final de la tarea relacionada y la fecha Inicial es calculada
        """
        if tarea == None:
            tarea = relacion.get_destino_object()
        if tarea_origen == None:
            tarea_origen = relacion.get_origen_object()

        duracion_dias = tarea_origen.duracion_dias
        fecha_inicio = fields.Date.from_string(tarea_origen.fecha_inicio)
        fecha_final = fields.Date.from_string(tarea_origen.fecha_fin)

        cal = Colombia()
        lag_en_dias = relacion._calcular_lag_en_dias(tarea.duracion_dias)
        tmp_fecha_inicial = None
        tmp_fecha_fin = None
        duracion_en_dias_a_sumar = tarea.duracion_dias - 1 # la duración de las tareas incluye la fecha de inicio, no desde el siguiente
        if duracion_en_dias_a_sumar < 0:
            duracion_en_dias_a_sumar = 0
        if relacion.tipo == 'FS':
            iniciar_en_dias = 1 # Indica debe iniciar la tarea sucesora un dia despues (valor por defecto)
            if tarea.duracion_dias == 0: # Si sucesora es un milestone no arranca al siguiente dia
                iniciar_en_dias = 0
                if lag_en_dias < 0:
                    lag_en_dias += 1 # un milestone al regresar en el tiempo descuenta un dia
            iniciar_en_dias += lag_en_dias
            tmp_fecha_inicial = cal.add_working_days(fecha_final, iniciar_en_dias)
            tmp_fecha_fin = cal.add_working_days(tmp_fecha_inicial, duracion_en_dias_a_sumar)
        elif relacion.tipo == 'SS':
            iniciar_en_dias = 0 # Indica debe iniciar la tarea sucesora un dia despues (valor por defecto)
            if duracion_dias == 0 and tarea.duracion_dias > 0:
                iniciar_en_dias = 1 # Si la predecesora es un milestone (hora es al final del dia) la tarea regular no puede iniciar sino al siguiente dia
            if tarea.duracion_dias == 0:
                if lag_en_dias > 0 and duracion_dias > 0:
                    lag_en_dias -= 1 # al ser milestone el dia de comienzo ya esta incluido
                if lag_en_dias < 0 and duracion_dias == 0:
                    lag_en_dias += 1 # al ser milestone la predecesora y la sucesora el dia de comienzo ya esta incluido
            iniciar_en_dias += lag_en_dias
            tmp_fecha_inicial = cal.add_working_days(fecha_inicio, iniciar_en_dias)
            tmp_fecha_fin = cal.add_working_days(tmp_fecha_inicial, duracion_en_dias_a_sumar)
        elif relacion.tipo == 'FF':
            tmp_fecha_fin = cal.add_working_days(fecha_final, lag_en_dias)
            tmp_fecha_inicial = cal.sub_working_days(tmp_fecha_fin, duracion_en_dias_a_sumar)
        elif relacion.tipo == 'SF':
            finalizar_en_dias = 0
            duracion_en_dias_a_sumar = tarea.duracion_dias
            if tarea.duracion_dias > 0 and duracion_dias > 0 and lag_en_dias > 0:
                lag_en_dias -= 1
                duracion_en_dias_a_sumar -= 1
            if tarea.duracion_dias == 0 and duracion_dias > 0 and lag_en_dias > 0:
                lag_en_dias -= 1
            if duracion_dias == 0 and tarea.duracion_dias > 0:
                duracion_en_dias_a_sumar -= 1
            if duracion_dias == 0 and lag_en_dias < 0:
                lag_en_dias += 1
                duracion_en_dias_a_sumar = tarea.duracion_dias
            finalizar_en_dias += lag_en_dias
            tmp_fecha_fin = cal.add_working_days(fecha_inicio, finalizar_en_dias)
            tmp_fecha_inicial = cal.sub_working_days(tmp_fecha_fin, duracion_en_dias_a_sumar)
        else:
            raise Exception('Tipo "{}" no reconocido para reprogramación[{}]: {}'.format(
                relacion.tipo, relacion.id, relacion.name,
            ))
        return tmp_fecha_inicial, tmp_fecha_fin

    @api.multi
    def _calcular_lag_en_dias(self, duracion=None):
        """Convierte el lag a dias tomando o valor en dias 0.0d o un porcentaje 0.0%
        duracion es la duración de la tarea sobre la cual se va a calcular el porcentaje.
        El resultado es un valor en dias enteros.
        """
        self.ensure_one()
        lag = self.lag
        if lag.find('d') > 0:
            return int(round(float(lag[:-1]),0))
        elif lag.find('%') > 0:
            numerador = duracion * float(lag[:-1])
            return int(round(numerador/100))
        else:
            raise Exception('Solo se reconoce lag en dias o porcentaje no "{}" para predecesor []: {}'.format(
                lag, self.id, self.name
            ))

    @api.model
    def get_origen_object(self):
        self.ensure_one()
        # Retorna el objeto origen, basado en el ID y el modelo
        modelo = self._map_model.get(self.origen_res_model)
        obj = self.env[modelo].browse(self.origen_res_id)
        return obj

    @api.model
    def get_destino_object(self):
        self.ensure_one()
        # Retorna el objeto origen, basado en el ID y el modelo
        modelo = self._map_model.get(self.destino_res_model)
        obj = self.env[modelo].browse(self.destino_res_id)
        return obj

    # TODO: Evitar dependencias circulares
    #@api.one
    #@api.constrains('origen_res_id', 'origen_res_model', 'xxxx')
    #def _check_no_circular()

class project_task_reporte_avance(models.Model):
    _name = 'project.task.reporte_avance'
    _description = 'Reportar Avance de Tareas'
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
            '|',
                ('user_id', '=', user_id),
                ('edt_id.user_id', '=', user_id),
            ('project_id', '=', project_id),
            ('progreso_metodo', '=','manual'),
            ('date_end', '!=', False),
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
