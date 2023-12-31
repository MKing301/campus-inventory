# Generated by Django 4.2.5 on 2023-09-27 00:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_area_map_loc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='item_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.area'),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='item_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.maplocation'),
        ),
    ]
