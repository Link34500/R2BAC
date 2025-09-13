from django.shortcuts import render
from panel.models import Card
from courses.models import Grade

def index(request):
    
    
    return render(request,template_name="r2bac/index.html")

def cgu(request):
    return render(request,template_name="r2bac/cgu.html")

def privacy_policy(request):
    return render(request,template_name="r2bac/privacy_policy.html")

def legal(request):
    return render(request,template_name="r2bac/legal.html")

def contact(request):
    return render(request,template_name="r2bac/contact.html")

def apropos(request):
    return render(request,template_name="r2bac/apropos.html")
