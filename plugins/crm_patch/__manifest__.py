# -*- coding: utf-8 -*-
{
    'name': "crm_patch",

    'summary': """
        Crea el proycto en Redmine, luego de marcar
        como ganada la oportunidad en Odoo
    """,

     'description': """
        Se encarga de enviar una request a Redmine para crear
        el proyecto luego de que en Odoo se marque como ganada una
        oportunidad
    """,

    'author': "LoopStud.io",
    'website': "http://www.loopstud.io",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Plugin',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm'],
}
