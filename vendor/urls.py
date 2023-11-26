from rest_framework.routers import DefaultRouter
from vendor.views import VendorViewSet, PurchaseOrderViewSet


router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase_orders', PurchaseOrderViewSet)