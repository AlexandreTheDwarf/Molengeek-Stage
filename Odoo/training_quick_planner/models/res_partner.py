from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    participant_tag_ids = fields.Many2many('participant.tag', string='Tags Participants')
