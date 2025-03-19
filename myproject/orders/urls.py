from django.urls import path
from .views import OrderRegistration, OrderDetail, OrderList, OrderDelete, OrderDeleteAll, RevenueCalculation, \
    OrderUpdate

urlpatterns = [
    path('orders/', OrderList.as_view(), name='order-list'),
    path('orders/create/', OrderRegistration.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderDetail.as_view(), name='order-detail'),
    path('orders/<int:pk>/update/', OrderUpdate.as_view(), name='order-update'),
    path('orders/<int:pk>/delete/', OrderDelete.as_view(), name='order-delete'),
    path('orders/delete-all/', OrderDeleteAll.as_view(), name='order-delete-all'),
    path('revenue/', RevenueCalculation.as_view(), name='revenue-calculation'),
]
