# -*- coding: utf-8 -*-

from openerp import models, fields, api, tools
from openerp.exceptions import ValidationError,AccessDenied,Warning
from openerp.addons.base_idu.models.create_user import find_area
import re
from datetime import timedelta, date, datetime
import logging
import ldap
from ldap.filter import filter_format

_logger = logging.getLogger(__name__)


class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    nombres = fields.Char('Nombres', size=120)
    apellidos = fields.Char('Apellidos', size=120)
    identificacion_numero = fields.Char('Número de identificación', size=64)
    identificacion_tipo = fields.Selection(
        [
            ('CC','Cédula de Ciudadanía'),
            ('TI','Tarjeta de Identidad'),
            ('CE','Cédula de Extranjería'),
            ('Pasaporte','Pasaporte'),
        ],
        string='Tipo de identificación',
    )
    tipo_persona = fields.Selection(
        [
            ('nat','Persona Natural'),
            ('jur','Persona Jurídica'),
        ],
        string='Tipo de Persona',
        default=lambda self: self._context.get('tipo_persona','jur'),
        required=True,
    )
    genero = fields.Selection(
        [
            ('M','Masculino'),
            ('F','Femenino'),
        ],
        string='Género',
    )
    twitter = fields.Char('Twitter', size=64)
    facebook = fields.Char('Facebook', size=240)
    district_id = fields.Many2one(
        'res.country.state.city.district',
        'Localidad',
    )
    neighborhood_id = fields.Many2one(
        'res.country.state.city.neighborhood',
        'Barrio',
        domain="[('district_id','=',district_id)]",
    )
    es_funcionario_idu = fields.Boolean(
        string='Es Funcionario IDU (carrera o PSP)?',
        compute='compute_es_funcionario_idu',
        store=True,
    )
    id_portal_idu = fields.Integer('ID del usuario en el Portal del IDU')

    @api.depends('email')
    @api.one
    def compute_es_funcionario_idu(self):
        self.es_funcionario_idu = (self.email and re.match("^.*idu\.gov\.co$", self.email))

    # TODO: Adicionar numero unico de identificación
    # TODO: Buscar por numero de identificación

    @api.onchange('email')
    def onchange_email(self):
        try:
            self._check_email()
        except Exception as e:
            return {
                'warning': { 'message': e.name }
            }

    @api.one
    @api.constrains('email')
    def _check_email(self):
        """
        Constraint:
        simple checking with regex /^[^@]+@[^@]+\.[^@]+$/
        """
        if self.env.context.get('no_check', False):
            return

        if (self.email != False) and (re.match("^[^@]+@[^@]+\.[^@]+$", self.email) == None):
            raise ValidationError('El email no es válido.')

    @api.onchange('phone')
    def onchange_phone(self):
        try:
            self._check_phone()
        except Exception as e:
            return {
                'warning': { 'message': e.name }
            }

    @api.one
    @api.constrains('phone')
    def _check_phone(self):
        """
        Constraint:
        Simple checking with regex /^\d{7}$/
        """
        if self.env.context.get('no_check', False):
            return

        if (self.phone != False) and (re.match('^\d{7}$', self.phone) == None):
            raise ValidationError('El número teléfonico no sigue el formato correcto, ej.  4035696')

    @api.onchange('mobile')
    def onchange_mobile(self):
        try:
            self._check_mobile()
        except Exception as e:
            return {
                'warning': { 'message': e.name }
            }

    @api.one
    @api.constrains('mobile')
    def _check_mobile(self):
        """
        Constraint:
        Simple checking with regex /^\d{10}$/
        """
        if self.env.context.get('no_check', False):
            return

        if (self.mobile != False) and (re.match('^\d{10}$', self.mobile) == None):
            raise ValidationError('El número celular no sigue el formato correcto, ej.  3112563458')

    @api.onchange('tipo_persona','nombres','apellidos')
    def onchange_nombres_persona_natural(self):
        """Calcula el nombre si es persona natural a partir de nombres y apellidos"""
        if self.tipo_persona == 'nat' and (self.nombres or self.apellidos):
            fullname = '{0} {1}'.format(self.nombres or '', self.apellidos or '')
            self.name = fullname.strip()

    @api.model
    def create(self, vals):
        """Calcula el nombre si es persona natural a partir de nombres y apellidos
           Persona Natural siempre es una compañia
           Limpia puntos del campo identificacion_numero si es que trae.
        """
        if vals.get('tipo_persona', 'jur') == 'jur':
            vals['is_company'] = True
            vals['company_type'] = 'company'
        else:
            vals['is_company'] = False
            vals['company_type'] = 'person'

        if vals.get('tipo_persona') == 'nat' and (vals.get('nombres') or vals.get('apellidos')):
            fullname = '{0} {1}'.format(vals.get('nombres',''), vals.get('apellidos',''))
            vals['name'] = fullname.strip()
        identificacion_numero = vals.get('identificacion_numero',False)
        if (identificacion_numero and isinstance(identificacion_numero, basestring)):
            vals['identificacion_numero'] = identificacion_numero.strip().replace('.','')

        return super(res_partner, self).create(vals)


    @api.one
    def write(self, vals):
        """Calcula el nombre si es persona natural a partir de nombres y apellidos
           Persona Natural siempre es una compañia
           Limpia puntos del campo identificacion_numero si es que trae.
        """
        if vals.get('tipo_persona', 'jur') == 'jur':
            vals['is_company'] = True
            vals['company_type'] = 'company'

        if vals.get('tipo_persona') or vals.get('nombres') or vals.get('apellidos'):
            if vals.get('tipo_persona', self.tipo_persona) == 'nat':
                vals['company_type'] = 'person'
            if vals.get('tipo_persona', self.tipo_persona) == 'nat' and (
                    vals.get('nombres', self.nombres) or
                    vals.get('apellidos', self.apellidos
                )
            ):
                fullname = '{0} {1}'.format(vals.get('nombres', self.nombres), vals.get('apellidos',self.apellidos))
                vals['name'] = fullname.strip()

        identificacion_numero = vals.get('identificacion_numero',False)
        if (identificacion_numero and isinstance(identificacion_numero, basestring)):
            vals['identificacion_numero'] = identificacion_numero.strip().replace('.','')

        return super(res_partner, self).write(vals)

    def signup_retrieve_info(self, cr, uid, token, context=None):
        """ Sobreescribe el metodo de /usr/lib/python2.7/dist-packages/openerp/addons/auth_signup/res_users.py
        Para permitir que se despliegue en el formulario web todas las cuentas a las cuales se le actualizaria la clave
        """
        res = super(res_partner, self).signup_retrieve_info(cr, uid, token, context)
        partner = self._signup_retrieve_partner(cr, uid, token, raise_exception=True, context=None)
        res['usuarios'] = partner.user_ids
        now = datetime.now()
        partner_user = res['login']
        for user in partner.user_ids: # Busca un usuario que no esta inactivo por fecha de expiracion
            if not user.fecha_expiracion:
                partner_user = user.login
                break
            elif user.fecha_expiracion and datetime.strptime(user.fecha_expiracion, "%Y-%m-%d") >= now:
                partner_user = user.login
                break
        res['login'] = partner_user
        return res

    @api.multi
    def _notify_by_email(self, message, force_send=False, user_signature=True):
        """No enviar email cuando el context tiene no_mail"""
        if self.env.context.get('mail_create_nolog', False):
            return True
        return super(res_partner, self)._notify_by_email(message, force_send, user_signature)

    @api.model
    def buscar_o_crear_partner_desde_portal(self, nombre, identificacion_numero, email, id_portal_idu):
        """Crea un res.partner utilizando los que vienen desde el portal del IDU en liferay"""
        contacto = self.search([
            ('id_portal_idu', '=', id_portal_idu)
        ])
        if not contacto:
            contacto = self.search([
                ('identificacion_numero', '=', identificacion_numero)
            ])
            if contacto:
                contacto.id_portal_idu = id_portal_idu
        if not contacto:
            contacto = self.search([
                ('email', '=', email)
            ])
            if contacto:
                contacto.id_portal_idu = id_portal_idu

        if not contacto:
            partes = nombre.split(' ')
            nombres = ''
            apellidos = ''
            if len(partes) == 2:
                nombres = partes[0]
                apellidos = partes[1]
            elif len(partes) >= 3:
                nombres = partes[:2]
                apellidos = partes[2:]
            else:
                raise ValidationError('Debe ingresar nombre y apellido completo, se recibió: {}'.format(nombre))

            contacto = self.create({
                'nombres': ' '.join(nombres),
                'apellidos': ' '.join(apellidos),
                'tipo_persona': 'nat',
                'identificacion_numero': identificacion_numero,
                'identificacion_tipo': 'CC',
                'email': email,
                'id_portal_idu': id_portal_idu,
            })

        return contacto

    _sql_constraints = [
        ('unique_email','unique(email)','Este correo electrónico ya está registrado.'),
        ('unique_twitter','unique(twitter)','Esta cuenta de twitter ya está registrada.'),
        ('unique_facebook','unique(facebook)','Esta cuenta de facebook ya está registrada.'),
        ('identificacion_numero_uniq', 'unique(identificacion_numero)', 'Este número de identificación ya está registrado.'),
        ('mobile_uniq', 'unique(mobile)', 'Este número de celular ya está registrado.'),
    ]

