# -*- coding: utf-8 -*-
{
    'name' : 'Expert Invoice',
    'version' : '1.1',
    'summary': 'Enhancement In Invoice Report',
    'description': """ Enhancement In Invoice Report""",
    'category': 'Accounting',
    'website': 'shimamostafa344@gmail.com',
    'depends' : ['account'],
    'data': [
        'report/account_invoice_report.xml',
        'report/custom_layout.xml',
    ],


    'installable': True,
    'application': False,
    'auto_install': False,
}
