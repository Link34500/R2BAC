from django.views.generic import *
from .models import *
from .mixins import *
from django.shortcuts import get_object_or_404

# Create your views here.

class GradeListView(TitleMixin,ContextUrlMixin,ListView):
  title = "classes"
  """Affiche la listes des classes disponibles"""
  model = Grade
  template_name = "courses/views/lists/grade_list.html"

class SubjectListView(TitleMixin,ContextUrlMixin,ListView):
  """Affiche les matières disponible selon la classe"""
  title = "matières"
  model = Subject
  template_name = "courses/views/lists/subject_list.html"

  
class ChapterListView(TitleMixin,ContextUrlMixin,ListView):
  """Affiche les chapitres disponible selon la matière"""
  title = "chapitres"
  model = Chapter
  template_name = "courses/views/lists/chapter_list.html"
  
class CourseListView(TitleMixin,ContextUrlMixin,ListView):
  """Affiche les cours disponibles selon le chapitre."""
  title = "cours"
  model = Course
  template_name = "courses/views/lists/course_list.html"


class CourseView(DetailView):
  model = Course
  template_name = "courses/views/course.html"
  slug_field = "slug"
  slug_url_kwarg = "course_id"
  
