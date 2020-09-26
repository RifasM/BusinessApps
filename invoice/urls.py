from django.urls import path

from invoice import views

app_name = "invoice"

urlpatterns = [
    path("", views.landing, name="landing_page"),
    path("create/", views.create, name="create"),
    path("saveAdd/", views.save_add, name="save_add"),
    path("saveTax/", views.save_tax, name="save_tax"),
    path("savePrint/", views.save_print, name="save_print"),
    path("save/", views.save, name="save"),
    path("print/<invoice_number>", views.print_invoice, name="print_inv"),
    path("modify/", views.modify_page, name="modify_page"),
    path("modify/<invoice_number>", views.modify, name="modify"),
]
