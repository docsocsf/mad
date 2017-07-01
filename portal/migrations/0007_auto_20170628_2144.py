# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_auto_20170627_2241'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='spouse',
            new_name='partner',
        ),
    ]