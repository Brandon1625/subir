# Generated by Django 2.2.4 on 2019-08-28 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0002_producto_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='activo',
            field=models.BooleanField(default=True, verbose_name='activo'),
        ),
        migrations.AddField(
            model_name='producto',
            name='visible',
            field=models.BooleanField(default=True, verbose_name='visible'),
        ),
    ]
