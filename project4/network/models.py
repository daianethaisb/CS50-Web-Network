from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userPost")
    content = models.CharField(max_length=200)       
    post_date = models.DateTimeField(null=True, auto_now_add=True)
    likes = models.IntegerField(default = '0')

    def __str__(self):
        return f"Post {self.id} made by {self.user} on {self.post_date.strftime('%d %b %Y %H:%M:%S')}"
    
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userFollowing")
    user_follows = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userFollowed")

    def __str__(self):
        return f"{self.user} is following {self.user_follows}"
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userLike")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postLike")

    def __str__(self):
        return f"{self.user} liked {self.post}"