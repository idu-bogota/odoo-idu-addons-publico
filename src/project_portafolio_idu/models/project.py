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
from openerp.addons.base_idu.models.filtros_mixin import adiciona_keywords_en_search


class project_programa(models.Model):
    _name = 'project.programa'
    _description = 'Programa de Proyectos'
    _inherit = ['mail.thread', 'models.soft_delete.mixin']

    # -------------------
    # Fields
    # -------------------
    name = fields.Char(
        string='Nombre',
        required=True,
        track_visibility='onchange',
        size=255,
    )
    user_id = fields.Many2one(
        string='Responsable',
        required=False,
        track_visibility='onchange',
        comodel_name='res.users',
        ondelete='restrict',
        default=lambda self: self._context.get('uid', False),
    )
    descripcion = fields.Text(
        string='Descripción',
        required=False,
    )
    project_ids = fields.One2many(
        string='Proyectos',
        required=False,
        comodel_name='project.project',
        inverse_name='programa_id',
        ondelete='restrict',
    )

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Este name ya está registrado'),
    ]

    # -------------------
    # methods
    # -------------------

    @api.model
    def create(self, vals):
        programa = super(project_programa, self).create(vals)
        return programa

class project_portafolio(models.Model):
    _name = 'project.portafolio'
    _description = 'Portafolio de Proyectos'
    _inherit = ['mail.thread', 'models.soft_delete.mixin']

    # -------------------
    # Fields
    # -------------------
    name = fields.Char(
        string='Nombre',
        required=True,
        track_visibility='onchange',
        size=255,
    )
    user_id = fields.Many2one(
        string='Responsable',
        required=False,
        track_visibility='onchange',
        comodel_name='res.users',
        ondelete='restrict',
        default=lambda self: self._context.get('uid', False),
    )
    descripcion = fields.Text(
        string='Descripción',
        required=False,
    )
    project_ids = fields.Many2many(
        string='Proyectos',
        required=False,
        comodel_name='project.project',
        ondelete='restrict',
    )

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Este name ya está registrado'),
    ]

    # -------------------
    # methods
    # -------------------

class project_linea_base(models.Model):
    _name = 'project.linea_base'
    _description = 'Linea Base de Proyecto'
    _inherit = ['models.soft_delete.mixin']

    # -------------------
    # Fields
    # -------------------
    name = fields.Char(
        string='Nombre',
        required=True,
        size=255,
    )
    es_snapshot = fields.Boolean(
        string='Es Histórico de Ejecución',
        help='Almacena valores ejecutados no planeados',
        required=False,
        default=False,
        readonly=True,
    )
    project_id = fields.Many2one(
        string='Proyecto',
        required=True,
        comodel_name='project.project',
        ondelete='restrict',
        readonly=True,
    )
    descripcion = fields.Text(
        string='Descripcion',
        required=False,
    )
    linea_raiz_id = fields.Many2one(
        string='Linea Raíz',
        required=False,
        comodel_name='project.linea_base.linea',
        ondelete='restrict',
        readonly=True,
    )
    linea_ids = fields.One2many(
        string='Lineas',
        required=False,
        comodel_name='project.linea_base.linea',
        inverse_name='linea_base_id',
        ondelete='restrict',
        readonly=True,
    )

    # -------------------
    # methods
    # -------------------

