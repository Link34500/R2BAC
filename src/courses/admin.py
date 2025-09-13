from django.contrib import admin
from .models import *


# Register your models here.


admin.site.register(Subject,admin.ModelAdmin)
admin.site.register(Grade,admin.ModelAdmin)