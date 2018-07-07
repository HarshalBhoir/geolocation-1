# -*- coding: utf-8 -*-
{
    'name': "SalesDSR",

    'summary': """
        SalesDSR for Sales Person tracking.
    """,

    'description': """
        SalesDSR for SalesPersons time and geolocation tracking. This modules allows you to track salesperson geolocation and using google api to calculate distance of their daily routes.
    """,

    'author': "Vikas Goyal",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['crm', 'product'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/views.xml',
        'views/salesdsr_report_view.xml',
        'views/geolocation_resource.xml',
        'views/res_company.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
