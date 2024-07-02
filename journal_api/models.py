from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.title