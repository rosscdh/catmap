from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
User = get_user_model()

from catmap import TRUTHY
from catmap.apps.cat.models import Cat

from pinax.eventlog.models import log

import arrow
import csv


class Command(BaseCommand):
    help = 'Import cat adoptions from a csv file'

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
                   outgoing_adoption_date,
                   adopter_id,
                   suburb_state_post,
                   jurisdiction,
                   status,
                   age_category_at_adoption,
                   sex,
                   animal_name,
                   microchip,
                   sorted_by_tab_no_only,
                   total_17345,
                   tab_1_2645,
                   tab_2_1294,
                   tab_3_4915,
                   tab_4_4667,
                   tab_5_3824) = cell
                except Exception as e:
                    import pdb;pdb.set_trace()

                cat, cat_is_new = Cat.objects.get_or_create(pk=animal_id)
                #print '%s (%s)' % (cat, status)

                outgoing_adoption_date = outgoing_adoption_date.strip()

                try:
                    outgoing_adoption_date = arrow.get(outgoing_adoption_date, 'D MMM YYYY')
                except Exception as e:
                    try:
                        outgoing_adoption_date = arrow.get(outgoing_adoption_date, 'D-MMM-YYYY')
                    except Exception as e:
                        try:
                            outgoing_adoption_date = arrow.get(outgoing_adoption_date, 'D/MM/YYYY')
                        except Exception as e:
                            try:
                                outgoing_adoption_date = arrow.get(outgoing_adoption_date, 'MMM D, YY')
                            except Exception as e:
                                try:
                                    outgoing_adoption_date = arrow.get(outgoing_adoption_date, 'MM/D/YYYY')
                                except Exception as e:
                                    import pdb;pdb.set_trace()

                #if cat_is_new is True:
                cat.name = animal_name
                cat.fake_date_event = outgoing_adoption_date.datetime

                try:
                    gender = sex.lower()[0]
                except IndexError:
                    gender = 'u'
                except Exception as e:
                    import pdb;pdb.set_trace()

                if gender in ['m', 'f']:
                    cat.sex = gender
                else:
                    cat.sex = None

                cat.save()

                log(user=self.user,
                    action=status.lower(),
                    obj=cat,
                    dateof=outgoing_adoption_date.datetime,
                    extra={
                        'animal_id': animal_id,
                        'outgoing_adoption_date': outgoing_adoption_date.datetime,
                        'adopter_id': adopter_id,
                        'suburb_state_post': suburb_state_post,
                        'jurisdiction': jurisdiction,
                        'status': status,
                        'age_category_at_adoption': age_category_at_adoption,
                        'sex': sex,
                        'gender': gender,
                        'animal_name': animal_name,
                        'microchip': microchip
                      })

            counter = counter + 1
        print counter