# R2BAC
Plateforme Open-Source développer par une équipe indépendante, de lycéens.
Cette plateforme à pour but d'aider les lycéens à réussir leurs années scolaire de la Seconde à la Terminal.

## Fonctionnalitées
- Système d'authentification sécurisé
- Système de profil personnalisée pour utilisateur

## Installation
Pour effectuer le lancemment du site de R2BAC en local c'est assez simple. Il vous suffis de télécharger [Docker](https://www.docker.com/), et [Docker Compose](https://docs.docker.com/compose/install/) si vous n'avez pas installer Docker Desktop.

Une fois Docker installer vous devez cloner le projet et y accéder via les commandes suivantes dans un Terminal :
> [!NOTE]
> ⚠️ [git](https://git-scm.com/downloads) est nécessaire pour pouvoir cloner le projet
```bash
git clone https://github.com/Link34500/R2BAC.git
cd R2BAC
```
---

## Note
- Vous devez faire attention et effectuer des vérification lors de la soummission de formulaire avec POST qui peut engedrer des attaques par DoS
- Egalemment réaliser une limite de requête GET sinon cela peut engendrer le même type d'attaque


## Prochainemment
### Accounts
- Vérifier le format de mot de passe,email,username,firstname dans le formulaire.
- Empecher d'envoyer des fichiers de plus de 5Mo
- Sauvegarder avec le nom de l'id de l'utilisateur et supprimer ses anciennes pp.
- Faire en sorte qu'ils ne puisse envoyer que des images avec les validateurs 
- Permettre la rénitialisation de mot de passe #
- Expiration du token de rénitialisation #
- Créer un cooldown pour l'envoie de vérification de mot de passe/compte/supression de compte
- Permettre la supression de compte avec vérification par mail
- Permettre de changer sont mot de passe/adressemail
- Cooldown de 15 minutes si on modifie le profil plus de 3 fois dans la même heure

### Cours
- Permettre de visionner les cours
- Permettre de commenter
- Permettre de répondre à un commentaire
- Cooldown entres commentaires

### Panel

- Pouvoir créer des cours/chapitres pour les profs.
- Pouvoir créer des classes et des matières pour les administrateur
- Panel de gestion utilisateur : role,informations, possibilitée de modifié les informations...

### Pour le front 
- Faire en sorte que la barre de sauvegarde ne s'affiche que si un changemment est effectuer (Un champ est modifié) dans le profile.html
- Faire en sorte de pouvoir redimensionner le logo

### Après front end
- Crée un système de Quiz.
- Mettre une partie Annales 