from django.db import models
from django.contrib.auth.models import User


class Word(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    english = models.CharField(max_length=50)
    ukrainian = models.CharField(max_length=50)
    complete = models.BooleanField(default=False)
    examples = models.CharField(max_length=100, default='no example')

    def __str__(self):
        return self.english

    class Meta:
        ordering = ['complete']
