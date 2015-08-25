from django.db import models
from django.template.defaultfilters import slugify


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
