from django.shortcuts import render
from invoice.forms import InvoiceForm


def landing(request):
    """
    Return and process Requests involving
    Creation of Invoices
    :param request: User Request (Get and Post)
    :return: Creation Page on GET, Display Invoice on POST
    """
    return render(request, "invoice/invoice_landing.html")


def create(request):
    """
    Return and process Requests involving
    Creation of Invoices
    :param request: User Request (Get and Post)
    :return: Creation Page on GET, Display Invoice on POST
    """
    return render(request,
                  "invoice/invoice_create.html",
                  {
                      "form": InvoiceForm()
                  })


def modify(request):
    """
    Return and process Requests involving
    Modification of Invoices
    :param request: User Request (Get and Post)
    :return: Modification Page on GET, Display Invoice on POST
    """
    pass
