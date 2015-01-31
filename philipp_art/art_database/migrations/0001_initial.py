# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArtPiece',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('purchase_price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('artist', models.CharField(max_length=200)),
                ('purchase_date', models.DateField()),
                ('notes', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArtPiecePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=200)),
                ('piece', models.ForeignKey(to='art_database.ArtPiece')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=400)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='artpiece',
            name='location',
            field=models.ForeignKey(to='art_database.Location'),
            preserve_default=True,
        ),
    ]
