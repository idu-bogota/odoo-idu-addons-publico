{
    'name': 'Portafolio Proyectos',
    'version': '1.0',
    'depends': [
        'base',
        'base_idu',
        'model_security',
        'project_edt_idu',
        'hr',
    ],
    'author': "Grupo de Investigación, Desarrollo e Innovación - STRT - IDU",
    'category': 'IDU',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizards/crear_linea_base_view.xml',
        'views/project_view.xml',
        'views/hr_view.xml',
        'data/project.meta.tipo.csv',
        'wizards/crear_proyecto_funcionamiento_view.xml',
        'workflow/reporte_desempeno_workflow.xml',
        'workflow/solicitud_cambio_workflow.xml',
    ],
    'test': [
        'tests/001_users.yml',
    ],
    'demo': [
        'tests/001_users.yml',
    ],
    'installable': True,
    'description': """
## Dependencias módulos Python
## Configuración adicional
    """,
}

