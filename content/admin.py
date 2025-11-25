from django.contrib import admin
from .models import Platform, Genre, Game, Comments, Community, Topic, Notification

# Register your models here.

class GameAdmin(admin.ModelAdmin):
    list_filter = ("author", "genre", "release_date",)
    list_display = ("title", "created_at", "author", "release_date", "cover_image",
                    "created_at", "content_type", "slug", "description")
    list_editable = ["cover_image", "release_date", "description"]
    # prepopulated_fields = {"slug": ("title",)}


class CommunityAdmin(admin.ModelAdmin):
    list_filter = ("name", "created_by", "is_main",)
    list_display = ("name", "created_by", "created_at", "is_main", "icon", "banner",
                    "content_type", "parent", "game", "slug")
    #list_editable = ["content_type"]
    

class TopicAdmin(admin.ModelAdmin):
    list_filter = ("title", "community", "created_at",)
    list_display = ("id", "title", "author", "created_at", "community", "slug", "content_type")


class NotificationAdmin(admin.ModelAdmin):
    list_filter = ("recipient", "actor", "verb", "is_read", "created_at")
    list_display = ("id", "recipient", "actor", "verb", "is_read", "created_at", "url")

class PlatformAdmin(admin.ModelAdmin):
    list_filter = ["name"]


class GenreAdmin(admin.ModelAdmin):
    list_filter = ["name"]


class CommentAdmin(admin.ModelAdmin):
    list_filter = ("content_type", "created_at", "author")
    list_display = ("id", "text", "content_type", "object_id", "created_at", "author", "parent")



admin.site.register(Game, GameAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Community, CommunityAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Comments, CommentAdmin)
admin.site.register(Notification, NotificationAdmin)
