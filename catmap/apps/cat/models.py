from django.db import models


class Cat(models.Model):
    CAT_GENDER = (('m', 'M'), ('f', 'F'))

    name = models.CharField(max_length=128, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=3, choices=CAT_GENDER, null=True, blank=True)
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

    @property
    def age(self):
        return self.dob  # - today

    def __unicode__(self):
        return '%s - (%s)' % (self.name, self.sex)
