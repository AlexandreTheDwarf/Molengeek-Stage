from odoo import models, fields

class TrainingRoom(models.Model):
    _name = 'training.room'
    _description = "Salle de formation"

    name = fields.Char(string="Nom de la salle", required=True)
    capacity = fields.Integer(string="Capacité maximale")
    equipment = fields.Text(string="Équipements disponibles")
