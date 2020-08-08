from django.db import models

class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True,default="product")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class MultipleImages(models.Model):
    photoDetails=models.ForeignKey(Photo, on_delete=models.CASCADE)
    img=models.ImageField(upload_to='upload/',default="dummy.jpg")
