# Generated by Django 4.1.6 on 2023-04-29 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(default='2000-06-24', verbose_name='Date of Birth'),
            preserve_default=False,
        ),
    ]
