# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, null=True, blank=True)),
                ('dob', models.DateField(null=True, blank=True)),
                ('sex', models.CharField(blank=True, max_length=3, null=True, choices=[(b'm', b'M'), (b'f', b'F')])),
                ('breed', models.CharField(max_length=128, null=True, blank=True)),
                ('coat_type', models.CharField(max_length=128, null=True, blank=True)),
                ('colour', models.CharField(max_length=128, null=True, blank=True)),
                ('prev_desex', models.NullBooleanField(default=False)),
                ('altered', models.NullBooleanField(default=False)),
                ('desex_done', models.NullBooleanField(default=False)),
                ('shire', models.CharField(max_length=128, null=True, blank=True)),
                ('tattoo', models.CharField(max_length=255, null=True, blank=True)),
                ('microchip_id', models.CharField(max_length=128, null=True, blank=True)),
                ('receipt_id', models.CharField(max_length=128, null=True, blank=True)),
                ('adopted_from', models.CharField(max_length=128, null=True, blank=True)),
                ('returned', models.NullBooleanField(default=False)),
                ('adoption_notes', models.CharField(max_length=255, null=True, blank=True)),
                ('animal_notes', models.CharField(max_length=255, null=True, blank=True)),
                ('date_adopted', models.DateField(null=True, blank=True)),
                ('current_status', models.CharField(max_length=128, null=True, blank=True)),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
