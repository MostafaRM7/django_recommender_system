from django.db.models import Sum, Case, When, FloatField
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from recommender.utils import category_weight_increase
from .serializers import CategorySerializer, ProductSerializer
from ..models import Category, Product
from recommender.models import CategoryWeight


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('categories').all()
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        category_weight_increase(request.user, instance.categories.all())
        serializer = self.get_serializer(instance)
        print(instance.recommendation_score(request.user))
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            recommendation_score=Sum(
                Case(
                    When(categories__categoryweight__user=user, then='categories__categoryweight__weight'),
                    default=0.0,
                    output_field=FloatField(),
                )
            )
        )
        queryset = queryset.order_by('-recommendation_score')
        return queryset


class HomeViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.prefetch_related('categories').all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = super().get_queryset()
            highest_weight = CategoryWeight.objects.filter(user=user).order_by('-weight')[0:10].values_list('category', flat=True)
            queryset = queryset.filter(categories__in=highest_weight)
            return queryset
