"""
In order to serialize and deserialize object
instances into JSON representations, serializers
must be defined. The following classes make
serialization and deserialization possible while
also maintaining the relationships between the
models.
"""

from rest_framework import serializers
from django.contrib.auth.models import User

from games.models import Game
from games.models import GameCategory
from games.models import Player
from games.models import PlayerScore


class GameCategorySerializer(serializers.HyperlinkedModelSerializer):
    """
    Each serializer will be a subclass of the
    HyperlinkedModelSerializer class. The
    HyperlinkedModelSerializer class represents relationships
    as hyperlinks instead of using primary key values.
    """
    games = serializers.HyperlinkedRelatedField(
        many=True,  # one-to-many relationship
        read_only=True,
        view_name='game-detail'  # the view to use when hyperlink is clicked
    )

    class Meta:
        model = GameCategory  # the model related to the Serializer
        fields = (
            'url',
            'pk',
            'name',
            'games'
        )  # fields to include in serialization


class GameSerializer(serializers.HyperlinkedModelSerializer):
    """
    A SlugRelatedField is a read-write field that represents
    the target of the relationship by a unique slug attribute,
    the 'name'.
    """
    owner = serializers.ReadOnlyField(source='owner.username')  # just display the owner username
    game_category = serializers.SlugRelatedField(
        queryset=GameCategory.objects.all(),
        slug_field='name'  # shows the related categories name instead of ID (default)
    )

    class Meta:
        model = Game
        depth = 4
        fields = (
            'url',
            'game_category',
            'name',
            'release_date',
            'played',
            'owner'
        )


class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    # The code below makes it possible to display all details for a game
    game = GameSerializer()

    # No reference to the Player has to be made, the Player model will use this Serializer
    class Meta:
        model = PlayerScore
        fields = (
            'url',
            'pk',
            'score',
            'score_date',
            'game'
        )


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    scores = ScoreSerializer(many=True, read_only=True)
    gender = serializers.ChoiceField(
        choices=Player.GENDER_CHOICES
    )
    gender_description = serializers.CharField(
        source='get_gender_display',
        read_only=True
    )

    class Meta:
        model = Player
        fields = (
            'url',
            'name',
            'gender',
            'gender_description',
            'scores'
        )


class PlayerScoreSerializer(serializers.HyperlinkedModelSerializer):
    player = serializers.SlugRelatedField(
        queryset=Player.objects.all(),
        slug_field='name'
    )
    game = serializers.SlugRelatedField(
        queryset=Game.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = PlayerScore
        fields = (
            'url',
            'pk',
            'score',
            'score_date',
            'player',
            'game'
        )


class UserGameSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes the games related to a user
    """
    class Meta:
        model = Game  # a Game that belongs to a user
        fields = (
            'url', 'name'
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    games = UserGameSerializer(many=True, read_only=True)

    class Meta:
        model = User  # an instance of django.contrib.auth.models.User
        fields = (
            'url', 'pk', 'username', 'games'
        )
