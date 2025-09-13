from django.shortcuts import get_object_or_404
from django.views.generic import *
from django.urls import reverse,reverse_lazy
from .models import *
from .forms import *
from courses.models import Course,Chapter
from django.http import JsonResponse,Http404
from .mixins import PanelPageMixin

# Create your views here.

class PanelView(PanelPageMixin,TemplateView):
    template_name = "panel/views/index.html"

class UsersView(PanelPageMixin,ListView):
    model = User
    template_name = "panel/views/users.html"

    def get_queryset(self):
        return User.objects.all()

class LogsView(PanelPageMixin,ListView):
    model = Log
    template_name = "panel/views/logs.html"

    def get_paginate_by(self, queryset):
        """Controle le nombre de logs sur le serveur"""
        try:
            paginate_by = int(self.request.GET.get("paginate"))
        except:
            paginate_by = 10
        return paginate_by if paginate_by <= 100 else 100

    def get_queryset(self):
        return Log.objects.all()


class CoursesView(PanelPageMixin,ListView):
    model = Course
    template_name = "panel/views/course/courses.html"

    def get_queryset(self):
        return Course.objects.all()
    

class ChatpersView(PanelPageMixin,ListView):
    model = Chapter
    template_name = "panel/views/chapter/chapters.html"
    
    def get_queryset(self):
        return Chapter.objects.all()
    
class CreateCourseView(PanelPageMixin,CreateView):
    model = Course
    template_name = "panel/views/course/create_course.html"
    form_class = CourseForm
    

    def get_success_url(self):
        self.success_url = reverse("panel:edit_course",kwargs={"pk":self.object.id})
        return super().get_success_url()

    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        return super().form_valid(form)

class EditCourseView(PanelPageMixin,UpdateView):
    model = Course
    template_name = "panel/views/course/edit_course.html"
    form_class = CourseForm


    def get_success_url(self):
        self.success_url = self.request.path
        return super().get_success_url()

    def form_valid(self, form):
        self.object:Course = form.save(commit=False)
        self.object.contributors.set(form.cleaned_data["contributors"])
        return super().form_valid(form)

class DeleteCourseView(PanelPageMixin,DeleteView):
    model = Course
    template_name = "panel/components/delete.html"
    success_url = reverse_lazy("panel:courses")

class CreateChapterView(PanelPageMixin,CreateView):
    model = Chapter
    template_name = "panel/views/chapter/create_chapter.html"
    form_class = ChapterForm

    def get_success_url(self):
        self.success_url = reverse("panel:edit_chapter",kwargs={"pk":self.object.id})
        return super().get_success_url()
    
class EditChapterView(PanelPageMixin,UpdateView):
    model = Chapter
    template_name = "panel/views/chapter/edit_chapter.html"
    form_class = ChapterForm

    def get_success_url(self):
        self.success_url = self.request.path
        return super().get_success_url()

class DeleteChapterView(PanelPageMixin,DeleteView):
    model = Chapter
    template_name = "panel/components/delete.html"
    success_url = reverse_lazy("panel:chapters")

def get_subjects(request):
    if not request.user.is_staff:
        return Http404("Non staff")
    try:
        if request.GET.get("grade_id"):
            grade:Grade = Grade.objects.get(pk=int(request.GET.get("grade_id")))
            response = {"subjects":[[subject.id,subject.name] for subject in grade.subjects.all()]}
        elif request.GET.get("subject_id"):
            subject = Subject.objects.get(pk=int(request.GET.get("subject_id")))
            response = {"chapters":[[chapter.id,chapter.name] for chapter in subject.chapters.all()]}

        return JsonResponse(response,safe=True)
    except Exception as e:
        return JsonResponse({"error":str(e)},safe=True)
    