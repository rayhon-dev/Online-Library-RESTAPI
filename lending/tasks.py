from celery import shared_task
from django.utils import timezone
from lending.models import BookReservation, BookLending
from decimal import Decimal

@shared_task
def expire_reservations():
    now = timezone.now()
    reservations = BookReservation.objects.filter(is_active=True, expires_at__lt=now)
    for res in reservations:
        res.is_active = False
        res.save()

@shared_task
def update_overdue_lendings():
    now = timezone.now()
    lendings = BookLending.objects.filter(status='active', due_date__lt=now)
    for lending in lendings:
        lending.status = 'overdue'
        # jarimani hisoblash
        days_overdue = (now - lending.due_date).days
        if days_overdue > 0:
            penalty_rate = Decimal('0.01')
            lending.penalty_amount = lending.daily_price * penalty_rate * days_overdue
        lending.save()


if __name__ == "__main__":
    from lending.tasks import deactivate_expired_reservations
    deactivate_expired_reservations.delay()

