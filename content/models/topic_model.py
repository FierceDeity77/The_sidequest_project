from django.db import models
from django.conf import settings  # this points to AUTH_USER_MODEL
from django.utils.text import slugify
from django.utils import timezone
from .community_model import Community
from django.contrib.contenttypes.fields import GenericRelation


class Topic(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="topics")
    title = models.CharField(max_length=255)
    text = models.TextField()
    spoiler = models.BooleanField(default=False) 
    created_at = models.DateTimeField(default=timezone.now)
    content_type = models.CharField(max_length=20, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, default=None)
    comments = GenericRelation("Comments", related_name="topic_comments") # for querying comments from generic relation

    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="topic_upvotes", blank=True)
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="topic_downvotes", blank=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_topics"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # ensure uniqueness
            while Topic.objects.filter(slug=slug).exists():
                slug = f"{self.author.id}-{base_slug}-{counter}" # topic id, slug and counter
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.community})"
    