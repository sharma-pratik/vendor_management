# your_app_name/serializers.py
from rest_framework import serializers
from vendor.models import Vendor, PurchaseOrder


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        exclude = [ 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate', 'id']

class PurchaseOrderSerializer(serializers.ModelSerializer):

    vendor_id = serializers.CharField()

    class Meta:
        model = PurchaseOrder
        fields = ['vendor_id', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'po_id', 'quality_rating']

    def validate_vendor_id(self, vendor_id):
        """
            Validating the vendor id exists for not
        """
        try:
            vendor = Vendor.objects.get(vendor_id=vendor_id)
            return vendor.pk
        except Vendor.DoesNotExist:
            raise serializers.ValidationError('Invalid vendor id')
    
    def validate(self, attrs):
        """
            Validating during edit operation on purchase order, that it's
            status should be in pending state.
        """

        if self.instance and self.instance.status != PurchaseOrder.PoStatus.PENDING.value:
            raise serializers.ValidationError("Order should be in pending state.")
        return super().validate(attrs)



class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        exclude = ['id', 'vendor', 'date']
