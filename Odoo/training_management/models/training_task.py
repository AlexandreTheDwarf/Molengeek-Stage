# -*- coding: utf-8 -*-

from odoo import models, fields

class TrainingTask(models.Model):
    _name = 'training.task'
    _description = 'Training Task'

    title = fields.Char(string="Titre", required=True)
    description = fields.Text(string="Description")
    deadline = fields.Date(string="Date limite")
    status = fields.Selection([
        ('draft', 'Brouillon'),
        ('in_progress', 'En cours'),
        ('done', 'Terminé'),
    ], default='draft', string='Statut')
    project_id = fields.Many2one('training.project', string="Projet", ondelete="set null")
