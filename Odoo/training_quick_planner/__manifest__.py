{
    'name': 'Training Quick Planner',
    'version': '1.0',
    'summary': 'Wizard pour planification rapide de sessions de formation',
    'description': 'Ajoute un assistant pour créer des sessions rapidement via un wizard simple.',
    'category': 'Training',
    'author': 'Alexandre',
    'depends': ['training_calendar'],
    'data': [
        'security/ir.model.access.csv',
        'views/quick_planner_wizard_view.xml',
        'views/training_session_import_participants_views.xml',
        'views/training_menu.xml',
        'views/res_partner_views.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
