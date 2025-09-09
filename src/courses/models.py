from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class Grade(models.Model):
  name = models.CharField("classe",max_length=16)
  slug = models.SlugField("url",max_length=16,unique=True,blank=True)

  def __str__(self):
    return self.name

  def save(self, *args,**kwargs):
    if not self.slug:
      self.slug = slugify(self.name)
    return super().save(*args,**kwargs)



class Subject(models.Model):
  grade = models.ForeignKey(Grade,on_delete=models.SET_DEFAULT,default="DELETED_GRADE",verbose_name="classe",related_name="subjects")
  name = models.CharField("matière",max_length=32)
  slug = models.SlugField("url",max_length=16,unique=True,blank=True)

  def __str__(self):
    return self.name

  def save(self, *args,**kwargs):
    if not self.slug:
      self.slug = slugify(self.name)
    return super().save(*args,**kwargs)

class Chapter(models.Model):
  subject = models.ForeignKey(Subject,on_delete=models.CASCADE,verbose_name="matière",related_name="chapters")
  number = models.IntegerField("numéro de chapitre",blank=False,null=False)
  name = models.CharField("titre",max_length=48)
  slug = models.SlugField("url",max_length=48,unique=True,blank=True)

  def __str__(self):
    return self.name

  def save(self, *args,**kwargs):
    if not self.slug:
      self.slug = slugify(self.name)
    return super().save(*args,**kwargs)

class Course(models.Model):
  chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE,related_name="cours",verbose_name="Chapitre")
  name = models.CharField("titre",max_length=48)
  slug = models.SlugField("url",max_length=48,unique=True,blank=True)
  contributors = models.ManyToManyField(User,related_name="contributions",blank=True,verbose_name="contributeurs")
  author = models.ForeignKey(User,on_delete=models.SET_DEFAULT,default=0,related_name="courses",blank=False,null=False)
  published = models.BooleanField("publiée",default=False)
  content = models.TextField(verbose_name="contenu",blank=False,null=True)


  def __str__(self):
    return self.name

  def save(self, *args,**kwargs):
    if not self.slug:
      self.slug = slugify(self.name)
    return super().save(*args,**kwargs)

