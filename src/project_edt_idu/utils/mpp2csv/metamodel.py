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

import java.text.SimpleDateFormat as SimpleDateFormat
import java.util.TimeZone as TimeZone

class Task(object):
    index_list = []
    def __init__(self, task, params):
        self.guid = task.getGUID().toString()
        Task.index_list.append(self)
        self.mpp_task = task
        self.name = task.getName().replace("'","").replace('"','')
        self.duration = task.getDuration()
        self.actual_duration = task.getActualDuration()
        self.percentage = task.getPercentageComplete()
        self.cost = task.getCost()
        self.actual_cost = task.getActualCost()
        self.parent_id = False
        if task.getParentTask():
            self.parent_id = task.getParentTask().getGUID().toString()
        self.outline_number = task.getOutlineNumber()
        self.is_leaf = len(task.getChildTasks()) == 0
        self.date_start = date_as_string(task.getStart().getTime())
        self.date_end = date_as_string(task.getFinish().getTime())
        if task.getActualStart():
            self.actual_date_start = date_as_string(task.getActualStart().getTime())
        else:
            self.actual_date_start = self.date_start

        if task.getActualFinish():
            self.actual_date_end = date_as_string(task.getActualFinish().getTime())
        else:
            self.actual_date_end = ''
        predecesores_lista = []
        predecesores = task.getPredecessors()
        if predecesores:
            for predecesor in predecesores:
                predecesor_id = predecesor.getSourceTask().getGUID().toString()
                predecesores_lista.append({'guid': predecesor_id, 'tipo': predecesor.getType().toString()})
        self.predecesor = predecesores_lista
        self.resources = []
        assignments = task.getResourceAssignments()
        for assignment in assignments:
            resource = assignment.getResource()
            if not resource:
                continue
            tipo = resource.getGroup()
            if tipo:
                tipo = tipo.strip().lower()
            email = resource.getEmailAddress() or resource.getName()
            if email:
                email = email.strip().lower()
            self.resources.append({
                'tipo': tipo,
                'email': email,
            })

    def export(self):
        print "{0} - {1}% [{2}]".format(self.name, self.percentage, self.guid)

    def __getattribute__(self, name):
        value = object.__getattribute__(self, name)
        if isinstance(value, basestring):
            return output_utf8(value)
        return value

def date_as_string(date):
    tz = TimeZone.getTimeZone("UTC")
    df = SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
    df.setTimeZone(tz)
    return df.format(date)

def output_utf8(word):
    #return word
    output = unicode(word).encode('utf8')
    return output
