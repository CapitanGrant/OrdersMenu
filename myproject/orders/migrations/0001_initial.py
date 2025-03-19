# Generated by Django 5.1.1 on 2025-03-19 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('table_number', models.IntegerField()),
                ('items', models.JSONField()),
                ('total_price', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('waiting', 'В ожидании'), ('ready', 'Готово'), ('paid', 'Оплачено')], default='waiting', max_length=10)),
            ],
        ),
    ]
