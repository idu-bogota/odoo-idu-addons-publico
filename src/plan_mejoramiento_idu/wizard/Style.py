#!/usr/bin/python
# -*- coding: utf-8 -*-
import xlwt
from openerp import exceptions
import cStringIO as StringIO
from subprocess import CalledProcessError
from base64 import encodestring
import logging

_logger = logging.getLogger(__name__)

class Style():
    def __init__(self, env, fecha_inicio, fecha_fin, tipo_calificacion_id, plan_tipo, agrupar):
        self.env = env
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.tipo_calificacion_id = tipo_calificacion_id
        self.plan_tipo = plan_tipo
        self.agrupar = agrupar
        self.root = self.env.ref('base.user_root')

    avances = ""
    avances_ids = ""
    acciones = ""
    acciones_ids = ""
    hallazgos = ""
    hallazgos_ids = ""
    planes =""
    workbook = ""
    sheet = ""

    # Metodos
    def parte_texto(self, texto, letras_ancho):
        if not texto:
            return ' '
        palabras = texto.split(' ')
        total_letras = 0
        parrafo = ''
        for palabra in palabras:
            total_letras += len(palabra) + 1
            if total_letras > letras_ancho:
                if len(palabra) > letras_ancho:
                    partes = len(palabra)/letras_ancho
                    inicio = fin = 0
                    for parte in range(partes + 1):
                        inicio = (parte * letras_ancho)
                        fin = inicio + (letras_ancho)
                        if inicio == 1:
                            inicio = 0
                        if parte == partes:
                            fin = None
                            total_letras = len(palabra[inicio:fin])
                        parrafo += '\n{}'.format(palabra[inicio:fin])
                else:
                    parrafo += '\n{}'.format(palabra)
                    total_letras = len(palabra)
            elif parrafo == '':
                parrafo = palabra
            else:
                parrafo += ' {}'.format(palabra)
        return parrafo

    def search_date(self):
            plan_obj = self.env['plan_mejoramiento.plan']
            avance_obj = self.env['plan_mejoramiento.avance']
            accion_obj = self.env['plan_mejoramiento.accion']
            hallazgo_obj = self.env['plan_mejoramiento.hallazgo']

            # Query Acciones
            if self.fecha_inicio and self.fecha_fin:
                self.acciones = accion_obj.sudo(self.root).search([
                                              ('plan_tipo', '=', self.plan_tipo),
                                              ('fecha_inicio', '>=', self.fecha_inicio),
                                              ('fecha_inicio', '<=', self.fecha_fin),
                                              ('fecha_fin', '>=', self.fecha_inicio),
                                              ('fecha_fin', '<=', self.fecha_fin),
                                            ])
                # Acciones con tipo calificacion
                if self.tipo_calificacion_id:
                    list_acciones_calsificadas =[]
                    # busqueda de max avances por cada accion
                    for i in self.acciones:
                        avance_max = avance_obj.sudo(self.root).search(
                            [
                                ('plan_tipo', '=', self.plan_tipo),
                                ('accion_id', '=', i.id)
                            ],
                            order='fecha_corte DESC',
                            limit=1,
                        )
                        # si tiene avances? entra
                        if avance_max:
                            # el maximo abance que tenga la calificacion
                            if avance_max.tipo_calificacion_id.id == self.tipo_calificacion_id.id:
                                list_acciones_calsificadas.append(i.id)
                    # Acciones Caslificados
                    self.acciones = accion_obj.sudo(self.root).search(
                        [
                            ('plan_tipo', '=', self.plan_tipo),
                            ('id', 'in',list_acciones_calsificadas )
                        ]
                    )
            else:
                self.acciones = accion_obj.sudo(self.root).search([('plan_tipo', '=', self.plan_tipo)])
                # Acciones con tipo calificacion
                if self.tipo_calificacion_id:
                    list_acciones_calsificadas =[]
                    # busqueda de max avances por cada accion
                    for i in self.acciones:
                        avance_max = avance_obj.sudo(self.root).search(
                            [
                                ('plan_tipo', '=', self.plan_tipo),
                                ('accion_id', '=', i.id)
                            ],
                            order='fecha_corte DESC',
                            limit=1,
                        )
                        # si tiene avances? entra
                        if avance_max:
                            # el maximo abance que tenga la calificacion
                            if avance_max.tipo_calificacion_id.id == self.tipo_calificacion_id.id:
                                list_acciones_calsificadas.append(i.id)
                    # Acciones Caslificados
                    self.acciones = accion_obj.sudo(self.root).search(
                        [
                            ('plan_tipo', '=', self.plan_tipo),
                            ('id', 'in',list_acciones_calsificadas )
                        ]
                    )
            self.acciones_ids = list(set([accion.id for accion in self.acciones]))

            # Query Hallazgo
            self.hallazgos = hallazgo_obj.sudo(self.root).search([
                                             ('plan_tipo', '=', self.plan_tipo),
                                             ('accion_ids', 'in', self.acciones_ids)
                                           ])
            self.hallazgos_ids = list(set([hallazgo.id for hallazgo in self.hallazgos]))
            self.planes = plan_obj.sudo(self.root).search([
                                      ('tipo', '=', self.plan_tipo),
                                      ('hallazgo_ids', 'in', self.hallazgos_ids)
                                    ])
            # Fin de Consulta
