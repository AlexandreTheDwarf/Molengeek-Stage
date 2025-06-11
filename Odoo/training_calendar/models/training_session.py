from markupsafe import Markup
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from lxml import etree
import json


class TrainingSession(models.Model):
    _name = "training.session"
    _description = "Session de formation"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # --- MÉTHODE POUR LE DEFAULT ---
    # NOUVEAU : Cette fonction sera appelée pour définir la valeur par défaut du formateur.
    def _default_trainer(self):
        # self.env.user est l'utilisateur actuellement connecté.
        # .partner_id est le contact (res.partner) lié à cet utilisateur.
        return self.env.user.partner_id

    # --- DÉFINITION DES CHAMPS ---
    name = fields.Char(required=True)
    start_datetime = fields.Datetime(required=True)
    end_datetime = fields.Datetime(required=True)
    # NOUVEAU : On ajoute l'attribut 'default' à notre champ.
    trainer_id = fields.Many2one(
        "res.partner", 
        string="Formateur", 
        required=True, 
        default=_default_trainer
    )
    room_id = fields.Many2one("training.room", string="Salle", required=True)
    participant_ids = fields.Many2many("res.partner", string="Participants")
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmée'),
        ('done', 'Terminée'),
    ], default='draft', string="État", tracking=True)

    # ... (le reste de ton code reste absolument identique)
    @api.constrains('participant_ids', 'room_id')
    def _check_room_capacity(self):
        for session in self:
            if session.room_id and len(session.participant_ids) > session.room_id.capacity:
                raise ValidationError(
                    f"La salle '{session.room_id.name}' ne peut accueillir que {session.room_id.capacity} personnes."
                )

    @api.constrains('trainer_id', 'start_datetime', 'end_datetime')
    def _check_trainer_availability(self):
        for session in self:
            overlapping = self.search([
                ('id', '!=', session.id),
                ('trainer_id', '=', session.trainer_id.id),
                ('start_datetime', '<', session.end_datetime),
                ('end_datetime', '>', session.start_datetime),
            ])
            if overlapping:
                raise ValidationError(
                    f"Le formateur {session.trainer_id.name} est déjà occupé sur une autre session."
                )

    @api.constrains('room_id', 'start_datetime', 'end_datetime')
    def _check_room_availability(self):
        for session in self:
            overlapping = self.search([
                ('id', '!=', session.id),
                ('room_id', '=', session.room_id.id),
                ('start_datetime', '<', session.end_datetime),
                ('end_datetime', '>', session.start_datetime),
            ])
            if overlapping:
                raise ValidationError(
                    f"La salle {session.room_id.name} est déjà réservée sur ce créneau."
                )

    def action_confirm(self):
        for session in self:
            if not session.room_id:
                raise UserError("Aucune salle sélectionnée.")
            if len(session.participant_ids) < 1:
                raise UserError("Nombre de participants insuffisant.")
            
            session.write({'state': 'confirmed'})

            recipients = session.trainer_id | session.participant_ids
            
            start_datetime_user_tz = fields.Datetime.context_timestamp(session, session.start_datetime)
            end_datetime_user_tz = fields.Datetime.context_timestamp(session, session.end_datetime)
            
            subject = f"Confirmation: Session de formation '{session.name}'"
            body = f"""
                <p>Bonjour,</p>
                <p>Ceci est une confirmation pour la session de formation <b>{session.name}</b>.</p>
                <ul>
                    <li><b>Début :</b> {start_datetime_user_tz.strftime('%d/%m/%Y à %H:%M')}</li>
                    <li><b>Fin :</b> {end_datetime_user_tz.strftime('%d/%m/%Y à %H:%M')}</li>
                    <li><b>Formateur :</b> {session.trainer_id.name}</li>
                    <li><b>Salle :</b> {session.room_id.name}</li>
                </ul>
                <p>Votre présence est attendue. Merci !</p>
            """
            
            session.message_post(
                body=Markup(body),
                subject=subject,
                partner_ids=recipients.ids,
                message_type='notification',
                subtype_xmlid='mail.mt_note', 
            )
            
    def action_done(self):
        for session in self:
            session.write({'state': 'done'})
            
    def action_draft(self):
        for session in self:
            session.write({'state': 'draft'})

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id, view_type, toolbar, submenu)
        if view_type == 'form' and not self.user_has_groups('base.group_system'):
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[not(@readonly)]"):
                modifiers = json.loads(node.get("modifiers", "{}"))
                domain = modifiers.get('readonly')
                if domain:
                    modifiers['readonly'] = ['|', ('state', '=', 'confirmed'), domain]
                else:
                    modifiers['readonly'] = [('state', '=', 'confirmed')]
                node.set("modifiers", json.dumps(modifiers))
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res

    def write(self, vals):
        if 'state' not in vals and len(vals) > 1:
            for session in self:
                if session.state == 'confirmed' and not self.env.user.has_group('training_calendar.group_formation_admin'):
                    raise UserError("Seul un administrateur peut modifier une session confirmée.")
        return super().write(vals)
    
    @api.model
    def _auto_close_sessions(self):
        now = fields.Datetime.now()
        sessions_to_close = self.search([
            ('state', '=', 'confirmed'),
            ('end_datetime', '<', now)
        ])
        for session in sessions_to_close:
            session.write({'state': 'done'})
        return True

    def print_upcoming_sessions(self):
        return self.env.ref('training_calendar.training_session_report').report_action(self)