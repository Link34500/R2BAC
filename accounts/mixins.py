from django.http import Http404
from .models import *
from django.shortcuts import redirect
from django.contrib import messages
from common.utils.messages import message as _


class MailSendVerificationMixin:
    
    def get(self,request,*args,**kwargs):
        mail_send = request.GET.get("mail_send")
        # Si le mail à correctemment été envoyée
        if mail_send == "true":
            messages.success(self.request,_("SUCESS_SEND_MAIL"))
        # Si le mail à mal été envoyée
        if mail_send == "false":
            messages.success(self.request,_("FAILED_SEND_MAIL_COOLDOWN"))
            
        return super().get(request,*args,**kwargs)

class TitleMixin:
    title = ""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context

class LogoutRequieredMixin:
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        if not user.info.is_verified:
            return redirect("accounts:verify")
        raise Http404("Non connecté")
    
class LoginRequieredMixin:
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated and user.info.is_verified:
            return super().dispatch(request, *args, **kwargs)
        return redirect("accounts:login")

class NotVerifiedRequieredMixin:
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated and not user.info.is_verified:
            return super().dispatch(request, *args, **kwargs)
        raise Http404("Déjà vérifier")

