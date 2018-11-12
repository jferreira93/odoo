# -*- coding: utf-8 -*-
{
    'name': "Test the request for Redmine",

    'summary': """
        This module send a request for Redmine when
        the oportunity is marked as won
    """,

    'description': """
        This module send a request for Redmine when
        the oportunity is marked as won
    """,

    'author': "LoopStud.io",
    'website': "http://www.loopstud.io",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Plugin',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
