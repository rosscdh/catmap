from django.db import models
from django.template.defaultfilters import slugify
from haystack.utils.geo import Point


class Shelter(models.Model):
    slug = models.SlugField(max_length=128, null=True, blank=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        super(Shelter, self).save(*args, **kwargs)


class Location(models.Model):
    slug = models.SlugField(max_length=128, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    jurisdiction  = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    lat = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    lon = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    altitude = models.CharField(max_length=255, null=True, blank=True, db_index=True)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.jurisdiction)

    @property
    def location_point(self):
        return Point(float(self.lon), float(self.lat))
