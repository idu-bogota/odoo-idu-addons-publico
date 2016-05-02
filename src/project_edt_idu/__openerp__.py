{
    'name': 'EDT',
    'version': '1.0',
    'depends': [
        'base',
        'base_idu',
        'model_security',
        'product',
    ],
    'author': "Grupo de Investigación, Desarrollo e Innovación - STRT - IDU",
    'category': 'IDU',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/project_view.xml',
        'views/config_view.xml',
        'wizards/importar_mpp_view.xml',
        'wizards/registrar_progreso_tarea_view.xml',
        'wizards/fecha_estado_view.xml',
        'workflow/task_reporte_avance_workflow.xml',
    ],
    'test': [
        'tests/001_users.yml',
    ],
    'demo': [
        'tests/001_users.yml',
        'demo/project.edt.csv',
        'demo/project.task.csv',
        'demo/project.project.csv',
        'demo/project.task.registro_progreso.csv',
        'demo/project.task.pendiente.csv',
    ],
    'installable': True,
    'description': """
## Dependencias módulos Python
## Configuración adicional
    """,
}

