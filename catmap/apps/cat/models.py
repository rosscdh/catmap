# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType

from pinax.eventlog.models import Log

from . import CAT_GENDER_CHOICES
from .managers import CatManager

from datetime import date


class Cat(models.Model):
    CAT_GENDER = CAT_GENDER_CHOICES

    name = models.CharField(max_length=128, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=3, choices=CAT_GENDER.get_choices(), null=True, blank=True)
    breed = models.CharField(max_length=128, null=True, blank=True)
    coat_type = models.CharField(max_length=128, null=True, blank=True)
    colour = models.CharField(max_length=128, null=True, blank=True)
    prev_desex = models.NullBooleanField(default=False, null=True, blank=True)
    altered = models.NullBooleanField(default=False, null=True, blank=True)
    desex_done = models.NullBooleanField(default=False, null=True, blank=True)
    shire = models.CharField(max_length=128, null=True, blank=True)
    tattoo = models.CharField(max_length=255, null=True, blank=True)
    microchip_id = models.CharField(max_length=128, null=True, blank=True)
    receipt_id = models.CharField(max_length=128, null=True, blank=True)
    adopted_from = models.CharField(max_length=128, null=True, blank=True)
    returned = models.NullBooleanField(default=False, null=True, blank=True)
    adoption_notes = models.CharField(max_length=255, null=True, blank=True)
    animal_notes = models.CharField(max_length=255, null=True, blank=True)
    date_adopted = models.DateField(null=True, blank=True)

    current_status = models.CharField(max_length=128, null=True, blank=True)
    owner = models.ForeignKey('auth.User', null=True, blank=True)

    objects = CatManager()

    @property
    def gender(self):
        return self.CAT_GENDER.get_desc_by_value(self.sex)

    @property
    def age(self):
        today = date.today()
        try:
            birthday = self.dob.replace(year=today.year)
        except ValueError:
            # raised when birth date is February 29 and the current year is not a leap year
            birthday = self.dob.replace(year=today.year, month=self.dob.month + 1, day=1)
        if birthday > today:
            return today.year - self.dob.year - 1
        else:
            return today.year - self.dob.year

    @property
    def events(self):
        return Log.objects.filter(content_type=ContentType.objects.get(app_label='cat', model='cat')) \
                          .filter(object_id=self.pk) \
                          .order_by('timestamp')

    def __unicode__(self):
        return '%s - (%s)' % (self.name, self.sex)