class project_linea_base_linea(models.Model):
    _name = 'project.linea_base.linea'
    _description = 'Linea de Linea Base de Proyecto'

    # -------------------
    # Fields
    # -------------------
    name = fields.Char(
        string='Nombre',
        required=True,
        size=255,
        readonly=True,
    )
    numero = fields.Char(
        string='Número',
        required=False,
        size=64,
        readonly=True,
    )
    parent_id = fields.Many2one(
        string='Línea Padre',
        required=False,
        comodel_name='project.linea_base.linea',
        ondelete='restrict',
        readonly=True,
    )
    child_ids = fields.One2many(
        string='Líneas Hijas',
        readonly=True,
        comodel_name='project.linea_base.linea',
        inverse_name='parent_id',
        ondelete='restrict',
    )
    linea_base_id = fields.Many2one(
        string='Línea Base',
        required=True,
        comodel_name='project.linea_base',
        ondelete='restrict',
        readonly=True,
    )
    active = fields.Boolean(
        string='Línea base esta activa?',
        required=False,
        readonly=True,
        related='linea_base_id.active',
        default=True,
    )
    res_model = fields.Char(
        string='Modelo relacionado',
        required=True,
        size=128,
        readonly=True,
    )
    res_id = fields.Integer(
        string='ID del modelo relacionado',
        required=True,
        readonly=True,
    )
    fecha_inicio = fields.Datetime(
        string='Fecha de Inicio',
        required=True,
        readonly=True,
    )
    fecha_fin = fields.Datetime(
        string='Fecha de finalización',
        required=True,
        readonly=True,
    )
    progreso = fields.Float(
        string='Progreso',
        required=True,
        readonly=True,
    )
    company_id = fields.Many2one(
        string='Compañía',
        required=True,
        invisible=True,
        comodel_name='res.company',
        ondelete='restrict',
        default=lambda self: self.env.user.company_id,
        readonly=True,
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
        required=True,
        readonly=True,
    )
    cantidad = fields.Float(
        string='Cantidad',
        required=False,
        readonly=True,
    )
    product_id = fields.Many2one(
        string='Código APU',
        required=False,
        comodel_name='product.product',
        ondelete='restrict',
        help='''Código APU oficial del IDU – Análisis de Precios Unitarios''',
        readonly=True,
    )
    product_id = fields.Many2one(
        string='Código APU',
        required=False,
        comodel_name='product.product',
        ondelete='restrict',
        help='''Código APU oficial del IDU – Análisis de Precios Unitarios''',
        readonly=True,
    )
    # -------------------
    # methods
    # -------------------

    @api.one
    @api.depends('res_id', 'res_model')
    def _compute_name(self):
        self.name = "Possimus explicabo hic ab eum."

class project_reporte_desempeno(models.Model):
    _name = 'project.reporte_desempeno'
    _description = 'Reporte de Desempeno de Proyecto'
    _inherit = ['models.soft_delete.mixin']

    # -------------------
    # Fields
    # -------------------
    name = fields.Char(
        string='Nombre',
        required=True,
        size=255,
    )
    state = fields.Selection(
        string='Estado',
        required=True,
        track_visibility='onchange',
        selection=[
            ('borrador', 'Borrador'),
            ('por_revisar', 'Por Revisar'),
            ('aprobado', 'Aprobado'),
            ('devuelto', 'Devuelto'),
        ],
        default='borrador',
    )
    project_id = fields.Many2one(
        string='Proyecto',
        required=True,
        comodel_name='project.project',
        ondelete='restrict',
    )
    linea_base_id = fields.Many2one(
        string='Línea Base',
        required=True,
        comodel_name='project.linea_base',
        ondelete='restrict',
        help='Línea base contra la que se hace la comparación',
    )
    linea_base_reporte_id = fields.Many2one(
        string='Detalle del Reporte',
        required=True,
        comodel_name='project.linea_base',
        ondelete='restrict',
        help='Valores utilizados para realizar el reporte',
    )
    fecha = fields.Datetime(
        string='Fecha',
        required=True,
        default=fields.Datetime.now,
    )
    analisis = fields.Html(
        string='Análisis de Desempeño',
        required=False,
    )
    causa_raiz = fields.Html(
        string='Análisis de Causa Raíz',
        required=False,
    )
    plan_contingencia = fields.Html(
        string='Plan de Contingencia',
        required=False,
    )

    # -------------------
    # methods
    # -------------------

    # -------------------
    # Workflow methods
    # -------------------
    def wkf_borrador(self):
        self.state = 'borrador'

    def wkf_aprobado(self):
        self.state = 'aprobado'

    def wkf_devuelto(self):
        self.state = 'devuelto'

    def wkf_por_revisar(self):
        self.state = 'por_revisar'


