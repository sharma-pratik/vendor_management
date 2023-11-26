import datetime
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


def get_po_number():
    """
        Generting unique purchase order number with following format : "PO/ex34/0000001"
    """
    last_obj = PurchaseOrder.objects.last()

    last_num = 1
    if last_obj:
        last_num = last_obj.pk + 1

    po_number = "PO/" + uuid.uuid4().hex[0:3] + "/" + str(last_num).rjust(6, "0")
    return po_number


def get_vendor_code():
    """
        Generting unique vendor code number with following format : "VDR-a3ac-0000001"
    """
    last_obj = Vendor.objects.last()

    last_num = 1
    if last_obj:
        last_num = last_obj.pk + 1

    vdr_number = "VDR-" + uuid.uuid4().hex[0:3] + "-" + str(last_num).rjust(6, "0")
    return vdr_number


class Vendor(models.Model):

    vendor_id = models.UUIDField(default=uuid.uuid4(), unique=True)
    name = models.CharField(max_length=100)
    contact_details = models.TextField(max_length=100)
    address = models.TextField(max_length=255)
    vendor_code = models.CharField(max_length=50, unique=True, default=get_vendor_code)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)
 
    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):

    class PoStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETE = 'completed', 'Completed'
        CANCELED = 'canceled', 'Canceled'

    po_id = models.UUIDField(default=uuid.uuid4(), unique=True)
    po_number = models.CharField(max_length=50, unique=True, default=get_po_number)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="vendor_pos")
    order_date = models.DateTimeField(null=True)
    delivery_date = models.DateTimeField(null=True)
    estimated_delivery_date = models.DateTimeField(null=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, choices=PoStatus.choices, default=PoStatus.PENDING)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number + f'( {self.vendor.name} ) - status : {self.status}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # storing the existing acknowlegment date, in order to check if acknowledgment has been changed or not.
        self.previous_acknowledgment_date = self.acknowledgment_date


class HistoricalPerformance(models.Model):

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="vendor_analytics")
    date = models.DateTimeField(auto_now=True)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)