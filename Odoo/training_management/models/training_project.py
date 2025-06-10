# -*- coding: utf-8 -*-

from odoo import models, fields

class TrainingProject(models.Model):
    _name = 'training.project'
    _description = 'Training Project'

    name = fields.Char(string="Nom du projet", required=True)
    description = fields.Text(string="Description")
    task_ids = fields.One2many('training.task', 'project_id', string="Tâches")