class project_reporte_desempeno_valor_ganado(models.Model):
    _name = 'project.reporte_desempeno.valor_ganado'
    _description = 'Valor Ganado Proyecto'

    # -------------------
    # Fields
    # -------------------
    name = fields.Char(
        string='Nombre',
        required=True,
        size=255,
        compute='_compute_name',
    )
    reporte_id = fields.Many2one(
        string='Reporte de Desempeño',
        required=True,
        comodel_name='project.reporte_desempeno',
        ondelete='restrict',
    )
    linea_base_linea_id = fields.Many2one(
        string='Linea de la Línea Base',
        required=True,
        comodel_name='project.linea_base.linea',
        ondelete='restrict',
    )
    active = fields.Boolean(
        string='Línea Base esta activa?',
        required=False,
        readonly=True,
        related='reporte_id.active',
        default=True,
    )
    planned_complete = fields.Float(
        string='Planned % complete',
        required=False,
    )
    actual_complete = fields.Float(
        string='Actual % complete',
        required=False,
    )
    bac = fields.Float(
        string='Budgeted At Completion (BAC)',
        required=False,
        help='How much was originally planned for this project to cost.',
    )
    ac = fields.Float(
        string='Actual Cost (AC)',
        required=False,
        help='Sum of the costs for the given period of time.',
    )
    es = fields.Float(
        string='Earn Scheduled (ES)',
        required=False,
        help='Time when PV has the same value of current EV',
    )
    at = fields.Float(
        string='Actual Time (AT)',
        required=False,
        help='Current time where the valuation is being done',
    )
    pv = fields.Float(
        string='Planned Value (PV)',
        required=False,
        compute='_compute_pv',
        help='PV = Planned % Complete x BAC',
    )
    ev = fields.Float(
        string='Earned Value (EV)',
        required=False,
        compute='_compute_ev',
        help='EV = Actual % Complete x BAC',
    )
    cv = fields.Float(
        string='Cost Variance (CV)',
        required=False,
        compute='_compute_cv',
        help='CV = EV-AC. The difference between what we expected to spend and what was actually spent.',
    )
    sv = fields.Float(
        string='Schedule Variance (SV)',
        required=False,
        compute='_compute_sv',
        help='SV = EV-PV. The difference between where we planned to be in the schedule and where we are in the schedule.',
    )
    cpi = fields.Float(
        string='Cost Performance Index (CPI)',
        required=False,
        compute='_compute_cpi',
        help='CPI = EV ÷ AC. The rate at which the project performance is meeting cost expectations during a given period of time.',
    )
    spi = fields.Float(
        string='Schedule Performance Index (SPI)',
        required=False,
        compute='_compute_spi',
        help='SPI = EV ÷ PV. The rate at which the project performance is meeting schedule expectations up to a point in time.',
    )
    sv_t = fields.Float(
        string='Schedule Variance SV(t)',
        required=False,
        compute='_compute_sv_t',
        help='SV(t) = ES – AT. Shows the variance in time expressed in time units',
    )
    spi_t = fields.Float(
        string='Schedule Performance Index SPI(t)',
        required=False,
        compute='_compute_spi_t',
        help='SPI(t) = ES / AT',
    )
    pcib = fields.Float(
        string='Percent Complete Index Budget',
        required=False,
        compute='_compute_pcib',
        help='PCIB = EV/BAC',
    )
    #Formulas para Proyecciones
    eac_t = fields.Float(
        string='Estimate at completion (typical)',
        required=False,
        compute='_compute_eac_t',
        help='EAC_T = BAC/CPI',
    )
    eac_a = fields.Float(
        string='Estimate at completion (atypical)',
        required=False,
        compute='_compute_eac_a',
        help='EAC_A = AC + BAC - EV',
    )
    etc_t = fields.Float(
        string='Estimate to complete (typical)',
        required=False,
        compute='_compute_etc_t',
        help='ETC_T = EAC_T/AC',
    )
    etc_a = fields.Float(
        string='Estimate to complete (atypical)',
        required=False,
        compute='_compute_etc_a',
        help='ETC_A = EAC_A/AC',
    )
    vac_t = fields.Float(
        string='Variance at Completion (typical)',
        required=False,
        compute='_compute_vac_t',
        help='VAC_T = BAC - EAC_T',
    )
    vac_a = fields.Float(
        string='Variance at Completion (atypical)',
        required=False,
        compute='_compute_vac_a',
        help='VAC_A = BAC - EAC_A',
    )
    tcpi_act = fields.Float(
        string='To complete performance index',
        required=False,
        compute='_compute_tcpi_act',
        help='TCPI_ACT = (BAC - EV)/(BAC - AC)',
    )
    tcpi_t = fields.Float(
        string='To complete performance index (typical)',
        required=False,
        compute='_compute_tcpi_t',
        help='TCPI_ACT = (BAC - EV)/(EAC_T - AC)',
    )
    tcpi_a = fields.Float(
        string='To complete performance index (atypical)',
        required=False,
        compute='_compute_tcpi_a',
        help='TCPI_ACT = (BAC - EV)/(EAC_A - AC)',
    )
    # -------------------
    # methods
    # -------------------

    @api.one
    @api.depends('reporte_id', 'linea_base_linea_id')
    def _compute_name(self):
        self.name = "Asperiores ut suscipit placeat impedit debitis vero."

    @api.one
    @api.depends('bac', 'planned_complete')
    def _compute_pv(self):
        self.pv = round(self.planned_complete*self.bac,2)

    @api.one
    @api.depends('bac', 'actual_complete')
    def _compute_ev(self):
        self.ev = round(self.actual_complete*self.bac,2)

    @api.one
    @api.depends('ev', 'ac')
    def _compute_cv(self):
        self.cv = round(self.ev - self.ac,2)

    @api.one
    @api.depends('ev', 'pv')
    def _compute_sv(self):
        self.sv = self.ev - self.pv

    @api.one
    @api.depends('ev', 'ac')
    def _compute_cpi(self):
        self.cpi = round(self.ev/self.ac,10)

    @api.one
    @api.depends('ev', 'pv')
    def _compute_spi(self):
        self.spi = round(self.ev/self.pv,2)

    @api.one
    @api.depends('bac', 'cpi')
    def _compute_eac_t(self):
        self.eac_t = round(self.bac/self.cpi,2)

    @api.one
    @api.depends('ac', 'bac', 'ev')
    def _compute_eac_a(self):
        self.eac_a = self.ac + self.bac - self.ev

    @api.one
    @api.depends('eac_t', 'ac')
    def _compute_etc_t(self):
        self.etc_t = round(self.eac_t - self.ac,2)

    @api.one
    @api.depends('eac_a', 'ac')
    def _compute_etc_a(self):
        self.etc_a = self.eac_a - self.ac

    @api.one
    @api.depends('bac', 'eac_t')
    def _compute_vac_t(self):
        self.vac_t = round(self.bac - self.eac_t,2)

    @api.one
    @api.depends('bac', 'eac_a')
    def _compute_vac_a(self):
        self.vac_a = self.bac - self.eac_a

    @api.one
    @api.depends('bac', 'ev', 'ac')
    def _compute_tcpi_act(self):
        self.tcpi_act = round((self.bac - self.ev)/(self.bac - self.ac),2)

    @api.one
    @api.depends('bac', 'ev', 'eac_t', 'ac')
    def _compute_tcpi_t(self):
        self.tcpi_t = round((self.bac - self.ev)/(self.eac_t - self.ac),2)

    @api.one
    @api.depends('bac', 'ev', 'eac_a', 'ac')
    def _compute_tcpi_a(self):
        self.tcpi_a = round((self.bac - self.ev)/(self.eac_a - self.ac),2)

    @api.one
    @api.depends('es', 'at')
    def _compute_sv_t(self):
        self.sv_t = round(self.es - self.at, 2)

    @api.one
    @api.depends('es', 'at')
    def _compute_spi_t(self):
        self.spi_t = round(self.es / self.at, 2)

