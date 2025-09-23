from django.db import models
from django.conf import settings  # this points to AUTH_USER_MODEL
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from content.models.game_model import Game

class Guide(models.Model):
    GUIDE_TYPES = [
        ("walkthrough", "Walkthrough"),
        ("tips", "Tips"),
        ("strategy", "Strategy"),
    ]

    title = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=GUIDE_TYPES)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    comments = GenericRelation("content.Comments", related_name="guide_comments")
    # points to content app

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="guides")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guides"
    )

    def __str__(self):
        return f"{self.title} ({self.guide_type})"
