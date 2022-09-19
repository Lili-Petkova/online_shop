from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'order', views.OrderViewSet)
router.register(r'orderitem', views.OrderItemViewSet)
# router.register(r'order_book', views.OrderItemBookItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    ]