class project_project(models.Model):
    _name = 'project.project'
    _inherit = ['project.project']

    # -------------------
    # Fields
    # -------------------
    project_padre_id = fields.Many2one(
        string='Proyecto Padre',
        required=False,
        track_visibility='onchange',
        comodel_name='project.project',
        ondelete='restrict',
    )
    dependencia_id = fields.Many2one(
        string='Dependencia',
        required=False,
        track_visibility='onchange',
        comodel_name='hr.department',
        ondelete='restrict',
    )
    alcance = fields.Text(
        string='Alcance',
        required=False,
        track_visibility='onchange',
    )
    notas = fields.Text(
        string='Notas',
        required=False,
        track_visibility='onchange',
    )
    proyecto_tipo = fields.Selection(
        string='Tipo de Proyecto',
        required=True,
        track_visibility='onchange',
        selection=[
            ('obra', 'Obra'),
            ('obra_etapa', 'Etapa de Obra'),
            ('obra_componente', 'Obra Componente'),
            ('funcionamiento', 'Funcionamiento/Apoyo'),
            ('plan_mejoramiento', 'Plan Mejoramiento'),
            ('plan_accion', 'Plan Acción'),
        ],
        default='funcionamiento',
    )
    linea_base_id = fields.Many2one(
        string='Línea Base Actual',
        required=False,
        comodel_name='project.linea_base',
        ondelete='restrict',
    )
    linea_base_ids = fields.One2many(
        string='Líneas Base',
        required=False,
        comodel_name='project.linea_base',
        inverse_name='project_id',
        domain=[('es_snapshot', '=', False)],
        ondelete='restrict',
    )
    snapshot_ids = fields.One2many(
        string='Históricos de ejecución',
        required=False,
        comodel_name='project.linea_base',
        inverse_name='project_id',
        ondelete='restrict',
        domain=[('es_snapshot', '=', True)],
    )
    financiacion_ids = fields.One2many(
        string='Financiación',
        required=False,
        comodel_name='project.financiacion',
        inverse_name='project_id',
        ondelete='restrict',
    )
    meta_ids = fields.One2many(
        string='Metas',
        required=False,
        comodel_name='project.meta',
        inverse_name='project_id',
        ondelete='restrict',
    )
    solicitud_cambio_ids = fields.One2many(
        string='Solicitudes de Cambio',
        required=False,
        comodel_name='project.solicitud_cambio',
        inverse_name='project_id',
        ondelete='restrict',
    )
    reporte_desempeno_ids = fields.One2many(
        string='Reportes de Desempeño',
        required=False,
        comodel_name='project.reporte_desempeno',
        inverse_name='project_id',
        ondelete='restrict',
    )
    programa_id = fields.Many2one(
        string='Programa',
        required=False,
        track_visibility='onchange',
        comodel_name='project.programa',
        ondelete='restrict',
    )
    portafolio_ids = fields.Many2many(
        string='Portafolios',
        required=False,
        comodel_name='project.portafolio',
        ondelete='restrict',
    )

    # -------------------
    # methods
    # -------------------
    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False, xtra=None):
        new_args = adiciona_keywords_en_search(self, cr, uid, args, offset, limit, order, context, count, xtra)
        return super(project_project, self).search(cr, uid, new_args, offset, limit, order, context, count)

    @api.multi
    def crear_linea_base(self, nombre):
        self.ensure_one()
        linea_base_model = self.env['project.linea_base']
        vals = {
            'name': nombre,
            'project_id': self.id,
            'es_snapshot': False,
        }
        linea_base = linea_base_model.create(vals)
        self.linea_base_id = linea_base.id
        linea_base.linea_raiz_id = self.edt_raiz_id.crear_linea_base_linea(linea_base.id).id
        return linea_base


    @api.multi
    def crear_snapshot(self, nombre):
        self.ensure_one()
        linea_base_model = self.env['project.linea_base']
        vals = {
            'name': nombre,
            'project_id': self.id,
            'es_snapshot': True,
        }
        linea_base = linea_base_model.create(vals)
        linea_base.linea_raiz_id = self.edt_raiz_id.crear_snapshot_linea(linea_base.id).id
        return linea_base

    def name_get(self, cr, uid, ids, context=None):
        """ Retorna el nombre del padre si se indica en el contexto display_parent_name
        """
        if not isinstance(ids, list):
            ids = [ids]
        if context is None:
            context = {}

        if not context.get('display_parent_name', False):
            return super(project_project, self).name_get(cr, uid, ids, context=context)

        res = []
        for project in self.browse(cr, uid, ids, context=context):
            names = []
            current = project
            while current:
                names.append(current.name)
                current = current.project_padre_id
            res.append((project.id, ' / '.join(reversed(names))))
        return res

    @api.multi
    def usuario_actual_actua_como_gerente(self):
        """Retorna True a los usuarios que pueden acceder a las funcionalidades que requieren un perfil de gerente para el proyecto"""
        res = super(project_project, self).usuario_actual_actua_como_gerente()
        if res:
            return res
        autorizado_ids = []
        user_id = self.env.user.id
        autorizado_ids.append(self.dependencia_id.manager_id.user_id.id)
        autorizado_ids.append(self.dependencia_id.proyecto_gerente_id.id)
        autorizado_ids.append(self.dependencia_id.proyecto_programador_id.id)
        if user_id and user_id in autorizado_ids:
            return True
        return False


