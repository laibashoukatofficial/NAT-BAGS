# Generated by Django 4.2.2 on 2024-04-27 12:34

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CartOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default='1.99', max_digits=99999999999999)),
                ('paid_status', models.BooleanField(blank=True, default=False, null=True)),
                ('order_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('product_status', models.CharField(choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='processing', max_length=30)),
                ('sku', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', blank=True, length=5, max_length=20, null=True, prefix='SKU')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Cart Order',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=10, max_length=20, prefix='cat', unique=True)),
                ('title', models.CharField(default='Bags', max_length=100)),
                ('image', models.ImageField(upload_to='category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=10, max_length=20, prefix='', unique=True)),
                ('title', models.CharField(default='Fresh Pear', max_length=100)),
                ('image', models.ImageField(default='product.jpg', upload_to=core.models.user_directory_path)),
                ('description', models.TextField(blank=True, default='This is the product', null=True)),
                ('price', models.DecimalField(decimal_places=2, default='1.99', max_digits=99999999999999)),
                ('old_price', models.DecimalField(decimal_places=2, default='2.99', max_digits=99999999999999)),
                ('specifications', models.TextField(blank=True, null=True)),
                ('product_status', models.CharField(choices=[('draft', 'Draft'), ('disabled', 'Disabled'), ('rejected', 'Rejected'), ('in_review', 'In Review'), ('published', 'Published')], default='in_review', max_length=10)),
                ('status', models.BooleanField(default=True)),
                ('in_stock', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
                ('digital', models.BooleanField(default=False)),
                ('sku', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=4, max_length=10, prefix='sku', unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='core.category')),
            ],
            options={
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='wishlist_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'wishlists',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=10, max_length=20, prefix='ven', unique=True)),
                ('title', models.CharField(default='RTW', max_length=100)),
                ('image', models.ImageField(default='vendor.jpg', upload_to=core.models.user_directory_path)),
                ('cover_image', models.ImageField(default='vendor.jpg', upload_to=core.models.user_directory_path)),
                ('description', models.TextField(blank=True, default='I am an Amazing Vendor', null=True)),
                ('address', models.CharField(default='123 Main Street.', max_length=100)),
                ('contact', models.CharField(default='+123 (456) 789', max_length=100)),
                ('chat_resp_time', models.CharField(default='100', max_length=100)),
                ('shipping_on_time', models.CharField(default='100', max_length=100)),
                ('authentic_rating', models.CharField(default='100', max_length=100)),
                ('days_return', models.CharField(default='100', max_length=100)),
                ('warranty_period', models.CharField(default='100', max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Vendors',
            },
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('rating', models.IntegerField(choices=[(1, '★☆☆☆☆'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★')], default=None)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews', to='core.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Product Reviews',
            },
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(default='product.jpg', upload_to='product-images')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='p_images', to='core.product')),
            ],
            options={
                'verbose_name_plural': 'Product Images',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.tags'),
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='core.vendor'),
        ),
        migrations.CreateModel(
            name='CartOrderProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.CharField(max_length=200)),
                ('product_status', models.CharField(max_length=200)),
                ('item', models.CharField(max_length=200)),
                ('image', models.CharField(max_length=200)),
                ('qty', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default='1.99', max_digits=99999999999999)),
                ('total', models.DecimalField(decimal_places=2, default='1.99', max_digits=99999999999999)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cartorder')),
            ],
            options={
                'verbose_name_plural': 'Cart Order Items',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=300, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Address',
            },
        ),
    ]
