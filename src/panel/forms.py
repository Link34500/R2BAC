from django import forms
from courses.models import *

class ChapterForm(forms.ModelForm):
  CHOICES = Grade.objects.all()
  grade = forms.ChoiceField(choices=((x.id,x.name) for x in CHOICES),label="Classe")
  class Meta:
    model = Chapter
    fields = ["name","number","grade","subject","slug"]

class CourseForm(forms.ModelForm):
  CHOICES_GRADES = Grade.objects.all()
  CHOICES_SUBJECTS = Subject.objects.all()
  grade = forms.ChoiceField(choices=((x.id,x.name) for x in CHOICES_GRADES),label="Classe")
  subject = forms.ChoiceField(choices=((x.id,x.name) for x in CHOICES_SUBJECTS),label="Matière")
  class Meta:
    model = Course
    fields = ["name","grade","subject","chapter","published","content","contributors"]