class project_financiacion(models.Model):
    _name = 'project.financiacion'
    _description = 'Financiacion Proyecto'
    _inherit = ['models.soft_delete.mixin']

    # -------------------
    # Fields
    # -------------------
    name = fields.Char(
        string='Descripción',
        required=True,
        track_visibility='onchange',
        size=255,
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
    project_id = fields.Many2one(
        string='Proyecto',
        required=True,
        track_visibility='onchange',
        comodel_name='project.project',
        ondelete='restrict',
        default=lambda self: self._context.get('project_id', None),
    )
    fuente_financiacion_id = fields.Many2one(
        string='Fuente de financiación',
        required=True,
        track_visibility='onchange',
        comodel_name='stone_erp.fuente',
        ondelete='restrict',
    )
    valor = fields.Monetary(
        string='Valor',
        required=True,
    )

    # -------------------
    # methods
    # -------------------

class project_solicitud_cambio(models.Model):
    _name = 'project.solicitud_cambio'
    _description = 'Solicitud de Cambio en Proyecto'
    _inherit = ['mail.thread', 'models.soft_delete.mixin']

    # -------------------
    # Fields
    # -------------------
    name = fields.Char(
        string='Nombre',
        required=True,
        track_visibility='onchange',
        size=255,
    )
    state = fields.Selection(
        string='Estado',
        required=True,
        track_visibility='onchange',
        selection=[
            ('nuevo', 'nuevo'),
            ('por_revisar', 'por_revisar'),
            ('aprobado', 'aprobado'),
            ('devuelto', 'devuelto'),
        ],
        default='nuevo',
    )
    project_id = fields.Many2one(
        string='Proyecto',
        required=True,
        track_visibility='onchange',
        comodel_name='project.project',
        ondelete='restrict',
    )

    # -------------------
    # methods
    # -------------------

    # -------------------
    # Workflow methods
    # -------------------
    def wkf_nuevo(self):
        self.state = 'nuevo'

    def wkf_aprobado(self):
        self.state = 'aprobado'

    def wkf_devuelto(self):
        self.state = 'devuelto'

    def wkf_por_revisar(self):
        self.state = 'por_revisar'


class project_meta(models.Model):
    _name = 'project.meta'
    _description = 'Meta de Proyecto'
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
    project_id = fields.Many2one(
        string='Proyecto',
        required=True,
        comodel_name='project.project',
        ondelete='restrict',
        default=lambda self: self._context.get('project_id', None),
    )
    tipo_id = fields.Many2one(
        string='Tipo',
        required=True,
        comodel_name='project.meta.tipo',
        ondelete='restrict',
    )
    cantidad = fields.Float(
        string='Cantidad',
        required=True,
    )
    edt_id = fields.Many2one(
        string='EDT',
        required=False,
        comodel_name='project.edt',
        ondelete='restrict',
    )
    progreso = fields.Integer(
        string='Progreso',
        required=False,
        readonly=True,
        related='edt_id.progreso',
    )

    # -------------------
    # methods
    # -------------------

    @api.one
    @api.depends('cantidad', 'tipo_id')
    def _compute_name(self):
        self.name = "Sapiente quis numquam voluptatem."

class project_meta_tipo(models.Model):
    _name = 'project.meta.tipo'
    _description = 'Tipificación Meta de Proyecto'
    _inherit = ['models.soft_delete.mixin']

    # -------------------
    # Fields
    # -------------------
    name = fields.Char(
        string='Nombre',
        required=True,
        size=255,
    )
    uom_id = fields.Many2one(
        string='Unidad de Medida',
        required=True,
        comodel_name='product.uom',
        ondelete='restrict',
    )

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Este name ya está registrado'),
    ]

    # -------------------
    # methods
    # -------------------


