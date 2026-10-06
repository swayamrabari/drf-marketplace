from django.urls import include, path  # noqa: I001

# from .views import CategoryListView, CategoryDetailView
from .views import CategoryViewSet, OrderViewSet, ProductViewSet
from rest_framework.routers import DefaultRouter

# urlpatterns = [
#     path('categories/', CategoryListView.as_view(), name='category-list'),
#     path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
# ]

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('products', ProductViewSet, basename='products')
router.register('orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
]
