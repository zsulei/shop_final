# Generated by Django 4.1.3 on 2022-12-05 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0008_remove_adminlog_products_product_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_popular',
            field=models.BooleanField(default=False),
        ),
    ]