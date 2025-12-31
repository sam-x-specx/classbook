from django.urls import path
from .import views

app_name = "stdadd" # <-- appname

urlpatterns = [
    path("/studentadder", views.stdadd ,name='stdadder'), # <-- htmlpage(stdadder) as name send to base.html and url show like "/stdadd" on that page
    path("/password", views.stdadd ,name='password_prompt'), # <-- htmlpage(stdadder) as name send to base.html and url show like "/stdadd" on that page
]
