import ast


class PeopleFavoriteFoodDetailsViewModel(object):
    def __init__(self, people):
        self.username = people.email
        self.age = people.age
        self.fruits = ast.literal_eval(people.favorite_fruits)
        self.vegetables = ast.literal_eval(people.favorite_vegetables)


class PeopleComparePeopleDetailsViewModel(object):
    def __init__(self, people, other_people, friends):
        self.first_people = people
        self.second_people = other_people
        self.common_friends = friends