class res_users(models.Model):
    _name = 'res.users'
    _inherit = ['res.users','mail.thread']

    # Fields
    groups_id = fields.Many2many(default=False) # Sobreescribe para que no se asigne ningún grupo por defecto.
    employee_id = fields.Many2one(
        'hr.employee',
        "Employee",
        domain="[('user_id','=',active_id)]",
    )
    department_id = fields.Many2one(
        related='employee_id.department_id',
        readonly=True,
    )
    fecha_expiracion = fields.Date(
        'Fecha Expiración',
    )
    fecha_cambio_clave = fields.Datetime(
        'Fecha Último cambio de clave',
        readonly=True,
    )
    es_funcionario_idu = fields.Boolean(
        string='Es Funcionario IDU (carrera o PSP)?',
        compute='compute_es_funcionario_idu',
        store=True,
    )

    @api.multi
    @api.depends('name', 'bic')
    def name_get(self):
        result = []
        for user in self:
            name = '{0} - {1}'.format(user.name, user.login)
            result.append((user.id, name))
        return result

    @api.depends('email', 'partner_id.email')
    @api.one
    def compute_es_funcionario_idu(self):
        self.es_funcionario_idu = ((self.email and re.match("^.*idu\.gov\.co$", self.email)) or self.employee_id.id)

    def notificar_expiracion_cuenta_cron(self, cr, uid, dias=7, context=None):
        fecha_limite = date.today() + timedelta(days=dias)
        fecha_limite = fecha_limite.strftime('%Y-%m-%d')
        usuarios_ids = self.search(cr, uid, [('fecha_expiracion','<',fecha_limite),('fecha_expiracion','>=',date.today().strftime('%Y-%m-%d'))], context=context)
        usuarios = self.browse(cr, uid, usuarios_ids)
        for us in usuarios:
            # enviar Correo
            mensaje = """Se apróxima la fecha de finalización de su cuenta {0} en openerp.idu.gov.co: {1}, desde esta fecha no tendrá acceso al sistema.


                    Nota: Esta es una notificación enviada automáticamente""".format(us.login, us.fecha_expiracion)
            self.message_post(
                cr, uid, us.id, context=None,
                subject='Notificación expiración de cuenta en openerp.idu.gov.co',
                type="email",
                res_id=us.id,
                body=mensaje,
                partner_ids=[us.partner_id.id]
            )
        return True


    @api.one
    def has_group_v8(self, group_ext_id):
        """Metodo para tener disponible el has_group que esta escrito en api de la v7.0,
        otras alternativas utilizando el decorador api.v8 generan errores para loguear usuarios nuevos"""
        return self.pool.get('res.users').has_group(self.env.cr, self.id, group_ext_id)

    @api.one
    def update_employee_with(self, employee):
        """Actualiza el campo employee_id si no hay uno asignado"""
        if employee == None:
            if len(self.employee_ids):
                self.write({'employee_id': self.employee_ids[0].id})
            else:
                self.write({'employee_id': False})
            return
        elif not self.employee_id:
            self.write({'employee_id': employee.id})
        # Desvincular otros usuarios que apunten a este mismo empleado
        otros_usuarios = self.search([('employee_id', '=', employee.id), ('id', '!=', self.id)])
        otros_usuarios.update_employee_with(None)
        self.invalidate_cache(['employee_ids','employee_id','department_id'])

    @api.constrains('employee_id')
    def check_employee_ids(self):
        if self.employee_id and not self.employee_id.id in [i.id for i in self.employee_ids]:
            raise ValidationError('El empleado seleccionado debe referenciar al usuario: {0}'.format(self.login))

    def check_credentials(self, cr, uid, password):
        super(res_users, self).check_credentials(cr, uid, password)
        cr.execute('SELECT login,fecha_expiracion FROM res_users WHERE id=%s AND active=TRUE AND (fecha_expiracion IS NULL OR fecha_expiracion >= now()::DATE)',
            (int(uid),)
        )
        res = cr.fetchone()
        if res:
            return
        else:
            raise AccessDenied()

    # Sobreescribe el metodo de auth_crypt para prevenir cambios de clave por usuarios IDU
    # Que solo deben autenticarse utilizando clave de LDAP
    def _set_password(self, cr, uid, id, password, context=None):
        """ Encrypts then stores the provided plaintext password for the user
        ``id``
        """
        user = self.pool.get('res.users').browse(cr, uid, id, context=context)
        ldap_activo = user._es_ldap_activo()
        if ldap_activo and user.es_funcionario_idu:
            _logger.warning('Usuario del IDU {0} intentó cambiar contraseña'.format(user.email))
            return
        self.write(cr, uid, id, {'fecha_cambio_clave': fields.Datetime.now()})
        super(res_users, self)._set_password(cr, uid, id, password, context=context)

    _ldap_activo = None
    @api.multi
    def _es_ldap_activo(self):
        if res_users._ldap_activo == None:
            if hasattr(self.company_id, 'ldaps') and len(self.company_id.ldaps):
                res_users._ldap_activo = True
            else:
                res_users._ldap_activo = False
        return res_users._ldap_activo

    def signup(self, cr, uid, values, token=None, context=None):
        """
        Sobreescribe el método que esta en auth_signup/res_users.py para permitir cambiar la contraseña a varios usuarios
        a la vez que estan asociados a un mismo res.partner
            :param values: a dictionary with field values that are written on user
            :param token: signup token (optional)
            :return: (dbname, login, password) for the signed up user
        """
        if token:
            # signup with a token: find the corresponding partner id
            res_partner = self.pool.get('res.partner')
            partner = res_partner._signup_retrieve_partner(
                            cr, uid, token, check_validity=True, raise_exception=True, context=None)
            # invalidate signup token
            partner.write({'signup_token': False, 'signup_type': False, 'signup_expiration': False})

            partner_user = partner.user_ids and partner.user_ids[0] or False

            # avoid overwriting existing (presumably correct) values with geolocation data
            if partner.country_id or partner.zip or partner.city:
                values.pop('city', None)
                values.pop('country_id', None)
            if partner.lang:
                values.pop('lang', None)

            if partner_user:
                # user exists, modify it according to values
                values.pop('login', None)
                values.pop('name', None)
                #HACK IDU
                partner.user_ids.write(values)
                now = datetime.now()
                for user in partner.user_ids:
                    if not user.fecha_expiracion:
                        partner_user = user
                        break
                    elif user.fecha_expiracion and datetime.strptime(user.fecha_expiracion, "%Y-%m-%d") >= now:
                        partner_user = user
                        break

                #FIN HACK IDU
                return (cr.dbname, partner_user.login, values.get('password'))
            else:
                # user does not exist: sign up invited user
                values.update({
                    'name': partner.name,
                    'partner_id': partner.id,
                    'email': values.get('email') or values.get('login'),
                })
                if partner.company_id:
                    values['company_id'] = partner.company_id.id
                    values['company_ids'] = [(6, 0, [partner.company_id.id])]
                self._signup_create_user(cr, uid, values, context=context)
        else:
            # no token, sign up an external user
            values['email'] = values.get('email') or values.get('login')
            self._signup_create_user(cr, uid, values, context=context)

        return (cr.dbname, values.get('login'), values.get('password'))

    @api.model
    def actualizar_listado_usuarios_cron(self):
        ldap_obj = self.env['res.company.ldap']
        conf = ldap_obj.get_ldap_dicts(ids=None)
        if not conf:
            return False
        conf = conf[0]
        users = self.with_context(active_test=False).search([('es_funcionario_idu','=',True),('login','not in',['admin', 'formulario_web']),('login','not like','CTO%')])
        _logger.info('Ejecutando actualizar_listado_usuarios para {} usuarios'.format(len(users)))
        for user in users:
            _logger.debug('Evaluando {} {}'.format(user.login, user.name))
            try:
                ldap_filter = filter_format(conf['ldap_filter'], (user.login,))
            except TypeError, e:
                _logger.warning('Could not format LDAP filter. Your filter should contain one \'%s\'.')
                return False
            try:
                results = ldap_obj.query(conf, ldap_filter.encode('utf-8'))
                # Get rid of (None, attrs) for searchResultReference replies
                results = [i for i in results if i[0]]
                if results and len(results) == 1:
                    if 'department' in results[0][1]:
                        dependencia = results[0][1]['department'][0]
                        if dependencia != user.employee_id.department_id.abreviatura:
                            _logger.info('Actualizando dependencia: {} {} {}'.format(user.login, user.name, dependencia))
                            area_id = find_area(self, dependencia, user.name)
                            user.employee_id.write({ 'department_id': area_id })
                    else:
                        _logger.warning('No hay registrada dependencia para: {} {}'.format(user.login, user.name))

                    if not user.active:
                        _logger.info('Activando usuario: {} {}'.format(user.login, user.name))
                        user.active = True
                        try:
                            user.employee_id.active = True
                        except Exception, e:
                            _logger.exception(e)

                elif user.active:
                    _logger.info('Desactivando usuario: {} {}'.format(user.login, user.name))
                    user.active = False
                    try:
                        user.employee_id.active = False
                    except Exception, e:
                        _logger.exception(e)
            except ldap.LDAPError, e:
                _logger.error('An LDAP exception occurred:')
                _logger.exception(e)
            except Exception, e:
                _logger.exception(e)
        return True


class res_company_location(models.Model):
    _name = 'res.company.location'
    _description = 'Company Location'

    # Fields
    name = fields.Char(
        string='Nombre',
        required=True,
        size=255,
    )
    address = fields.Char(
        string='Dirección',
        size=255,
    )
    company_id = fields.Many2one(
        string='Compañía',
        required=True,
        comodel_name='res.company',
        ondelete='restrict',
    )



