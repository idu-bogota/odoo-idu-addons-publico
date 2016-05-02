#!/usr/bin/jython
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

import csv
import json
from metamodel import Task

from optparse import OptionParser
import logging
logging.basicConfig()
_logger = logging.getLogger(__name__)

def main():
    usage = "Takes a MPP and creates a CSV file:\njython -Dpython.path=javalib/mpxj.jar:javalib/poi-3.11-20141221.jar:javalib/rtfparserkit-1.1.0.jar %prog -f file.mpp"
    parser = OptionParser(usage)
    parser.add_option("-f", "--filename", dest="filename", help="MPP file")
    parser.add_option("-o", "--output", dest="output", help="CSV file")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Display debug message", default=False)

    (options, args) = parser.parse_args()
    _logger.setLevel(0)
    if options.debug:
        _logger.setLevel(10)
    if not options.filename:
        parser.error('Indique el archivo .mpp a importar')

    import net.sf.mpxj.mpp.MPPReader
    reader = net.sf.mpxj.mpp.MPPReader()
    file = reader.read(options.filename)
    for task in file.getChildTasks():
        task_process(task, {})

    f = open(options.output, 'wt')
    try:
        writer = csv.writer(f)
        writer.writerow( ('guid', 'outline_number', 'name', 'is_leaf', 'duration', 'date_start', 'date_end', 'actual_duration', 'actual_date_start', 'actual_date_end', 'percentage', 'cost', 'actual_cost', 'parent_id', 'predecesor', 'resources') )
        for t in Task.index_list:
            writer.writerow((
                t.guid, t.outline_number, t.name, t.is_leaf, t.duration, t.date_start, t.date_end, t.actual_duration, t.actual_date_start, t.actual_date_end,
                t.percentage, t.cost, t.actual_cost, t.parent_id,
                json.dumps(t.predecesor),
                json.dumps(t.resources),
            ))
    finally:
        f.close()

def task_process(task, params):
    Task(task, params)
    for i in task.getChildTasks():
        task_process(i, params)


if __name__ == '__main__':
    main()