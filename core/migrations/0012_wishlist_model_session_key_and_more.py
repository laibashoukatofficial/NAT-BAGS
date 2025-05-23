# Generated by Django 4.2.2 on 2024-06-30 00:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion





class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0011_cartorder_is_cod_cartorder_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist_model',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='payment_method',
            field=models.CharField(default='cod', max_length=50),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(default='BAGS', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(default='NAT BAGS', max_length=100),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='title',
            field=models.CharField(default='NAT', max_length=100),
        ),
        migrations.AlterField(
            model_name='wishlist_model',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product'),
        ),
        migrations.AlterField(
            model_name='wishlist_model',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
