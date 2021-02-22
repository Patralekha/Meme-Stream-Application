from django.db import models
from django.utils import timezone
# Create your models here.


#Meme model with attributes of a meme as fields
class Meme(models.Model):
    id=models.AutoField(primary_key=True)
    caption=models.TextField(blank=True)
    url=models.URLField(max_length=200)
    name=models.CharField(max_length=200)
    creationDateTime=models.DateTimeField(blank=True,null=True)
    creationDate=models.DateField(blank=True,null=True)
    lastUpdate=models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return "{}-{}".format(self.id,self.caption,self.url)






