from django import forms
from .models import *
from uuid import uuid4
from django.contrib.auth import authenticate
from common.utils.messages import message as _
from .validators import *


class RegisterForm(forms.ModelForm):
    received_email = forms.BooleanField(widget=forms.CheckboxInput(),required=False,label=_("LABEL_SUBSCRIBE_NEWSLETTER"))
    cgu = forms.BooleanField(required=True,label=_("LABEL_CGU_ACCEPT"))
    username = forms.CharField(max_length=22,required=True,label=_("LABEL_USERNAME"),validators=[username_validator])
    first_name = forms.CharField(max_length=30,required=False,label=_("LABEL_FIRST_NAME"),validators=[name_validator])
    last_name = forms.CharField(max_length=30,required=False,label=_("LABEL_LAST_NAME"),validators=[name_validator])
    email = forms.EmailField(max_length=255,required=True,label=_("LABEL_EMAIL"),validators=[email_validator])
    password = forms.CharField(max_length=256,required=True,label=_("LABEL_PASSWORD"),widget=forms.PasswordInput(),validators=[password_validator])

    class Meta:
        model = User
        fields = ["username","first_name","last_name","email","password"]
        widgets = {
            "password":forms.PasswordInput()
        }

    def clean_email(self):
        """Récupère l'email et vérifie qu'il n'est pas déjà utilisé par un autre utilisateur

        Raises:
            forms.ValidationError: Si l'adresse mail est déjà utilisé par un autre utilisateur

        Returns:
            (User): Retourne l'utilisateur si tout est bon
        """
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
            raise forms.ValidationError(_("ERROR_EMAIL_ALREADY_USED"))
        except User.DoesNotExist:
            pass
        return email

    def clean_username(self):
        """Récupère le username et vérifie qu'il n'est pas déjà utilisé par un autre utilisateur

        Raises:
            forms.ValidationError: Si le nom d'utilisateur est déjà utilisé par un autre utilisateur

        Returns:
            (User): Retourne l'utilisateur si tout est bon
        """
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
            raise forms.ValidationError(_("ERROR_USERNAME_ALREADY_USED"))
        except User.DoesNotExist:
            pass
        return username

    def save(self,commit=True):
        """Sauvegarde l'utilisateur en base de donnée crée le profile et les infos...

        Args:
            commit (bool, optional): Est ce que les changemments se font directemment en base de données ?
            Attention car mettre à False fait qu'il faut crée le profile et l'info de l'utilisateur. Defaults to True.

        Returns:
            (User): Retourne l'instance de l'utilisateur
        """
        user:User = super().save(commit=False)
        # Encode le password
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            UserInfo.objects.create(user=user,uuid=uuid4(),received_email=self.cleaned_data["received_email"])
            Profile.objects.create(user=user)

        return user


class LoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=255,required=True,label=_("LABEL_EMAIL_OR_USERNAME"))
    password = forms.CharField(widget=forms.PasswordInput(),required=True,label="Mot de passe")

    def clean(self):
        """Vérifie que les identifiants sont valides

        Raises:
            forms.ValidationError: Si le mot de passe ou l'adresse mail n'es pas remplie (None).
            forms.ValidationError: Si jamais l'adresse mail n'es liée à aucun compte.
            forms.ValidationError: Si le password est incorrecte.

        Returns:
            (dict): Si tout ce basse bien le contexte est retourné.
        """
        cleaned_data = super().clean()
        username_email = cleaned_data.get("username_or_email")
        password = cleaned_data.get("password")

        # Si le mot de passe ou le username/mail est vide
        if not password or not username_email:
            return cleaned_data
        
        user = authenticate(username_or_email=username_email,password=password)

        if not user:
            raise forms.ValidationError(_("INVALID_CREDITALS"))
        else:
            cleaned_data["user"] = user
        
        return cleaned_data



