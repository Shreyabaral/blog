

# Create your models here.
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver


from django.db import models



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            instance.profile.save()

class post(models.Model):
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    title= models.CharField(max_length=100)
    text = models.TextField()
    created_date= models.DateTimeField(auto_now=True)
    published_date= models.DateTimeField(auto_now_add=True)

    def approve_comments(self):
        return self.comments.filter(approved_comments=True)

    def get_absolute_url(self):
        return reverse('post_details', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
class Comments(models.Model):
    post = models.ForeignKey('blog1.post', related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def approve (self):
        self.approved_comments= True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text

