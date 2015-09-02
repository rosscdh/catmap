# -*- coding: utf-8 -*-
from django.db import models


class CatManager(models.Manager):
    def gender_breakdown(self, cat_ids=[]):
        qs = self.get_queryset().filter(pk__in=cat_ids)
        return {
            'male': qs.filter(sex=self.model.CAT_GENDER.male).count(),
            'female': qs.filter(sex=self.model.CAT_GENDER.female).count(),
            'unspecified': qs.exclude(sex__in=[self.model.CAT_GENDER.male, self.model.CAT_GENDER.female]).count(),
            'desexed': {
                'male': qs.filter(sex=self.model.CAT_GENDER.male, desex_done=True).count(),
                'female': qs.filter(sex=self.model.CAT_GENDER.female, desex_done=True).count(),
                'unspecified': qs.exclude(sex__in=[self.model.CAT_GENDER.male, self.model.CAT_GENDER.female], desex_done=True).count(),
            }
        }
