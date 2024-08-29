# Generated by Django 4.2.15 on 2024-08-29 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0006_payment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loan',
            old_name='amount',
            new_name='remaining_amount',
        ),
        migrations.AddField(
            model_name='loan',
            name='paid_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AddField(
            model_name='loan',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
            preserve_default=False,
        ),
    ]
