# -*- coding: utf-8 -*-
{
    'name': "Cash Managment",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Finance Trust Bank",
    'website': "http://www.financetrust.co.ug",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mail','base'],

    # always loaded
    'data': [
        'security/cashmanagment_security.xml',
        'security/ir.model.access.csv',
        'data/email_template_cash_managment.xml',
        'wizard/cash_validate_view.xml',
        'wizard/cash_approve_view.xml',
        'wizard/cash_reject_view.xml',
        'wizard/cash_confirm_view.xml',
        'wizard/cash_cancel_request.xml',
        'wizard/cancel_cash_supervision.xml',
        'wizard/cash_request_approve_view.xml',
        'wizard/cash_confirm_cashcenter.xml',
        'wizard/from_manager.xml',
        'wizard/to_manager.xml',
        'wizard/from_manager_cash_center.xml',
        'wizard/to_manager_cash_center.xml',
        'views/branch.xml',
        'views/cash_request.xml',
        'views/cash_users.xml',
        'views/cash_transfer.xml',
        'views/report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}