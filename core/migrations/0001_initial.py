# Generated by Django 3.1.1 on 2020-09-14 16:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('featured_image', models.ImageField(default='featured_image/default.jpg', upload_to='featured_image')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('old_img', models.ImageField(blank=True, null=True, upload_to='shop')),
                ('new_img', models.ImageField(upload_to='shop')),
                ('price', models.IntegerField(blank=True, default=0, null=True)),
                ('discount_price', models.IntegerField(blank=True, null=True)),
                ('is_free', models.BooleanField()),
                ('download_file', models.FileField(upload_to='files')),
                ('downloads', models.PositiveIntegerField(default=0)),
                ('views', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_categories', to='core.categories')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]