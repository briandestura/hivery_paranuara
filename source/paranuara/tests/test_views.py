import json, ast

from django.db.models import Avg

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from paranuara.models import People, Company, Friendship
from paranuara.views import CompanyEmployeesView, PeopleCompareView, PeopleFavoriteFoodView


def initialise_data():
    Company.objects.bulk_create([
        Company(name='Company 1'),
        Company(name='Company 2'),
        Company(name='Company 3')
    ])
    companies = Company.objects.all()

    People.objects.bulk_create([
        People(
            _id='SomeID1',
            name='one',
            eyeColor='brown',
            company=companies[0],
            favorite_fruits=['apple', 'banana'],
            favorite_vegetables=['artichoke', 'asparagus']
        ),
        People(
            _id='SomeID2',
            name='two',
            eyeColor='blue',
            company=companies[0],
            favorite_fruits=['apple'],
            favorite_vegetables=['artichoke']
        ),
        People(
            _id='SomeID3',
            name='three',
            eyeColor='brown',
            company=companies[1],
            favorite_fruits=[],
            favorite_vegetables=[]
        )
    ])
    people = People.objects.all()

    Friendship.objects.bulk_create([
        Friendship(
            person=people[0],
            friend=people[1],
        ),
        Friendship(
            person=people[0],
            friend=people[2],
        ),
        Friendship(
            person=people[1],
            friend=people[2],
        ),
        Friendship(
            person=people[2],
            friend=people[0],
        ),
        Friendship(
            person=people[2],
            friend=people[1],
        ),
    ])


class CompanyEmployeesViewViewTest(APITestCase):
    def setUp(self):
        initialise_data()

        self.request_factory = APIRequestFactory()
        self.view = CompanyEmployeesView

    def test_valid_data_returns_all_employees_status_code_200(self):
        company = Company.objects.first()
        employees = People.objects.filter(company=company)

        url = reverse('v1.company-employees', kwargs={'company_id': company.pk})
        request = self.request_factory.get(url)
        response = self.view.as_view()(request, company_id=company.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [{'_id': e._id, 'name': e.name, 'email': e.email} for e in employees]
        )

    def test_unknown_company_returns_empty_status_code_200(self):

        url = reverse('v1.company-employees', kwargs={'company_id': 1000})
        request = self.request_factory.get(url)
        response = self.view.as_view()(request, company_id=1000)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_empty_company_returns_empty_status_code_200(self):
        company = Company.objects.last()
        url = reverse('v1.company-employees', kwargs={'company_id': company.pk})
        request = self.request_factory.get(url)
        response = self.view.as_view()(request, company_id=company.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


class PeopleCompareViewTest(APITestCase):
    def setUp(self):
        initialise_data()

        self.request_factory = APIRequestFactory()
        self.view = PeopleCompareView

    def test_valid_data_returns_correct_data_status_code_200(self):

        people = People.objects.all()

        url = reverse('v1.people-compare', kwargs={'people_id': people[0].pk, 'other_people_id': people[1].pk})
        request = self.request_factory.get(url)
        response = self.view.as_view()(request, people_id=people[0].pk, other_people_id=people[1].pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "first_people": {
                    "name": people[0].name,
                    "address": people[0].address,
                    "age": people[0].age,
                    "phone": people[0].phone,
                },
                "second_people": {
                    "name": people[1].name,
                    "address": people[1].address,
                    "age": people[1].age,
                    "phone": people[1].phone,
                },
                "common_friends": [
                    {
                        "name": people[2].name,
                        "eyeColor": 'brown',
                        "has_died": False,
                    }
                ]
            }
        )

    def test_valid_data_no_common_friends_returns_correct_data_status_code_200(self):

        people = People.objects.all()

        url = reverse('v1.people-compare', kwargs={'people_id': people[1].pk, 'other_people_id': people[2].pk})
        request = self.request_factory.get(url)
        response = self.view.as_view()(request, people_id=people[1].pk, other_people_id=people[2].pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "first_people": {
                    "name": people[1].name,
                    "address": people[1].address,
                    "age": people[1].age,
                    "phone": people[1].phone,
                },
                "second_people": {
                    "name": people[2].name,
                    "address": people[2].address,
                    "age": people[2].age,
                    "phone": people[2].phone,
                },
                "common_friends": []
            }
        )

    def test_same_id_in_url_returns_406(self):

        people = People.objects.first()

        url = reverse('v1.people-compare', kwargs={'people_id': people.pk, 'other_people_id': people.pk})
        request = self.request_factory.get(url)
        response = self.view.as_view()(request, people_id=people.pk, other_people_id=people.pk)

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data, "Can't compare with own ID")

    def test_one_unknown_people_returns_406(self):

        people = People.objects.last()

        url = reverse('v1.people-compare', kwargs={'people_id': 1000, 'other_people_id': people.pk})
        request = self.request_factory.get(url)
        response = self.view.as_view()(request, people_id=1000, other_people_id=people.pk)

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data, 'One or more people searched is missing!')

    def test_both_unknown_people_returns_406(self):

        url = reverse('v1.people-compare', kwargs={'people_id': 1000, 'other_people_id': 1001})
        request = self.request_factory.get(url)
        response = self.view.as_view()(request, people_id=1000, other_people_id=1001)

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data, 'One or more people searched is missing!')


class PeopleFavoriteFoodViewTest(APITestCase):
    def setUp(self):
        initialise_data()

        self.request_factory = APIRequestFactory()
        self.view = PeopleFavoriteFoodView

    def test_returns_valid_data_returns_200(self):

        people = People.objects.first()

        url = reverse('v1.people-favorite-food', kwargs={'people_id': people.pk})
        request = self.request_factory.get(url)
        response = self.view.as_view()(request, people_id=people.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'username': people.email,
                'age': people.age,
                'fruits': ast.literal_eval(people.favorite_fruits),
                'vegetables': ast.literal_eval(people.favorite_vegetables)
            }
        )

    def test_no_favorite_returns_200(self):

        people = People.objects.last()

        url = reverse('v1.people-favorite-food', kwargs={'people_id': people.pk})
        request = self.request_factory.get(url)
        response = self.view.as_view()(request, people_id=people.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'username': people.email,
                'age': people.age,
                'fruits': [],
                'vegetables': [],
            }
        )

    def test_unknown_people_returns_404(self):

        url = reverse('v1.people-favorite-food', kwargs={'people_id': 1000})
        request = self.request_factory.get(url)
        response = self.view.as_view()(request, people_id=1000)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'Not found.'})