class linea_base_linea_mixin(models.AbstractModel):
    _name = 'project.linea_base.linea.mixin'
    _description = 'Linea Base Linea Mixin'

    _snapshot_campos_map = {} # Campos para generar un snapshot de la ejecución actual
    _linea_base_campos_map = {} # Campos para ser almacenados como línea base
    _descendientes_map = {} #one2many or many2many objects to include in the baseline

    linea_base_linea_ids = fields.One2many(
        comodel_name='project.linea_base.linea',
        inverse_name='res_id',
        string='Valores en otras líneas base',
        domain=lambda self: [('res_model', '=', self._name), ('linea_base_id.es_snapshot', '=', False)],
        auto_join=True,
    )
    snapshot_linea_ids = fields.One2many(
        comodel_name='project.linea_base.linea',
        inverse_name='res_id',
        string='Valores en otras líneas base',
        domain=lambda self: [('res_model', '=', self._name), ('linea_base_id.es_snapshot', '=', True)],
        auto_join=True,
    )

    @api.multi
    def crear_linea_base_linea(self, linea_base_id):
        """Genera la líneas utilizando el mapeo para linea base, para guardar valores planeados"""
        return self._crear_linea_base_linea(linea_base_id, self._linea_base_campos_map)[0]

    @api.multi
    def crear_snapshot_linea(self, linea_base_id):
        """Genera la líneas utilizando el mapeo para snapshot, para guardar valores actuales"""
        return self._crear_linea_base_linea(linea_base_id, self._snapshot_campos_map)[0]

    @api.one
    def _crear_linea_base_linea(self, linea_base_id, mapeo, parent=None):
        linea_model = self.env['project.linea_base.linea']
        data = self.sudo().read(mapeo.values() + self._descendientes_map.values())
        linea = None
        for record in data:
            vals = {
                'linea_base_id': linea_base_id,
                'res_model': self._name,
                'res_id': record['id'],
            }
            for field, obj_field in mapeo.items():
                if isinstance(record[obj_field], tuple):
                    vals[field] = record[obj_field][0] #set ID
                else:
                    vals[field] = record[obj_field]
            if parent:
                vals['parent_id'] = parent.id
            linea = linea_model.create(vals)
            for child_model, child_field in self._descendientes_map.items():
                child_model = self.env[child_model]
                if child_field in record:
                    child_ids = record[child_field]
                    child_model.browse(child_ids)._crear_linea_base_linea(linea_base_id, mapeo, linea)
        return linea


