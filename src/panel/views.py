from django.shortcuts import render
from django.views.generic import *
from .models import *
from .mixins import *
# Create your views here.

class PanelView(TemplateView):
    template_name = "panel/index.html"


class LogsView(TableListMixin,ListView):
    model = Log
    template_name = "panel/logs.html"
    context_object_name = "logs"    
    
    def get_paginate_by(self, queryset):
        """Controle le nombre de logs sur le serveur"""
        try:
            paginate_by = int(self.request.GET.get("paginate"))
        except:
            paginate_by = 10
        return paginate_by if paginate_by <= 100 else 100

    def get_queryset(self):
        return Log.objects.all()

