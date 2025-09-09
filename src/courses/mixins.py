from .models import *
from django.shortcuts import get_object_or_404

class TitleMixin:
  title = ""

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update({"title":self.title})
    return context
  


class ContextUrlMixin:
  def transform_context_url(self):
    context = {}

    if self.kwargs.get('grade_id',None):
      grade = get_object_or_404(Grade,slug=self.kwargs['grade_id'])
      context.update({'grade':grade})
    if self.kwargs.get('subject_id',None):
      subject = get_object_or_404(grade.subjects,slug=self.kwargs['subject_id'])
      context.update({'subject':subject})
    if self.kwargs.get('chapter_id',None):
      chapter = get_object_or_404(subject.chapters,slug=self.kwargs['chapter_id'])
      context.update({'chapter':chapter})
    if self.kwargs.get('course_id',None):
      course = get_object_or_404(subject.chapters,slug=self.kwargs['course_id'])
      context.update({'course':course})
    return context

  def get_context_data(self,**kwargs):
    context = super().get_context_data(**kwargs)
    context.update(self.transform_context_url())

    return context


  def get_queryset(self,*args,**kwargs):
    context_url = self.transform_context_url()

    if context_url.get("chapter"):
      return Course.objects.filter(chapter=context_url['chapter'])

    if context_url.get("subject"):
      return Chapter.objects.filter(subject=context_url['subject'])

    if context_url.get("grade"):
      return Subject.objects.filter(grade=context_url['grade'])

    return super().get_queryset(*args,**kwargs)
