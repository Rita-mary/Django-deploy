# Generated by Django 4.0.4 on 2022-06-19 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_product_sller_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='sller_name',
            new_name='seller_name',
        ),
    ]
