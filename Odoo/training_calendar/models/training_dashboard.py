# models/training_dashboard.py
from odoo import models, fields, api
from datetime import datetime, timedelta

class TrainingDashboard(models.TransientModel):
    _name = 'training.dashboard'
    _description = 'Tableau de bord des formations'

    sessions_this_week = fields.Integer(string="Sessions cette semaine", compute="_compute_dashboard")
    most_active_trainers = fields.Text(string="Formateurs les plus actifs", compute="_compute_dashboard")
    next_session = fields.Char(string="Prochaine session", compute="_compute_dashboard")
    filling_rate = fields.Char(string="Taux de remplissage moyen", compute="_compute_dashboard")

    @api.depends()
    def _compute_dashboard(self):
        from odoo.fields import Datetime
        today = fields.Date.context_today(self)
        start_week = Datetime.to_datetime(today) - timedelta(days=Datetime.to_datetime(today).weekday())
        end_week = start_week + timedelta(days=6, hours=23, minutes=59, seconds=59)

        Session = self.env['training.session']
        sessions = Session.search([
            ('start_datetime', '>=', fields.Datetime.to_string(start_week)),
            ('start_datetime', '<=', fields.Datetime.to_string(end_week))
        ])

        self.sessions_this_week = len(sessions)

        # Formateurs les plus actifs
        trainer_count = {}
        for s in sessions:
            if s.trainer_id:
                trainer_count[s.trainer_id.name] = trainer_count.get(s.trainer_id.name, 0) + 1
        sorted_trainers = sorted(trainer_count.items(), key=lambda x: x[1], reverse=True)
        self.most_active_trainers = ', '.join([f"{name} ({count})" for name, count in sorted_trainers[:3]])

        # Prochaine session
        next_session = Session.search([('start_datetime', '>', fields.Datetime.now())], order="start_datetime asc", limit=1)
        self.next_session = next_session.name if next_session else "Aucune"

        # Taux de remplissage
        total_capacity = sum(s.room_id.capacity for s in sessions if s.room_id and s.room_id.capacity)
        total_participants = sum(len(s.participant_ids) for s in sessions)
        if total_capacity:
            self.filling_rate = f"{(total_participants / total_capacity) * 100:.1f}%"
        else:
            self.filling_rate = "N/A"

    @api.model
    def open_dashboard(self):
            dashboard = self.create({})
            return {
                'name': "📊 Dashboard",
                'type': 'ir.actions.act_window',
                'res_model': 'training.dashboard',
                'view_mode': 'form',
                'res_id': dashboard.id,
                'target': 'current',
            }