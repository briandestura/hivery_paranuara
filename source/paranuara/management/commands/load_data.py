import os, json
from django.core.management.base import BaseCommand

from paranuara.models import Company
from paranuara.serializers.loader import LoadPeopleSerializer


def initialise_data():

    with open(
            '{}/../../../../resources/companies.json'.format(os.path.dirname(__file__)), 'r'
    ) as company_data:
        data = json.load(company_data)
        companies = []

        for company in data:
            companies.append(
                Company(
                    id=company['index'],
                    name=company['company']
                )
            )

        Company.objects.bulk_create(companies)

    with open(
            '{}/../../../../resources/people.json'.format(os.path.dirname(__file__)), 'r'
    ) as people_data:
        data = json.load(people_data)

        serializer = LoadPeopleSerializer(data=data, many=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()


class Command(BaseCommand):
    help = 'Initialise data for paranuara app'
    requires_system_checks = False

    def handle(self, *args, **options):
        initialise_data()
