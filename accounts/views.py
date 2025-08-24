<from django.views.generic import *
from .forms import *
from .models import *
from .mixins import *
from django.contrib.auth import login,logout
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.shortcuts import redirect,render,get_object_or_404
from common.utils.messages import message as _
# Create your views here.

class RegisterView(TitleMixin,LogoutRequieredMixin,FormView):
    """Représente la page de création de compte"""
    form_class = RegisterForm
    template_name = "accounts/register.html"
    title = "Créer un compte"
    success_url = reverse_lazy("accounts:verify")

    def form_valid(self, form:RegisterForm):
        # Sauvegarde l'utilisateur dans la base de donnée
        user = form.save()
        # Connecte l'utilisateur à son compte
        login(self.request,user)
        # Message de bienvenue
        Mail.noreply.send_mail(self.request,f"[{PROJECT_NAME}]",[user.email],"accounts/emails/welcome.html",{"user":user})
        # Génère le token de rénitialisation
        user.info.generate_verify_token(self.request)

        return super().form_valid(form)

class VerifyView(NotVerifiedRequieredMixin,MailSendVerificationMixin,TemplateView):
    """Représente la page de vérification de compte"""
    template_name = "accounts/verify.html"

    def get(self,request,*args,**kwargs):
        token = request.GET.get("token")
        user = self.request.user
        # Si le token correspond à celui de vérification de l'utilisateur.
        if token and user.info.verify_token == token:
            user.info.is_verified = True
            user.info.save()
            return render(request=self.request,template_name="accounts/welcome.html")

        return super().get(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):

        user = self.request.user

        user.info.generate_verify_token(self.request)

        return redirect(reverse("accounts:verify")+"?mail_send=true")

class SendResetPasswordView(LogoutRequieredMixin,TitleMixin,MailSendVerificationMixin,FormView):
    title = "Envoyer un mail de rénitialisation"
    form_class = SendResetPasswordForm
    template_name = "accounts/send_reset_password.html"
    success_url = reverse_lazy("accounts:reset_password")
    
    def get_success_url(self):
        return f"{self.success_url}?mail_send=true"

    def form_valid(self, form:SendResetPasswordForm):
        token = PasswordReset.objects.create(user=User.objects.get(email=form.cleaned_data["email"]),token=get_random_string(64))
        Mail.noreply.send_mail(self.request,f"[{PROJECT_NAME}] DEMANDE DE RENITIALISATION DE MOT DE PASSE",[form.cleaned_data["email"]],"accounts/emails/reset_password.html",context={"token":token.token})
        return super().form_valid(form)

class PasswordResetView(LogoutRequieredMixin,TitleMixin,FormView):
    title = "Rénitialiser mon mot de passe"
    form_class = PasswordResetForm
    template_name = "accounts/reset_password.html"
    success_url = reverse_lazy("accounts:login")

    def get(self, request, *args, **kwargs):
        token = get_object_or_404(PasswordReset,token=self.kwargs["token_id"])
        if token.is_expired():
            raise Http404("Token expiré")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form:PasswordResetForm):
        token = get_object_or_404(PasswordReset,token=self.kwargs["token_id"])
        user = token.user
        form.update(user).save()
        return super().form_valid(form)


class LoginView(TitleMixin,LogoutRequieredMixin,FormView):
    """Représente la page de Login de l'utilisateur"""
    form_class = LoginForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy("home")
    title = "Se connecter"

    def form_valid(self, form:LoginForm):
        user = form.cleaned_data["user"]
        login(self.request,user)

        return super().form_valid(form)

class LogoutView(LoginRequieredMixin,View):
    def get(self,request):
        logout(request)
        return redirect("home")


class ProfileView(LoginRequieredMixin,UpdateView):
    """Vue du profil des utilisateurs"""
    model = User
    form_class = ProfileForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("accounts:profile")
    
    def get_initial(self):
        initial = super().get_initial()
        initial.update({"name_is_username":self.object.profile.name_is_username})
        return initial.copy()

    def get_object(self):
        return self.request.user

class SettingsView(LoginRequieredMixin,FormView):
    template_name = "accounts/settings.html"
    sucess_url = reverse_lazy("accounts:settings")
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user":self.request.user})
        return kwargs

    def form_valid(self, form:PasswordChangeForm):
        form.update()
        return super().form_valid(form)
