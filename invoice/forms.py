from django import forms

from invoice.models import unit_choices


class InitialInvoice(forms.Form):
    reference_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "PO/Reference Number"
            }),
        required=True
    )
    reference_date = forms.DateField(
        widget=forms.SelectDateWidget(
            attrs={
                "class": "form-control"
            }
        ),
        required=True
    )
    addressed_to = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Party Address"
            }
        ),
        required=True
    )
    party_gst = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Party GST"
            }
        ),
        required=True
    )


class ItemForm(forms.Form):
    short_description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Short Description"
            }
        ),
        required=True
    )
    particulars = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Particulars"
            }
        ),
        required=True
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Quantity",
            }),
        required=True
    )
    unit = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        ),
        choices=unit_choices,
        required=True
    )
    unit_price = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Unit Price"
            }
        ),
        required=True
    )
    total = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Total"
            }
        ),
        required=False
    )


class InvoiceForm(forms.Form):
    invoice_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Invoice Number",
            }),
        required=False
    )
    s_gst = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "S GST Percentage",
            }),
        required=True,
        initial=9
    )
    c_gst = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "C GST Percentage",
            }),
        required=True,
        initial=9
    )
    other_charges = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Other Charges",
            }),
        required=True,
        initial=0
    )
    grand_total = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Grand Total",
            }),
        required=True
    )
    additional_notes = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Additional Notes"
            }
        ),
        required=False,
        max_length=50
    )
