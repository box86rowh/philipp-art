# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('art_database', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artpiecephoto',
            name='image',
            field=models.FileField(null=True, upload_to=b''),
            preserve_default=True,
        ),
    ]
