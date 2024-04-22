from django.shortcuts import get_object_or_404

from collection_project.money_collections.models import Payment


def payments_list():
    return Payment.objects.select_related("collection", "contributor").all()


def get_payment(payment_id):
    return get_object_or_404(Payment.objects.select_related("collection", "contributor"), id=payment_id)
