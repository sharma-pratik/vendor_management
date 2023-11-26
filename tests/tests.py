from tests.fixtures import django_client, init_db
from vendor.models import *
from django.urls import *
import pytest
from datetime import datetime, timedelta
from rest_framework import status



@pytest.mark.django_db
def test_create_po_order(django_client):
    po_url = reverse('purchaseorder-list')
    vendor = Vendor.objects.first()
    request_data = {
        "vendor_id" : vendor.vendor_id,
        "estimated_delivery_date" : datetime.now() + timedelta(days=3),
        "items" : '{"products" : ["milk"]}',
        "quantity" : 1,
    }

    response = django_client.post(
        po_url,
        data=request_data
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_acknowledge_po_order(django_client):
    po_obj = PurchaseOrder.objects.filter(status=PurchaseOrder.PoStatus.PENDING.value).last()
    
    po_url = reverse('purchaseorder-acknowledge-po', kwargs={"po_id": po_obj.po_id})

    response = django_client.get(po_url)
    assert response.status_code == status.HTTP_200_OK



@pytest.mark.django_db
def test_complete_order(django_client):
    po_obj = PurchaseOrder.objects.filter(status=PurchaseOrder.PoStatus.PENDING.value).last()
    
    po_url = reverse('purchaseorder-detail', kwargs={"po_id": po_obj.po_id})
    request_data = {
        "status" : PurchaseOrder.PoStatus.COMPLETE.value,
        "delivery_date" : (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
        "quality_rating" : 10
    }
    import json
    response = django_client.patch(po_url, data=json.dumps(request_data), content_type="application/json")
    print(response.content)
    assert response.status_code == status.HTTP_200_OK

    po_obj.refresh_from_db()

    assert po_obj.quality_rating == 10
    assert po_obj.delivery_date !=None