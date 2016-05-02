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
from openerp import SUPERUSER_ID


class ir_attachment(models.Model):
    _inherit = 'ir.attachment'

    active = fields.Boolean(
        string='No borrado',
        default=True,
    )

    def unlink(self, cr, uid, ids, context=None):
        """Soft Delete"""
        if isinstance(ids, (int, long)):
            ids = [ids]
        self.check(cr, uid, ids, 'unlink', context=context)
        self.write(cr, uid, ids, {'active': False}, context=context)

    # Sobre escribe openerp.base.ir.ir_attachment.py para que al eliminar un archivo verifique si el usuario tiene permisos de eliminar
    # el objeto relacionado y no solo si hay restricciones de dominio como esta sucediendo en odoo
    def check(self, cr, uid, ids, mode, context=None, values=None):
        """Restricts the access to an ir.attachment, according to referred model
        In the 'document' module, it is overriden to relax this hard rule, since
        more complex ones apply there.
        """
        res_ids = {}
        require_employee = False
        if ids:
            if isinstance(ids, (int, long)):
                ids = [ids]
            cr.execute('SELECT res_model, res_id, create_uid, public FROM ir_attachment WHERE id = ANY (%s)', (ids,))
            for rmod, rid, create_uid, public in cr.fetchall():
                if public and mode == 'read':
                    continue
                if not (rmod and rid):
                    if create_uid != uid:
                        require_employee = True
                    continue
                res_ids.setdefault(rmod,set()).add(rid)
        if values:
            if values.get('res_model') and values.get('res_id'):
                res_ids.setdefault(values['res_model'],set()).add(values['res_id'])

        ima = self.pool.get('ir.model.access')
        for model, mids in res_ids.items():
            # ignore attachments that are not attached to a resource anymore when checking access rights
            # (resource was deleted but attachment was not)
            if not self.pool.get(model):
                require_employee = True
                continue
            existing_ids = self.pool[model].exists(cr, uid, mids)
            if len(existing_ids) != len(mids):
                require_employee = True
            # For related models, check if we can write to the model, as unlinking
            # and creating attachments can be seen as an update to the model
            if (mode in ['unlink','create']):
                ima.check(cr, uid, model, 'write')
            else:
                ima.check(cr, uid, model, mode)
            # HACK: Inicio HACK IDU
            self.pool[model].check_access_rights(cr, uid, mode, raise_exception=True)
            # HACK: FIN HACK IDU
            self.pool[model].check_access_rule(cr, uid, existing_ids, mode, context=context)
        if require_employee:
            if not uid == SUPERUSER_ID and not self.pool['res.users'].has_group(cr, uid, 'base.group_user'):
                raise AccessError(_("Sorry, you are not allowed to access this document."))

class ir_ui_menu(models.Model):
    _name = 'ir.ui.menu'
    _inherit = ['ir.ui.menu', 'models.soft_delete.mixin']
