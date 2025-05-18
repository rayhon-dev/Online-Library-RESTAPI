from celery import shared_task
from django.utils import timezone
from lending.models import BookReservation, BookLending
from decimal import Decimal

@shared_task
def expire_reservations():
    now = timezone.now()
    BookReservation.objects.filter(is_active=True, expires_at__lt=now).update(is_active=False)


@shared_task
def update_overdue_lendings():
    now = timezone.now()
    lendings = BookLending.objects.filter(status='active', due_date__lt=now)

    updated_lendings = []
    for lending in lendings:
        days_overdue = (now - lending.due_date).days
        if days_overdue > 0:
            lending.status = 'overdue'
            lending.penalty_amount = lending.daily_price * Decimal('0.01') * days_overdue
            updated_lendings.append(lending)

    if updated_lendings:
        BookLending.objects.bulk_update(updated_lendings, ['status', 'penalty_amount'])


if __name__ == "__main__":
    from lending.tasks import deactivate_expired_reservations
    deactivate_expired_reservations.delay()

