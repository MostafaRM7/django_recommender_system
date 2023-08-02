from .models import CategoryWeight


def category_weight_increase(user, categories: list):
    for category in categories:
        obj, created = CategoryWeight.objects.get_or_create(user=user, category=category)
        obj.weight += 0.1
        obj.save()
        print(obj.weight)
