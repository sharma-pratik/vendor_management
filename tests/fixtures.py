import pytest
from vendor.models import Vendor, PurchaseOrder, HistoricalPerformance
from django.test import Client
from datetime import datetime, timedelta
import random
from django.db.models import Count, Avg, Q,F, DurationField, FloatField, ExpressionWrapper
from django.db.models.functions import Cast
import uuid
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@pytest.fixture
def init_db():
    """
        Creating default vendor and purchase data for test cases
    """
    vendor = Vendor.objects.create(name="Vendor 1", contact_details="+919999999999", address="test address")

    # creating 10 on time purchase orders
    current_time = datetime.now()
    for i in range(10):
        PurchaseOrder.objects.create(
            po_id = uuid.uuid4(),   
            vendor = vendor,
            delivery_date = current_time + timedelta(days=2),
            estimated_delivery_date = current_time + timedelta(days=3),
            items = {"products" : ["milk", "fruits basket"]},
            quantity = 2,
            status = PurchaseOrder.PoStatus.COMPLETE.value,
            quality_rating = random.randint(8, 10),
            acknowledgment_date = current_time + timedelta(days=1)
        )

    # creating complete orders which are not on time one's
    for i in range(10):
        PurchaseOrder.objects.create(
            po_id = uuid.uuid4(),
            vendor = vendor,
            delivery_date = current_time + timedelta(days=4),
            estimated_delivery_date = current_time + timedelta(days=3),
            items = {"products" : ["milk", "fruits basket"]},
            quantity = 2,
            status = PurchaseOrder.PoStatus.COMPLETE.value,
            quality_rating = random.randint(4, 7),
            acknowledgment_date = current_time + timedelta(days=2)
        )

    # creating pending orders
    for i in range(4):
        PurchaseOrder.objects.create(
            po_id = uuid.uuid4(),
            vendor = vendor,
            estimated_delivery_date = current_time + timedelta(days=6),
            items = {"products" : ["milk", "fruits basket"]},
            quantity = 2,
            status = PurchaseOrder.PoStatus.PENDING.value,
            acknowledgment_date = current_time + timedelta(days=3)
        )

    # create a normal pending order
    PurchaseOrder.objects.create(
            po_id = uuid.uuid4(),
            vendor = vendor,
            estimated_delivery_date = current_time + timedelta(days=3),
            items = {"products" : ["milk", "fruits basket"]},
            quantity = 2,
            status = PurchaseOrder.PoStatus.PENDING.value
        )

    # creating cancelled orders
    for i in range(4):
        PurchaseOrder.objects.create(
            po_id = uuid.uuid4(),
            vendor = vendor,
            estimated_delivery_date = current_time + timedelta(days=7),
            items = {"products" : ["milk", "fruits basket"]},
            quantity = 2,
            status = PurchaseOrder.PoStatus.CANCELED.value,
            acknowledgment_date = current_time + timedelta(days=4)
        )

    # Set historical data
    result = PurchaseOrder.objects.filter(
                vendor=vendor,
            ).aggregate(
                total_ontime_delivered_orders=Count('id', filter=Q(delivery_date__lte=F('estimated_delivery_date'))),
                total_completed_orders=Count('id', filter=Q(status="completed")),
                total_orders=Count('id'),
                avg_quality_rating=Avg('quality_rating', filter=Q(status=PurchaseOrder.PoStatus.COMPLETE.value)),
                avg_on_time_delivery_Rate=Cast(F('total_ontime_delivered_orders') * 100 / F('total_completed_orders'),
                                            FloatField()),
                fullfillment_rate=Cast(F('total_completed_orders') * 100 / F('total_orders'), FloatField()),
                average_time_difference=Avg(
                    ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField()),
                    filter=Q(acknowledgment_date__isnull=False))
            )

    average_time_diff_in_days = result['average_time_difference'].days
        
    update_fields = {
                'on_time_delivery_rate' : result['avg_on_time_delivery_Rate'],
                'quality_rating_avg' : result['avg_quality_rating'],
                'fulfillment_rate' : result['fullfillment_rate'],
                "average_response_time" : average_time_diff_in_days
            }
    
    HistoricalPerformance.objects.filter(
            vendor=vendor
        ).update(
            **update_fields
        )

    yield

@pytest.fixture
def django_client(init_db):
    client = APIClient()

    user = User.objects.create_user(username='testuser', password='testpassword')
    token = Token.objects.create(user=user)

    # Include the token in the Authorization header
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    yield client
