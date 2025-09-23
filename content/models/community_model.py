from django.db import models
from django.conf import settings  # this points to AUTH_USER_MODEL
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save
from .game_model import Game


class Community(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="communities")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    # creator/author of the community
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    icon = models.ImageField(upload_to="community_icons/", blank=True, null=True)
    banner = models.ImageField(upload_to="community_banners/", blank=True, null=True)
    content_type = models.CharField(max_length=20, null=True)
    rules = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, default=None)
    is_main = models.BooleanField(default=False)  # True for the game's main community, False for sub-communities
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="sub_communities")
    
     # Members/followers
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="CommunityMembership", related_name="joined_communities")
    # Community-specific moderators
    moderators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="moderated_communities", blank=True)

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
        community = Community.objects.create(
            game=instance,
            name=instance.title,
            is_main=True,
            content_type="Community",
            description=f"The main community for {instance.title}",
            created_by=instance.author,  # always set from the game's author this comes from author field from game model
        )
        # Then add the game's author as moderator after creating the community
        community.moderators.add(instance.author)


class CommunityMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_moderator = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "community")  # prevent duplicate joins