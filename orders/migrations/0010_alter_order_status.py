# Generated by Django 4.2 on 2024-07-11 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('Accepted', 'Accepted'), ('New', 'New'), ('Completed', 'Completed')], default='New', max_length=100),
        ),
    ]
