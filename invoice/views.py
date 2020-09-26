import datetime
import json
import re

from django.shortcuts import render, redirect
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

    data = Invoice.objects.all().order_by("-number")[:10]

    return render(request,
                  "invoice/invoice_landing.html",
                  {
                      "invoices": data
                  })


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
    if re.search("datetime.date\\((.*?)\\)", initial_data):
        date_val = re.findall("datetime.date\\((.*?)\\)", initial_data)
        for date in date_val:
            dates = list(map(int, date.split(", ")))
            initial_data = re.sub("datetime.date\\((.*?)\\)",
                                  "'" + datetime.date(dates[0], dates[1], dates[2]).strftime("%d %B, %Y") + "'",
                                  initial_data, 1)
    initial_data = json.loads(initial_data.replace("'", "\""))

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
            "total_cost": str(float(request.POST["quantity"]) * float(request.POST["unit_price"]))
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
            "s_gst": request.POST["s_gst"],
            "c_gst": request.POST["c_gst"],
            "other_charges": request.POST["other_charges"],
            "additional_notes": request.POST["additional_notes"]
        }

        if request.POST["invoice_number"] == "":
            inv_num = Invoice.objects.order_by("-number").first()

            if inv_num is None:
                inv_num = 1
            else:
                inv_num = inv_num.number + 1

        elif request.POST["invoice_number"] != "" \
                and \
                Invoice.objects.filter(number=request.POST["invoice_number"]).exists():
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
        else:
            inv_num = request.POST["invoice_number"]

        sub_total = sum([float(a.get("total_cost")) for a in data])
        grand_total = sub_total + float(tax_data.get("other_charges")) + \
                      ((float(request.POST["s_gst"]) +
                        float(request.POST["c_gst"])) / 100) * sub_total

        return render(request,
                      "invoice/invoice_preview.html",
                      {
                          "invoice_number": inv_num,
                          "initial_data": initial_data,
                          "prev_data": data,
                          "sub_total": sub_total,
                          "tax_data": tax_data,
                          "grand_total": grand_total
                      })


def save(request):
    """
    View to save and print Invoice
    :param request: User Request (POST)
    :return: Return Printable view
    """
    inv_num = request.POST["invoice_number"]
    initial_data, data = process_request(request)
    tax_data = json.loads(request.POST["tax_data"].replace("'", "\""))
    grand_total = request.POST["grand_total"]

    Invoice.objects.create(number=inv_num,
                           invoice_date=datetime.datetime.strptime(initial_data.get("invoice_date"), "%d %B, %Y"),
                           reference_number=initial_data.get("reference_number"),
                           reference_date=datetime.datetime.strptime(initial_data.get("reference_date"), "%d %B, %Y"),
                           addressed_to=initial_data.get("addressed_to"),
                           party_gst=initial_data.get("party_gst"),
                           created_at=datetime.datetime.now(),
                           modified_at=datetime.datetime.now(),
                           notes=tax_data.get("additional_notes"),
                           items=data,
                           s_gst=tax_data.get("s_gst"),
                           c_gst=tax_data.get("c_gst"),
                           other_charges=tax_data.get("other_charges"),
                           total=grand_total
                           ).save()

    return redirect("/invoice/print/" + inv_num)


def print_invoice(request, invoice_number):
    """
    Return the invoice print page for given invoice number
    :param request: User request(GET)
    :param invoice_number: Required invoice number to print
    :return: Rendered Invoice Page
    """

    data = Invoice.objects.get(number=invoice_number)

    sub_total = sum([a.get("total_cost") for a in data.items])
    s_gst_val = float(sub_total) * (float(data.s_gst) / 100)
    c_gst_val = float(sub_total) * (float(data.c_gst) / 100)

    return render(request,
                  "invoice/invoice_print.html",
                  {
                      "data": data,
                      "sub_total": sub_total,
                      "s_gst_value": s_gst_val,
                      "c_gst_value": c_gst_val
                  })


def modify(request, invoice_number):
    """
    Return and process Requests involving
    Modification of Invoices
    :param invoice_number: Invoice Number to modify
    :param request: User Request (Get and Post)
    :return: Modification Page on GET, Display Invoice on POST
    """
    if request.method == "POST":
        n = Invoice.objects.filter(number=request.POST["invoice_number"])
        items = n.get().items

        for i, item in enumerate(items):
            item["short_description"] = request.POST[str(i + 1) + "_short_description"]
            item["particulars"] = request.POST[str(i + 1) + "_particulars"]
            item["quantity"] = request.POST[str(i + 1) + "_quantity"]
            item["unit"] = request.POST[str(i + 1) + "_unit"]
            item["unit_price"] = request.POST[str(i + 1) + "_unit_price"]
            item["total_cost"] = request.POST[str(i + 1) + "_total_cost"]

        n.update(
            number=request.POST["invoice_number"],
            invoice_date=request.POST["invoice_date"],
            reference_number=request.POST["reference_number"],
            reference_date=request.POST["reference_date"],
            addressed_to=request.POST["addressed_to"],
            party_gst=request.POST["party_gst"],
            items=items,
            c_gst=request.POST["c_gst"],
            s_gst=request.POST["s_gst"],
            other_charges=request.POST["other_charges"],
            notes=request.POST["additional_notes"],
            total=request.POST["total"],
            modified_at=datetime.datetime.now()
        )
        return redirect("index_page")

    data = Invoice.objects.get(number=invoice_number)

    sub_total = sum([a.get("total_cost") for a in data.items])

    return render(request,
                  "invoice/invoice_modify.html",
                  {
                      "invoice": data,
                      "sub_total": sub_total
                  })


def modify_page(request):
    """
    Render Modification Page
    :param request: User Request (GET)
    :return: Modification Page
    """
    pass
