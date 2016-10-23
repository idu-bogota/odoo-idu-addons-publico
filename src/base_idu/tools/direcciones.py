# -*- coding: utf-8 -*-
import urllib
import math
from pyproj import Proj
from pyproj import transform
import re, json
import logging
_logger = logging.getLogger(__name__)

def geocodificar(direccion, srid, uri = '', zone = 1100100, url_2 = ''): #Default = Bogota
    """
    Geolocalización utilizando el servicio disponible en el SIGIDU
    Parameters :
    direccion = Dirección a geo codificar
    srid = Spatial Reference System ID. in this format ie "epsg:4326" or "other.extra:900913"
    uri = Dirección del servicio web del SIGIDU, for idu = http://gi03cc01/ArcGIS/rest/services/GeocodeIDU/GeocodeServer/findAddressCandidates?
    zone = Código de la ciudad - Bogota = 1100100
    REST POST Example http://gi03cc01/ArcGIS/rest/services/GeocodeIDU/GeocodeServer/findAddressCandidates?Street=cra+82+a+6+37&Zone=Bogot%C3%A1+D.C.&outFields=&outSR=&f=html
    ejemplo=http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?singleLine=cl+89+b+116+A+30,Bogota,colombia&outFields=City,Country&maxLocations=1&f=pjson
    """
    #return '{"type":"Point","coordinates":[-8246435.141098299995065,512561.201248599973042]}';
    punto_encontrado = False
    try:
        direccion = direccion.encode('utf8')
        if punto_encontrado == False:
            if not url_2:
                raise Warning('Por favor configure el parametro de sistema llamado pqrs.esri_geocodificador_url.')
            url_2 = "{}singleLine={},Bogota,colombia&outFields=City,Country&maxLocations=1&f=pjson".format(url_2, direccion)
            _logger.info("URL: {0}".format(url_2))
            jsonstr = urllib.urlopen(url_2).read()
            vals = json.loads(jsonstr)
            if (len(vals) >= 2):
                candidates = vals['candidates']
                _logger.info("candidates: {0}".format(candidates))
                for candidate in candidates :
                    if candidate['address'] != 'Bogotá, D.C.':
                        location = candidate['location']
                        x = location['x']
                        y = location['y']
                        punto = {
                            'type': "Point",
                            'coordinates': [x, y]
                        }
                        punto_encontrado = True
                        return punto
    except Exception as e:
        _logger.error(str(e))
        return False

    try:
        direccion = direccion.encode('utf8')
        url = "{0}Street={1}&Zone={2}&outSR={3}&f=pjson".format(uri, direccion, zone, 4326) #Convertir las coordenadas a geográficas
        _logger.info("URL: {0}".format(url))
        jsonstr = urllib.urlopen(url).read()
        vals = json.loads(jsonstr)
        if (len(vals) >= 2):
            candidates = vals['candidates']
            if candidates:
                _logger.info("candidates: {0}".format(candidates))
                for candidate in candidates :
                    location = candidate['location']
                    x = location['x']
                    y = location['y']
                    punto = {
                        'type': "Point",
                        'coordinates': [x, y]
                    }
                    return punto
    except Exception as e:
        _logger.error(str(e))
        return False
    return False

