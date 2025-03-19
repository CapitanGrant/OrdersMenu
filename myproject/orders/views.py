from rest_framework import generics, status
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.views import APIView

from .models import Order
from .serializers import OrderSerializer


class OrderRegistration(generics.CreateAPIView):
    serializer_class = OrderSerializer


class OrderFilter(filters.FilterSet):
    table_number = filters.CharFilter(field_name='table_number')
    status = filters.CharFilter(field_name='status')

    class Meta:
        model = Order
        fields = ['table_number', 'status']


class OrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = OrderFilter


class OrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderUpdate(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDeleteAll(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def delete(self, request, *args, **kwargs):
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderDelete(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class RevenueCalculation(APIView):
    def get(self, request):
        paid_orders = Order.objects.filter(status='paid')
        total_revenue = sum(order.total_price for order in paid_orders)
        return Response({'total_revenue': total_revenue}, status=status.HTTP_200_OK)