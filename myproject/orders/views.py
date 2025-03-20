from venv import logger

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
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
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'orders/order_list.html'
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = OrderFilter
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            response.data = {'orders': response.data}
            logger.info("Запрос на получение списка заказов.")
            return response
        except Exception as e:
            logger.error(f"Ошибка при получении списка заказов: {e}")
            return Response(
                {"detail": "Произошла ошибка при получении списка заказов."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            logger.info(f"Запрос на получение деталей заказа с ID {kwargs['pk']}.")
            return super().retrieve(request, *args, **kwargs)
        except Order.DoesNotExist:
            logger.warning(f"Заказ с ID {kwargs['pk']} не найден.")
            return Response(
                {"detail": "Заказ не найден."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Ошибка при получении деталей заказа: {e}")
            return Response(
                {"detail": "Произошла ошибка при получении деталей заказа."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderUpdate(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info(f'Заказ с ID {instance.id} успешно обновлен.')
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Ошибка при обновлении заказа: {e}')
            return Response(
                {'detail': 'Произошла ошибка при обновлении заказа.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderDeleteAll(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            logger.warning("Попытка удалить все заказы, но заказы отсутствуют.")
            return Response({'detail': 'Заказы отсутствуют'}, status=status.HTTP_404_NOT_FOUND)
        queryset.delete()
        logger.info('Все заказы успешно удалены.')
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderDelete(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_destroy(self, instance):
        logger.info(f'Заказ с ID: {instance.id} удален.')
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'detail': 'Заказ успешно удален.'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Ошибка при удалении заказа: {e}')
            return Response({'detail': 'Произошла ошибка при удалении заказа.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RevenueCalculation(APIView):
    def get(self, request):
        paid_orders = Order.objects.filter(status='paid')
        total_revenue = sum(order.total_price for order in paid_orders)
        return Response({'total_revenue': total_revenue}, status=status.HTTP_200_OK)


create = {
    "table_number": 5,
    "items": [
        {"name": "Кофе", "price": 100},
        {"name": "Пирог", "price": 150}
    ],
    "status": "waiting"
}
