from django.db import models
from store.models import Category, Product
from django.contrib.auth import get_user_model

# Create your models here.


class CategoryWeight(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    weight = models.FloatField(default=0.0, db_index=True)

    def __str__(self):
        return f'{self.category.name} - {self.weight}'
