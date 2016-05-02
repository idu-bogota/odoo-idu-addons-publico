plan_m = model('plan_mejoramiento.plan')
hallazgo_m = model('plan_mejoramiento.hallazgo')
accion_m = model('plan_mejoramiento.accion')
avance_m = model('plan_mejoramiento.avance')
edt_m = model('project.edt')
project_m = model('project.project')

###################
# Avance
###################

record_model = avance_m
record_ids = avance_m.search([])
for record_id in record_ids:
    record = record_model.get(record_id).unlink()

###################
# Accion
###################

record_model = accion_m
record_ids = record_model.search([])
for record_id in record_ids:
    record = record_model.get(record_id)
    record.unlink()

###################
# Hallazgo
###################

record_model = hallazgo_m
record_ids = record_model.search([])
for record_id in record_ids:
    record = record_model.get(record_id)
    record.unlink()

###################
# Plan
###################

record_model = plan_m
record_ids = record_model.search([])
for record_id in record_ids:
    record = record_model.browse(record_id)
    record.unlink()

record_model = project_m
record_ids = record_model.search(['proyecto_tipo = "plan_mejoramiento"'])
edt_ids = []
for record_id in record_ids:
    record = record_model.browse(record_id)
    edt_id = record.edt_raiz_id.id
    edt_ids += edt_m.search([('id','child_of',edt_id)])
    record.active = False

try:
    edt_m.unlink(edt_ids)
except:
    pass

seq = model('ir.sequence').browse(['name = "name_accion.secuencia"'])
seq.write({'number_next': 1})