# ***********************************************************
    def style_general(self):
        avance_obj = self.env['plan_mejoramiento.avance']
        titulos = [
            'No.',
            'Código Hallazgo',
            'Descripción hallazgo ',
            'Causa del hallazgo',
            'Efecto del hallazgo',
            'Acción de mejoramiento',
            'Propósito de la Acción de Mejora',
            'Descripción de las Actividades ',
            'Denominación de la Unidad de medida de la Actividad',
            'Cantidad de Medida de la Actividad',
            'Fecha iniciación de la Actividad',
            'Fecha terminación de la Actividad',
            'Plazo en semanas de la Actividad',
            'Área Responsable',
            'No. Actividad',
            'No. MEMORANDO o SOPORTE RECIBIDO EN OCI',
            'ANALISIS DE CUMPLIMIENTO',
            'CUANTIFICACIÓN DE CUMPLIMIENTO Y/O AVANCE',
            'CUALIFICACIÓN DE CUMPLIMIENTO DE LAS METAS',
        ]
        self.workbook = xlwt.Workbook(encoding = 'utf-8')
        self.sheet = self.workbook.add_sheet("Plan de Mejoramiento")

        # add new colour to palette and set RGB colour value
        xlwt.add_palette_colour("gris_titulo", 0x21)
        self.workbook.set_colour_RGB(0x21, 192, 192, 192)

        # posibles bordes: http://bytes.com/topic/python/answers/876543-xlwt-borders-type
        style_titulo = xlwt.easyxf('pattern: pattern solid, fore_colour gris_titulo;'
                                   'font: bold True; align: wrap on, vert centre, horiz center;'
                                    'borders: top thin, bottom thin, left thin, right thin;')
        style_cabecera = xlwt.easyxf('font: bold True; align: wrap on, vert centre, horiz center;')
        style_campo = xlwt.easyxf('font: bold False; align: wrap on, vert centre, horiz center;')

        #Cabecera
        self.sheet.write_merge(0, 0, 0, 18, 'INFORME PRESENTADO A LA CONTRALORIA GENERAL DE LA REPUBLICA',style_cabecera)
        self.sheet.write_merge(1, 1, 0, 18, 'SUSCRIPCIÓN PLANES DE MEJORAMIENTO',style_cabecera)
        self.sheet.write_merge(2, 2, 0, 18, 'FORMULARIO No 14',style_cabecera)

        # Pintar Titulo
        fil = 5
        col = 0
        letras_ancho = 20
        todas_lineas = []
        for texto in titulos:
            parrafo = self.parte_texto(texto, letras_ancho)
            todas_lineas.append(len(parrafo.split('\n')))
            self.sheet.col(col).width = 256 * letras_ancho
            self.sheet.write_merge(fil,fil+1,col,col,parrafo,style_titulo)
            col += 1
        self.sheet.row(fil).height = 900 * int(max(todas_lineas) * 0.7)
        fil += 1

        # Busqueda de objetos
        self.search_date()

        try:
            # Maquetado de datos al archivo
            todas_lineas = {}
            filas_hallazgo = []
            filas_accion = []
            for hallazgo in self.hallazgos:
                if hallazgo.id in self.hallazgos_ids:
                    fil += 1
                    filas_hallazgo.append(fil)
                    todas_lineas[fil] = []
                    col2 = 0
                    self.sheet.write(fil,col2,hallazgo.id,style_campo)
                    col2 += 1
                    texto = self.parte_texto(hallazgo.name, letras_ancho)
                    todas_lineas[fil].append(len(texto.split('\n')))
                    self.sheet.write(fil,col2,texto,style_campo)
                    col2 += 1
                    texto = self.parte_texto(hallazgo.descripcion, letras_ancho)
                    todas_lineas[fil].append(len(texto.split('\n')))
                    self.sheet.write(fil,col2,texto,style_campo)
                    col2 += 1
                    texto = self.parte_texto(hallazgo.causa, letras_ancho)
                    todas_lineas[fil].append(len(texto.split('\n')))
                    self.sheet.write(fil,col2,texto,style_campo)
                    col2 += 1
                    texto = self.parte_texto(hallazgo.efecto, letras_ancho)
                    todas_lineas[fil].append(len(texto.split('\n')))
                    self.sheet.write(fil,col2,texto,style_campo)
                    accion_cont = 0
                    for accion in hallazgo.accion_ids:
                        if accion.id in self.acciones_ids:
                            accion_cont += 1
                            if accion_cont > 1:
                                fil += 1
                                todas_lineas[fil] = []
                                # repetir Hallazgo
                                if not self.agrupar:
                                    filas_hallazgo.append(fil)
                                    todas_lineas[fil] = []
                                    col2 = 0
                                    self.sheet.write(fil,col2,hallazgo.id,style_campo)
                                    col2 += 1
                                    texto = self.parte_texto(hallazgo.name, letras_ancho)
                                    todas_lineas[fil].append(len(texto.split('\n')))
                                    self.sheet.write(fil,col2,texto,style_campo)
                                    col2 += 1
                                    texto = self.parte_texto(hallazgo.descripcion, letras_ancho)
                                    todas_lineas[fil].append(len(texto.split('\n')))
                                    self.sheet.write(fil,col2,texto,style_campo)
                                    col2 += 1
                                    texto = self.parte_texto(hallazgo.causa, letras_ancho)
                                    todas_lineas[fil].append(len(texto.split('\n')))
                                    self.sheet.write(fil,col2,texto,style_campo)
                                    col2 += 1
                                    texto = self.parte_texto(hallazgo.efecto, letras_ancho)
                                    todas_lineas[fil].append(len(texto.split('\n')))
                                    self.sheet.write(fil,col2,texto,style_campo)
                                # fin repetir Hallazgo
                            filas_accion.append(fil)
                            col3 = col2 + 1
                            texto = self.parte_texto(accion.accion_correctiva, letras_ancho)
                            todas_lineas[fil].append(len(texto.split('\n')))
                            self.sheet.write(fil,col3,texto,style_campo)
                            col3 += 1
                            texto = self.parte_texto(accion.objetivo, letras_ancho)
                            todas_lineas[fil].append(len(texto.split('\n')))
                            self.sheet.write(fil,col3,texto,style_campo)
                            col3 += 1
                            texto = self.parte_texto(accion.descripcion, letras_ancho)
                            todas_lineas[fil].append(len(texto.split('\n')))
                            self.sheet.write(fil,col3,texto,style_campo)
                            col3 += 1
                            texto = self.parte_texto(accion.denominacion_medida, letras_ancho)
                            todas_lineas[fil].append(len(texto.split('\n')))
                            self.sheet.write(fil,col3,texto,style_campo)
                            col3 += 1
                            texto = self.parte_texto(accion.unidad_medida, letras_ancho)
                            todas_lineas[fil].append(len(texto.split('\n')))
                            self.sheet.write(fil,col3 ,texto,style_campo)
                            col3 += 1
                            self.sheet.write(fil,col3,accion.fecha_fin,style_campo)
                            col3 += 1
                            self.sheet.write(fil,col3,accion.fecha_fin,style_campo)
                            col3 += 1
                            self.sheet.write(fil,col3,'Plazo?',style_campo)
                            col3 += 1
                            texto = self.parte_texto(accion.dependencia_id.name, letras_ancho)
                            todas_lineas[fil].append(len(texto.split('\n')))
                            self.sheet.write(fil,col3,texto,style_campo)
                            col3 += 1
                            texto = self.parte_texto(accion.name, letras_ancho)
                            todas_lineas[fil].append(len(texto.split('\n')))
                            self.sheet.write(fil,col3,texto,style_campo)
                            col3 += 1
                            self.sheet.write(fil,col3,'?????',style_campo)
                            # avance maximo de la acción
                            avance_max = avance_obj.sudo(self.root).search(
                                [
                                    ('plan_tipo', '=', self.plan_tipo),
                                    ('accion_id', '=', accion.id)
                                ],
                                order='fecha_corte DESC',
                                limit=1,
                            )
                            for avance in accion.avances_ids:
                                if avance.id == avance_max.id:
                                    col4 = col3 + 1
                                    texto = self.parte_texto(avance.descripcion, letras_ancho)
                                    todas_lineas[fil].append(len(texto.split('\n')))
                                    self.sheet.write(fil,col4,texto,style_campo)
                                    col4+=1
                                    self.sheet.write(fil,col4,avance.porcentaje,style_campo)
                                    col4 += 1
                                    self.sheet.write(fil,col4,avance.tipo_calificacion_id.name,style_campo)
            # Ancho de registros
            for fila,lineas in todas_lineas.iteritems():
                self.sheet.row(fila).height = 256 * max(lineas)
            # Unión de celdas hallazgos
            if self.agrupar:
                for col in range(5):
                    i = 0
                    for fila_hallazgo in filas_hallazgo:
                        if filas_hallazgo[-1] != fila_hallazgo:
                            self.sheet.merge(fila_hallazgo,filas_hallazgo[i + 1] - 1,col,col)
                            i += 1
                        else:
                            self.sheet.merge(fila_hallazgo,fil,col,col)
            try:
                imagen = self.env['ir.config_parameter'].get_param('plan_mejoramiento.excel.image_path', default=False)
                self.sheet.insert_bitmap(imagen,0,13, 0, 0,0.4,0.4)
            except Exception as e:
                print 'Hay un problema con el parametro de la imagen para la cabecera del reporte Excel de plan mejoramiento, error: {}'.format(e)
            xlsfile=StringIO.StringIO()
            self.workbook.save(xlsfile)

        except CalledProcessError, e:
            print 'Error {}'.format(e)
            _logger.exception('Error generando archivo .xls')
            _logger.error(e.output)
            message = 'Ocurrio un problema al generar archivo xls.'
            raise exceptions.Warning(message, str(e))

        result = encodestring(xlsfile.getvalue())
        return result

