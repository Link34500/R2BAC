from django.urls import path
from .views import *

app_name = "panel"

urlpatterns = [
  path("api/get/",get_subjects,name="api_get_subjects"),
  path("",PanelView.as_view(),name="home"),
  path("users/",UsersView.as_view(),name="users"),
  path("logs/",LogsView.as_view(),name="logs"),
  path("courses/",CoursesView.as_view(),name="courses"),
  path("chapters/",ChatpersView.as_view(),name="chapters"),
  path("course/create/",CreateCourseView.as_view(),name="create_course"),
  path("course/edit/<int:pk>/",EditCourseView.as_view(),name="edit_course"),
  path("course/delete/<int:pk>/",DeleteCourseView.as_view(),name="delete_course"),
  path("chapter/create/",CreateChapterView.as_view(),name="create_chapter"),
  path("chapter/edit/<int:pk>/",EditChapterView.as_view(),name="edit_chapter"),
  path("chapter/delete/<int:pk>/",DeleteChapterView.as_view(),name="delete_chapter"),
]