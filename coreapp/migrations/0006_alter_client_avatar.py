# Generated by Django 4.1.3 on 2022-11-30 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0005_alter_client_options_alter_client_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='avatar',
            field=models.ImageField(default='avatars/default.svg', upload_to='avatars/'),
        ),
    ]