# ***********************************************************
    def style_interno(self):
        titulos = [
            'No.',
            'Fecha',
            'Origen plan de mejoramiento',
            'sub-origen plan de mejoramiento',
            'Proceso origen plan de mejoramiento',
            'Dependencia que formula el plan',
            'Responsable Seguimiento OCI',
            'Memorando OCI con el que se informó el SEGUIMIENTO DE ESTE TRIMESTRE al área',
            'Nombre Oportunidad de Mejora, Hallazgo de Auditoría ó No Conformidad',
            'Descripción Oportunidad de Mejora, Hallazgo de Auditoría ó No Conformidad',
            'Causas',
            'Acción Correctiva o Acción de Mejoramiento',
            'Acción Tipo',
            'Objetivo',
            'Indicador',
            'Meta',
            'Unidad de Medida',
            'Área Responsable',
            'Recursos',
            'Fecha Inicial',
            'Fecha Final',
            'Estado de la Acción',
        ]
        subtitulos=[
            'Descripción Avance',
            'Estado Avance',
            'Calificación Avance',
            '% Avance'
        ]
        self.workbook = xlwt.Workbook(encoding = 'utf-8')
        self.sheet = self.workbook.add_sheet("Plan de Mejoramiento")

        # add new colour to palette and set RGB colour value
        xlwt.add_palette_colour("gris_titulo", 0x21)
        self.workbook.set_colour_RGB(0x21, 192, 192, 192)

        # posibles bordes: http://bytes.com/topic/python/answers/876543-xlwt-borders-type
        style_titulo = xlwt.easyxf('pattern: pattern solid, fore_colour gris_titulo;'
                                   'font: bold True; align: wrap on, vert centre, horiz center;'
                                    'borders: top thin, bottom thin, left thin, right thin;')
        style_cabecera = xlwt.easyxf('font: bold True; align: wrap on, vert centre, horiz center;')
        style_campo = xlwt.easyxf('font: bold False; align: wrap on, vert centre, horiz center;')

        #Cabecera
        self.sheet.write_merge(0, 0, 0, 25, 'INSTITUTO DE DESARROLLO URBANO',style_cabecera)
        self.sheet.write_merge(1, 1, 0, 25, 'PLAN DE MEJORAMIENTO INTERNO Y/O POR PROCESOS',style_cabecera)
        self.sheet.write_merge(2, 2, 0, 25, 'Corte 31/12/2014',style_cabecera)

        # Pintar Titulo
        fil = 5
        col = 0
        letras_ancho = 20
        todas_lineas = []
        for texto in titulos:
            parrafo = self.parte_texto(texto, letras_ancho)
            todas_lineas.append(len(parrafo.split('\n')))
            self.sheet.col(col).width = 256 * letras_ancho
            self.sheet.write_merge(fil,fil+1,col,col,parrafo,style_titulo)
            #sheet.write(fil,col,parrafo,style_titulo)
            col += 1
        self.sheet.row(fil).height = 256 * int(max(todas_lineas) * 0.7)
        self.sheet.row(fil + 1).height = 256 * (max(todas_lineas) - (int(max(todas_lineas) * 0.7)))
        self.sheet.write_merge(fil,fil,col,col+3,'Observaciones y Seguimiento',style_titulo)

        fil += 1
        for subtitulo in subtitulos:
            parrafo = self.parte_texto(subtitulo, letras_ancho)
            todas_lineas.append(len(parrafo.split('\n')))
            self.sheet.col(col).width = 256 * letras_ancho
            self.sheet.write(fil,col,parrafo,style_titulo)
            col += 1

        # Busqueda de objetos
        self.search_date()
        try:
            # Maquetado de datos al archivo
            todas_lineas = {}
            filas_plan = []
            filas_hallazgo = []
            filas_accion = []
            filas_avance = []
            for plan in self.planes:
                fil += 1
                filas_plan.append(fil)
                todas_lineas[fil] = []
                col = 0
                self.sheet.write(fil,col,plan.id,style_campo)
                col+=1
                self.sheet.write(fil,col,plan.fecha_creacion,style_campo)
                col+=1
                texto = self.parte_texto(plan.origen_id.name, letras_ancho)
                todas_lineas[fil].append(len(texto.split('\n')))
                self.sheet.write(fil,col,texto,style_campo)
                col+=1
                texto = self.parte_texto(plan.sub_origen_id.name, letras_ancho)
                todas_lineas[fil].append(len(texto.split('\n')))
                self.sheet.write(fil,col,texto,style_campo)
                col+=1
                texto = self.parte_texto(plan.proceso_id.name, letras_ancho)
                todas_lineas[fil].append(len(texto.split('\n')))
                self.sheet.write(fil,col,texto,style_campo)
                col+=1
                texto = self.parte_texto(plan.dependencia_id.name, letras_ancho)
                todas_lineas[fil].append(len(texto.split('\n')))
                self.sheet.write(fil,col,texto,style_campo)
                col+=1
                texto = self.parte_texto(plan.user_id.login, letras_ancho)
                todas_lineas[fil].append(len(texto.split('\n')))
                self.sheet.write(fil,col,texto,style_campo)
                col+=1
                self.sheet.write(fil,col,plan.radicado_orfeo,style_campo)
                hallazgo_cont = 0
                for hallazgo in plan.hallazgo_ids:
                    if hallazgo.id in self.hallazgos_ids:
                        hallazgo_cont += 1
                        if hallazgo_cont > 1:
                            fil += 1
                            todas_lineas[fil] = []
                            # *** repetir plan ***
                            if not self.agrupar:
                                filas_plan.append(fil)
                                todas_lineas[fil] = []
                                col = 0
                                self.sheet.write(fil,col,plan.id,style_campo)
                                col+=1
                                self.sheet.write(fil,col,plan.fecha_creacion,style_campo)
                                col+=1
                                texto = self.parte_texto(plan.origen_id.name, letras_ancho)
                                todas_lineas[fil].append(len(texto.split('\n')))
                                self.sheet.write(fil,col,texto,style_campo)
                                col+=1
                                texto = self.parte_texto(plan.sub_origen_id.name, letras_ancho)
                                todas_lineas[fil].append(len(texto.split('\n')))
                                self.sheet.write(fil,col,texto,style_campo)
                                col+=1
                                texto = self.parte_texto(plan.proceso_id.name, letras_ancho)
                                todas_lineas[fil].append(len(texto.split('\n')))
                                self.sheet.write(fil,col,texto,style_campo)
                                col+=1
                                texto = self.parte_texto(plan.dependencia_id.name, letras_ancho)
                                todas_lineas[fil].append(len(texto.split('\n')))
                                self.sheet.write(fil,col,texto,style_campo)
                                col+=1
                                texto = self.parte_texto(plan.user_id.login, letras_ancho)
                                todas_lineas[fil].append(len(texto.split('\n')))
                                self.sheet.write(fil,col,texto,style_campo)
                                col+=1
                                self.sheet.write(fil,col,plan.radicado_orfeo,style_campo)
                            # *** fin repetir plan ***
                        filas_hallazgo.append(fil)
                        col2 = col + 1
                        texto = self.parte_texto(hallazgo.name, letras_ancho)
                        todas_lineas[fil].append(len(texto.split('\n')))
                        self.sheet.write(fil,col2,texto,style_campo)
                        col2+=1
                        texto = self.parte_texto(hallazgo.descripcion, letras_ancho)
                        todas_lineas[fil].append(len(texto.split('\n')))
                        self.sheet.write(fil,col2,texto,style_campo)
                        col2+=1
                        texto = self.parte_texto(hallazgo.causa, letras_ancho)
                        todas_lineas[fil].append(len(texto.split('\n')))
                        self.sheet.write(fil,col2,texto,style_campo)
                        accion_cont = 0
                        for accion in hallazgo.accion_ids:
                            if accion.id in self.acciones_ids:
                                accion_cont += 1
                                if accion_cont > 1:
                                    fil += 1
                                    todas_lineas[fil] = []
                                    # *** repetir plan ***
                                    if not self.agrupar:
                                        filas_plan.append(fil)
                                        todas_lineas[fil] = []
                                        col = 0
                                        self.sheet.write(fil,col,plan.id,style_campo)
                                        col+=1
                                        self.sheet.write(fil,col,plan.fecha_creacion,style_campo)
                                        col+=1
                                        texto = self.parte_texto(plan.origen_id.name, letras_ancho)
                                        todas_lineas[fil].append(len(texto.split('\n')))
                                        self.sheet.write(fil,col,texto,style_campo)
                                        col+=1
                                        texto = self.parte_texto(plan.sub_origen_id.name, letras_ancho)
                                        todas_lineas[fil].append(len(texto.split('\n')))
                                        self.sheet.write(fil,col,texto,style_campo)
                                        col+=1
                                        texto = self.parte_texto(plan.proceso_id.name, letras_ancho)
                                        todas_lineas[fil].append(len(texto.split('\n')))
                                        self.sheet.write(fil,col,texto,style_campo)
                                        col+=1
                                        texto = self.parte_texto(plan.dependencia_id.name, letras_ancho)
                                        todas_lineas[fil].append(len(texto.split('\n')))
                                        self.sheet.write(fil,col,texto,style_campo)
                                        col+=1
                                        texto = self.parte_texto(plan.user_id.login, letras_ancho)
                                        todas_lineas[fil].append(len(texto.split('\n')))
                                        self.sheet.write(fil,col,texto,style_campo)
                                        col+=1
                                        self.sheet.write(fil,col,plan.radicado_orfeo,style_campo)
                                    # *** fin repetir plan ***
                                    # *** repetir Hallazgo ***
                                        filas_hallazgo.append(fil)
                                        col2 = col + 1
                                        texto = self.parte_texto(hallazgo.name, letras_ancho)
                                        todas_lineas[fil].append(len(texto.split('\n')))
                                        self.sheet.write(fil,col2,texto,style_campo)
                                        col2+=1
                                        texto = self.parte_texto(hallazgo.descripcion, letras_ancho)
                                        todas_lineas[fil].append(len(texto.split('\n')))
                                        self.sheet.write(fil,col2,texto,style_campo)
                                        col2+=1
                                        texto = self.parte_texto(hallazgo.causa, letras_ancho)
                                        todas_lineas[fil].append(len(texto.split('\n')))
                                        self.sheet.write(fil,col2,texto,style_campo)
                                    # *** fin repetir Hallazgo ***
                                filas_accion.append(fil)
                                col3 = col2 + 1
                                texto = self.parte_texto(accion.accion_correctiva, letras_ancho)
                                todas_lineas[fil].append(len(texto.split('\n')))
                                self.sheet.write(fil,col3,texto,style_campo)
                                col3+=1
                                texto = self.parte_texto(accion.accion_tipo, letras_ancho)
                                todas_lineas[fil].append(len(texto.split('\n')))
                                self.sheet.write(fil,col3,texto,style_campo)
                                col3+=1
                                texto = self.parte_texto(accion.objetivo, letras_ancho)
                                todas_lineas[fil].append(len(texto.split('\n')))
                                self.sheet.write(fil,col3,texto,style_campo)
                                col3+=1
                                texto = self.parte_texto(accion.indicador, letras_ancho)
                                todas_lineas[fil].append(len(texto.split('\n')))
                                self.sheet.write(fil,col3,texto,style_campo)
                                col3+=1
                                texto = self.parte_texto(accion.meta, letras_ancho)
                                todas_lineas[fil].append(len(texto.split('\n')))
                                self.sheet.write(fil,col3,texto,style_campo)
                                col3+=1
                                self.sheet.write(fil,col3,accion.unidad_medida,style_campo)
                                col3+=1
                                texto = self.parte_texto(accion.dependencia_id.name, letras_ancho)
                                todas_lineas[fil].append(len(texto.split('\n')))
                                self.sheet.write(fil,col3,texto,style_campo)
                                col3+=1
                                texto = self.parte_texto(accion.recurso, letras_ancho)
                                todas_lineas[fil].append(len(texto.split('\n')))
                                self.sheet.write(fil,col3,texto,style_campo)
                                col3+=1
                                self.sheet.write(fil,col3,accion.fecha_inicio,style_campo)
                                col3+=1
                                self.sheet.write(fil,col3,accion.fecha_fin,style_campo)
                                col3+=1
                                self.sheet.write(fil,col3,accion.state,style_campo)
                                avance_cont = 0
                                for avance in accion.avances_ids:
                                    #if avance.id in avances_ids:
                                    avance_cont += 1
                                    if avance_cont > 1:
                                        fil += 1
                                        todas_lineas[fil] = []
                                        # *** repetir plan ***
                                        if not self.agrupar:
                                            filas_plan.append(fil)
                                            todas_lineas[fil] = []
                                            col = 0
                                            self.sheet.write(fil,col,plan.id,style_campo)
                                            col+=1
                                            self.sheet.write(fil,col,plan.fecha_creacion,style_campo)
                                            col+=1
                                            texto = self.parte_texto(plan.origen_id.name, letras_ancho)
                                            todas_lineas[fil].append(len(texto.split('\n')))
                                            self.sheet.write(fil,col,texto,style_campo)
                                            col+=1
                                            texto = self.parte_texto(plan.sub_origen_id.name, letras_ancho)
                                            todas_lineas[fil].append(len(texto.split('\n')))
                                            self.sheet.write(fil,col,texto,style_campo)
                                            col+=1
                                            texto = self.parte_texto(plan.proceso_id.name, letras_ancho)
                                            todas_lineas[fil].append(len(texto.split('\n')))
                                            self.sheet.write(fil,col,texto,style_campo)
                                            col+=1
                                            texto = self.parte_texto(plan.dependencia_id.name, letras_ancho)
                                            todas_lineas[fil].append(len(texto.split('\n')))
                                            self.sheet.write(fil,col,texto,style_campo)
                                            col+=1
                                            texto = self.parte_texto(plan.user_id.login, letras_ancho)
                                            todas_lineas[fil].append(len(texto.split('\n')))
                                            self.sheet.write(fil,col,texto,style_campo)
                                            col+=1
                                            self.sheet.write(fil,col,plan.radicado_orfeo,style_campo)
                                        # *** fin repetir plan ***
                                        # *** repetir Hallazgo ***
                                            filas_hallazgo.append(fil)
                                            col2 = col + 1
                                            texto = self.parte_texto(hallazgo.name, letras_ancho)
                                            todas_lineas[fil].append(len(texto.split('\n')))
                                            self.sheet.write(fil,col2,texto,style_campo)
                                            col2+=1
                                            texto = self.parte_texto(hallazgo.descripcion, letras_ancho)
                                            todas_lineas[fil].append(len(texto.split('\n')))
                                            self.sheet.write(fil,col2,texto,style_campo)
                                            col2+=1
                                            texto = self.parte_texto(hallazgo.causa, letras_ancho)
                                            todas_lineas[fil].append(len(texto.split('\n')))
                                            self.sheet.write(fil,col2,texto,style_campo)
                                        # *** fin repetir Hallazgo ***
                                        # *** repetir Acciones ***
                                            filas_accion.append(fil)
                                            col3 = col2 + 1
                                            texto = self.parte_texto(accion.accion_correctiva, letras_ancho)
                                            todas_lineas[fil].append(len(texto.split('\n')))
                                            self.sheet.write(fil,col3,texto,style_campo)
                                            col3+=1
                                            texto = self.parte_texto(accion.accion_tipo, letras_ancho)
                                            todas_lineas[fil].append(len(texto.split('\n')))
                                            self.sheet.write(fil,col3,texto,style_campo)
                                            col3+=1
                                            texto = self.parte_texto(accion.objetivo, letras_ancho)
                                            todas_lineas[fil].append(len(texto.split('\n')))
                                            self.sheet.write(fil,col3,texto,style_campo)
                                            col3+=1
                                            texto = self.parte_texto(accion.indicador, letras_ancho)
                                            todas_lineas[fil].append(len(texto.split('\n')))
                                            self.sheet.write(fil,col3,texto,style_campo)
                                            col3+=1
                                            texto = self.parte_texto(accion.meta, letras_ancho)
                                            todas_lineas[fil].append(len(texto.split('\n')))
                                            self.sheet.write(fil,col3,texto,style_campo)
                                            col3+=1
                                            self.sheet.write(fil,col3,accion.unidad_medida,style_campo)
                                            col3+=1
                                            texto = self.parte_texto(accion.dependencia_id.name, letras_ancho)
                                            todas_lineas[fil].append(len(texto.split('\n')))
                                            self.sheet.write(fil,col3,texto,style_campo)
                                            col3+=1
                                            texto = self.parte_texto(accion.recurso, letras_ancho)
                                            todas_lineas[fil].append(len(texto.split('\n')))
                                            self.sheet.write(fil,col3,texto,style_campo)
                                            col3+=1
                                            self.sheet.write(fil,col3,accion.fecha_inicio,style_campo)
                                            col3+=1
                                            self.sheet.write(fil,col3,accion.fecha_fin,style_campo)
                                            col3+=1
                                            self.sheet.write(fil,col3,accion.state,style_campo)
                                        # *** fin repetir Hallazgo ***
                                    filas_avance.append(fil)
                                    col4 = col3 + 1
                                    texto = self.parte_texto(avance.descripcion, letras_ancho)
                                    todas_lineas[fil].append(len(texto.split('\n')))
                                    self.sheet.write(fil,col4,texto,style_campo)
                                    col4+=1
                                    self.sheet.write(fil,col4,avance.state,style_campo)
                                    col4+=1
                                    texto = self.parte_texto(avance.tipo_calificacion_id.name, letras_ancho)
                                    todas_lineas[fil].append(len(texto.split('\n')))
                                    self.sheet.write(fil,col4,texto,style_campo)
                                    col4+=1
                                    self.sheet.write(fil,col4,avance.porcentaje,style_campo)
            # Ancho de registros
            for fila,lineas in todas_lineas.iteritems():
                self.sheet.row(fila).height = 256 * max(lineas)

            # Unión de celdas
            if self.agrupar:
                for col in range(8):
                    i = 0
                    for fila_plan in filas_plan:
                        if filas_plan[len(filas_plan) - 1] != fila_plan:
                            self.sheet.merge(fila_plan,filas_plan[i + 1] - 1,col,col)
                            i += 1
                        else:
                            self.sheet.merge(fila_plan,fil,col,col)
                for col in range(8, 11):
                    i = 0
                    for fila_hallazgo in filas_hallazgo:
                        if filas_hallazgo[len(filas_hallazgo) -1] != fila_hallazgo:
                            self.sheet.merge(fila_hallazgo,filas_hallazgo[i + 1] - 1,col,col)
                            i += 1
                        else:
                            self.sheet.merge(fila_hallazgo,fil,col,col)
                for col in range(11, 22):
                    i = 0
                    for fila_accion in filas_accion:
                        if filas_accion[len(filas_accion) -1] != fila_accion:
                            self.sheet.merge(fila_accion,filas_accion[i + 1] - 1,col,col)
                            i += 1
                        else:
                            self.sheet.merge(fila_accion,fil,col,col)
            # Guardar cambios en los archivos
            xlsfile=StringIO.StringIO()
            self.workbook.save(xlsfile)

        except CalledProcessError, e:
            print 'Error {}'.format(e)
            _logger.exception('Error generando archivo .xls')
            _logger.error(e.output)
            message = 'Ocurrio un problema al generar archivo xls.'
            raise exceptions.Warning(message, str(e))

        result = encodestring(xlsfile.getvalue())
        return result

    def style_bogota(self):
        avance_obj = self.env['plan_mejoramiento.avance']
        titulos = [
           'LINEA DE AUDITORIA',
           'NUMERO Y DESCRIPCION DEL HALLAZGO',
           'ACCIONES CORRECTIVAS',
           'INDICADORES',
           'META',
           'ÁREA RESPONSABLE',
           'RESPONSABLES DE LA EJECUCIÓN',
           'RECURSOS',
        ]
        subtitulos = [
            'INICIO',
            'FINALIZACIÓN',
        ]
        titulos2 = [
            'RESULTADO DEL INDICADOR CONTRALORÍA',
            'RESULTADO DEL SEGUIMIENTO ENTIDAD',
        ]
        subtitulos2 = [
            'CALIFICACIÓN',
            '% DE AVANCE',
        ]

        self.workbook = xlwt.Workbook(encoding = 'utf-8')
        self.sheet = self.workbook.add_sheet("Contraloría Distrital", cell_overwrite_ok=True)
        #worksheet = workbook.add_sheet("Sheet 1", cell_overwrite_ok=True)

        # add new colour to palette and set RGB colour value
        xlwt.add_palette_colour("amarillo_titulo", 0x21)
        self.workbook.set_colour_RGB(0x21, 255, 255, 0)#FFFF00

        # posibles bordes: http://bytes.com/topic/python/answers/876543-xlwt-borders-type
        style_titulo = xlwt.easyxf('pattern: pattern solid, fore_colour amarillo_titulo;'
                                   'font: bold True; align: wrap on, vert centre, horiz center;'
                                    'borders: top thin, bottom thin, left thin, right thin;')
        style_cabecera = xlwt.easyxf('font: bold True; align: wrap on, vert centre, horiz center;')
        style_campo = xlwt.easyxf('font: bold False; align: wrap on, vert centre, horiz center;')

        fil = 5
        col = 0
        letras_ancho = 20
        todas_lineas = []
        for texto in titulos:
            parrafo = self.parte_texto(texto, letras_ancho)
            todas_lineas.append(len(parrafo.split('\n')))
            self.sheet.col(col).width = 256 * letras_ancho
            self.sheet.write_merge(fil,fil+1,col,col,parrafo,style_titulo)
            #self.sheet.write(fil,col,parrafo,style_titulo)
            col += 1
        self.sheet.row(fil).height = 256 * int(max(todas_lineas) * 0.7)
        self.sheet.row(fil + 1).height = 256 * (max(todas_lineas) - (int(max(todas_lineas) * 0.7)))
        self.sheet.write_merge(fil,fil,col,col+1,'FECHA',style_titulo)

        fil += 1
        for subtitulo in subtitulos:
            parrafo = self.parte_texto(subtitulo, letras_ancho)
            todas_lineas.append(len(parrafo.split('\n')))
            self.sheet.col(col).width = 256 * letras_ancho
            self.sheet.write(fil,col,parrafo,style_titulo)
            col += 1

        fil -= 1
        letras_ancho = 20
        todas_lineas = []
        for texto in titulos2:
            parrafo = self.parte_texto(texto, letras_ancho)
            todas_lineas.append(len(parrafo.split('\n')))
            self.sheet.col(col).width = 256 * letras_ancho
            self.sheet.write_merge(fil,fil+1,col,col,parrafo,style_titulo)
            #self.sheet.write(fil,col,parrafo,style_titulo)
            col += 1
        self.sheet.row(fil).height = 256 * int(max(todas_lineas) * 0.7)
        self.sheet.row(fil + 1).height = 256 * (max(todas_lineas) - (int(max(todas_lineas) * 0.7)))
        self.sheet.write_merge(fil,fil,col,col+1,'AVANCE ACCIONES DE MEJORAMIENTO',style_titulo)

        #Cabecera
        self.sheet.write_merge(0, 0, 0, 13, 'INSTITUTO DE DESARROLLO URBANO',style_cabecera)
        self.sheet.write_merge(1, 1, 0, 13, 'PLAN DE MEJORAMIENTO CONTRALORÍA DISTRITAL',style_cabecera)
        self.sheet.write_merge(2, 2, 0, 13, 'Corte 31/12/2014',style_cabecera)

        # Pintar Titulo
        fil += 1
        for subtitulo in subtitulos2:
            parrafo = self.parte_texto(subtitulo, letras_ancho)
            todas_lineas.append(len(parrafo.split('\n')))
            self.sheet.col(col).width = 256 * letras_ancho
            self.sheet.write(fil,col,parrafo,style_titulo)
            col += 1
        # Busqueda de objetos
        self.search_date()

        try:
            # Maquetado de datos al archivo
            todas_lineas = {}
            filas_plan = []
            filas_hallazgo = []
            filas_accion = []
            for plan in self.planes:
                fil += 1
                filas_plan.append(fil)
                col = 0
                self.sheet.write_merge(fil,fil,col,col+13,plan.name,style_campo)
                for hallazgo in plan.hallazgo_ids:
                    if hallazgo.id in self.hallazgos_ids:
                        fil += 1
                        filas_hallazgo.append(fil)
                        todas_lineas[fil] = []
                        col2 = col
                        texto = self.parte_texto(hallazgo.name, letras_ancho)
                        todas_lineas[fil].append(len(texto.split('\n')))
                        self.sheet.write(fil,col2,texto,style_campo)
                        col2 += 1
                        texto = self.parte_texto(hallazgo.descripcion, letras_ancho)
                        todas_lineas[fil].append(len(texto.split('\n')))
                        self.sheet.write(fil,col2,texto,style_campo)
                        accion_cont = 0
                        for accion in hallazgo.accion_ids:
                            if accion.id in self.acciones_ids:
                                accion_cont += 1
                                if accion_cont > 1:
                                    fil += 1
                                    todas_lineas[fil] = []
                                    # *** repetir hallazgo ***
                                    if not self.agrupar:
                                        filas_hallazgo.append(fil)
                                        todas_lineas[fil] = []
                                        col2 = col
                                        texto = self.parte_texto(hallazgo.name, letras_ancho)
                                        todas_lineas[fil].append(len(texto.split('\n')))
                                        self.sheet.write(fil,col2,texto,style_campo)
                                        col2 += 1
                                        texto = self.parte_texto(hallazgo.descripcion, letras_ancho)
                                        todas_lineas[fil].append(len(texto.split('\n')))
                                        self.sheet.write(fil,col2,texto,style_campo)
                                    # *** Fin repetir hallazgo ***
                                filas_accion.append(fil)
                                col3 = col2 + 1
                                texto = self.parte_texto(accion.accion_correctiva, letras_ancho)
                                todas_lineas[fil].append(len(texto.split('\n')))
                                self.sheet.write(fil,col3,texto,style_campo)
                                col3 += 1
                                texto = self.parte_texto(accion.indicador, letras_ancho)
                                todas_lineas[fil].append(len(texto.split('\n')))
                                self.sheet.write(fil,col3,texto,style_campo)
                                col3 += 1
                                texto = self.parte_texto(accion.meta, letras_ancho)
                                todas_lineas[fil].append(len(texto.split('\n')))
                                self.sheet.write(fil,col3,texto,style_campo)
                                col3 += 1
                                texto = self.parte_texto(accion.dependencia_id.name, letras_ancho)
                                todas_lineas[fil].append(len(texto.split('\n')))
                                self.sheet.write(fil,col3,texto,style_campo)
                                col3 += 1
                                texto = self.parte_texto(accion.ejecutor_id.login, letras_ancho)
                                todas_lineas[fil].append(len(texto.split('\n')))
                                self.sheet.write(fil,col3 ,texto,style_campo)
                                col3 += 1
                                texto = self.parte_texto(accion.recurso, letras_ancho)
                                todas_lineas[fil].append(len(texto.split('\n')))
                                self.sheet.write(fil,col3,texto,style_campo)
                                col3 += 1
                                self.sheet.write(fil,col3,accion.fecha_inicio,style_campo)
                                col3 += 1
                                self.sheet.write(fil,col3,accion.fecha_fin,style_campo)
                                # avance maximo de la acción
                                avance_max = avance_obj.sudo(self.root).search(
                                    [
                                        ('plan_tipo', '=', self.plan_tipo),
                                        ('accion_id', '=', accion.id)
                                    ],
                                    order='fecha_corte DESC',
                                    limit=1,
                                )
                                for avance in accion.avances_ids:
                                    if avance.id == avance_max.id:
                                        col4 = col3 + 1
                                        self.sheet.write(fil,col4,avance.porcentaje,style_campo)
                                        col4+=1
                                        texto = self.parte_texto(avance.descripcion, letras_ancho)
                                        todas_lineas[fil].append(len(texto.split('\n')))
                                        self.sheet.write(fil,col4,texto,style_campo)
                                        col4 += 1
                                        self.sheet.write(fil,col4,avance.tipo_calificacion_id.name,style_campo)
                                        col4 += 1
                                        self.sheet.write(fil,col4,avance.porcentaje,style_campo)
            # Ancho de registros
            for fila,lineas in todas_lineas.iteritems():
                self.sheet.row(fila).height = 256 * max(lineas)
            # Unión de celdas hallazgos
            if self.agrupar:
                for col in range(2):
                    i = 0
                    for fila_hallazgo in filas_hallazgo:
                        if filas_hallazgo[-1] != fila_hallazgo:
                            self.sheet.merge(fila_hallazgo,filas_hallazgo[i + 1] - 2,col,col)
                            i += 1
                        else:
                            self.sheet.merge(fila_hallazgo,fil,col,col)
            try:
                imagen = self.env['ir.config_parameter'].get_param('plan_mejoramiento.excel.image_path', default=False)
                self.sheet.insert_bitmap(imagen,0,13, 0, 0,0.4,0.4)
            except Exception as e:
                print 'Hay un problema con el parametro de la imagen para la cabecera del reporte Excel de plan mejoramiento, error: {}'.format(e)
            xlsfile=StringIO.StringIO()
            self.workbook.save(xlsfile)

        except CalledProcessError, e:
            print 'Error {}'.format(e)
            _logger.exception('Error generando archivo .xls')
            _logger.error(e.output)
            message = 'Ocurrio un problema al generar archivo xls.'
            raise exceptions.Warning(message, str(e))

        result = encodestring(xlsfile.getvalue())
        return result
