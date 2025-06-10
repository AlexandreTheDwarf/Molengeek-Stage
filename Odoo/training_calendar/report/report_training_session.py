# training_management/report/report_training_session.py
from odoo import models, fields

class ReportTrainingSessions(models.AbstractModel):
    _name = 'report.training_management.report_training_sessions'
    _description = 'Rapport PDF des sessions de formation à venir'

    def _get_report_values(self, docids, data=None):
        docs = self.env['training.session'].browse(docids)
        sessions = docs.filtered(lambda s: s.start_datetime and s.start_datetime >= fields.Datetime.now())

        # Tri par projet
        if data and data.get('sort_by') == 'project':
            sessions = sessions.sorted(key=lambda s: s.project_id.name)

        # Tri par formateur
        elif data and data.get('sort_by') == 'trainer':
            sessions = sessions.sorted(key=lambda s: s.trainer_id.name)

        # Tri par défaut par date de début
        else:
            sessions = sessions.sorted(key=lambda s: s.start_datetime)

        return {
            'doc_ids': docids,
            'doc_model': 'training.session',
            'docs': sessions,
        }
