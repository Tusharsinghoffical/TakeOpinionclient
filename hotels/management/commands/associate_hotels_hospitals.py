from django.core.management.base import BaseCommand
from hotels.models import Hotel
from hospitals.models import Hospital


class Command(BaseCommand):
    help = 'Associate hotels with nearby hospitals'

    def handle(self, *args, **options):
        # Get all hotels and hospitals
        hotels = Hotel._default_manager.all()
        hospitals = Hospital._default_manager.all()

        # Associate hotels with hospitals based on city
        associations_made = 0
        for hotel in hotels:
            # Find hospitals in the same city as the hotel
            nearby_hospitals = Hospital._default_manager.filter(city=hotel.city)
            
            if nearby_hospitals.exists():
                # Associate the hotel with nearby hospitals
                hotel.nearby_hospitals.set(nearby_hospitals)
                associations_made += nearby_hospitals.count()
                self.stdout.write(
                    f'Associated {nearby_hospitals.count()} hospitals with hotel "{hotel.name}"'
                )
            else:
                self.stdout.write(
                    f'No hospitals found in {hotel.city} for hotel "{hotel.name}"'
                )

        self.stdout.write(
            f'Successfully made {associations_made} hotel-hospital associations'
        )