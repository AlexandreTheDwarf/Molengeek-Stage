{
    'name': "Gestion de Formation",
    'version': '1.0',
    'author': "Alexandre",
    'category': 'Training',
    'summary': "Module de gestion de tâches de formation",
    'depends': ['base'],
    'data': [
        'security/training_security.xml',
        'security/ir.model.access.csv',        # ✅ Ensuite les accès
        'views/training_task_views.xml',
        'views/training_views.xml',
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'application': True,
}
