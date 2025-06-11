# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

# On crée une classe de test qui hérite de TransactionCase.
# Cela signifie que chaque test sera exécuté dans sa propre transaction de base de données,
# qui sera annulée à la fin. Ainsi, les tests ne polluent pas ta vraie base de données.
class TestSessionLogic(TransactionCase):

    # La méthode setUp est spéciale : elle est exécutée avant CHAQUE méthode de test.
    # C'est l'endroit parfait pour créer les données de base dont on aura besoin.
    def setUp(self, *args, **kwargs):
        super(TestSessionLogic, self).setUp(*args, **kwargs)

        # On prépare des "raccourcis" vers les modèles qu'on va utiliser
        self.Partner = self.env['res.partner']
        self.Session = self.env['training.session']
        self.Room = self.env['training.room']

        # On crée des données de test
        self.test_trainer = self.Partner.create({'name': 'Marc Formateur Test'})
        self.test_room = self.Room.create({'name': 'Salle de Test Alpha', 'capacity': 10})
        
        # On définit une date de début pour nos tests, par exemple dans 15 jours.
        self.test_start_date = datetime.now() + timedelta(days=15)
        self.test_end_date = self.test_start_date + timedelta(hours=4)

    # --- TEST 1 : Conflit de Formateur ---
    def test_01_trainer_conflict(self):
        """
        Vérifie qu'une erreur ValidationError est levée si on essaie de réserver
        un formateur qui est déjà pris sur le même créneau.
        """
        # "Arrange" : On prépare le scénario en créant une première session valide.
        self.Session.create({
            'name': 'Session Initiale',
            'trainer_id': self.test_trainer.id,
            'room_id': self.test_room.id,
            'start_datetime': self.test_start_date,
            'end_datetime': self.test_end_date,
        })

        # "Act & Assert" : On exécute l'action qui doit déclencher l'erreur.
        # `with self.assertRaises(ValidationError)`: ce bloc s'attend à recevoir une erreur
        # de type ValidationError. Si l'erreur se produit, le test est un succès.
        # Si aucune erreur ne se produit, le test échoue.
        with self.assertRaises(ValidationError, msg="Un conflit de formateur aurait dû être détecté."):
            self.Session.create({
                'name': 'Session en Conflit',
                'trainer_id': self.test_trainer.id,  # <-- Même formateur
                'room_id': self.test_room.id,
                'start_datetime': self.test_start_date, # <-- Même heure de début
                'end_datetime': self.test_end_date,
            })
        
    # --- TEST 2 : Conflit de Salle ---
    def test_02_room_conflict(self):
        """Vérifie la détection de conflit pour une salle."""
        # Arrange
        self.Session.create({
            'name': 'Première réservation de salle',
            'trainer_id': self.test_trainer.id,
            'room_id': self.test_room.id,
            'start_datetime': self.test_start_date,
            'end_datetime': self.test_end_date,
        })

        # Crée un autre formateur pour éviter un conflit de formateur
        other_trainer = self.Partner.create({'name': 'Jeanne Autre Formatrice'})

        # Act & Assert
        with self.assertRaises(ValidationError, msg="Un conflit de salle aurait dû être détecté."):
            self.Session.create({
                'name': 'Session en Conflit de Salle',
                'trainer_id': other_trainer.id, # <-- Formateur différent
                'room_id': self.test_room.id,    # <-- Même salle
                'start_datetime': self.test_start_date,
                'end_datetime': self.test_end_date,
            })

    # --- TEST 3 : Mise à jour de l'état de la session ---
    def test_03_session_state_update_on_confirm(self):
        """Vérifie que l'état passe bien à 'confirmed' après l'appel de action_confirm."""
        # Arrange : On crée une session à l'état initial 'draft'.
        session_to_confirm = self.Session.create({
            'name': 'Session à Confirmer',
            'trainer_id': self.test_trainer.id,
            'room_id': self.test_room.id,
            'start_datetime': self.test_start_date,
            'end_datetime': self.test_end_date,
            'participant_ids': [(4, self.Partner.create({'name': 'Un Participant'}).id)]
        })
        # On vérifie que l'état de départ est bien 'draft'
        self.assertEqual(session_to_confirm.state, 'draft')

        # Act : On appelle la méthode à tester.
        session_to_confirm.action_confirm()

        # Assert : On vérifie que le résultat est celui attendu.
        self.assertEqual(session_to_confirm.state, 'confirmed', "L'état de la session aurait dû être 'confirmée'.")