from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.


class Profile(models.Model):

    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=50, null=False, blank=False)
    bio = models.CharField(max_length=250, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profilepic', null=True, blank=False)
    is_celeb = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user_id.username

    def split_biography(self):
        return self.bio.split("\n")


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=250, null=True, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    liked = models.ManyToManyField(
        User, default=None, blank=True, related_name='liked')

    likes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-posted_on']

    # def __str__(self):
    #     return self.caption


class Post_media(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to='post_uploaded',
                            validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png', 'MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    position = models.IntegerField()


class Follow(models.Model):
    id = models.AutoField(primary_key=True)
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return self.follower.username + '->' + self.following.username


class Like(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):

    text = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='commenter')
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='child')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['created_at']


class Story(models.Model):
    story = models.FileField(upload_to='Stories_uploaded',
                             validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png', 'MOV', 'avi', 'mp4', 'webm', 'mkv'])])

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='story')