class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30,required=False,label=_("LABEL_FIRST_NAME"),validators=[name_validator])
    last_name = forms.CharField(max_length=30,required=False,label=_("LABEL_LAST_NAME"),validators=[name_validator])
    username = forms.CharField(max_length=22,required=True,label=_("LABEL_USERNAME"),validators=[username_validator])
    avatar = forms.FileField(widget=forms.FileInput(attrs={"accept":"image/png, image/jpeg"}),required=False)
    name_is_username = forms.BooleanField(required=False,label=_("LABEL_NAME_IS_USERNAME"))
    class Meta:
        model = User
        fields = ["avatar","first_name","last_name","username"]

    def clean_avatar(self):
        avatar = self.cleaned_data["avatar"]
        if avatar:
            if avatar.size > 5*1024*1024:
                raise forms.ValidationError(_("ERROR_AVATAR_SIZE"))
            if not avatar.content_type in ["image/png","image/jpeg"]:
                raise forms.ValidationError(_("ERROR_AVATAR_FORMAT"))
        avatar.name = f"{uuid4()}.{avatar.name.split('.')[-1]}" # Renomme le fichier avec le format uuid.extension
        return avatar

    def clean_username(self):
        """Récupère le username et vérifie qu'il n'est pas déjà utilisé par un autre utilisateur

        Raises:
            forms.ValidationError: Si le nom d'utilisateur est déjà utilisé par un autre utilisateur

        Returns:
            (User): Retourne l'utilisateur si tout est bon
        """
        username = self.cleaned_data["username"]
        try:
            user = User.objects.get(username=username)
            if self.instance.pk != user.pk:
                raise forms.ValidationError(_("ERROR_USERNAME_ALREADY_USED"))
        except User.DoesNotExist:
            pass
        return username

    def save(self, commit = True):
        """Mets à jour les infos de l'instance
        
        Args:
            commit (bool, optional): Est ce que les changemments se font directemment en base de données ?
            Attention ! Si la valeur est à False vous devez effectuer les changements des Infos et du Profile manuellemment

        Returns:
            (User): Retourne l'instance de l'utilisateur
        """
        instance = super().save(commit=False)
        if self.cleaned_data["avatar"]:
            instance.profile.avatar = self.cleaned_data["avatar"]
        instance.profile.name_is_username = self.cleaned_data["name_is_username"]
        if commit:
            instance.profile.save()
            instance.save()
        return instance


class SendResetPasswordForm(forms.Form):
    email = forms.EmailField(max_length=255,required=True,validators=[email_validator])
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(_("ERROR_EMAIL_NOT_FOUND"))
        return email

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(required=True,widget=forms.PasswordInput(),validators=[password_validator])
    confirm_new_password = forms.CharField(required=True,widget=forms.PasswordInput())
    

    def clean(self):
        """Vérifie que les mots de passes sont valides et qu'ils correspondent entres eux.

        Raises:
            forms.ValidationError: Si un des champs est vide
            forms.ValidationError: Si les mots de passe ne correspondent pas
        
        Returns:
            (dict): Retourne le dictionnaire des données si rien n'es mal formatté
        """
        clean_data = super(forms.Form,self).clean()
        new_password = clean_data.get("new_password")
        confirm_new_password = clean_data.get("confirm_new_password")
        
        if not new_password or not confirm_new_password:
            return clean_data

        if new_password != confirm_new_password:
            raise forms.ValidationError(_("ERROR_PASSWORDS_NOT_MATCH"))

        return clean_data

    def update(self, user:User):
        """Change le mot de passe de l'instance et la retourne
        Returns:
            (User): Retourne l'instance
        """
        user.set_password(self.cleaned_data["new_password"])

        return user

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(required=True,widget=forms.PasswordInput(),label=_("LABEL_PASSWORD"))

    new_password = forms.CharField(required=True,widget=forms.PasswordInput(),label=_("NEW_PASSWORD"),validators=[password_validator])
    confirm_new_password = forms.CharField(required=True,widget=forms.PasswordInput(),label=_("CONFIRM_NEW_PASSWORD"))


    def __init__(self,user,*args,**kwargs):
        super(PasswordChangeForm,self).__init__(*args,**kwargs)
        self.user = user

    
    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(_("INVALID_PASSWORD"))
        return old_password

    def clean(self):
        """Reprend les mêmes propriété de la méthode PasswordReset.clean"""
        
        return PasswordResetForm.clean(self)

    def update(self):
        self.user.set_password(self.cleaned_data["new_password"])




