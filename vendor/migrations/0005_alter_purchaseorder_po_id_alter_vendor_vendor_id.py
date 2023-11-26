# Generated by Django 4.2.7 on 2023-11-26 17:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0004_alter_purchaseorder_po_id_alter_vendor_vendor_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='po_id',
            field=models.UUIDField(default=uuid.UUID('dab2d9c9-d1d9-4c1e-8fd1-7e1386c4dd81'), unique=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vendor_id',
            field=models.UUIDField(default=uuid.UUID('9a168ea2-ed5a-4198-a285-ab525894ae19'), unique=True),
        ),
    ]