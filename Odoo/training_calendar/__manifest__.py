{
    'name': "Gestion de Formation",
    'version': '1.0',
    'author': "Alexandre",
    'category': 'Training',
    'summary': "Module de planification de sessions de formation",
    'depends': [
        'base', 
        'mail',
    ],
    'data': [
        'security/formation_security.xml',
        'security/ir.model.access.csv',
        'views/training_session_views.xml',
        'views/training_room_views.xml',
        'views/res_partner_views.xml',
        'data/ir_cron.xml',
        'report/training_session_report.xml',
        'views/training_dashboard_views.xml',
    ],
    'installable': True,
    'application': True,
}