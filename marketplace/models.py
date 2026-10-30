from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    skills = models.CharField(max_length=300)
    experience = models.IntegerField()
    portfolio = models.URLField(blank=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    bio = models.TextField()

    def __str__(self):
        return self.name


class Project(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, default="Web Development")
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    skills_required = models.CharField(max_length=300)
    deadline = models.DateField()

    STATUS_CHOICES = [
       ("Open", "Open"),
       ("Closed", "Closed"),
       ("Completed", "Completed"),
    ]

    status = models.CharField(
       max_length=20,
       choices=STATUS_CHOICES,
       default="Open"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    
class Bid(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="bids"
    )

    freelancer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    delivery_days = models.IntegerField()

    proposal = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Accepted", "Accepted"),
            ("Rejected", "Rejected"),
        ],
        default="Pending",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.freelancer.username} - {self.project.title}"
    
class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    message = models.CharField(max_length=255)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    

class Review(models.Model):

    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE
    )

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="given_reviews"
    )

    freelancer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_reviews"
    )

    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.client.username} rated "
            f"{self.freelancer.username} ({self.rating}/5)"
        )
    
class Conversation(models.Model):
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="client_conversations"
    )

    freelancer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="freelancer_conversations"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.username} ↔ {self.freelancer.username}"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender.username}: {self.message[:25]}"
    

from django.utils import timezone


class Message(models.Model):

    sender = models.ForeignKey(
        User,
        related_name="sent_messages",
        on_delete=models.CASCADE
    )

    receiver = models.ForeignKey(
        User,
        related_name="received_messages",
        on_delete=models.CASCADE
    )

    message = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"