class project_edt(models.Model):
    _name = 'project.edt'
    _inherit = ['project.edt', 'project.linea_base.linea.mixin']

    _linea_base_campos_map = {
        'name': 'name',
        'numero': 'numero',
        'fecha_inicio': 'fecha_planeada_inicio',
        'fecha_fin': 'fecha_planeada_fin',
        'progreso': 'progreso_aprobado',
        'costo': 'costo_planeado',

    }
    _snapshot_campos_map = {
        'name': 'name',
        'numero': 'numero',
        'fecha_inicio': 'fecha_inicio',
        'fecha_fin': 'fecha_fin',
        'progreso': 'progreso',
        'costo': 'costo',

    }
    _descendientes_map = {
        'project.edt': 'child_ids',
        'project.task': 'task_ids',
    }

class project_task(models.Model):
    _name = 'project.task'
    _inherit = ['project.task', 'project.linea_base.linea.mixin']

    _linea_base_campos_map = {
        'name': 'name',
        'numero': 'numero',
        'fecha_inicio': 'fecha_planeada_inicio',
        'fecha_fin': 'fecha_planeada_fin',
        'progreso': 'progreso_aprobado',
        'costo': 'costo_planeado',
        'cantidad': 'cantidad_planeada',
    }

    _snapshot_campos_map = {
        'name': 'name',
        'numero': 'numero',
        'fecha_inicio': 'fecha_inicio',
        'fecha_fin': 'fecha_fin',
        'progreso': 'progreso',
        'costo': 'costo',
        'cantidad': 'cantidad',
        'product_id': 'product_id',
    }

    # -------------------
    # Fields
    # -------------------
    dependencia_id = fields.Many2one(
        string='Dependencia',
        required=False,
        track_visibility='onchange',
        comodel_name='hr.department',
        ondelete='restrict',
        invisible=True,
    )

    # -------------------
    # methods
    # -------------------

