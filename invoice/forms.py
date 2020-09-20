from django import forms

from invoice.models import Invoice, unit_choices


class InvoiceForm(forms.Form):
    invoice_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Invoice Number",
            })
    )
    reference_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Reference Number"
            }),
        required=True
    )
    reference_date = forms.DateInput(
        attrs={
            "class": "form-control"
        }
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
    total = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Total"
            }
        ),
        required=True
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

    class Meta:
        model = Invoice
        fields = ("invoice_date",
                  "reference_number",
                  "reference_date",
                  "addressed_to",
                  "party_gst",
                  "notes",
                  "items",
                  "s_gst",
                  "c_gst",
                  "other_charges",
                  "total")
