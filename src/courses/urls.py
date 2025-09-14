from django.urls import path
from .views import *

app_name = "courses"
urlpatterns = [
  path("",GradeListView.as_view(),name="grade_list"),
  path("<slug:grade_id>/",SubjectListView.as_view(),name="subject_list"),
  path("<slug:grade_id>/<slug:subject_id>/",ChapterListView.as_view(),name="chapter_list"),
  path("<slug:grade_id>/<slug:subject_id>/<slug:chapter_id>/",CourseListView.as_view(),name="course_list"),
  path("<slug:grade_id>/<slug:subject_id>/<slug:chapter_id>/<slug:course_id>/",CourseView.as_view(),name="course"),
  path("comment/delete/<int:pk>", DeleteCommentView.as_view(), name="delete_comment"),
]