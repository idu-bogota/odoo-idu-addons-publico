#!/usr/bin/python
# -*- coding: utf-8 -*-
from optparse import OptionParser
import erppeek
import logging

logging.basicConfig()
_logger = logging.getLogger('script')

def main():
    usage = "Script para carga de datos en OpenERP\nusage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-n", "--odoo_db_name", dest="odoo_db_name", help="Odoo database name")
    parser.add_option("-u", "--odoo_db_user",dest="odoo_db_user",help="Odoo database user", default="admin")
    parser.add_option("-p", "--odoo_db_password", dest="odoo_db_password", help="Odoo database password", default="admin")
    parser.add_option("-s", "--odoo_host", dest="odoo_host", help="Odoo server host", default="http://localhost:8069")

    parser.add_option("-N", "--oe_db_name", dest="oe_db_name", help="Sistema anterior database name")
    parser.add_option("-U", "--oe_db_user",dest="oe_db_user",help="Sistema anterior database user", default="admin")
    parser.add_option("-P", "--oe_db_password", dest="oe_db_password", help="Sistema anterior database password", default="admin")
    parser.add_option("-S", "--oe_host", dest="oe_host", help="Sistema anterior server host", default="http://localhost:8069")

    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Display debug message", default=False)

    (options, args) = parser.parse_args()
    _logger.setLevel(0)
    if options.debug:
        _logger.setLevel(10)

    check_obligatorios = ['odoo_db_name', 'odoo_db_user', 'odoo_db_password', 'oe_db_name', 'oe_db_user', 'oe_db_password']
    for i in check_obligatorios:
        if not getattr(options, i):
            parser.error('{0} es obligatorio'.format(i))
    procesar_proyecto(options)

def procesar_proyecto(options):
    odoo = conectar_odoo_openerp(options.odoo_host, options.odoo_db_name, options.odoo_db_user, options.odoo_db_password)
    openerp = conectar_odoo_openerp(options.oe_host, options.oe_db_name, options.oe_db_user, options.oe_db_password)

    oe_zipa = openerp.model('project_idu.proyecto')
    odoo_zipa = odoo.model('project_obra.proyecto')
    total_registros_oe = len(oe_zipa.search([]))
    total_registros_odoo = len(odoo_zipa.search([]))
    state = {'iniciacion' : 'draft',
             'ejecucion' : 'open',
             'cierre' : 'close',
             'planeacion' : 'pending',
             'aplazado' : 'cancel',
             }
    _logger.info("TOTAL PQRS OE: {0}".format(total_registros_oe))
    _logger.info("TOTAL PQRS ODOO: {0} ".format(total_registros_odoo))

    contador = 0
    for oe_zipa_id in oe_zipa.search([]):
        contador += 1
        proy_check = False
        _logger.info("Procesando Proyecto [{2}] {0} de {1}".format(contador, total_registros_oe, oe_zipa_id))
        proy_name = oe_zipa.browse([oe_zipa_id]).name[0]
        if not odoo_zipa.search([('name', '=', proy_name)]):
            crear_modificar_proyecto(oe_zipa_id, openerp, odoo_zipa, odoo, proy_check, state)
        else:
            _logger.warning( 'Proyecto ya creado : {0}'.format(proy_name))
            proy_check = True
            crear_modificar_proyecto(oe_zipa_id, openerp, odoo_zipa, odoo, proy_check, state)

def crear_modificar_proyecto(oe_zipa_id, openerp, odoo_zipa, odoo, proy_check, state):
    # Se busca por id de la pqr y modelo si existe algún dato ajunto creado
    odoo_zipa = odoo.model('project_obra.proyecto')
    odoo_origen = odoo.model('project_obra.proyecto.origen')
    odoo_eje = odoo.model('project_obra.proyecto.eje')
    odoo_img = odoo.model('photo_gallery.photo')
    oe_zipa = openerp.model('project_idu.proyecto')
    oe_origen = openerp.model('project_idu.proyecto.origen')
    oe_eje = openerp.model('project_pmi.program')
    oe_img = openerp.model('photo_gallery.photo')

    oe_zipa_object = oe_zipa.browse([oe_zipa_id])
    odoo_zipa_object = odoo_zipa.browse([('name', '=', oe_zipa_object.name[0])])
    odoo_origen_id = check_origen(odoo_origen, oe_origen, oe_zipa_object)
    odoo_eje_id = check_eje(odoo_eje, oe_eje, oe_zipa_object)
    odoo_img_ids = check_imgs(odoo_img, oe_img, oe_zipa_object, odoo_zipa_object)
