{
    'name' : "Supermarket Warehouse Management",
    "website": "",
    'author': 'Group 56 - NhatHieu',
    'summary': 'IUH Warehouse Inventory',
    'category': "Others",
    'data': [
        'security/security.xml',

        'views/res_users_view.xml',
        'views/stock_location_view.xml',
        'views/stock_move_view.xml',
        'views/stock_quant_view.xml',
    ],
    'depends' : ['base', 'stock','mass_mailing_sms','sale_stock','sale'],

    'application': True
}
