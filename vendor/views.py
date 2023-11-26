import datetime

from rest_framework import viewsets
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from vendor.serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class VendorViewSet(viewsets.ModelViewSet):
    """

        Endpoint for performing CRUD operation for Vendor and getting analytics data of purchase orders
    
    """

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'vendor_id'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True)
    def analytic_matrix(self, request, *args, **kwargs):
        """
            function to fetch the historical performance data of purchase orders 
            by specific vendor

            PARAMTERS
            ---------
            request : Request
            args : *args
            kwargs : **kwargs

            RETURN
            ------
            Response : 200 returning json data containg analytics data
            Response : 404 returning not found  
        """

        obj = self.get_object()
        try:
            historical_obj = HistoricalPerformance.objects.get(vendor=obj)
            response_data = {
                "on_time_delivery_rate": historical_obj.on_time_delivery_rate,
                "quality_rating_avg": historical_obj.quality_rating_avg,
                "average_response_time": historical_obj.average_response_time,
                "fulfillment_rate": historical_obj.fulfillment_rate
            }
        except HistoricalPerformance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK, data=response_data)


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'po_id'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True)
    def acknowledge_po(self, request, *args, **kwargs):
        """
            function to update the acknowledge date time for the purchase order

            PARAMTERS
            ---------
            request : Request
            args : *args
            kwargs : **kwargs

            RETURN
            ------
            Response : 200 on successsfully updating the acknowledge date
            Response : 400 on error 
            Respone : 404 on purchase order not found
        """
        obj = self.get_object()

        # To validate to check if status is completed
        ser = self.serializer_class(obj, partial=True, data={})
        ser.is_valid(raise_exception=True)
        obj.acknowledgment_date = datetime.datetime.now()
        obj.save()

        return Response(status=status.HTTP_200_OK)