from django.views.generic import *
from .models import *
from .mixins import *
from .forms import CommentForm
from django.shortcuts import redirect
from django.urls import reverse


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

  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.course = self.object
      comment.author = request.user
      comment.save()
      return redirect(self.request.path)
    form = CommentForm()
    return self.get(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["form"] = CommentForm()
    context["comments"] = self.object.comments.all().order_by("-created_at")
    return context



class DeleteCommentView(DeleteView):
  model = Comment
  template_name = "courses/components/delete.html"
  
  def get_success_url(self):
    course = self.object.course
    return reverse("courses:course", kwargs={
      "grade_id": course.chapter.subject.grade.slug,
      "subject_id": course.chapter.subject.slug,
      "chapter_id": course.chapter.slug,
      "course_id": course.slug
    })