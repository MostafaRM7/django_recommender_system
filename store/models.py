from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    categories = models.ManyToManyField(Category, related_name='products')

    def recommendation_score(self, user):
        from recommender.models import CategoryWeight
        try:
            category_weights = CategoryWeight.objects.filter(user=user)
            category_weights = category_weights.filter(category__in=self.categories.all())
            category_weights = category_weights.aggregate(weight=models.Sum('weight'))
            return category_weights.get('weight') or 0.0
        except CategoryWeight.DoesNotExist:
            return 0.0

    def __str__(self):
        return self.title
