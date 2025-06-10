from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TrainingQuickPlannerWizard(models.TransientModel):
    _name = 'training.quick.planner.wizard'
    _description = "Assistant de planification rapide"

    name = fields.Char(string="Nom de la session", required=True)
    trainer_id = fields.Many2one(
        'res.partner',
        string="Formateur",
        domain="[('is_trainer', '=', True)]",
        required=True
    )
    room_id = fields.Many2one('training.room', string="Salle", required=True)
    start_date = fields.Datetime(string="Date de début", required=True)
    end_date = fields.Datetime(string="Date de fin", required=True)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for wizard in self:
            if wizard.start_date >= wizard.end_date:
                raise ValidationError("La date de début doit être antérieure à la date de fin.")

    def action_create_session(self):
        self.ensure_one()
        session = self.env['training.session'].create({
            'name': self.name,
            'trainer_id': self.trainer_id.id,
            'room_id': self.room_id.id,
            'start_datetime': self.start_date,
            'end_datetime': self.end_date,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Session',
            'view_mode': 'form',
            'res_model': 'training.session',
            'res_id': session.id,
            'target': 'current',
        }
