import sys, traceback

from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from paranuara.models import Company, People

from paranuara.serializers.company import CompanyEmployeesSerializer
from paranuara.serializers.people import PeopleFavoriteFoodSerializer, PeopleComparePeopleDetailsSerializer

from paranuara.view_models.people import PeopleFavoriteFoodDetailsViewModel, PeopleComparePeopleDetailsViewModel


class CompanyEmployeesView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, company_id, *args, **kwargs):
        people = People.objects.filter(company_id=company_id)
        serializer = CompanyEmployeesSerializer(people, many=True)

        return Response(data=serializer.data)


class PeopleCompareView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, people_id, other_people_id, *args, **kwargs):

        if people_id == other_people_id:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data="Can't compare with own ID")

        people = People.objects.filter(index__in=[people_id, other_people_id])

        if people.count() < 2:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data="One or more people searched is missing!")

        friends = People.objects.prefetch_related('friendship_set').filter(
            index__in=(
                people[0].friendship_set.exclude(friend_id__in=[people_id, other_people_id]).values_list('friend_id').intersection(
                people[1].friendship_set.exclude(friend_id__in=[people_id, other_people_id]).values_list('friend_id')).values_list('friend_id')
            ),
            eyeColor='brown',
            has_died=False
        ).distinct()

        vm = PeopleComparePeopleDetailsViewModel(people=people[0], other_people=people[1], friends=friends)
        serializer = PeopleComparePeopleDetailsSerializer(vm)

        return Response(data=serializer.data)


class PeopleFavoriteFoodView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, people_id, *args, **kwargs):
        people = get_object_or_404(People, index=people_id)
        vm = PeopleFavoriteFoodDetailsViewModel(people)
        serializer = PeopleFavoriteFoodSerializer(vm)

        return Response(data=serializer.data)