from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate_table_number(self, value):
        if value < 1 or value > 50:
            raise serializers.ValidationError('Номер столика должен быть от 1 до 50.')
        return value

    def validate_items(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError('Поле items должно быть списком.')

        for item in value:
            if not isinstance(item, dict) or 'name' not in item or 'price' not in item:
                raise serializers.ValidationError('Каждый элемент items должен содержать name и price.')
            if not isinstance(item['price'], (int, float)) or item['price'] < 0:
                raise serializers.ValidationError('Цена блюда должна быть положительным числом.')

        return value

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f'Недопустимый статус заказа. Допустимые значения: {", ".join(valid_statuses)}.')
        return value

    def validate(self, data):
        if 'items' in data:
            data['total_price'] = sum(item['price'] for item in data['items'])

        return data