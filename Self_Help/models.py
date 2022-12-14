from django.db import models


# Create your models here.
class TestModel(models.Model):
    tast = models.CharField(max_length=120)
    test = models.IntegerField()
    tust = models.CharField(max_length=120)

    def __str__(self):
        return self.tast
