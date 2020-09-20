import json

from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from invoice.forms import InvoiceForm, InitialInvoice, ItemForm
from invoice.models import Invoice


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


def process_request(request):
    """
    Function to process items
    :param request: User request
    :return: Processed initial_data and data
    """
    initial_data = request.POST["initial_data"]
    old_data = json.loads(request.POST["prev_data"].replace("'", "\"")) if "prev_data" in request.POST else None
    data = []
    try:
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
    except MultiValueDictKeyError:
        data = old_data

    return initial_data, data


def save_add(request):
    """
    Return View with added item
    :param request: User Request(POST)
    :return: Added Item View
    """
    if request.method == "POST":
        initial_data, data = process_request(request)
        return render(request,
                      "invoice/invoice_create.html",
                      {
                          "form": ItemForm(),
                          "stage": "2",
                          "prev_data": data,
                          "initial_data": initial_data
                      })


def save_tax(request):
    """
    View to return fields related to taxes
    :param: User Request(POST)
    :return: return tax and totalling data
    """
    if request.method == "POST":
        initial_data, data = process_request(request)
        return render(request,
                      "invoice/invoice_create.html",
                      {
                          "form": InvoiceForm,
                          "stage": "3",
                          "prev_data": data,
                          "initial_data": initial_data
                      })


def save_print(request):
    """
    Return Final View of Invoice
    :param request: User Request (POST)
    :return: Return Preview
    """
    if request.method == "POST":
        initial_data, data = process_request(request)
        tax_data = {
            "invoice_number": request.POST["invoice_number"],
            "s_gst": request.POST["s_gst"],
            "c_gst": request.POST["c_gst"],
            "other_charges": request.POST["other_charges"],
            "grand_total": request.POST["grand_total"],
            "additional_notes": request.POST["additional_notes"]
        }

        if request.POST["invoice_number"] is not "" \
                and \
                Invoice.objects.get(pk=tax_data.get("invoice_number")) is not None:
            error = "Error, Invoice number Exists"
            return render(request,
                          "invoice/invoice_create.html",
                          {
                              "form": InvoiceForm,
                              "stage": "3",
                              "prev_data": data,
                              "initial_data": initial_data,
                              "error": error
                          })

        print(initial_data, data)
        pass


def modify(request):
    """
    Return and process Requests involving
    Modification of Invoices
    :param request: User Request (Get and Post)
    :return: Modification Page on GET, Display Invoice on POST
    """
    pass
