from decimal import Decimal
from uuid import uuid4

from django.db import transaction

from apps.cart.models import Cart, CartItem
from apps.inventory.models import Stock, StockLog

from .models import Order, OrderItem


def generate_order_number():
    return uuid4().hex[:24]


@transaction.atomic
def create_order_from_cart(*, user):
    cart = Cart.objects.select_for_update().get(user=user)
    cart_items = list(
        CartItem.objects.select_related("product")
        .filter(cart=cart, selected=True)
        .order_by("id")
    )

    if not cart_items:
        raise ValueError("购物车中没有可结算商品")

    stocks = {
        stock.product_id: stock
        for stock in Stock.objects.select_for_update().filter(
            product_id__in=[item.product_id for item in cart_items]
        )
    }

    total_amount = Decimal("0.00")
    for item in cart_items:
        stock = stocks.get(item.product_id)
        if stock is None or stock.quantity < item.quantity:
            raise ValueError("部分商品库存不足，请重新确认购物车")
        total_amount += item.product.price * item.quantity

    order = Order.objects.create(
        order_number=generate_order_number(),
        user=user,
        total_amount=total_amount,
        pay_amount=total_amount,
        status=Order.STATUS_PENDING_PAYMENT,
    )

    order_items = []
    stock_logs = []
    for item in cart_items:
        subtotal = item.product.price * item.quantity
        order_items.append(
            OrderItem(
                order=order,
                product_id=item.product_id,
                product_name=item.product.name,
                product_image=item.product.main_image,
                product_price=item.product.price,
                quantity=item.quantity,
                subtotal=subtotal,
            )
        )

        stock = stocks[item.product_id]
        before_qty = stock.quantity
        stock.quantity -= item.quantity
        stock.save(update_fields=["quantity", "updated_at"])
        stock_logs.append(
            StockLog(
                product_id=item.product_id,
                change_type=StockLog.CHANGE_OUT,
                change_amount=item.quantity,
                before_qty=before_qty,
                after_qty=stock.quantity,
                operator=user,
                remark=f"订单 {order.order_number} 提交扣减库存",
            )
        )

    OrderItem.objects.bulk_create(order_items)
    StockLog.objects.bulk_create(stock_logs)
    CartItem.objects.filter(id__in=[item.id for item in cart_items]).delete()

    return order


@transaction.atomic
def cancel_order(*, order, user):
    if order.user_id != user.id:
        raise PermissionError("无权取消该订单")

    if order.status != Order.STATUS_PENDING_PAYMENT:
        raise ValueError("当前订单不可取消")

    order_items = list(order.items.all().order_by("id"))
    stocks = {
        stock.product_id: stock
        for stock in Stock.objects.select_for_update().filter(
            product_id__in=[item.product_id for item in order_items]
        )
    }

    stock_logs = []
    for item in order_items:
        stock = stocks.get(item.product_id)
        if stock is None:
            continue

        before_qty = stock.quantity
        stock.quantity += item.quantity
        stock.save(update_fields=["quantity", "updated_at"])
        stock_logs.append(
            StockLog(
                product_id=item.product_id,
                change_type=StockLog.CHANGE_ROLLBACK,
                change_amount=item.quantity,
                before_qty=before_qty,
                after_qty=stock.quantity,
                operator=user,
                remark=f"订单 {order.order_number} 取消回补库存",
            )
        )

    if stock_logs:
        StockLog.objects.bulk_create(stock_logs)

    order.status = Order.STATUS_CANCELLED
    from django.utils import timezone

    order.cancelled_at = timezone.now()
    order.save(update_fields=["status", "cancelled_at"])
    return order


@transaction.atomic
def pay_order(*, order, user, payment_method):
    if order.user_id != user.id:
        raise PermissionError("无权支付该订单")

    if order.status != Order.STATUS_PENDING_PAYMENT:
        raise ValueError("当前订单不可支付")

    if payment_method not in {
        Order.PAYMENT_WECHAT,
        Order.PAYMENT_ALIPAY,
        Order.PAYMENT_BALANCE,
    }:
        raise ValueError("不支持的支付方式")

    from django.utils import timezone

    order.status = Order.STATUS_PAID
    order.payment_method = payment_method
    order.paid_at = timezone.now()
    order.save(update_fields=["status", "payment_method", "paid_at"])
    return order


@transaction.atomic
def complete_order(*, order, user):
    if getattr(user, "role", None) != "merchant":
        raise PermissionError("仅商家可完成订单")

    if order.status != Order.STATUS_PAID:
        raise ValueError("当前订单不可完成")

    from django.utils import timezone

    order.status = Order.STATUS_COMPLETED
    order.completed_at = timezone.now()
    order.save(update_fields=["status", "completed_at"])
    return order
