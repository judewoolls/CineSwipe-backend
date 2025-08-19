from django.db import models
from django.contrib.auth.models import User
import random
import string

class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_movies")
    movie_id = models.IntegerField()  # TMDb ID
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie_id')  # Prevent duplicates

    def __str__(self):
        return f"{self.title} ({self.release_year})"

class Couple(models.Model):
    """Model to represent a couple formed by two users."""
    # if the user1 wants to cancel then the status will be set to 
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
    ]
    
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="couple_user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="couple_user2")
    invite_code = models.CharField(max_length=10, unique=True)  # Unique invite code for the couple
    status = models.CharField(max_length=20, default='waiting', choices=STATUS_CHOICES) 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure that a couple is unique by the combination of user1 and user2
        constraints = [
        models.UniqueConstraint(fields=['user1', 'user2'], name='unique_couple')
    ]

    def __str__(self):
        if not self.user2:
            return f"Couple: {self.user1.username} & Waiting for partner"
        else:
            return f"Couple: {self.user1.username} & {self.user2.username}"
    
    def create_invite_code(self):
        invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        if Couple.objects.filter(invite_code=invite_code).exists():
            return self.create_invite_code()
        return invite_code
        
    
    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self.create_invite_code()
        super().save(*args, **kwargs)
        
class CoupleRequest(models.Model):
    """Model to handle requests between users to form a couple."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="couple_requests_sent")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="couple_requests_received")
    couple = models.ForeignKey(Couple, on_delete=models.CASCADE, related_name="requests")
    status = models.CharField(max_length=20, default='pending', choices=STATUS_CHOICES)  # pending, accepted, rejected
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.sender.username} to {self.receiver.username} for couple {self.couple.id}"