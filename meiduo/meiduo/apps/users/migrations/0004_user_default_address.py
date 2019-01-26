# Generated by Django 2.0.5 on 2019-01-26 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='default_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='users.Address', verbose_name='默认地址'),
        ),
    ]
