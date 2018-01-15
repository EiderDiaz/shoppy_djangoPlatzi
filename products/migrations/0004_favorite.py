# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
        ('products', '0003_auto_20180115_1832'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product', models.ForeignKey(to='products.Product')),
                ('user', models.ForeignKey(to='client.Client')),
            ],
            options={
                'verbose_name': 'Favorite',
                'verbose_name_plural': 'Favorites',
            },
        ),
    ]
