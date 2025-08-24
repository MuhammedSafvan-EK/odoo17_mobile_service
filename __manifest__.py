# -*- coding: utf-8 -*-
{
    'name': "Mobile Service",

    'summary': "Mobile repair and service management module",

    'description': """
        A module to manage mobile service jobs, customers, and repairs.
    """,

    'author': "Safvan",
    'website': "https://www.yourcompany.com",

    'category': 'Services',
    'version': '0.1',

    'depends': ['base', 'sale', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'sequence/service_sequence.xml',
        'reports/service_report.xml',
        'reports/service_report_template.xml',
        'views/service.xml',
        'views/technisian.xml',
        'views/mobile_brand.xml',
        'views/account_report_invoice_document.xml',
        'views/technician_dashboard.xml',
        'wizard/service_print_wizard_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'mobile_service/static/src/css/user_error.css',
        ],
    },

    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
