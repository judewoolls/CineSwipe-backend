from rest_framework import serializers
from .models import Movie, Couple

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'movie_id', 'title', 'poster_path', 'release_year', 'created_at']

class CoupleSerializer(serializers.ModelSerializer):
    user1 = serializers.CharField(source='user1.username')
    user2 = serializers.CharField(source='user2.username', allow_null=True)

    class Meta:
        model = Couple
        fields = ['user1', 'user2', 'invite_code']
        
class CreateCoupleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Couple
        fields = ['user1']

    
    
class JoinCoupleSerializer(serializers.ModelSerializer):
    invite_code = serializers.CharField()

    class Meta:
        model = Couple
        fields = ['invite_code']

    def validate_invite_code(self, value):
        if not Couple.objects.filter(invite_code=value).exists():
            raise serializers.ValidationError("Invalid invite code.")
        return value