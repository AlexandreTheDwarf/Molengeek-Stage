from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
import csv
from io import StringIO

class TrainingSessionImportParticipantsWizard(models.TransientModel):
    _name = 'training.session.import.participants'
    _description = "Importer des participants via CSV"

    session_id = fields.Many2one('training.session', string="Session", required=True)
    file = fields.Binary(string="Fichier CSV", required=True)
    filename = fields.Char(string="Nom du fichier")

    def action_import(self):
        self.ensure_one()
        if not self.file:
            raise UserError("Veuillez sélectionner un fichier CSV à importer.")
        
        file_data = base64.b64decode(self.file)
        file_input = StringIO(file_data.decode('utf-8'))
        csv_reader = csv.DictReader(file_input)

        partner_obj = self.env['res.partner']
        added = 0

        for row in csv_reader:
            # Exemple : on cherche le partenaire par email, sinon on le crée
            email = row.get('email', '').strip()
            name = row.get('name', '').strip()
            if not email or not name:
                continue  # ignore si données manquantes

            partner = partner_obj.search([('email', '=', email)], limit=1)
            if not partner:
                partner = partner_obj.create({
                    'name': name,
                    'email': email,
                    'is_participant': True,
                })
            # Ajout à la session si pas déjà présent
            if partner not in self.session_id.participant_ids:
                self.session_id.write({'participant_ids': [(4, partner.id)]})
                added += 1

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
