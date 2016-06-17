from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
User = get_user_model()

from catmap import TRUTHY
from catmap.apps.cat.models import Cat

from pinax.eventlog.models import log

import arrow
import csv


class Command(BaseCommand):
    help = 'Import cat hisotry from a csv file'

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
                  (tab_no,
                   animal_id,
                   received_surrender_date,
                   surrender_source,
                   suburb_state_post,
                   jurisdiction,
                   status,
                   age_category_at_adoption,
                   sex,
                   animal_name,
                   sorted_by_tab_no_only,
                   correct_total_of_28360_cats,
                   tab_1_5323,
                   tab_2_384,
                   tab_3_6754,
                   tab_4_8795,
                   tab_5_7104) = cell
                except Exception as e:
                    import pdb;pdb.set_trace()

                cat, cat_is_new = Cat.objects.get_or_create(pk=animal_id)
                #print '%s (%s)' % (cat, status)

                try:
                    received_surrender_date = arrow.get(received_surrender_date, 'D MMM YYYY')
                except Exception as e:
                    try:
                        received_surrender_date = arrow.get(received_surrender_date, 'D-MMM-YYYY')
                    except Exception as e:
                        try:
                            received_surrender_date = arrow.get(received_surrender_date, 'D/MM/YYYY')
                        except Exception as e:
                            import pdb;pdb.set_trace()

                # if cat_is_new is True:
                cat.name = animal_name
                cat.fake_date_event = received_surrender_date.datetime

                gender = sex.lower()[0]
                if gender in ['m', 'f']:
                    cat.sex = gender
                else:
                    cat.sex = None

                cat.save()

                log(user=self.user,
                    action=status.lower(),
                    obj=cat,
                    dateof=received_surrender_date.datetime,
                    extra={'animal_id': animal_id,
                           'received_surrender_date': received_surrender_date.datetime,
                           'surrender_source': surrender_source,
                           'suburb_state_post': suburb_state_post,
                           'jurisdiction': jurisdiction,
                           'status': status,
                           'age_category_at_adoption': age_category_at_adoption,
                           'sex': sex,
                           'gender': gender,
                           'animal_name': animal_name,
                           })

            counter = counter + 1
        print counter