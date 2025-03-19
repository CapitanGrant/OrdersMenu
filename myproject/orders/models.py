from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [('waiting', 'В ожидании'),
                      ('ready', 'Готово'),
                      ('paid', 'Оплачено')]
    id = models.AutoField(primary_key=True)  # Уникальный идентификатор
    table_number = models.IntegerField()  # номер стола
    items = models.JSONField()  # список заказанных блюд с ценами
    total_price = models.FloatField(default=0)  # общая стоимость заказа
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='waiting')  # статус заказа: “в ожидании”, “готово”, “оплачено”

    def __str__(self):
        return f'Заказ #{self.id} (Стол {self.table_number}) - {self.total_price} руб.'

    def save(self, *args, **kwargs):
        self.total_price = sum(item['price'] for item in self.items)
        super().save(*args, **kwargs)
