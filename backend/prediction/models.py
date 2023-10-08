from django.db import models

# Create your models here.
class PredictionImages(models.Model):
    image = models.ImageField(null=True,blank=True,upload_to="predictionImages")
    