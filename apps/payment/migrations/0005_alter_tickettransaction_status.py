# Generated by Django 5.1.7 on 2025-07-10 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_remove_tickettransaction_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickettransaction',
            name='status',
            field=models.CharField(choices=[('p', 'pending'), ('s', 'success'), ('c', 'cancelled')], default='PENDING', max_length=20),
        ),
    ]
