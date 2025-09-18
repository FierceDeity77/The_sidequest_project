from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.templatetags.static import static

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields): 
        if not email: # email is required
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email) # converts the email into a consistent format
        user = self.model(email=email, **extra_fields) # create instance of your custom User model with email + extra fields
        user.set_password(password)  # securely hashes password before saving
        user.save(using=self._db) # saves to the database
        return user

    def create_superuser(self, email, password=None, **extra_fields): # defines how superuser is created
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True: # prevents mistake like creating superuser without privileges
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields) # returns create user logic
    
    
class CustomUser(AbstractBaseUser, PermissionsMixin): # no need to add password field, abstractbaseuser already has a password field and handles hashing
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, blank=True, null=False)
    avatar = models.ImageField(upload_to="user_avatars/", null=True)
    about = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=50, choices=[("admin", "Admin"), ("moderator", "Moderator"), ("user", "User")], default="user")
    karma = models.IntegerField(default=0)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    following = models.ManyToManyField(
    "self",
    through="UserFollow",
    symmetrical=False,
    related_name="followers"
)

    objects = CustomUserManager() # tells django to use your custommanager when creating users

    USERNAME_FIELD = 'email' # the field django uses for login
    REQUIRED_FIELDS = ['password'] # add fields here if you want them to be required

    def __str__(self): # for readability in admin/shell
        return self.email
    
    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return static("default_images/default-avatar.jpg") # returns default avatar if user has not uploaded one
    
    
class UserFollow(models.Model):
    follower = models.ForeignKey("CustomUser", related_name="following_rel", on_delete=models.CASCADE)
    following = models.ForeignKey("CustomUser", related_name="followers_rel", on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")