# Generated by Django 4.2.7 on 2023-11-26 18:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0006_alter_purchaseorder_po_id_alter_vendor_vendor_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='po_id',
            field=models.UUIDField(default=uuid.UUID('5c66eab2-d0c6-4b76-ae5b-e31e4ee0484e'), unique=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vendor_id',
            field=models.UUIDField(default=uuid.UUID('60c4cbbd-c24d-4d5f-acb4-44de64ed17d1'), unique=True),
        ),
    ]
