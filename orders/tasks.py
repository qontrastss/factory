import time

from celery import shared_task

from orders.models import Order


@shared_task
def process_order(order_code):
    print(order_code)
    order = Order.objects.filter(code=order_code).first()
    print(order)
    time.sleep(10)
    order.order_status = 'Processed'
    order.save()
    return