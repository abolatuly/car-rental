# Generated by Django 4.1.6 on 2023-04-29 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_status_alter_orderitem_car_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='number',
            field=models.CharField(default='1231231234', max_length=10, unique=True),
            preserve_default=False,
        ),
    ]
