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
                   animal_name,
                   type_colour,
                   breed,
                   date_from,
                   return_reason,
                   status,
                   none,
                   other_reason,
                   last_owner_notes,
                   shelter_location,
                   adoption_date) = cell
                except Exception as e:
                    import pdb;pdb.set_trace()

                cat, cat_is_new = Cat.objects.get_or_create(pk=animal_id)
                if cat_is_new is True:
                    cat.name = animal_name
                    cat.sex = sex.lower()[0] if sex else None
                    cat.breed = breed
                    cat.save()

                message = '%s' % return_reason
                if other_reason:
                    message = '%s, - %s' % (message, other_reason)

                log(user=self.user,
                    action=status.lower(),
                    obj=cat,
                    dateof=parse(date_from) if date_from else None,
                    extra={'animal_id': animal_id,
                           'name': animal_name,
                           'type': type_colour,
                           'breed': breed,
                           'date_from': parse(date_from) if date_from else None,
                           'return_reason': return_reason,
                           'status': status,
                           'other_reason': other_reason,
                           'last_owner_notes': last_owner_notes,
                           'shelter_location': shelter_location,
                           'adoption_date': parse(adoption_date) if date_from else None,})

            counter = counter + 1