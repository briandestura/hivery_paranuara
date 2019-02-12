from rest_framework import serializers

from paranuara.models import Company, People, Friendship


FRUITS = ['apple', 'apricot', 'banana', 'bilberry', 'blackberry', 'blackcurrant', 'blueberry', 'cantaloupe', 'cherimoya', 'cherry', 'clementine', 'cloudberry', 'coconut', 'currant', 'damson', 'date', 'durian', 'elderberry', 'feijoa', 'fig', 'fruit', 'gooseberry', 'grape', 'grapefruit', 'honeydew', 'huckleberry', 'jackfruit', 'jambul', 'jujube', 'kiwifruit', 'kumquat', 'lemon', 'lime', 'loquat', 'lychee', 'mango', 'mangosteen', 'melon', 'nectarine', 'orange', 'passionfruit', 'peach', 'pear', 'pineapple', 'plum', 'plumcot', 'pomegranate', 'pomelo', 'prune', 'purple', 'raisin', 'rambutan', 'raspberry', 'redcurrant', 'rock', 'satsuma', 'strawberry', 'tangerine', 'tomato', 'ugli', 'watermelon']
VEGETABLES = ['artichoke', 'asparagus', 'aubergine', 'beet', 'beetroot', 'bell pepper', 'broccoli', 'brussels sprout', 'cabbage', 'carrot', 'cauliflower', 'celery', 'corn', 'courgette', 'cucumber', 'eggplant', 'green bean', 'green onion', 'leek', 'lettuce', 'mushroom', 'onion', 'pea', 'pepper', 'potato', 'pumpkin', 'radish', 'spring onion', 'squash', 'sweet potato', 'tomato', 'zucchini']


class LoadCompanySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=True)

    def save(self):
        company = Company(
            id=self.validated_data['id'],
            name=self.validated_data['name']
        )
        company.save()


class StringListField(serializers.ListField):
    child = serializers.CharField()


class LoadPeopleSerializer(serializers.Serializer):
    index = serializers.IntegerField(required=True)
    _id = serializers.CharField(allow_blank=True, allow_null=True)
    guid = serializers.CharField(allow_blank=True, allow_null=True)
    has_died = serializers.BooleanField()
    balance = serializers.CharField(allow_blank=True, allow_null=True)
    picture = serializers.URLField(allow_blank=True, allow_null=True)
    age = serializers.IntegerField(allow_null=True)
    eyeColor = serializers.CharField(allow_blank=True, allow_null=True)
    name = serializers.CharField(allow_blank=True, allow_null=True)
    gender = serializers.CharField(allow_blank=True, allow_null=True)
    company_id = serializers.IntegerField(allow_null=True)
    email = serializers.EmailField(allow_blank=True, allow_null=True)
    phone = serializers.CharField(allow_blank=True, allow_null=True)
    address = serializers.CharField(allow_blank=True, allow_null=True)
    about = serializers.CharField(allow_blank=True, allow_null=True)
    registered = serializers.DateTimeField(input_formats=["%Y-%m-%dT%I:%M:%S %z"], allow_null=True)
    tags = StringListField()
    friends = serializers.ListField(required=False)
    greeting = serializers.CharField(allow_blank=True, allow_null=True)
    favouriteFood = StringListField()

    def create(self, validated_data):

        friends = validated_data['friends']
        company_id = validated_data['company_id']
        favorite_fruits = []
        favorite_vegetables = []

        for food in validated_data['favouriteFood']:
            favorite_fruits.append(food) if food in FRUITS \
                else favorite_vegetables.append(food)

        del validated_data['favouriteFood']
        del validated_data['friends']
        del validated_data['company_id']

        person, created = People.objects.update_or_create(
            index=validated_data['index'],
            defaults=validated_data
        )

        person.favorite_fruits = favorite_fruits
        person.favorite_vegetables = favorite_vegetables

        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            person.company = None
        else:
            person.company = company
        person.save()

        for friend in friends:
            friend, created = People.objects.get_or_create(
                index=friend['index']
            )

            Friendship.objects.create(
                person=person,
                friend=friend,
            )

        return person