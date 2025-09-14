# R2BAC

R2BAC est une **plateforme open-source développée par une équipe indépendante de lycéens**.
Elle a pour objectif d'aider les lycéens à réussir leurs années scolaires, de la Seconde à la Terminale.

---

## Fonctionnalités

- Système d'authentification sécurisé
- Profils utilisateurs personnalisables
- Gestion des cours et chapitres
- Système de commentaires et réponses sur les cours X
- Panel de gestion pour les enseignants et administrateurs X # Il faussi pouvoir envoyer des emails
- Interface potable et responsive
- Notifications pour les nouveaux cours ou mises à jour par email
- Création d'articles X
- News Letter X

---

## Prérequis

Avant d'installer R2BAC, assurez-vous d'avoir :

- [Docker](https://www.docker.com/) et [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads) pour cloner le projet
- Une connexion internet stable pour télécharger les images Docker

---

## Installation

1. Clonez le dépôt :

```bash
git clone https://github.com/Link34500/R2BAC.git
cd R2BAC
```

2. Lancez le projet avec Docker Compose :

```bash
docker-compose up -d
```

3. Accédez à la plateforme depuis votre navigateur :

```
http://localhost:8000
```

> Les ports peuvent être configurés dans le fichier `docker-compose.yml` si nécessaire.

---

## Utilisation

- **Création d'un compte :** Inscrivez-vous avec votre email et mot de passe pour accéder aux cours.
- **Navigation :** Accédez aux cours par matière et par chapitre.
- **Commentaires :** Participez aux discussions et posez des questions sur les cours.
- **Panel enseignants :** Créez, modifiez ou supprimez des cours et chapitres. Gérez les utilisateurs et leurs permissions.

---

## Contribution

Nous accueillons toutes les contributions !

Pour contribuer :

1. Fork le projet
2. Créez une branche pour votre fonctionnalité ou correction de bug :

```bash
git checkout -b ma-fonctionnalite
```

3. Commitez vos changements :

```bash
git commit -m "Ajout d'une nouvelle fonctionnalité"
```

4. Poussez votre branche :

```bash
git push origin ma-fonctionnalite
```

5. Ouvrez une Pull Request sur GitHub.

---

## Support

Pour toute question ou problème, contactez-nous via GitHub Issues ou notre Discord.

---

## Licence

R2BAC est sous licence **NCCL**. Consultez le fichier `LICENSE` pour plus de détails.

---

## Technologies utilisées

- Python / Django
- HTML, CSS/SCSS, Bulma, JavaScript
- PostgreSQL
- Docker & Docker Compose
