# controllers/main.py
from odoo import http
from odoo.http import request, Response
import json

class TrainingSessionController(http.Controller):

    @http.route('/api/training_sessions', auth='public', type='http', methods=['GET'], csrf=False)
    def get_training_sessions(self, **kwargs):
        # Récupérer les sessions de formation
        training_sessions = request.env['training.session'].search([])

        # Préparer les données à retourner
        sessions_data = []
        for session in training_sessions:
            sessions_data.append({
                'title': session.name,
                'trainer': session.trainer_id.name,
                'start_datetime': session.start_datetime.isoformat() if session.start_datetime else None,
                'end_datetime': session.end_datetime.isoformat() if session.end_datetime else None,
            })

        # Retourner les données en tant que réponse JSON
        return request.make_response(
            json.dumps(sessions_data),
            headers=[('Content-Type', 'application/json')],
        )
