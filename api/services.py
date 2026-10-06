from django.db import transaction
from rest_framework.exceptions import ValidationError

from .models import Category, Order, OrderItem, Product


@transaction.atomic
def create_order(*, user, product, quantity):

    product = Product.objects.select_for_update().get(id=product.id)

    # check stock
    if product.stock < quantity:
        raise ValidationError({'quantity': 'Not enough stock available.'})

    # calculate price using original price of the product
    total_amount = product.price * quantity

    order = Order.objects.create(user=user, total_amount=total_amount)

    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=quantity,
        price=product.price,
    )

    # reduce stock
    product.stock -= quantity
    product.save(update_fields=['stock'])

    return order
