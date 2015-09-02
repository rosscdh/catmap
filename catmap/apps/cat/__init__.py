# -*- coding: utf-8 -*-
from catmap.utils import get_namedtuple_choices


CAT_GENDER_CHOICES = get_namedtuple_choices('CAT_GENDER', (
    ('m', 'male', 'Male'),
    ('f', 'female', 'Female'),
))


default_app_config = 'catmap.apps.cat.apps.CatConfig'
