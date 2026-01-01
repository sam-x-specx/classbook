from django.urls import path
from .import views

app_name = "studentviewer" # <-- appname

urlpatterns = [
    path("", views.studentviewer ,name='studentviewerhome'), # <-- htmlpage as name(studentviewerhome) send in base.html
]
