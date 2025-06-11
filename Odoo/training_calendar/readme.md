# Module de Gestion de Formations (training_calendar)

Ce module pour Odoo v16+ permet une gestion complète et sécurisée des sessions de formation, de la planification à la notification des participants.

## 🎯 Objectif du Module

L'objectif de `training_calendar` est de fournir un outil centralisé pour organiser des événements de formation, en s'assurant que les bonnes personnes ont les bons niveaux d'accès et que la communication est fluide et automatisée.

## ✨ Fonctionnalités Clés

* **Planification de Sessions :** Créez et organisez des sessions avec des dates, des horaires, une salle et un formateur dédiés.
* **Gestion des Participants :** Inscrivez et suivez facilement les participants pour chaque session.
* **Logique Métier Robuste :**
    * Vérification automatique de la capacité des salles.
    * Vérification des conflits de disponibilité pour les formateurs et les salles pour éviter les doubles réservations.
* **Sécurité Avancée :** Gestion des droits via 3 niveaux d'accès :
    * **Stagiaire :** Accès en lecture seule à ses sessions.
    * **Formateur :** Peut voir et gérer les sessions qu'il anime. Le champ "Formateur" est automatiquement rempli avec son nom à la création.
    * **Administrateur de Formation :** Accès complet à la configuration et à la gestion de toutes les sessions.
* **Notifications Automatiques :** Le formateur et les participants sont notifiés via le chatter Odoo lors de la confirmation d'une session. Les messages sont formatés en HTML et affichent l'heure dans le fuseau horaire de l'utilisateur.
* **Tests Automatisés :** Une suite de tests unitaires garantit la stabilité et la non-régression des fonctionnalités clés (gestion des conflits, changement d'états).

## ⚙️ Installation

1.  Placez le dossier `training_calendar` dans le répertoire `addons` de votre instance Odoo.
2.  Redémarrez le service Odoo.
3.  Activez le mode développeur dans Odoo.
4.  Allez dans le menu `Apps`.
5.  Cliquez sur `Mettre à jour la liste des applications`.
6.  Recherchez "Gestion de Formation" ou "training_calendar" et cliquez sur **Installer**.

## 🛠️ Configuration Requise

Après l'installation, un administrateur doit assigner les groupes de sécurité aux utilisateurs concernés :

1.  Allez dans `Paramètres > Utilisateurs & Compagnies > Utilisateurs`.
2.  Sélectionnez un utilisateur.
3.  Cliquez sur "Modifier".
4.  Dans la section "Droits d'accès", sous "Gestion de Formation", cochez le niveau d'accès approprié (`Stagiaire`, `Formateur` ou `Administrateur`).
5.  Sauvegardez les modifications.

## 🚀 Utilisation

* **L'Administrateur** peut créer de nouvelles salles, de nouveaux cours, et planifier n'importe quelle session pour n'importe quel formateur.
* **Le Formateur** peut accéder au menu "Formation", voir la liste de ses sessions, et en créer de nouvelles pour lui-même. Il peut confirmer ses sessions pour notifier les participants.
* **Le Stagiaire** peut consulter les sessions auxquelles il est inscrit (accès en lecture seule).

## 🧪 Lancer les Tests

Pour exécuter la suite de tests unitaires, lancez Odoo avec l'option `--test-enable` en spécifiant le module :

```bash
python odoo-bin -d <votre_base_de_donnees> -u training_calendar --test-enable
```