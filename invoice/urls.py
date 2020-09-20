from django.urls import path

from invoice import views

app_name = "invoice"

urlpatterns = [
    path("", views.landing, name="landing_page"),
    path("create/", views.create, name="create"),
    path("saveAdd/", views.save_add, name="save_add"),
    path("saveTax/", views.save_tax, name="save_tax"),
    path("savePrint/", views.save_print, name="save_print"),
    path("modify/", views.modify, name="modify"),
]
