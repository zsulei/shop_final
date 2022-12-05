# Generated by Django 4.1.3 on 2022-11-30 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0004_alter_client_avatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ('first_name', 'last_name', 'username'), 'permissions': [('can_buy_products', 'this permission for simple buyers only')]},
        ),
        migrations.AlterField(
            model_name='client',
            name='avatar',
            field=models.ImageField(default='avatars/default.svg', upload_to='avatars'),
        ),
    ]