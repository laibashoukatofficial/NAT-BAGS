# Generated by Django 4.2.2 on 2024-06-28 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_productreview_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='is_cod',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='payment_method',
            field=models.CharField(choices=[('cod', 'Cash on Delivery'), ('online', 'Online Payment')], default='cod', max_length=50),
        ),
    ]
