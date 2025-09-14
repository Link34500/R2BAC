from django.shortcuts import render
from accounts.forms import ContactForm
from django.views.generic import FormView
from django.contrib import messages
from common.utils.messages import message as _

def index(request):
    return render(request,template_name="r2bac/index.html")

def cgu(request):
    return render(request,template_name="r2bac/cgu.html")

def privacy_policy(request):
    return render(request,template_name="r2bac/privacy_policy.html")

def legal(request):
    return render(request,template_name="r2bac/legal.html")

class ContactView(FormView):
    """Affiche la page de contact et gère l'envoie de mail"""

    template_name = "r2bac/contact.html"
    form_class = ContactForm
    success_url = "/contact/?success=true"

    def get(self, request, *args, **kwargs):
        if 'success' in request.GET:
            messages.success(request, _("MESSAGE_SEND_SUCCESS"))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form:ContactForm):
        form.save()
        return super().form_valid(form)



def apropos(request):
    return render(request,template_name="r2bac/apropos.html")
