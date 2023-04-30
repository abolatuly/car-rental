# Generated by Django 4.1.6 on 2023-04-23 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rental_centers', '0006_alter_rentalcenter_location'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='drop_off_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='drop_off_location', to='rental_centers.rentalcenter', verbose_name='Drop-off location'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='orders.order'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='pick_up_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pick_up_location', to='rental_centers.rentalcenter', verbose_name='Pick-up location'),
        ),
    ]
