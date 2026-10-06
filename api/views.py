# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.generics import (
#     ListCreateAPIView,
#     RetrieveUpdateDestroyAPIView,
# )

# from django.shortcuts import get_object_or_404
from rest_framework.permissions import (  # noqa: I001
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.viewsets import ModelViewSet

from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import action

from .models import Category, Order, Product
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from .serializers import (
    CategoryDetailSerializer,
    CategorySerializer,
    ProductSerializer,
    OrderSerializer,
)

from .filters import ProductFilter
from .pagination import ProductPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from django.db import transaction


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategorySerializer

    permission_classes = [IsAdminOrReadOnly]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filterset_class = ProductFilter
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]

    search_fields = ['name', 'description']
    ordering_fields = ['price', 'stock', 'created_at', 'name']

    pagination_class = ProductPagination


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrAdmin, IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()

        if order.status in ['delivered', 'canceled']:
            return Response(
                {
                    'error': 'Cannot cancel an order that is already delivered or canceled.'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        order.status = 'canceled'
        order.save(update_fields=['status'])

        return Response(
            {'status': 200, 'message': 'Order canceled successfully.'},
            status=status.HTTP_200_OK,
        )
