from django.db import models


class Edition(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploads/edition/', default='')

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_editions():
        return Edition.objects.all()
