from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Log(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_DEFAULT,verbose_name="utilisateur",default="USER_DELETED",related_name="log",related_query_name="logs")
    action = models.CharField(verbose_name="action effectuer",max_length=64)
    adresse_ip = models.CharField(verbose_name="adresse IP",max_length=39,null=False,blank=False)
    executed_at = models.DateTimeField(verbose_name="heure d'exécution",auto_now=True,null=False)


# Personalize
class Card(models.Model):
    title = models.CharField(verbose_name="titre",max_length=32)
    content = models.TextField(verbose_name="contenu")