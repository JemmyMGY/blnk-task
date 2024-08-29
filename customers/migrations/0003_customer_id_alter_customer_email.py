# Generated by Django 5.1 on 2024-08-25 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_alter_customer_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
    ]
