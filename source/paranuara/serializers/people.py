from rest_framework import serializers

from paranuara.models import People


class StringListField(serializers.ListField):
    child = serializers.CharField()


class PeopleFavoriteFoodSerializer(serializers.Serializer):
    username = serializers.EmailField()
    age = serializers.IntegerField()
    fruits = StringListField()
    vegetables = StringListField()


class PeopleCompareDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ('name', 'address', 'age', 'phone')


class PeopleCommonFriendsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ('name', 'eyeColor', 'has_died')


class PeopleComparePeopleDetailsSerializer(serializers.Serializer):
    first_people = PeopleCompareDetailsSerializer()
    second_people = PeopleCompareDetailsSerializer()
    common_friends = PeopleCommonFriendsDetailsSerializer(many=True, required=False, allow_null=True)