def es_formato_valido_bogota(address):
    """ This function checks if the parameter fits Bogotá D.C. address schema.

    >>> print es_formato_valido_bogota('KR 102 10 30')
    True
    >>> print es_formato_valido_bogota('KR 102 10 30 INT 2 AP 1023')
    True
    >>> print es_formato_valido_bogota('KR 102 10 30 INT 2')
    True
    >>> print es_formato_valido_bogota('KR 102 10 30 AP 1123')
    True
    >>> print es_formato_valido_bogota('KR 102 A 10 A 30')
    True
    >>> print es_formato_valido_bogota('KR 102 A 10 A 30 INT 3 AP 12')
    True
    >>> print es_formato_valido_bogota('KR 102 A 10 A BIS 30')
    True
    >>> print es_formato_valido_bogota('KR 102 A 10 A BIS Z 30')
    True
    >>> print es_formato_valido_bogota('KR 102 BIS 10 30')
    True
    >>> print es_formato_valido_bogota('KR 102 BIS 10 30 AP 12')
    True
    >>> print es_formato_valido_bogota('KR 102 BIS 10 A 30')
    True
    >>> print es_formato_valido_bogota('KR 102 BIS 10 BIS 30')
    True
    >>> print es_formato_valido_bogota('KR 102 BIS 10 BIS Z 30')
    True
    >>> print es_formato_valido_bogota('KR 102 BIS 10 A BIS 30')
    True
    >>> print es_formato_valido_bogota('KR 102 BIS 10 A BIS Z 30')
    True
    >>> print es_formato_valido_bogota('KR 102 BIS 10 A BIS Z 30 INT 3 LOC 4')
    True
    >>> print es_formato_valido_bogota('KR 102 BIS A 10 30')
    True
    >>> print es_formato_valido_bogota('KR 102 BIS A 10 30 E')
    True
    >>> print es_formato_valido_bogota('KR 102 BIS A 10 A 30')
    True
    >>> print es_formato_valido_bogota('KR 102 BIS A 10 A BIS 30')
    True
    >>> print es_formato_valido_bogota('KR 102 BIS A 10 A BIS A 30')
    True
    >>> print es_formato_valido_bogota('KR 102 BIS A 10 A BIS A 30 LOC 5')
    True
    >>> print es_formato_valido_bogota('KR 102 BIS A 10 BIS Z 30')
    True
    >>> print es_formato_valido_bogota('KR 102 A BIS 10 30')
    True
    >>> print es_formato_valido_bogota('KR 102 A BIS 10 A 30')
    True
    >>> print es_formato_valido_bogota('KR 102 A BIS 10 A BIS 30')
    True
    >>> print es_formato_valido_bogota('KR 102 A BIS 10 A BIS A 30')
    True
    >>> print es_formato_valido_bogota('KR 102 A BIS 10 BIS Z 30')
    True
    >>> print es_formato_valido_bogota('KR 102 A BIS Z 10 30')
    True
    >>> print es_formato_valido_bogota('KR 102 A BIS Z 10 30 SE')
    True
    >>> print es_formato_valido_bogota('KR 102 A BIS Z 10 A 30')
    True
    >>> print es_formato_valido_bogota('KR 102 A BIS Z 10 A BIS 30')
    True
    >>> print es_formato_valido_bogota('KR 102 A BIS Z 10 A BIS A 30')
    True
    >>> print es_formato_valido_bogota('KR 102 A BIS Z 10 BIS Z 30')
    True
    >>> print es_formato_valido_bogota('KR 102 A BIS Z 10 BIS Z 30 N')
    True
    >>> print es_formato_valido_bogota('TV 34 F 45 B BIS Z 32 MZ 32 INT 5 TO 23 AP 123 S')
    True
    >>> print es_formato_valido_bogota('CL 22 A 52 07 TO C AP 1102')
    True
    """
    st_type = '(CL|AC|DG|KR|AK|TV|CA|CT|PS|KM|VRD|CGMT)'
    st_number = '[0-9]+'
    st_suffix = '(\s[A-Z])?((\sBIS)|(\sBIS\s[A-Z]))?'
    st_horizontal = '(\s(AP|OF|CON|PEN|LOC|DEP|GJ|P)\s[0-9]+)?'
    st_interior = '(\s((INT|BQ|TO|CA|BG|EN|SO)\s[0-9A-Z]+))?'
    st_manzana = '(\s((MZ|LO|ET|SM)\s[A-Z0-9]+))?'
    st_sector = '(\s(N|E|S|O|NE|SE|SO|NO))?'
    regex = "^{0}\s{1}{2}\s{1}{2}\s{1}{5}{6}{6}{3}{3}{4}(\s[A-Z])?{5}$".format(st_type, st_number, st_suffix, st_interior, st_horizontal, st_sector, st_manzana);
    #print regex
    if re.match(regex, address) != None:
        return True
    else:
        return False

def extraer_datos_basicos(address):
    """
    Si la dirección sigue el formato del IDU ej. CL 22 A 52 07 TO C AP 1102, entonces se remueve datos como torre, apto, etc
    """
    st_type = '(CL|AC|DG|KR|AK|TV|CA|CT|PS|KM|VRD|CGMT)'
    st_number = '[0-9]+'
    st_suffix = '(\s[A-Z])?((\sBIS)|(\sBIS\s[A-Z]))?'
    st_horizontal = '(\s(AP|OF|CON|PEN|LOC|DEP|GJ|P)\s[0-9]+)?'
    st_interior = '(\s((INT|BQ|TO|CA|BG|EN|SO)\s[0-9A-Z]+))?'
    st_manzana = '(\s((MZ|LO|ET|SM)\s[A-Z0-9]+))?'
    st_sector = '(\s(N|E|S|O|NE|SE|SO|NO))?'
    regex = "^({0}\s{1}{2}\s{1}{2}\s{1}{5}).*$".format(st_type, st_number, st_suffix, st_interior, st_horizontal, st_sector, st_manzana);
    #print regex
    result = re.search(regex, address)
    if re.search(regex, address):
        return result.group(1)
    return address


if __name__ == "__main__":
    import doctest
    doctest.testmod()
