# Generated by Django 4.2.5 on 2023-09-27 01:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_inventoryitem_item_area_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='map_loc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.maplocation'),
        ),
    ]
