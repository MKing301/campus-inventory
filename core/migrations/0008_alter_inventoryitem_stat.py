# Generated by Django 3.2.12 on 2023-09-22 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20230922_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='stat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.itemstatus'),
        ),
    ]