#     if oe_zipa_object.name[0] =="Bici Carril Bosa":
#         s = 1

    if not proy_check:
        odoo_zipa.create({
                        'name' : oe_zipa_object.name[0],
                        'alcance' : oe_zipa_object.descripcion[0],
                        'fecha_planeada_inicio' : oe_zipa_object.fecha_inicio_edt[0],
                        'fecha_planeada_fin' : oe_zipa_object.fecha_fin_edt[0],
                        'state' : state[oe_zipa_object.state[0]],
                        'codigo_sigidu' : oe_zipa_object.codigo_sigidu[0]
                            if (oe_zipa_object.codigo_sigidu[0]) else False,
                        'origen_id' : odoo_origen_id,
                        'eje_id' : odoo_eje_id,
                        'photo_ids' : [(6, 0, odoo_img_ids)],
                        })
        _logger.info("Proyecto Creado: {0}".format(oe_zipa_object.name[0]))

    else:
        odoo_zipa.write(odoo_zipa_object.id, {
                        'alcance' : oe_zipa_object.descripcion[0],
                        'fecha_planeada_inicio' : oe_zipa_object.fecha_inicio_edt[0],
                        'fecha_planeada_fin' : oe_zipa_object.fecha_fin_edt[0],
                        'state' : state[oe_zipa_object.state[0]],
                        'codigo_sigidu' : oe_zipa_object.codigo_sigidu[0]
                            if (oe_zipa_object.codigo_sigidu[0]) else False,
                        'origen_id' : odoo_origen_id,
                        'eje_id' : odoo_eje_id,
                        'photo_ids' : [(6, 0, odoo_img_ids)],
                        })
        _logger.info("Proyecto Actualizado: {0}".format(oe_zipa_object.name[0]))

def check_origen(odoo_origen, oe_origen, oe_zipa_object):
    oe_zipa_origen = oe_zipa_object.origen
    if oe_zipa_origen.id[0]:
        oe_origen_name = oe_zipa_origen.name[0]
    else:
        oe_origen_name = "Por Defecto"
        _logger.warning("No Existe Origen en Proyecto: {0}".format(oe_zipa_object.name[0]))
    odoo_origen_object = odoo_origen.browse([('name', '=', oe_origen_name)])
    if not odoo_origen_object:
        odoo_origen_id = odoo_origen.create({'name' : oe_origen_name}).id
        _logger.info("Se crea Origen: {0}".format(oe_origen_name))
    else:
        odoo_origen_id = odoo_origen_object.id[0]
        _logger.info("Origen ya existe: {0}".format(oe_origen_name))
    return odoo_origen_id

def check_eje(odoo_eje, oe_eje, oe_zipa_object):
    oe_zipa_eje = oe_zipa_object.program_id
    if oe_zipa_eje.id[0]:
        oe_eje_name = oe_zipa_eje.name[0]
    else:
        _logger.warning("No Existe Eje en Proyecto: {0}".format(oe_zipa_object.name[0]))
        oe_eje_name = "Por Defecto"
    odoo_eje_object = odoo_eje.browse([('name', '=', oe_eje_name)])
    if not odoo_eje_object:
        odoo_eje_id = odoo_eje.create({'name' : oe_eje_name}).id
        _logger.info("Se crea Eje: {0}".format(oe_eje_name))
    else:
        odoo_eje_id = odoo_eje_object.id[0]
        _logger.info("Eje ya existe: {0}".format(oe_eje_name))
    return odoo_eje_id

def check_imgs(odoo_img, oe_img, oe_zipa_object, odoo_zipa_object):
    oe_zipa_imgs = oe_zipa_object.foto_ids
    odoo_img_ids = []
    if oe_zipa_imgs[0]:
        for img in oe_zipa_imgs[0]:
            oe_img_name = img.name
            odoo_img_object = False
            if odoo_zipa_object.photo_ids:
                odoo_img_object = odoo_img.browse([
                                ('name', '=', oe_img_name),
                                ('id','in',odoo_zipa_object.photo_ids[0].id)
                                ])
            if not odoo_img_object:
                odoo_img_id = odoo_img.create({
                            'name' : oe_img_name,
                            'photo' : img.photo,
                            'datetime' : img.datetime,
                            'location' : img.location,
                            'photographer' : img.photographer,
                            'description' : img.description,
                            'url' : img.url,
                            }).id
                _logger.info("Se crea Imagen: {0}".format(oe_img_name))
            else:
                odoo_img_id = odoo_img_object.id[0]
                _logger.info("Imagen ya existe: {0}".format(oe_img_name))
            if not odoo_img_id in odoo_img_ids:
                odoo_img_ids.append(odoo_img_id)
    else:
        _logger.warning("No hay Imagenes en Proyecto: {0}".format(oe_zipa_object.name[0]))
    return odoo_img_ids

def conectar_odoo_openerp(server, db_name, user, password):
    _logger.debug('Contectando a: {0} {1}'.format(server, db_name));
    client = erppeek.Client(
        server,
        db_name,
        user,
        password,
    )
    return client

if __name__ == '__main__':
    main()
