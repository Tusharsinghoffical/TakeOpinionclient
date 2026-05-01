from django.core.management.base import BaseCommand
from hotels.models import Hotel
from hospitals.models import Hospital


class Command(BaseCommand):
    help = 'Populate sample hotel data for testing'

    def handle(self, *args, **options):
        # Sample hotel data
        hotels_data = [
            {
                'name': 'Grand Plaza Hotel',
                'description': 'Luxury hotel with excellent amenities and services',
                'address': '123 Main Street',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'postal_code': '400001',
                'phone': '+91 22 1234 5678',
                'email': 'info@grandplaza.com',
                'website': 'https://www.grandplaza.com',
                'rating': 4.5,
                'price_per_night': 8000.00,
                'amenities': 'Free WiFi, Swimming Pool, Gym, Restaurant, Spa, Parking',
            },
            {
                'name': 'Seaside Resort',
                'description': 'Beautiful seaside resort with ocean views',
                'address': '456 Beach Road',
                'city': 'Goa',
                'state': 'Goa',
                'postal_code': '403001',
                'phone': '+91 832 234 5678',
                'email': 'reservations@seasideresort.com',
                'website': 'https://www.seasideresort.com',
                'rating': 4.2,
                'price_per_night': 6500.00,
                'amenities': 'Free WiFi, Beach Access, Pool, Restaurant, Bar, Spa',
            },
            {
                'name': 'Mountain View Inn',
                'description': 'Cozy inn with stunning mountain views',
                'address': '789 Hill Road',
                'city': 'Manali',
                'state': 'Himachal Pradesh',
                'postal_code': '175131',
                'phone': '+91 1902 234 567',
                'email': 'info@mountainviewinn.com',
                'website': 'https://www.mountainviewinn.com',
                'rating': 4.0,
                'price_per_night': 4500.00,
                'amenities': 'Free WiFi, Mountain Views, Restaurant, Parking, Fireplace',
            },
            {
                'name': 'City Central Hotel',
                'description': 'Conveniently located in the heart of the city',
                'address': '101 Central Avenue',
                'city': 'Delhi',
                'state': 'Delhi',
                'postal_code': '110001',
                'phone': '+91 11 2345 6789',
                'email': 'bookings@citycentral.com',
                'website': 'https://www.citycentral.com',
                'rating': 4.3,
                'price_per_night': 5500.00,
                'amenities': 'Free WiFi, Central Location, Restaurant, Gym, Parking',
            },
            {
                'name': 'Heritage Palace',
                'description': 'Historic palace converted into a luxury hotel',
                'address': '202 Heritage Lane',
                'city': 'Jaipur',
                'state': 'Rajasthan',
                'postal_code': '302001',
                'phone': '+91 141 234 5678',
                'email': 'reservations@heritagepalace.com',
                'website': 'https://www.heritagepalace.com',
                'rating': 4.7,
                'price_per_night': 9500.00,
                'amenities': 'Free WiFi, Heritage Architecture, Pool, Spa, Restaurant, Parking',
            }
        ]

        # Create hotels
        for hotel_data in hotels_data:
            hotel, created = Hotel._default_manager.get_or_create(
                name=hotel_data['name'],
                defaults=hotel_data
            )
            if created:
                self.stdout.write(
                    f'Successfully created hotel "{hotel.name}"'
                )
            else:
                self.stdout.write(
                    f'Hotel "{hotel.name}" already exists'
                )

        self.stdout.write(
            'Successfully populated sample hotel data'
        )