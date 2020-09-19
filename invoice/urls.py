from django.urls import path, include
from invoice import views

app_name = "invoice"

urlpatterns = [
    path("", views.landing, name="landing_page"),
    path("create", views.create, name="create"),
    path("modify", views.modify, name="modify"),
]
