from django.db.models.signals import post_save
from django.dispatch import receiver
from vendor.models import Vendor, PurchaseOrder, HistoricalPerformance
from  django.db.models import Count, Avg, Q,F, DurationField, FloatField, ExpressionWrapper
from  django.db.models.functions import Cast


@receiver(post_save, sender=PurchaseOrder)
def update_historical_analytics_data(sender, **kwargs):
    """
        Function will update historical data for the given vendor
        This will update only when there is edit operation is 
        performed. Also in 2 cases more, when acknowledge date get
        changed and when status of purchase set to complete.
    """
    instance = kwargs["instance"]
    vendor = instance.vendor
    update_fields = {} # dict for updating the historical performance model instance

    # checking is purchase order is not created
    if kwargs['created'] == False:

        # Checking if acknowledge date has been changed
        if instance.previous_acknowledgment_date !=  instance.acknowledgment_date:
            avg_time_diff =  PurchaseOrder.objects.filter(
                vendor=vendor,
            ).aggregate(
                average_time_difference=Avg(
                    ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField()),
                    filter=Q(acknowledgment_date__isnull=False))
            )['average_time_difference']

            average_time_diff_in_days = avg_time_diff.seconds / (24 * 3600)

            update_fields = {
                "average_response_time" : average_time_diff_in_days
            }

        # Checking if instance is set completed
        if instance.status == PurchaseOrder.PoStatus.COMPLETE.value:

            result = PurchaseOrder.objects.filter(
                vendor=vendor,
            ).aggregate(
                total_ontime_delivered_orders=Count('id', filter=Q(delivery_date__lte=F('estimated_delivery_date'))),
                total_completed_orders=Count('id', filter=Q(status="completed")),
                total_orders=Count('id'),
                avg_quality_rating=Avg('quality_rating', filter=Q(status=PurchaseOrder.PoStatus.COMPLETE.value)),
                avg_on_time_delivery_Rate=Cast(F('total_ontime_delivered_orders') * 100 / F('total_completed_orders'),
                                            FloatField()),
                fullfillment_rate=Cast(F('total_completed_orders') * 100 / F('total_orders'), FloatField())
            )

            update_fields = {
                'on_time_delivery_rate' : result['avg_on_time_delivery_Rate'],
                'quality_rating_avg' : result['avg_quality_rating'],
                'fulfillment_rate' : result['fullfillment_rate']
            }

        HistoricalPerformance.objects.filter(
            vendor=vendor
        ).update(
            **update_fields
        )


@receiver(post_save, sender=Vendor)
def create_vendor_default_historical_record(sender, **kwargs):
    """
        This function will create HistoricalPerformance instance 
        for that vendor when vendor get created
    """

    if kwargs['created']:
        instance = kwargs['instance']
        HistoricalPerformance.objects.create(
            vendor=instance
        )