from rest_framework import generics, permissions, status
from .models import Movie, Couple
from .serializers import MovieSerializer, CoupleSerializer
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
        serializer.save(user=self.request.user)

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
