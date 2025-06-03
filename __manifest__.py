# -*- coding: utf-8 -*-
{
    'name': "Gestión de Biblioteca",
    
    'summary': "Módulo para la gestión de una biblioteca",
    
    'description': "Módulo para gestionar libros, préstamos y devoluciones en una biblioteca.",
    
    'author': "Pablo",
    
    'website': "https://github.com/pablobarroso83",
    
    'application': True,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/Library',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/libro_views.xml',
        'views/prestamo_views.xml',
        'views/menu_views.xml',
        'reports/report_libro.xml',
        'reports/libro_report_template.xml',
        'data/demo_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'data/demo_data.xml',
    ],
    
    # Carga icono modulo
    'images': ['static/description/icon.png'],
}

