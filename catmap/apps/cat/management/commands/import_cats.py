from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
User = get_user_model()

from catmap.apps.cat.models import Cat

from dateutil.parser import parse

import uuid
import openpyxl
import datetime

from catmap import TRUTHY


def _user_exists(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None


class Command(BaseCommand):
    help = 'Import cats from a xls file'

    def add_arguments(self, parser):
        parser.add_argument('workbook', nargs='+', type=unicode)

    def handle(self, *args, **options):
        for wb in options.get('workbook'):
            book = openpyxl.load_workbook(wb)
            self.import_objects(cats=book['CATS'])
            self.import_objects(cats=book['KITTENS'])

    def _get_unique_username(self, username):
        username = slugify(username)  # apply the transforms first so that the lookup acts on the actual username
        username = username[0:29]
        while _user_exists(username=username):
            username = '%s-%s' % (username, uuid.uuid4().get_hex()[:4])
            username = username[0:29]  # be aware of fencepost error here field limit is 30

        return username

    def import_objects(self, cats):
            counter = 0
            for cell in cats.rows:
                owner = None
                if counter >= 1:
                    (Animal_ID,
                     Name,
                     Date_Adopted,
                     DOB,
                     Animal_Age,
                     Sex,
                     Breed,
                     CoatType,
                     Colour,
                     Prev_Desex,
                     Altered,
                     Desex_Done,
                     Owner_First_Name,
                     Owner_Last_Name,
                     Owner_Address,
                     Contact_Numbers,
                     Owner_Email,
                     Shire,
                     Microchip,
                     Receipt_ID,
                     Adopted_From,
                     Returned,
                     Adoption_Notes,
                     Animal_Notes, Something) = cell

                    if Owner_Email.value:
                        owner, owner_is_new = User.objects.get_or_create(username=self._get_unique_username(Owner_Email.value.split('@')[0]), email=Owner_Email.value)
                        owner.first_name = Owner_First_Name.value
                        owner.last_name = Owner_Last_Name.value
                        owner.save()

                    cat, cat_is_new = Cat.objects.get_or_create(pk=Animal_ID.value)

                    #if cat_is_new is True:
                    cat.name = Name.value
                    cat.date_adopted = parse(Date_Adopted.value) if Date_Adopted.value else None
                    cat.dob = parse(DOB.value) if DOB.value else None
                    cat.sex = Sex.value.lower()[0]
                    cat.breed = Breed.value
                    cat.coat_type = CoatType.value
                    cat.colour = Colour.value
                    cat.prev_desex = Prev_Desex.value in TRUTHY
                    cat.altered = Altered.value in TRUTHY
                    cat.desex_done = Desex_Done.value in TRUTHY
                    cat.shire = Shire.value
                    cat.microchip_id = Microchip.value
                    cat.receipt_id = Receipt_ID.value
                    cat.adopted_from = Adopted_From.value
                    cat.returned = Returned.value in TRUTHY
                    cat.adoption_notes = Adoption_Notes.value
                    cat.animal_notes = Animal_Notes.value
                    if owner:
                        cat.owner = owner
                    cat.save()

                counter = counter+1
