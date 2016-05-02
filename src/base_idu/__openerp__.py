{
    "name" : "base_idu",
    "version" : "odoo9.0-rev-2016012500",
    "author" : "Instituto de Desarrollo Urbano - STRT I+D+I",
    "category" : "idu", 
    "description" : """Módulo base IDU""",
    "depends" : [
        'base',
        'website',
        'hr',
        'l10n_co_base',
        'project',
        'model_security',
        'auth_ldap',
    ],
    "data" : [
        'views/templates.xml',
        'views/res_view.xml',
        'views/hr_view.xml',
        'views/project_view.xml',
        'data/hr.department.csv',
        'data/base_idu_data.xml',
        'wizard/registrar_mensaje_view.xml',
        'security/ir.model.access.csv',
    ],
    "test": [
        'tests/res_partner.yml',
    ],
    "installable" : True,
}