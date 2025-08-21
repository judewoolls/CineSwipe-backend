from rest_framework import generics, permissions, status
from .models import Movie, Couple, Match
from .serializers import MovieSerializer, CoupleSerializer, JoinCoupleSerializer, MatchSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# API views for handling liked movies and couple data
class LikedMoviesListCreateView(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]  # 🔐 JWT required

    def get_queryset(self):
        return Movie.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        movie, created = Movie.objects.get_or_create(
            user=self.request.user,
            movie_id=serializer.validated_data['movie_id'],
            defaults={
                "title": serializer.validated_data.get("title"),
                "poster_path": serializer.validated_data.get("poster_path"),
                "release_year": serializer.validated_data.get("release_year"),
            }
        )

        try:
            couple = Couple.objects.get(user1=self.request.user)
        except Couple.DoesNotExist:
            try:
                couple = Couple.objects.get(user2=self.request.user)
            except Couple.DoesNotExist:
                couple = None
                
        
        if couple:
            partner = couple.user1 if couple.user2 == self.request.user else couple.user2
            
            if partner:
                partner_liked = Movie.objects.filter(user=partner, movie_id=movie.movie_id).exists()
                
                if partner_liked:
                    if not Match.objects.filter(couple=couple, movie__movie_id=movie.movie_id).exists():
                        Match.objects.get_or_create(couple=couple, movie=movie)
                    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def couple_data_view(request):
    """
    Retrieve the logged-in user's couple data.
    """
    try:
        couple = Couple.objects.get(user1=request.user)
    except Couple.DoesNotExist:
        try:
            couple = Couple.objects.get(user2=request.user)
        except Couple.DoesNotExist:
            couple = None

    if not couple:
        return Response({"error": "No couple data found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CoupleSerializer(couple)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_couple_view(request):
    """
    Create a couple instance with the given users.
    """
    if Couple.objects.filter(user1=request.user).exists() or Couple.objects.filter(user2=request.user).exists():
        return Response({"error": "User is already in a couple."}, status=status.HTTP_400_BAD_REQUEST)

    couple = Couple(user1=request.user)
    couple.invite_code = couple.create_invite_code()
    invite_code = couple.invite_code
    couple.save()
    return Response({"invite_code": invite_code}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_couple_view(request):
    """
    Join an existing couple using the invite code.
    """
    serializer = JoinCoupleSerializer(data=request.data)
    if serializer.is_valid():
        invite_code = serializer.validated_data['invite_code']
        try:
            couple = Couple.objects.get(invite_code=invite_code)
            if couple.user2:
                return Response({"error": "Couple already has two members."}, status=status.HTTP_400_BAD_REQUEST)
            couple.user2 = request.user
            couple.status = 'active'
            couple.save()
            return Response({"message": "Successfully joined the couple."}, status=status.HTTP_200_OK)
        except Couple.DoesNotExist:
            return Response({"error": "Invalid invite code."}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def leave_couple_view(request):
    """
    Leave the couple if the user is part of one.
    """
    try:
        couple = Couple.objects.get(user1=request.user)
        couple.delete()
        return Response({"message": "Successfully left the couple."}, status=status.HTTP_200_OK)
    except Couple.DoesNotExist:
        try:
            couple = Couple.objects.get(user2=request.user)
            couple.user2 = None
            couple.status = 'waiting'
            couple.save()
            return Response({"message": "Successfully left the couple."}, status=status.HTTP_200_OK)
        except Couple.DoesNotExist:
            return Response({"error": "You are not part of any couple."}, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def matches_view(request):
    """
    Retrieve matches for the logged-in user.
    """
    try:
        couple = Couple.objects.get(user1=request.user)
    except Couple.DoesNotExist:
        try:
            couple = Couple.objects.get(user2=request.user)
        except Couple.DoesNotExist:
            return Response({"error": "No couple data found."}, status=status.HTTP_404_NOT_FOUND)

    matches = Match.objects.filter(couple=couple)
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
