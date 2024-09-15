# Generated by Django 4.2 on 2024-09-15 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Accepted', 'Accepted'), ('Cancelled', 'Cancelled'), ('New', 'New')], default='New', max_length=100),
        ),
    ]