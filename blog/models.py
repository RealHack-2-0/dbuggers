from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from .bad_words import isBad
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_even(value):
    if isBad(value):
        raise ValidationError(
            _('"%(value)s" contains offensive word(s)'),
            params={'value': value},
        )

class Post(models.Model):
    title = models.CharField(max_length=100, validators=[validate_even])
    content = models.TextField(validators=[validate_even])
    date_posted= models.DateTimeField(default= timezone.now)
    author= models.ForeignKey(User,on_delete=models.CASCADE)
    read = models.BooleanField(default= 0)
    tags = models.TextField(max_length=100,null=True)
    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Answer(models.Model):
    content = models.TextField( validators=[validate_even])
    date_posted= models.DateTimeField(default= timezone.now)
    author= models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Post, on_delete=models.CASCADE)

class Tag(models.Model):
    content = models.TextField(null=True)



class Qvote(models.Model):

    votes =  models.IntegerField(default =0)
    author= models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Post, on_delete=models.CASCADE)

class Avote(models.Model):

    votes =  models.IntegerField(default =0)
    author= models.ForeignKey(User,on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)