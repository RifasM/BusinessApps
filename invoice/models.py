from djongo import models

unit_choices = (("Sq. Mtr", "sq_mtr"),
                ("Sq. Ft", "sq_ft"),
                ("Unit(s)", "unit"))


class Item(models.Model):
    """
    Model to hold Items/Particulars
    """
    short_description = models.CharField(max_length=30,
                                         help_text="Short Description",
                                         blank=False)
    particulars = models.CharField(max_length=3000,
                                   help_text="Item Particulars",
                                   blank=False)
    quantity = models.IntegerField(help_text="Quantity of Item",
                                   blank=False)
    unit = models.CharField(max_length=5,
                            help_text="Unit of Item",
                            choices=unit_choices)
    unit_price = models.IntegerField(help_text="Unit Price of Item",
                                     blank=False)
    total_cost = models.IntegerField(default=quantity * unit_price,
                                     blank=False)

    class Meta:
        abstract = True
        ordering = ["short_description"]

    def __str__(self):
        return self.short_description

    def get_total(self):
        return self.total_cost


class Invoice(models.Model):
    """
    Invoice Model
    """
    number = models.AutoField(primary_key=True,
                              help_text="Invoice Number",
                              blank=False)
    invoice_date = models.DateField(auto_now_add=True)
    reference_number = models.CharField(max_length=30,
                                        help_text="Enter Reference Number/PO",
                                        blank=False)
    reference_dated = models.DateField(help_text="PO/Order Date",
                                       blank=False)
    addressed_to = models.CharField(max_length=300,
                                    help_text="Invoice Addressed To",
                                    blank=False)
    party_gst = models.CharField(max_length=15,
                                 help_text="GST Number of buyer",
                                 blank=True)
    created_at = models.DateTimeField(auto_created=True, editable=False)
    modified_at = models.DateField(auto_now_add=True)
    notes = models.CharField(max_length=1000,
                             blank=True,
                             help_text="Additional Notes")
    items = models.ArrayField(model_container=Item)
    s_gst = models.IntegerField(help_text="S_GST Percentage",
                                default=9)
    c_gst = models.IntegerField(help_text="C_GST Percentage",
                                default=9)
    other_charges = models.IntegerField(help_text="Other Charges as needed")
    total = models.IntegerField(help_text="Invoice Total")

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return "{}".format(self.number)
