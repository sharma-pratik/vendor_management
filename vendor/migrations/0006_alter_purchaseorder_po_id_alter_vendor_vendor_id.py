# Generated by Django 4.2.7 on 2023-11-26 17:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_alter_purchaseorder_po_id_alter_vendor_vendor_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='po_id',
            field=models.UUIDField(default=uuid.UUID('cb53ffb6-b4f3-4492-9cd6-d9e7412f2134'), unique=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vendor_id',
            field=models.UUIDField(default=uuid.UUID('fd467cf5-b46a-4240-9a0d-d10e8bbb0430'), unique=True),
        ),
    ]
