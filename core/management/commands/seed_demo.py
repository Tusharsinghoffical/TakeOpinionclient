from django.core.management.base import BaseCommand

from treatments.models import TreatmentCategory, Treatment
from hospitals.models import Hospital, HospitalMedia
from doctors.models import Doctor
from blogs.models import BlogPost
from bookings.models import Accommodation
from core.models import Country, State


class Command(BaseCommand):
    help = "Seed demo data for TakeOpinion"

    def handle(self, *args, **options):
        # Categories
        medical = TreatmentCategory.objects.get_or_create(
            name="Orthopedics", type="medical"
        )[0]
        aesthetic = TreatmentCategory.objects.get_or_create(
            name="Cosmetic", type="aesthetic"
        )[0]
        wellness = TreatmentCategory.objects.get_or_create(
            name="Ayurveda", type="wellness"
        )[0]

        # Treatments
        knee = Treatment.objects.get_or_create(
            name="Knee Replacement", category=medical, defaults={"description": "Knee replacement details."}
        )[0]
        rhinoplasty = Treatment.objects.get_or_create(
            name="Rhinoplasty", category=aesthetic, defaults={"description": "Nose reshaping surgery."}
        )[0]
        panchakarma = Treatment.objects.get_or_create(
            name="Panchakarma", category=wellness, defaults={"description": "Ayurvedic detox therapy."}
        )[0]

        # Countries & States
        india = Country.objects.get_or_create(name="India", code="IN")[0]
        turkey = Country.objects.get_or_create(name="Turkey", code="TR")[0]
        maharashtra = State.objects.get_or_create(country=india, name="Maharashtra")[0]
        kerala = State.objects.get_or_create(country=india, name="Kerala")[0]
        istanbul = State.objects.get_or_create(country=turkey, name="Istanbul")[0]

        # Hospitals
        hosp1 = Hospital.objects.get_or_create(
            name="City Care Hospital",
            defaults={
                "country": india,
                "state": maharashtra,
                "about": "Multi-speciality hospital.",
                "is_takeopinion_choice": True,
            },
        )[0]
        hosp1.treatments.add(knee, rhinoplasty)
        HospitalMedia.objects.get_or_create(hospital=hosp1, image_url="https://picsum.photos/seed/h1/600/400")

        hosp2 = Hospital.objects.get_or_create(
            name="Green Wellness Center",
            defaults={"country": india, "state": kerala, "about": "Wellness and Ayurveda center."},
        )[0]
        hosp2.treatments.add(panchakarma)
        HospitalMedia.objects.get_or_create(hospital=hosp2, image_url="https://picsum.photos/seed/h2/600/400")

        # Doctors
        doc1 = Doctor.objects.get_or_create(
            name="Dr. Arjun Mehta",
            defaults={"key_points": "Orthopedic surgeon", "education": "MS Ortho", "experience_years": 12},
        )[0]
        doc1.treatments.add(knee)
        doc1.hospitals.add(hosp1)

        doc2 = Doctor.objects.get_or_create(
            name="Dr. Sara Kapoor",
            defaults={"key_points": "Cosmetic surgeon", "education": "MCh Plastic", "experience_years": 9},
        )[0]
        doc2.treatments.add(rhinoplasty)
        doc2.hospitals.add(hosp1)

        # Blogs
        BlogPost.objects.get_or_create(
            title="Knee Replacement: What to Expect",
            defaults={"content": "Pre-op, procedure, and recovery.", "treatment": knee, "doctor": doc1, "hospital": hosp1},
        )
        BlogPost.objects.get_or_create(
            title="Medical Visa Guide for India",
            defaults={"content": "Documents, process, timelines.", "is_medical_visa": True},
        )

        # Accommodations
        Accommodation.objects.get_or_create(hospital=hosp1, name="Hotel Comfort Inn", price_per_night=80)
        Accommodation.objects.get_or_create(hospital=hosp1, name="Budget Stay", price_per_night=45)
        Accommodation.objects.get_or_create(hospital=hosp2, name="Kerala Retreat", price_per_night=90)

        self.stdout.write(self.style.SUCCESS("Demo data seeded."))


