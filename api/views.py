from rest_framework import generics, permissions
from .models import Movie
from .serializers import MovieSerializer

class LikedMoviesListCreateView(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]  # 🔐 JWT required

    def get_queryset(self):
        return Movie.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
