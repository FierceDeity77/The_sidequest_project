from django.db import models
from django.conf import settings  # this points to AUTH_USER_MODEL
from django.utils.text import slugify
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Platform(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class Game(models.Model):
    title = models.CharField(max_length=255)
    platforms = models.ManyToManyField(Platform, related_name="games")
    genre = models.ManyToManyField(Genre, related_name="games")
    description = models.TextField()
    release_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    average_rating = models.FloatField(default=0.0)
    cover_image = models.ImageField(upload_to="game_covers/", blank=True, null=True)
    content_type = models.CharField(max_length=20, null=True)
    slug = models.SlugField(unique=True)


    class Meta:
        unique_together = ("title", "slug")



    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # references your custom User model
        null=True,
        on_delete=models.CASCADE,
        related_name="game_author"
    )


    def save(self, *args, **kwargs):
            if not self.slug:  # Only generate if slug is not already set
                self.slug = slugify(f"{self.author.id}-{self.title}") # add value into slug field using title and id of the author
            super().save(*args, **kwargs)


    def update_average_rating(self):
        ratings = self.ratings.all()  # reverse relationship "ratings" being related name in the relationship
        if ratings.exists():
            self.average_rating = sum(r.value for r in ratings) / ratings.count() # gets the average rating from ratings table
        else:
            self.average_rating = 0
        self.save()


    def __str__(self):
        return self.title
    

class Community(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="communities")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    icon = models.ImageField(upload_to="community_icons/", blank=True, null=True)
    banner = models.ImageField(upload_to="community_banners/", blank=True, null=True)
    content_type = models.CharField(max_length=20, null=True)
    slug = models.SlugField(unique=True, default=None)
    is_main = models.BooleanField(default=False)  # True for the game's main community, False for sub-communities
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="sub_communities")


    class Meta:
        unique_together = ("game", "name", "parent")  # Prevent duplicates inside same game


    def save(self, *args, **kwargs):
            if not self.slug:  # Only generate if slug is not already set
                self.slug = slugify(f"{self.created_by.id}-{self.name}") # add value into slug field using title and id of the author
            super().save(*args, **kwargs)


    def __str__(self):
        if self.parent:
            return f"{self.parent.name} › {self.name}"
        return self.name
    

# Signal: When a game is created, also create its main community
@receiver(post_save, sender=Game)
def create_main_community(sender, instance, created, **kwargs):
    if created:
        Community.objects.create(
            game=instance,
            name=instance.title,
            is_main=True,
            content_type="Community",
            description=f"The main community for {instance.title}",
            created_by=instance.author  # always set from the game's author this comes from author field from game model
        )
    

class Topic(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="topics")
    title = models.CharField(max_length=255)
    content = models.TextField()
    spoiler = models.BooleanField(default=False) 
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, default=None)
    comments = GenericRelation("Comments", related_name="topic_comments") # for querying comments from generic relation

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
    

    
class Rating(models.Model):
    game = models.ForeignKey(Game, related_name="ratings", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()  # e.g. 1–5 stars
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("game", "author")  # prevent same user rating the same game multiple times

    def __str__(self):
            return f"{self.user} rated {self.game} {self.value}"
    
    

class Review(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    comments = GenericRelation("Comments", related_name="review_comments")


    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # references your custom User model
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    def __str__(self):
        return f"{self.title} by {self.author}"
    
    

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
    comments = GenericRelation("Comments", related_name="guide_comments")

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="guides")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guides"
    )

    def __str__(self):
        return f"{self.title} ({self.guide_type})"
    

    
class Comments(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    # ---- Generic relation to ANY model ----
    content_type = models.ForeignKey(ContentType, null=True,on_delete=models.CASCADE)  # tells Django what model
    object_id = models.PositiveIntegerField(null=True)  # stores the ID of that object
    content_object = GenericForeignKey("content_type", "object_id")  # links to the object

     # This allows a comment to be a reply to another comment, relationship to itself
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )