# Generated by Django 3.1.1 on 2020-09-20 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ip_address',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
    ]
