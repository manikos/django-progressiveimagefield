from django.db import models

from progressiveimagefield.fields import ProgressiveImageField


class TestModel(models.Model):
    """ A model for testing ProgressiveImageField """
    name = models.CharField(max_length=50)
    img = ProgressiveImageField()

    def __str__(self):
        return self.name
