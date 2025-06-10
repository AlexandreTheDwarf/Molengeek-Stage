from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_trainer = fields.Boolean(string="Est formateur")
    is_participant = fields.Boolean(string="Est participant")
