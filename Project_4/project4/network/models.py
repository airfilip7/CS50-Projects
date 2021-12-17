from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
   following = models.ManyToManyField('User', default= None, blank = True, related_name="fllwing")
   followers = models.ManyToManyField('User', default=None, blank=True, related_name="fllwers")
   
   def __str__(self):
       return self.username
   
   def serialize(self):
       return {
           "following": [user.username for user in self.following.all()],
           "followers": [user.username for user in self.followers.all()],
       }

   

class Post(models.Model):
    User = models.ForeignKey('User', on_delete=models.CASCADE,)
    content = models.CharField(max_length=4056, null = False, blank = False)
    likes = models.ManyToManyField('User', blank = True, default=None, related_name="like")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.User.username} ({self.pk}) on date {self.timestamp}'
    
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.User,
            "content": self.content,
            "likes": [User.username for user in self.likes.all()],
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
        }

    
