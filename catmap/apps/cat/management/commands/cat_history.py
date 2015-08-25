from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
User = get_user_model()

from dateutil.parser import parse

from catmap import TRUTHY
from catmap.apps.cat.models import Cat

from pinax.eventlog.models import log

# import openpyxl
import csv


class Command(BaseCommand):
    help = 'Import cat hisotry from a xls file'

    def add_arguments(self, parser):
        parser.add_argument('workbook', nargs='+', type=unicode)

    # def handle(self, *args, **options):
    #     for wb in options.get('workbook'):
    #         book = openpyxl.load_workbook(wb)
    #         self.history(cats=book['datasheet'])
    def handle(self, *args, **options):
        self.user = User.objects.all().first()
        for wb in options.get('workbook'):
            with open(wb, 'rb') as csvfile:
                csv_reader = csv.reader(csvfile)
                self.history(cats=csv_reader)

    def history(self, cats):
        counter = 0
        for cell in cats:
            cat = None
            if counter >= 1:
                # print len(cell)
                # if len(cell) != 18:
                #   print ', '.join(cell)
                try:
                  (animal_id,
                   physical_location,
                   shelter_loc,
                   animal_name,
                   breed,
                   type_colour,
                   has_tattoo,
                   has_microchip,
                   lost_found_address,
                   sex,
                   desexed,
                   status,
                   sub_status,
                   source,
                   date_in,
                   due_date_out,
                   date_out,
                   identification_type) = cell
                except Exception as e:
                    import pdb;pdb.set_trace()

                cat, cat_is_new = Cat.objects.get_or_create(pk=animal_id)
                if cat_is_new is True:
                    cat.name = animal_name
                    cat.sex = sex.lower()[0] if sex else None
                    cat.breed = breed
                    cat.coat_type = type_colour
                    cat.colour = type_colour
                    cat.tattoo = has_tattoo
                    cat.desex_done = desexed in TRUTHY
                    cat.save()

                message = '%s' % status
                if sub_status:
                    message = '%s, - %s' % (message, sub_status)

                log(user=self.user,
                    action=status.lower(),
                    obj=cat,
                    dateof=parse(date_in) if date_in else None,
                    extra={'physical_location': physical_location,
                           'shelter_loc': shelter_loc,
                           'animal_name': animal_name,
                           'breed': breed,
                           'type_colour': type_colour,
                           'has_tattoo': has_tattoo,
                           'has_microchip': has_microchip,
                           'lost_found_address': lost_found_address,
                           'sex': sex,
                           'desexed': desexed,
                           'status': status,
                           'sub_status': sub_status,
                           'source': source,
                           'date_in': date_in,
                           'due_date_out': due_date_out,
                           'date_out': date_out,
                           'identification_type': identification_type})

            counter = counter + 1