import json
from datetime import datetime

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from invoice.forms import InvoiceForm, InitialInvoice, ItemForm


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
    if request.method == "POST":
        form = InitialInvoice(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            return render(request,
                          "invoice/invoice_create.html",
                          {
                              "form": ItemForm(),
                              "stage": "2",
                              "initial_data": data
                          })

    return render(request,
                  "invoice/invoice_create.html",
                  {
                      "form": InitialInvoice(),
                      "stage": "1"
                  })


def save_add(request):
    if request.method == "POST":
        initial_data = request.POST["initial_data"]
        old_data = json.loads(request.POST["prev_data"].replace("'", "\"")) if "prev_data" in request.POST else None
        data = []
        if old_data is not None:
            data += old_data
        data.append({
            "short_description": request.POST["short_description"],
            "particulars": request.POST["particulars"],
            "quantity": request.POST["quantity"],
            "unit": request.POST["unit"],
            "unit_price": request.POST["unit_price"],
            "total": str(float(request.POST["quantity"]) * float(request.POST["unit_price"]))
        })
        return render(request,
                      "invoice/invoice_create.html",
                      {
                          "form": ItemForm(),
                          "stage": "2",
                          "prev_data": data,
                          "initial_data": initial_data
                      })


def modify(request):
    """
    Return and process Requests involving
    Modification of Invoices
    :param request: User Request (Get and Post)
    :return: Modification Page on GET, Display Invoice on POST
    """
    pass
