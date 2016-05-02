# -*- coding: utf-8 -*-

from openerp import models, fields, api

class hr_department(models.Model):
    _name = "hr.department"
    _inherit = ['hr.department']

    #Fields
    codigo = fields.Integer('Código Dependencia', required=True)
    abreviatura = fields.Char('Abreviatura', size=20, required=True)

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name = '{0} - {1}'.format(record.abreviatura, record.name)
            res.append((record.id, name))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([
                    '|',('name', 'ilike', name),
                        ('abreviatura', 'ilike', name),
                ] + args,
                limit=limit
            )
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()


class hr_employee(models.Model):
    _name = "hr.employee"
    _inherit = ['hr.employee']

    @api.model
    def create(self, vals):
        """Al crear el empleado con un user_id asignado, actualiza el user_id
        para que apunte a este empleado"""
        res = super(hr_employee, self).create(vals)
        if vals.get('user_id', False):
            user = self.env['res.users'].browse(vals.get('user_id'))
            user.update_employee_with(res)
        return res

    @api.one
    def write(self, vals):
        """Al actualizar el empleado con un user_id asignado, actualiza el user_id
        para que apunte a este empleado"""
        res = super(hr_employee, self).write(vals) 
        if vals.get('user_id', False):
            user = self.env['res.users'].browse(vals.get('user_id'))
            user.update_employee_with(self)
        return res
