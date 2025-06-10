from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_trainer_contact = fields.Boolean(string="Contact Formateur")