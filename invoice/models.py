from djongo import models

unit_choices = (("Sq. Mtr", "Sq. Mtr"),
                ("Sq. Ft", "Sq. Ft"),
                ("Unit(s)", "Unit(s)"))


class Item(models.Model):
    """
    Model to hold Items/Particulars
    """
    short_description = models.CharField(max_length=30,
                                         help_text="Short Description",
                                         blank=False)
    particulars = models.TextField(max_length=3000,
                                   help_text="Item Particulars",
                                   blank=False)
    quantity = models.FloatField(help_text="Quantity of Item",
                                 blank=False)
    unit = models.CharField(max_length=5,
                            help_text="Unit of Item",
                            choices=unit_choices)
    unit_price = models.FloatField(help_text="Unit Price of Item",
                                   blank=False)
    total_cost = models.FloatField(help_text="Total",
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
    invoice_date = models.DateField(help_text="Invoice Date",
                                    blank=False)
    reference_number = models.CharField(max_length=30,
                                        help_text="Enter Reference Number/PO",
                                        blank=False)
    reference_date = models.DateField(help_text="PO/Order Date",
                                      blank=False)
    addressed_to = models.TextField(max_length=300,
                                    help_text="Invoice Addressed To",
                                    blank=False)
    party_gst = models.CharField(max_length=15,
                                 help_text="GST Number of buyer",
                                 blank=True)
    created_at = models.DateTimeField(auto_created=True, editable=False)
    modified_at = models.DateField(auto_now_add=True)
    notes = models.TextField(max_length=1000,
                             blank=True,
                             help_text="Additional Notes")
    items = models.ArrayField(model_container=Item)
    s_gst = models.FloatField(help_text="S_GST Percentage",
                              default=9)
    c_gst = models.FloatField(help_text="C_GST Percentage",
                              default=9)
    other_charges = models.FloatField(help_text="Other Charges as needed")
    total = models.FloatField(help_text="Invoice Total")

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return "{}".format(self.number)
