from django.shortcuts import render
from panel.models import Card
from courses.models import Grade

def index(request):
    
    
    return render(request,template_name="r2bac/index.html",context={"cards":Card.objects.all()})

def cgu(request):
    return render(request,template_name="cgu.html")

def privacy_policy(request):
    return render(request,template_name="privacy_policy.html")

def legal(request):
    return render(request,template_name="legal.html")

def contact(request):
    return render(request,template_name="contact.html")

def apropos(request):
    return render(request,template_name="apropos.html")
