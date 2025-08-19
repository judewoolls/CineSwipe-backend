from rest_framework import serializers
from .models import Movie, Couple

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'movie_id', 'title', 'poster_path', 'release_year', 'created_at']

class CoupleSerializer(serializers.ModelSerializer):
    partner1 = serializers.CharField(source='user1.username')
    partner2 = serializers.CharField(source='user2.username', allow_null=True)

    class Meta:
        model = Couple
        fields = ['partner1', 'partner2', 'invite_code']