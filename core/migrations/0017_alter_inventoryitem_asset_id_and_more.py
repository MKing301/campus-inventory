# Generated by Django 4.2.5 on 2023-10-22 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_inventoryitem_asset_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='asset_id',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='purchased_from',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
