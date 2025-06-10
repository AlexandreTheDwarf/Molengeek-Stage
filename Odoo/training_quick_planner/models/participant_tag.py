from odoo import models, fields

class ParticipantTag(models.Model):
    _name = 'participant.tag'
    _description = 'Tag pour les participants'

    name = fields.Char(string='Nom du Tag', required=True)
