import uuid
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from notification.models import Notification
# Create your models here.

def user_directory_path(instance,filename):
    # The post pictures will be uploaded to MEDIA_ROOT/user_<id>/filename
    return 'user_{0}/{1}'.format(instance.user.id,filename)


class Tag(models.Model):
    title = models.CharField(max_length=50,verbose_name='Tag')
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name_plural='Tags'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tag_posts", args=[self.slug])
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class PostFileContent(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='content_owner')
    file = models.FileField(upload_to=user_directory_path)

class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    content = models.ManyToManyField(PostFileContent,related_name='contents')
    caption = models.TextField(max_length=9000,verbose_name='Caption')
    posted = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag,related_name='tags')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("post_details", args=[str(self.id)])
    
    def __str__(self):
        return f'Post User: {str(self.user).capitalize()} | Post Creation: {self.posted.strftime("%d %B, %Y at %I:%M:%S %p")}'
    
    def save(self,*args, **kwargs):
        if not self.caption and not self.content.exists():
            raise ValidationError("You must either provide caption or content for the post")
        super(Post,self).save(*args, **kwargs)
class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name='follower')
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')

    def user_follow(sender,instance,*args,**kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following

        notify = Notification(sender=sender,user=following,notification_type=3)
        notify.save()
    
    def user_unfollow(sender,instance,*args,**kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following

        notify = Notification.objects.filter(sender=sender,user=following,notification_type=3)
        notify.delete()

    def __str__(self):
        return f'{self.follower} follows {self.following}'


class Stream(models.Model):
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name='stream_following')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    date = models.DateTimeField()

    def add_post(sender,instance,*args, **kwargs):
        post = instance
        user= post.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post,user=follower.follower,date=post.posted,following=user)
            stream.save()

    def __str__(self):
        return f'Post of "{self.following.username}" ({self.post.id}) streamed to "{self.user.username}"'
    
class Likes(models.Model):
    user = models.ForeignKey(User, related_name='user_like', on_delete=models.CASCADE)
    post = models.ForeignKey(Post,related_name='post_like', on_delete=models.CASCADE)

    def user_liked_post(sender,instance,*args, **kwargs):
        like = instance
        post = like.post
        sender = like.user

        notify = Notification(post=post,sender=sender,user=post.user,notification_type=1)
        notify.save()

    def user_unlike_post(sender,instance,*args,**kwargs):
        like = instance
        post =like.post
        sender = like.user
        notify = Notification.objects.filter(post=post,sender=sender,notification_type=1)
        notify.delete()

# For Stream
post_save.connect(Stream.add_post,sender=Post)

# For Follow
post_save.connect(Follow.user_follow,sender=Follow)

# For Unfollow
post_delete.connect(Follow.user_unfollow,sender=Follow)

# For Like
post_save.connect(Likes.user_liked_post,sender=Likes)

# For Unlike
post_delete.connect(Likes.user_unlike_post,sender=Likes)