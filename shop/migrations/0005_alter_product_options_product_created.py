# Generated by Django 5.0.3 on 2024-05-22 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_region_customer_order_orderproduct_city_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-pk']},
        ),
        migrations.AddField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
