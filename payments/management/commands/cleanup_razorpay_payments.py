from django.core.management.base import BaseCommand
from payments.models import Payment


class Command(BaseCommand):
    help = 'Remove Razorpay-related payments from the database'

    def handle(self, *args, **options):
        # Count payments with razorpay_order_id
        razorpay_payments_count = Payment._default_manager.exclude(razorpay_order_id='').count()
        
        if razorpay_payments_count > 0:
            # Remove payments with razorpay_order_id
            deleted_count = Payment._default_manager.exclude(razorpay_order_id='').delete()[0]
            self.stdout.write(
                self.style.SUCCESS(f'Successfully removed {deleted_count} Razorpay payments')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('No Razorpay payments found in the database')
            )