from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from datetime import datetime,timedelta
from common.utils.mail_sender import Mail
from common.settings import PROJECT_NAME


# Create your models here.


class Role(models.Model):
    """Model représentant un role utilisateur.

    Attrs:
        users (~QuerySet[User]): Représente la liste des utilisateur qui sont relié à ce Role
        display_name (str): Nom d'affichage du role peut contenir des caractères UTF-8
        name (str): Nom du role, unique et suis la notation alpha
    """
    users = models.ManyToManyField(User,related_name="roles",related_query_name="role")
    display_name = models.CharField(max_length=32,verbose_name="nom d'affichage",blank=False,null=False)
    name = models.SlugField(max_length=32,verbose_name="nom",blank=True,null=False,unique=True)

    def has_permission(self,permission:str):
        """Permet de vérifier si le role possède la permission spécifié.

        Args:
            permission (str): Nom de la permission.

        Returns:
            bool: A la permission ?
        """
        return getattr(self.permissions,permission,False)

    def save(self, *args,**kwargs):
        # Mise à jour du champ name si il n'existe pas.
        if not self.name:
            self.name = slugify(self.display_name)
        return super().save(*args,**kwargs)

    def __str__(self):
        # Mise à jour du nom de l'objet pour plus de lisibilitée
        return self.name

class Permissions(models.Model):
    """Représente la liste des permissions des roles.

    Attrs:
        role (Role): Role représentant les permissions
        ... (bool) : Role a la permission ?
    """
    role = models.ForeignKey(Role,on_delete=models.CASCADE,related_query_name="permission",related_name="permissions")
    ADMIN = models.BooleanField(verbose_name="administrateur",default=False)

class UserInfo(models.Model):
    """Représente les informations de l'utilisateur, si il est vérfier, son uuid...

    Attrs:
        user (User): Représente l'utilisateur qui est relié à cette class
        uuid (UUID): UUID de l'utilisateurs
        premium (bool): Membre VIP ?
        verfy_token (str): Token d'activation du compte
        is_verified (bool): Compte vérifier ?
        cgu (bool): Conditions d'utilisation accepter ?
        received_email: Accepte de recevoir des email ?
    """
    user = models.OneToOneField(User,related_name="info",on_delete=models.CASCADE,null=True,blank=False)
    uuid = models.UUIDField(unique=True,editable=False,null=False)
    premium = models.BooleanField(default=False)
    verify_token = models.CharField(max_length=64,null=True)
    is_verified = models.BooleanField(default=False)
    cgu = models.BooleanField(default=True,blank=False,verbose_name="accepter les conditions d'utilisation")
    received_email = models.BooleanField(default=True,verbose_name="recevoir des emails d'annonces/mise à jour",blank=True)
    
    def generate_verify_token(self,request,send_mail=True):
        """Génère un token de vérfication de compte et l'envoie par mail

        Returns:
            (str): Retourne le token de vérfication
        """
        # Génère un token de vérification
        self.verify_token = get_random_string(64)
        self.save()
        # Envoie du token de vérification par mail
        if send_mail:
            Mail.noreply.send_mail(request,f"[{PROJECT_NAME}] - Active ton compte",[self.user.email],"accounts/emails/verify_token.html",{'token':self.verify_token,"user":self.user})
        
        return self.verify_token
    
    

    def __str__(self):
        # Mise à jour du champ de l'utilisateur
        return f"Info of {self.user.username}"

class PasswordReset(models.Model):
    """Représente le token de rénitialisation

    Attrs:
        user (User): L'utilisateur relié au token
        token (str): Le token de rénitialisation

    """
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="passwordreset")
    token = models.CharField(unique=True,max_length=64)
    created_at = models.DateTimeField(auto_now=True)
    used = models.BooleanField(default=False)

    def is_expired(self):
        """Vérifie si le token a expiré

        Returns:
            bool: Token expiré ?
        """
        if (self.created_at + timedelta(minutes=15)).timestamp() < datetime.now().timestamp():
            return True
        return False


class Profile(models.Model):
    """Représente le profil de l'utilisateur

    Attrs:
        user (User): L'utilisateur à qui appartient ce profil.
        avatar (Img): L'image de profil de l'utilisateur.
    """
    user = models.OneToOneField(User,related_name="profile",on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="pdp")
    name_is_username = models.BooleanField(default=False,verbose_name="utiliser le nom comme pseudo")

    @property
    def avatar_url(self):
        """Retourne l'url de l'avatar

        Returns:
            str: URL de l'avatar
        """
        if self.avatar and hasattr(self.avatar,'url'):
            return self.avatar.url
        return "/static/avatar_blank.png"

    def get_username(self):
        """Retourne le nom d'affichage de l'utilisateur

        Returns:
            str: Nom d'affichage
        """
        if not self.name_is_username:
            return self.user.username
        return self.user.get_full_name()

class Contact(models.Model):
    """Représente un message envoyé par le formulaire de contact

    Attrs:
        email (str): Email de l'utilisateur
        subject (str): Sujet du message
        message (str): Contenu du message
        created_at (datetime): Date de création du message
    """
    email = models.EmailField(blank=False,null=False)
    subject = models.CharField(max_length=128,blank=False,null=False)
    message = models.TextField(blank=False,null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.email} - {self.subject}"