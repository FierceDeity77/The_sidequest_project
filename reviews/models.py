from django.db import models
from django.utils import timezone
from django.conf import settings  # this points to AUTH_USER_MODEL
from content.models.game_model import Game
from django.contrib.contenttypes.fields import GenericRelation


class Review(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    comments = GenericRelation("content.Comments", related_name="review_comments")
    # points to content app

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # references your custom User model
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    def __str__(self):
        return f"{self.title} by {self.author}"