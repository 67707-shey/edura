from . import views
from django.urls import path

app_name = 'students'

urlpatterns = [
    path("list/", views.student_list, name = "student_list"),
    path("crea te/", views.student_create, name = "student_create")
]