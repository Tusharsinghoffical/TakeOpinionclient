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
        # Create countries
        india, _ = Country._default_manager.get_or_create(name="India", code="IN")  # type: ignore
        turkey, _ = Country._default_manager.get_or_create(name="Turkey", code="TR")  # type: ignore
        thailand, _ = Country._default_manager.get_or_create(name="Thailand", code="TH")  # type: ignore
        mexico, _ = Country._default_manager.get_or_create(name="Mexico", code="MX")  # type: ignore
        malaysia, _ = Country._default_manager.get_or_create(name="Malaysia", code="MY")  # type: ignore
        
        # Create states
        maharashtra, _ = State._default_manager.get_or_create(country=india, name="Maharashtra")  # type: ignore
        kerala, _ = State._default_manager.get_or_create(country=india, name="Kerala")  # type: ignore
        delhi, _ = State._default_manager.get_or_create(country=india, name="Delhi")  # type: ignore
        bangalore, _ = State._default_manager.get_or_create(country=india, name="Karnataka")  # type: ignore
        tamil_nadu, _ = State._default_manager.get_or_create(country=india, name="Tamil Nadu")  # type: ignore
        
        istanbul, _ = State._default_manager.get_or_create(country=turkey, name="Istanbul")  # type: ignore
        antalya, _ = State._default_manager.get_or_create(country=turkey, name="Antalya")  # type: ignore
        
        bangkok, _ = State._default_manager.get_or_create(country=thailand, name="Bangkok")  # type: ignore
        phuket, _ = State._default_manager.get_or_create(country=thailand, name="Phuket")  # type: ignore
        
        cancun, _ = State._default_manager.get_or_create(country=mexico, name="Quintana Roo")  # type: ignore
        mexico_city, _ = State._default_manager.get_or_create(country=mexico, name="Mexico City")  # type: ignore
        
        kuala_lumpur, _ = State._default_manager.get_or_create(country=malaysia, name="Kuala Lumpur")  # type: ignore
        penang, _ = State._default_manager.get_or_create(country=malaysia, name="Penang")  # type: ignore

        # Create treatment categories
        medical_categories = [
            "Orthopedics", "Cardiology", "Neurology", "Oncology", "Dermatology",
            "Gastroenterology", "Urology", "Ophthalmology", "ENT", "Pediatrics"
        ]
        
        aesthetic_categories = [
            "Cosmetic Surgery", "Dermatology", "Dental", "Hair Transplant", "Body Contouring"
        ]
        
        wellness_categories = [
            "Ayurveda", "Yoga", "Meditation", "Detox", "Weight Management", 
            "Spa Treatments", "Alternative Medicine"
        ]
        
        # Create medical treatment categories
        medical_category_objects = []
        for cat_name in medical_categories:
            category, _ = TreatmentCategory._default_manager.get_or_create(  # type: ignore
                name=cat_name, type="medical"
            )
            medical_category_objects.append(category)
            
        # Create aesthetic treatment categories
        aesthetic_category_objects = []
        for cat_name in aesthetic_categories:
            category, _ = TreatmentCategory._default_manager.get_or_create(  # type: ignore
                name=cat_name, type="aesthetic"
            )
            aesthetic_category_objects.append(category)
            
        # Create wellness treatment categories
        wellness_category_objects = []
        for cat_name in wellness_categories:
            category, _ = TreatmentCategory._default_manager.get_or_create(  # type: ignore
                name=cat_name, type="wellness"
            )
            wellness_category_objects.append(category)

        # Create 50+ treatments
        treatments_data = [
            # Orthopedics treatments
            {"name": "Knee Replacement", "category": medical_category_objects[0], "description": "Surgical procedure to replace damaged knee joint with artificial components.", "starting_price": 8000.00},
            {"name": "Hip Replacement", "category": medical_category_objects[0], "description": "Surgical procedure to replace damaged hip joint with artificial components.", "starting_price": 9500.00},
            {"name": "Spinal Fusion", "category": medical_category_objects[0], "description": "Surgical technique to join two or more vertebrae in the spine.", "starting_price": 12000.00},
            {"name": "Arthroscopic Surgery", "category": medical_category_objects[0], "description": "Minimally invasive procedure to diagnose and treat joint problems.", "starting_price": 4500.00},
            {"name": "Shoulder Replacement", "category": medical_category_objects[0], "description": "Surgical procedure to replace damaged shoulder joint with artificial components.", "starting_price": 11000.00},
            
            # Cardiology treatments
            {"name": "Angioplasty", "category": medical_category_objects[1], "description": "Procedure to open blocked heart arteries using balloon catheter.", "starting_price": 7500.00},
            {"name": "Bypass Surgery", "category": medical_category_objects[1], "description": "Surgical procedure to redirect blood flow around blocked arteries.", "starting_price": 15000.00},
            {"name": "Heart Valve Replacement", "category": medical_category_objects[1], "description": "Surgical procedure to replace damaged heart valves.", "starting_price": 18000.00},
            {"name": "Pacemaker Implantation", "category": medical_category_objects[1], "description": "Procedure to implant a device that regulates heart rhythm.", "starting_price": 6000.00},
            {"name": "Cardiac Ablation", "category": medical_category_objects[1], "description": "Procedure to correct heart rhythm problems by destroying abnormal tissue.", "starting_price": 8500.00},
            
            # Neurology treatments
            {"name": "Brain Tumor Removal", "category": medical_category_objects[2], "description": "Surgical procedure to remove abnormal growths in the brain.", "starting_price": 20000.00},
            {"name": "Spinal Cord Surgery", "category": medical_category_objects[2], "description": "Surgical treatment for spinal cord injuries and conditions.", "starting_price": 16000.00},
            {"name": "Deep Brain Stimulation", "category": medical_category_objects[2], "description": "Treatment for movement disorders using implanted electrodes.", "starting_price": 25000.00},
            {"name": "Epilepsy Surgery", "category": medical_category_objects[2], "description": "Surgical treatment for drug-resistant epilepsy.", "starting_price": 18000.00},
            {"name": "Stroke Rehabilitation", "category": medical_category_objects[2], "description": "Comprehensive rehabilitation program for stroke patients.", "starting_price": 3500.00},
            
            # Oncology treatments
            {"name": "Chemotherapy", "category": medical_category_objects[3], "description": "Treatment using drugs to destroy cancer cells.", "starting_price": 5000.00},
            {"name": "Radiation Therapy", "category": medical_category_objects[3], "description": "Treatment using high-energy radiation to kill cancer cells.", "starting_price": 7000.00},
            {"name": "Immunotherapy", "category": medical_category_objects[3], "description": "Treatment that helps immune system fight cancer.", "starting_price": 12000.00},
            {"name": "Targeted Therapy", "category": medical_category_objects[3], "description": "Treatment that targets specific cancer cell features.", "starting_price": 15000.00},
            {"name": "Stem Cell Transplant", "category": medical_category_objects[3], "description": "Procedure to replace damaged bone marrow with healthy stem cells.", "starting_price": 22000.00},
            
            # Cosmetic treatments
            {"name": "Rhinoplasty", "category": aesthetic_category_objects[0], "description": "Surgical reshaping of the nose for aesthetic or functional reasons.", "starting_price": 4500.00},
            {"name": "Breast Augmentation", "category": aesthetic_category_objects[0], "description": "Surgical procedure to increase breast size using implants.", "starting_price": 6000.00},
            {"name": "Liposuction", "category": aesthetic_category_objects[0], "description": "Surgical procedure to remove excess fat from specific body areas.", "starting_price": 3500.00},
            {"name": "Facelift", "category": aesthetic_category_objects[0], "description": "Surgical procedure to reduce signs of aging in the face and neck.", "starting_price": 8000.00},
            {"name": "Tummy Tuck", "category": aesthetic_category_objects[0], "description": "Surgical procedure to remove excess skin and fat from the abdomen.", "starting_price": 5500.00},
            
            # Hair transplant treatments
            {"name": "FUE Hair Transplant", "category": aesthetic_category_objects[3], "description": "Follicular Unit Extraction hair restoration technique.", "starting_price": 2500.00},
            {"name": "FUT Hair Transplant", "category": aesthetic_category_objects[3], "description": "Follicular Unit Transplantation hair restoration technique.", "starting_price": 2000.00},
            {"name": "Beard Transplant", "category": aesthetic_category_objects[3], "description": "Hair transplant procedure specifically for facial hair restoration.", "starting_price": 1800.00},
            {"name": "Eyebrow Transplant", "category": aesthetic_category_objects[3], "description": "Hair transplant procedure for eyebrow restoration.", "starting_price": 1500.00},
            
            # Dental treatments
            {"name": "Dental Implants", "category": aesthetic_category_objects[2], "description": "Surgical component that interfaces with the bone of the jaw to support dental prosthetics.", "starting_price": 1200.00},
            {"name": "Teeth Whitening", "category": aesthetic_category_objects[2], "description": "Cosmetic dental procedure to improve the appearance of teeth.", "starting_price": 300.00},
            {"name": "Veneers", "category": aesthetic_category_objects[2], "description": "Thin custom-made shells to cover the front surface of teeth.", "starting_price": 800.00},
            {"name": "Invisalign", "category": aesthetic_category_objects[2], "description": "Clear aligner system to straighten teeth without traditional braces.", "starting_price": 2500.00},
            
            # Ayurveda treatments
            {"name": "Panchakarma", "category": wellness_category_objects[0], "description": "Traditional Ayurvedic detoxification and rejuvenation therapy.", "starting_price": 1500.00},
            {"name": "Abhyanga", "category": wellness_category_objects[0], "description": "Therapeutic Ayurvedic massage with herbal oils.", "starting_price": 80.00},
            {"name": "Shirodhara", "category": wellness_category_objects[0], "description": "Ayurvedic therapy involving continuous pouring of warm oil on the forehead.", "starting_price": 100.00},
            
            # Yoga and meditation treatments
            {"name": "Yoga Retreat", "category": wellness_category_objects[1], "description": "Comprehensive yoga program for physical and mental well-being.", "starting_price": 500.00},
            {"name": "Meditation Workshop", "category": wellness_category_objects[2], "description": "Guided meditation sessions for stress relief and mindfulness.", "starting_price": 150.00},
            
            # Weight management treatments
            {"name": "Weight Loss Program", "category": wellness_category_objects[4], "description": "Comprehensive program for sustainable weight loss and healthy lifestyle.", "starting_price": 800.00},
            {"name": "Bariatric Surgery", "category": medical_category_objects[8], "description": "Weight loss surgery to help with extreme obesity.", "starting_price": 7000.00},
        ]
        
        # Create treatments
        treatments = []
        for treatment_data in treatments_data:
            treatment, _ = Treatment._default_manager.get_or_create(  # type: ignore
                name=treatment_data["name"],
                defaults=treatment_data
            )
            treatments.append(treatment)

        # Create 20+ hospitals
        hospitals_data = [
            {
                "name": "Apollo Hospitals",
                "country": india,
                "state": maharashtra,
                "city": "Mumbai",
                "about": "Leading multi-specialty hospital chain in India with state-of-the-art facilities and internationally trained doctors.",
                "is_takeopinion_choice": True,
                "starting_price": 5000.00,
                "rating": 4.8,
                "established_year": 1983,
                "beds_count": 700,
                "staff_count": 1200,
                "departments_count": 50,
                "awards_count": 150,
                "jci_accredited": True,
                "nabh_accredited": True,
                "iso_certified": True,
                "phone": "+91 22 1234 5678",
                "email": "info@apollohospitals.com",
                "website": "https://www.apollohospitals.com",
                "profile_picture": "https://picsum.photos/seed/apollo/600/400"
            },
            {
                "name": "Fortis Healthcare",
                "country": india,
                "state": delhi,
                "city": "Delhi",
                "about": "Comprehensive healthcare provider with multiple facilities across India, known for cardiac and orthopedic care.",
                "is_takeopinion_choice": True,
                "starting_price": 4500.00,
                "rating": 4.6,
                "established_year": 1996,
                "beds_count": 500,
                "staff_count": 900,
                "departments_count": 40,
                "awards_count": 120,
                "jci_accredited": True,
                "nabh_accredited": True,
                "iso_certified": True,
                "phone": "+91 11 2345 6789",
                "email": "info@fortishealthcare.com",
                "website": "https://www.fortishealthcare.com",
                "profile_picture": "https://picsum.photos/seed/fortis/600/400"
            },
            {
                "name": "Max Healthcare",
                "country": india,
                "state": delhi,
                "city": "Delhi",
                "about": "Multi-specialty hospital network offering advanced medical treatments with a focus on cardiac sciences and neurosciences.",
                "is_takeopinion_choice": True,
                "starting_price": 5200.00,
                "rating": 4.7,
                "established_year": 2000,
                "beds_count": 450,
                "staff_count": 800,
                "departments_count": 35,
                "awards_count": 100,
                "jci_accredited": True,
                "nabh_accredited": True,
                "iso_certified": True,
                "phone": "+91 11 3456 7890",
                "email": "info@maxhealthcare.com",
                "website": "https://www.maxhealthcare.com",
                "profile_picture": "https://picsum.photos/seed/max/600/400"
            },
            {
                "name": "Manipal Hospitals",
                "country": india,
                "state": bangalore,
                "city": "Bangalore",
                "about": "Prestigious healthcare institution with advanced medical technology and internationally trained specialists.",
                "is_takeopinion_choice": True,
                "starting_price": 4800.00,
                "rating": 4.5,
                "established_year": 1953,
                "beds_count": 650,
                "staff_count": 1100,
                "departments_count": 45,
                "awards_count": 130,
                "jci_accredited": True,
                "nabh_accredited": True,
                "iso_certified": True,
                "phone": "+91 80 2345 6789",
                "email": "info@manipalhospitals.com",
                "website": "https://www.manipalhospitals.com",
                "profile_picture": "https://picsum.photos/seed/manipal/600/400"
            },
            {
                "name": "Medanta - The Medicity",
                "country": india,
                "state": delhi,
                "city": "Gurgaon",
                "about": "Institute of Neurosciences, known for advanced cardiac and neurological treatments with cutting-edge technology.",
                "is_takeopinion_choice": True,
                "starting_price": 6000.00,
                "rating": 4.9,
                "established_year": 2009,
                "beds_count": 550,
                "staff_count": 1000,
                "departments_count": 30,
                "awards_count": 90,
                "jci_accredited": True,
                "nabh_accredited": True,
                "iso_certified": True,
                "phone": "+91 124 234 5678",
                "email": "info@medanta.org",
                "website": "https://www.medanta.org",
                "profile_picture": "https://picsum.photos/seed/medanta/600/400"
            },
            {
                "name": "Cleveland Clinic Abu Dhabi",
                "country": turkey,
                "state": istanbul,
                "city": "Istanbul",
                "about": "Internationally renowned medical center offering American-standard healthcare with specialized treatments.",
                "is_takeopinion_choice": True,
                "starting_price": 7000.00,
                "rating": 4.8,
                "established_year": 2015,
                "beds_count": 350,
                "staff_count": 700,
                "departments_count": 25,
                "awards_count": 80,
                "jci_accredited": True,
                "nabh_accredited": False,
                "iso_certified": True,
                "phone": "+90 212 123 4567",
                "email": "info@clevelandclinicabudhabi.com",
                "website": "https://www.clevelandclinicabudhabi.com",
                "profile_picture": "https://picsum.photos/seed/cleveland/600/400"
            },
            {
                "name": "American Hospital",
                "country": turkey,
                "state": antalya,
                "city": "Antalya",
                "about": "JCI-accredited hospital offering comprehensive medical services with a focus on cosmetic and bariatric surgery.",
                "is_takeopinion_choice": True,
                "starting_price": 3500.00,
                "rating": 4.6,
                "established_year": 1997,
                "beds_count": 200,
                "staff_count": 400,
                "departments_count": 20,
                "awards_count": 60,
                "jci_accredited": True,
                "nabh_accredited": False,
                "iso_certified": True,
                "phone": "+90 242 234 5678",
                "email": "info@americanhospital.com.tr",
                "website": "https://www.americanhospital.com.tr",
                "profile_picture": "https://picsum.photos/seed/american/600/400"
            },
            {
                "name": "Bumrungrad International Hospital",
                "country": thailand,
                "state": bangkok,
                "city": "Bangkok",
                "about": "World-renowned international hospital providing high-quality medical care to patients from over 190 countries.",
                "is_takeopinion_choice": True,
                "starting_price": 4000.00,
                "rating": 4.7,
                "established_year": 1980,
                "beds_count": 300,
                "staff_count": 600,
                "departments_count": 35,
                "awards_count": 100,
                "jci_accredited": True,
                "nabh_accredited": False,
                "iso_certified": True,
                "phone": "+66 2 123 4567",
                "email": "info@bumrungrad.com",
                "website": "https://www.bumrungrad.com",
                "profile_picture": "https://picsum.photos/seed/bumrungrad/600/400"
            },
            {
                "name": "Bangpakok 9 International Hospital",
                "country": thailand,
                "state": bangkok,
                "city": "Bangkok",
                "about": "International-standard hospital specializing in orthopedics, cosmetic surgery, and wellness treatments.",
                "is_takeopinion_choice": False,
                "starting_price": 3200.00,
                "rating": 4.4,
                "established_year": 1994,
                "beds_count": 150,
                "staff_count": 300,
                "departments_count": 15,
                "awards_count": 40,
                "jci_accredited": True,
                "nabh_accredited": False,
                "iso_certified": True,
                "phone": "+66 2 234 5678",
                "email": "info@bangpakok9.com",
                "website": "https://www.bangpakok9.com",
                "profile_picture": "https://picsum.photos/seed/bangpakok/600/400"
            },
            {
                "name": "Hospital Angeles Chihuahua",
                "country": mexico,
                "state": mexico_city,
                "city": "Mexico City",
                "about": "Leading private hospital offering comprehensive medical services with JCI accreditation and modern facilities.",
                "is_takeopinion_choice": True,
                "starting_price": 2800.00,
                "rating": 4.5,
                "established_year": 1985,
                "beds_count": 250,
                "staff_count": 500,
                "departments_count": 30,
                "awards_count": 70,
                "jci_accredited": True,
                "nabh_accredited": False,
                "iso_certified": True,
                "phone": "+52 55 1234 5678",
                "email": "info@angeleschihuahua.com",
                "website": "https://www.angeleschihuahua.com",
                "profile_picture": "https://picsum.photos/seed/angeles/600/400"
            },
            {
                "name": "American British Cowdray Medical Center",
                "country": mexico,
                "state": mexico_city,
                "city": "Mexico City",
                "about": "International-standard hospital providing comprehensive healthcare services with American-trained specialists.",
                "is_takeopinion_choice": False,
                "starting_price": 3000.00,
                "rating": 4.3,
                "established_year": 1951,
                "beds_count": 200,
                "staff_count": 400,
                "departments_count": 25,
                "awards_count": 50,
                "jci_accredited": True,
                "nabh_accredited": False,
                "iso_certified": True,
                "phone": "+52 55 2345 6789",
                "email": "info@abcmedicalcenter.com",
                "website": "https://www.abcmedicalcenter.com",
                "profile_picture": "https://picsum.photos/seed/abc/600/400"
            },
            {
                "name": "KPJ Healthcare",
                "country": malaysia,
                "state": kuala_lumpur,
                "city": "Kuala Lumpur",
                "about": "Leading private healthcare provider in Malaysia with multiple specialized centers and international accreditations.",
                "is_takeopinion_choice": True,
                "starting_price": 3300.00,
                "rating": 4.6,
                "established_year": 1997,
                "beds_count": 300,
                "staff_count": 550,
                "departments_count": 28,
                "awards_count": 65,
                "jci_accredited": True,
                "nabh_accredited": False,
                "iso_certified": True,
                "phone": "+60 3 1234 5678",
                "email": "info@kpjhealthcare.com",
                "website": "https://www.kpjhealthcare.com",
                "profile_picture": "https://picsum.photos/seed/kpj/600/400"
            },
            {
                "name": "Gleneagles Hospital",
                "country": malaysia,
                "state": penang,
                "city": "Penang",
                "about": "Internationally accredited hospital offering comprehensive medical services with advanced diagnostic and treatment facilities.",
                "is_takeopinion_choice": False,
                "starting_price": 3700.00,
                "rating": 4.5,
                "established_year": 1995,
                "beds_count": 250,
                "staff_count": 450,
                "departments_count": 22,
                "awards_count": 55,
                "jci_accredited": True,
                "nabh_accredited": False,
                "iso_certified": True,
                "phone": "+60 4 234 5678",
                "email": "info@gleneaglespenang.com",
                "website": "https://www.gleneaglespenang.com",
                "profile_picture": "https://picsum.photos/seed/gleneagles/600/400"
            },
            {
                "name": "Narayana Health City",
                "country": india,
                "state": bangalore,
                "city": "Bangalore",
                "about": "Multi-specialty medical institution known for cardiac care, orthopedics, and affordable high-quality healthcare.",
                "is_takeopinion_choice": True,
                "starting_price": 4200.00,
                "rating": 4.7,
                "established_year": 2000,
                "beds_count": 1000,
                "staff_count": 1500,
                "departments_count": 55,
                "awards_count": 110,
                "jci_accredited": True,
                "nabh_accredited": True,
                "iso_certified": True,
                "phone": "+91 80 3456 7890",
                "email": "info@narayanahealth.org",
                "website": "https://www.narayanahealth.org",
                "profile_picture": "https://picsum.photos/seed/narayana/600/400"
            },
            {
                "name": "Kokilaben Dhirubhai Ambani Hospital",
                "country": india,
                "state": maharashtra,
                "city": "Mumbai",
                "about": "State-of-the-art tertiary care hospital with advanced technology and internationally trained medical professionals.",
                "is_takeopinion_choice": True,
                "starting_price": 5500.00,
                "rating": 4.8,
                "established_year": 2009,
                "beds_count": 750,
                "staff_count": 1300,
                "departments_count": 48,
                "awards_count": 95,
                "jci_accredited": True,
                "nabh_accredited": True,
                "iso_certified": True,
                "phone": "+91 22 4455 6677",
                "email": "info@kda-hospital.com",
                "website": "https://www.kda-hospital.com",
                "profile_picture": "https://picsum.photos/seed/kokilaben/600/400"
            },
            {
                "name": "Indraprastha Apollo Hospitals",
                "country": india,
                "state": delhi,
                "city": "Delhi",
                "about": "Flagship hospital of Apollo Hospitals group with comprehensive medical services and cutting-edge technology.",
                "is_takeopinion_choice": True,
                "starting_price": 5300.00,
                "rating": 4.7,
                "established_year": 1995,
                "beds_count": 680,
                "staff_count": 1150,
                "departments_count": 42,
                "awards_count": 125,
                "jci_accredited": True,
                "nabh_accredited": True,
                "iso_certified": True,
                "phone": "+91 11 5566 7788",
                "email": "info@indraprasthaapollo.com",
                "website": "https://www.indraprasthaapollo.com",
                "profile_picture": "https://picsum.photos/seed/indraprastha/600/400"
            },
            {
                "name": "Global Hospitals",
                "country": india,
                "state": tamil_nadu,
                "city": "Chennai",
                "about": "Multi-specialty hospital with advanced medical technology and specialized centers for cardiac, oncology, and orthopedic care.",
                "is_takeopinion_choice": False,
                "starting_price": 4600.00,
                "rating": 4.5,
                "established_year": 2000,
                "beds_count": 550,
                "staff_count": 950,
                "departments_count": 38,
                "awards_count": 85,
                "jci_accredited": True,
                "nabh_accredited": True,
                "iso_certified": True,
                "phone": "+91 44 2345 6789",
                "email": "info@globalhospitalsindia.com",
                "website": "https://www.globalhospitalsindia.com",
                "profile_picture": "https://picsum.photos/seed/global/600/400"
            },
            {
                "name": "Sunny Beach Hospital",
                "country": turkey,
                "state": antalya,
                "city": "Antalya",
                "about": "Specialized in cosmetic surgery and wellness treatments with modern facilities and experienced surgeons.",
                "is_takeopinion_choice": False,
                "starting_price": 2900.00,
                "rating": 4.3,
                "established_year": 2005,
                "beds_count": 120,
                "staff_count": 250,
                "departments_count": 12,
                "awards_count": 30,
                "jci_accredited": False,
                "nabh_accredited": False,
                "iso_certified": True,
                "phone": "+90 242 345 6789",
                "email": "info@sunnybeachhospital.com",
                "website": "https://www.sunnybeachhospital.com",
                "profile_picture": "https://picsum.photos/seed/sunnybeach/600/400"
            },
            {
                "name": "Samitivej Hospital",
                "country": thailand,
                "state": phuket,
                "city": "Phuket",
                "about": "International-standard hospital providing comprehensive medical services with a focus on wellness and preventive care.",
                "is_takeopinion_choice": False,
                "starting_price": 3100.00,
                "rating": 4.4,
                "established_year": 1999,
                "beds_count": 180,
                "staff_count": 350,
                "departments_count": 18,
                "awards_count": 45,
                "jci_accredited": True,
                "nabh_accredited": False,
                "iso_certified": True,
                "phone": "+66 76 123 4567",
                "email": "info@samitivejphuket.com",
                "website": "https://www.samitivejphuket.com",
                "profile_picture": "https://picsum.photos/seed/samitivej/600/400"
            },
            {
                "name": "Cancun International Hospital",
                "country": mexico,
                "state": cancun,
                "city": "Cancun",
                "about": "Modern hospital offering comprehensive medical services with a focus on cosmetic surgery and wellness treatments.",
                "is_takeopinion_choice": False,
                "starting_price": 2700.00,
                "rating": 4.2,
                "established_year": 2008,
                "beds_count": 100,
                "staff_count": 200,
                "departments_count": 15,
                "awards_count": 25,
                "jci_accredited": False,
                "nabh_accredited": False,
                "iso_certified": True,
                "phone": "+52 998 123 4567",
                "email": "info@cancunhospital.com",
                "website": "https://www.cancunhospital.com",
                "profile_picture": "https://picsum.photos/seed/cancun/600/400"
            }
        ]
        
        # Create hospitals
        hospitals = []
        for hospital_data in hospitals_data:
            hospital, _ = Hospital._default_manager.get_or_create(  # type: ignore
                name=hospital_data["name"],
                defaults=hospital_data
            )
            hospitals.append(hospital)
            # Add some media items for each hospital
            HospitalMedia._default_manager.get_or_create(  # type: ignore
                hospital=hospital,
                image_url=hospital_data["profile_picture"]
            )
            # Add some treatments to each hospital
            # Assign 5-10 random treatments to each hospital
            import random
            num_treatments = random.randint(5, 10)
            treatment_sample = random.sample(treatments, min(num_treatments, len(treatments)))
            hospital.treatments.set(treatment_sample)

        # Create 20+ doctors
        doctors_data = [
            {
                "name": "Dr. Ramesh Sharma",
                "specialization": "Orthopedic Surgeon",
                "key_points": "20+ years experience in joint replacement surgeries",
                "about": "Dr. Sharma is a renowned orthopedic surgeon with extensive experience in knee and hip replacement surgeries. He has performed over 2000 successful joint replacement procedures.",
                "education": "MBBS, MS Orthopedics, Fellowship in Joint Replacement",
                "experience_years": 22,
                "rating": 4.9,
                "review_count": 350,
                "medical_license_number": "MED12345",
                "languages_spoken": "English, Hindi, Marathi",
                "phone": "+91 98765 43210",
                "email": "dr.sharma@apollohospitals.com",
                "website": "https://www.apollohospitals.com/doctors/ramesh-sharma",
                "profile_picture": "https://ui-avatars.com/api/?name=Ramesh+Sharma&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. Priya Patel",
                "specialization": "Cardiac Surgeon",
                "key_points": "Expert in minimally invasive cardiac procedures",
                "about": "Dr. Patel is a leading cardiac surgeon specializing in minimally invasive procedures. She has pioneered several new techniques in heart surgery with faster recovery times.",
                "education": "MBBS, MS General Surgery, MCh Cardiothoracic Surgery",
                "experience_years": 18,
                "rating": 4.8,
                "review_count": 280,
                "medical_license_number": "MED23456",
                "languages_spoken": "English, Hindi, Gujarati",
                "phone": "+91 98765 43211",
                "email": "dr.patel@fortishealthcare.com",
                "website": "https://www.fortishealthcare.com/doctors/priya-patel",
                "profile_picture": "https://ui-avatars.com/api/?name=Priya+Patel&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. Ahmed Khan",
                "specialization": "Neurosurgeon",
                "key_points": "Specialist in brain tumor removal and spinal surgeries",
                "about": "Dr. Khan is a highly skilled neurosurgeon with expertise in complex brain and spinal surgeries. He has successfully treated over 1500 patients with various neurological conditions.",
                "education": "MBBS, MS General Surgery, MCh Neurosurgery",
                "experience_years": 20,
                "rating": 4.9,
                "review_count": 320,
                "medical_license_number": "MED34567",
                "languages_spoken": "English, Hindi, Urdu",
                "phone": "+91 98765 43212",
                "email": "dr.khan@maxhealthcare.com",
                "website": "https://www.maxhealthcare.com/doctors/ahmed-khan",
                "profile_picture": "https://ui-avatars.com/api/?name=Ahmed+Khan&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. Sarah Johnson",
                "specialization": "Oncologist",
                "key_points": "Expert in immunotherapy and targeted cancer treatments",
                "about": "Dr. Johnson is a leading oncologist specializing in advanced cancer treatments including immunotherapy and targeted therapy. She has contributed to several research publications in oncology.",
                "education": "MBBS, MD Internal Medicine, DM Oncology",
                "experience_years": 16,
                "rating": 4.7,
                "review_count": 290,
                "medical_license_number": "MED45678",
                "languages_spoken": "English",
                "phone": "+91 98765 43213",
                "email": "dr.johnson@manipalhospitals.com",
                "website": "https://www.manipalhospitals.com/doctors/sarah-johnson",
                "profile_picture": "https://ui-avatars.com/api/?name=Sarah+Johnson&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. Rajesh Gupta",
                "specialization": "Plastic Surgeon",
                "key_points": "Renowned for rhinoplasty and facial reconstruction",
                "about": "Dr. Gupta is a distinguished plastic surgeon with expertise in facial plastic surgery, rhinoplasty, and reconstructive procedures. He has won several awards for his artistic approach to cosmetic surgery.",
                "education": "MBBS, MS General Surgery, MCh Plastic Surgery",
                "experience_years": 19,
                "rating": 4.8,
                "review_count": 420,
                "medical_license_number": "MED56789",
                "languages_spoken": "English, Hindi",
                "phone": "+91 98765 43214",
                "email": "dr.gupta@medanta.org",
                "website": "https://www.medanta.org/doctors/rajesh-gupta",
                "profile_picture": "https://ui-avatars.com/api/?name=Rajesh+Gupta&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. Emily Chen",
                "specialization": "Dermatologist",
                "key_points": "Expert in laser treatments and skin rejuvenation",
                "about": "Dr. Chen is a renowned dermatologist specializing in advanced laser treatments, skin rejuvenation, and cosmetic dermatology. She has extensive experience in treating complex skin conditions.",
                "education": "MBBS, MD Dermatology, Fellowship in Cosmetic Dermatology",
                "experience_years": 15,
                "rating": 4.7,
                "review_count": 250,
                "medical_license_number": "MED67890",
                "languages_spoken": "English, Mandarin",
                "phone": "+91 98765 43215",
                "email": "dr.chen@clevelandclinicabudhabi.com",
                "website": "https://www.clevelandclinicabudhabi.com/doctors/emily-chen",
                "profile_picture": "https://ui-avatars.com/api/?name=Emily+Chen&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. Mehmet Yilmaz",
                "specialization": "Bariatric Surgeon",
                "key_points": "Specialist in weight loss surgeries with excellent results",
                "about": "Dr. Yilmaz is a leading bariatric surgeon with expertise in various weight loss procedures. He has helped over 1000 patients achieve significant weight loss and improved health outcomes.",
                "education": "MD, General Surgery, Fellowship in Bariatric Surgery",
                "experience_years": 17,
                "rating": 4.8,
                "review_count": 380,
                "medical_license_number": "MED78901",
                "languages_spoken": "English, Turkish",
                "phone": "+90 532 123 4567",
                "email": "dr.yilmaz@americanhospital.com.tr",
                "website": "https://www.americanhospital.com.tr/doctors/mehmet-yilmaz",
                "profile_picture": "https://ui-avatars.com/api/?name=Mehmet+Yilmaz&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. Somsak Prasert",
                "specialization": "Orthopedic Surgeon",
                "key_points": "Expert in sports medicine and arthroscopic surgery",
                "about": "Dr. Prasert is a renowned orthopedic surgeon specializing in sports medicine and minimally invasive arthroscopic procedures. He has treated numerous professional athletes.",
                "education": "MD, Orthopedic Surgery, Fellowship in Sports Medicine",
                "experience_years": 21,
                "rating": 4.7,
                "review_count": 310,
                "medical_license_number": "MED89012",
                "languages_spoken": "English, Thai",
                "phone": "+66 81 234 5678",
                "email": "dr.prasert@bumrungrad.com",
                "website": "https://www.bumrungrad.com/doctors/somsak-prasert",
                "profile_picture": "https://ui-avatars.com/api/?name=Somsak+Prasert&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. Maria Gonzalez",
                "specialization": "Gynecologist",
                "key_points": "Specialist in minimally invasive gynecological surgeries",
                "about": "Dr. Gonzalez is a leading gynecologist with expertise in minimally invasive procedures for various gynecological conditions. She focuses on patient-centered care and holistic treatment approaches.",
                "education": "MD, Gynecology and Obstetrics, Fellowship in Minimally Invasive Gynecologic Surgery",
                "experience_years": 18,
                "rating": 4.8,
                "review_count": 270,
                "medical_license_number": "MED90123",
                "languages_spoken": "English, Spanish",
                "phone": "+52 55 1234 5678",
                "email": "dr.gonzalez@angeleschihuahua.com",
                "website": "https://www.angeleschihuahua.com/doctors/maria-gonzalez",
                "profile_picture": "https://ui-avatars.com/api/?name=Maria+Gonzalez&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. Lim Wei Ming",
                "specialization": "Cardiologist",
                "key_points": "Expert in interventional cardiology and heart rhythm disorders",
                "about": "Dr. Lim is a distinguished cardiologist specializing in interventional procedures and treatment of heart rhythm disorders. He has performed over 3000 cardiac procedures with excellent outcomes.",
                "education": "MBBS, MD Internal Medicine, DM Cardiology",
                "experience_years": 20,
                "rating": 4.9,
                "review_count": 340,
                "medical_license_number": "MED01234",
                "languages_spoken": "English, Mandarin, Malay",
                "phone": "+60 12 345 6789",
                "email": "dr.lim@kpjhealthcare.com",
                "website": "https://www.kpjhealthcare.com/doctors/lim-wei-ming",
                "profile_picture": "https://ui-avatars.com/api/?name=Lim+Wei+Ming&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. Anil Reddy",
                "specialization": "Urologist",
                "key_points": "Specialist in robotic surgery and kidney transplants",
                "about": "Dr. Reddy is a leading urologist with expertise in robotic surgery and kidney transplantation. He has successfully performed over 500 robotic surgeries with minimal complications.",
                "education": "MBBS, MS General Surgery, MCh Urology",
                "experience_years": 19,
                "rating": 4.8,
                "review_count": 290,
                "medical_license_number": "MED11223",
                "languages_spoken": "English, Hindi, Telugu",
                "phone": "+91 98765 43220",
                "email": "dr.reddy@narayanahealth.org",
                "website": "https://www.narayanahealth.org/doctors/anil-reddy",
                "profile_picture": "https://ui-avatars.com/api/?name=Anil+Reddy&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. Kavita Desai",
                "specialization": "Pediatric Surgeon",
                "key_points": "Expert in neonatal and pediatric surgical procedures",
                "about": "Dr. Desai is a renowned pediatric surgeon with extensive experience in neonatal and complex pediatric surgical procedures. She has treated over 2000 pediatric cases with exceptional care.",
                "education": "MBBS, MS General Surgery, MCh Pediatric Surgery",
                "experience_years": 17,
                "rating": 4.9,
                "review_count": 260,
                "medical_license_number": "MED22334",
                "languages_spoken": "English, Hindi, Marathi",
                "phone": "+91 98765 43221",
                "email": "dr.desai@kokilabenhospital.com",
                "website": "https://www.kokilabenhospital.com/doctors/kavita-desai",
                "profile_picture": "https://ui-avatars.com/api/?name=Kavita+Desai&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. James Wilson",
                "specialization": "ENT Specialist",
                "key_points": "Specialist in head and neck surgeries and cochlear implants",
                "about": "Dr. Wilson is a leading ENT specialist with expertise in complex head and neck surgeries and cochlear implant procedures. He has pioneered several new techniques in ENT surgery.",
                "education": "MBBS, MD ENT, Fellowship in Head and Neck Surgery",
                "experience_years": 18,
                "rating": 4.7,
                "review_count": 240,
                "medical_license_number": "MED33445",
                "languages_spoken": "English",
                "phone": "+91 98765 43222",
                "email": "dr.wilson@indraprasthaapollo.com",
                "website": "https://www.indraprasthaapollo.com/doctors/james-wilson",
                "profile_picture": "https://ui-avatars.com/api/?name=James+Wilson&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. Fatima Al-Mansoori",
                "specialization": "Ophthalmologist",
                "key_points": "Expert in laser eye surgery and cataract procedures",
                "about": "Dr. Al-Mansoori is a distinguished ophthalmologist specializing in advanced laser eye surgeries and complex cataract procedures. She has successfully treated over 5000 patients with vision problems.",
                "education": "MD, Ophthalmology, Fellowship in Cornea and Refractive Surgery",
                "experience_years": 16,
                "rating": 4.8,
                "review_count": 310,
                "medical_license_number": "MED44556",
                "languages_spoken": "English, Arabic",
                "phone": "+971 50 123 4567",
                "email": "dr.almansoori@globalhospitals.com",
                "website": "https://www.globalhospitals.com/doctors/fatima-almansoori",
                "profile_picture": "https://ui-avatars.com/api/?name=Fatima+Al-Mansoori&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. Burak Demir",
                "specialization": "Cosmetic Surgeon",
                "key_points": "Renowned for facial aesthetic procedures and body contouring",
                "about": "Dr. Demir is a leading cosmetic surgeon with expertise in facial aesthetic procedures and advanced body contouring techniques. He has trained in the latest cosmetic surgery methods in Europe and USA.",
                "education": "MD, Plastic and Reconstructive Surgery, Fellowship in Aesthetic Surgery",
                "experience_years": 15,
                "rating": 4.7,
                "review_count": 390,
                "medical_license_number": "MED55667",
                "languages_spoken": "English, Turkish, German",
                "phone": "+90 533 234 5678",
                "email": "dr.demir@sunnybeachhospital.com",
                "website": "https://www.sunnybeachhospital.com/doctors/burak-demir",
                "profile_picture": "https://ui-avatars.com/api/?name=Burak+Demir&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. Niranjan Kumar",
                "specialization": "Gastroenterologist",
                "key_points": "Expert in endoscopic procedures and liver diseases",
                "about": "Dr. Kumar is a renowned gastroenterologist specializing in advanced endoscopic procedures and treatment of complex liver diseases. He has contributed to several research papers in gastroenterology.",
                "education": "MBBS, MD Internal Medicine, DM Gastroenterology",
                "experience_years": 18,
                "rating": 4.8,
                "review_count": 280,
                "medical_license_number": "MED66778",
                "languages_spoken": "English, Hindi, Tamil",
                "phone": "+91 98765 43225",
                "email": "dr.kumar@globalhospitals.com",
                "website": "https://www.globalhospitals.com/doctors/niranjan-kumar",
                "profile_picture": "https://ui-avatars.com/api/?name=Niranjan+Kumar&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. Preecha Srisuwan",
                "specialization": "Dental Surgeon",
                "key_points": "Specialist in implantology and cosmetic dentistry",
                "about": "Dr. Srisuwan is a leading dental surgeon with expertise in dental implants and advanced cosmetic dentistry procedures. He has treated patients from over 50 countries with excellent results.",
                "education": "DDS, MD Oral and Maxillofacial Surgery, Fellowship in Implantology",
                "experience_years": 17,
                "rating": 4.7,
                "review_count": 230,
                "medical_license_number": "MED77889",
                "languages_spoken": "English, Thai",
                "phone": "+66 82 345 6789",
                "email": "dr.srisuwan@samitivejphuket.com",
                "website": "https://www.samitivejphuket.com/doctors/preecha-srisuwan",
                "profile_picture": "https://ui-avatars.com/api/?name=Preecha+Srisuwan&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. Carlos Rodriguez",
                "specialization": "Orthopedic Surgeon",
                "key_points": "Expert in sports injuries and joint preservation",
                "about": "Dr. Rodriguez is a distinguished orthopedic surgeon specializing in sports injuries and joint preservation techniques. He has worked with several professional sports teams as a consultant.",
                "education": "MD, Orthopedic Surgery, Fellowship in Sports Medicine",
                "experience_years": 19,
                "rating": 4.8,
                "review_count": 320,
                "medical_license_number": "MED88990",
                "languages_spoken": "English, Spanish",
                "phone": "+52 55 2345 6789",
                "email": "dr.rodriguez@cancunhospital.com",
                "website": "https://www.cancunhospital.com/doctors/carlos-rodriguez",
                "profile_picture": "https://ui-avatars.com/api/?name=Carlos+Rodriguez&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. Tan Wei Ling",
                "specialization": "Fertility Specialist",
                "key_points": "Specialist in IVF and assisted reproductive technologies",
                "about": "Dr. Tan is a leading fertility specialist with expertise in IVF and other assisted reproductive technologies. She has helped over 1000 couples achieve successful pregnancies.",
                "education": "MBBS, MD Obstetrics and Gynecology, Fellowship in Reproductive Medicine",
                "experience_years": 16,
                "rating": 4.9,
                "review_count": 270,
                "medical_license_number": "MED99001",
                "languages_spoken": "English, Mandarin, Malay",
                "phone": "+60 13 456 7890",
                "email": "dr.tan@gleneaglespenang.com",
                "website": "https://www.gleneaglespenang.com/doctors/tan-wei-ling",
                "profile_picture": "https://ui-avatars.com/api/?name=Tan+Wei+Ling&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. Deepak Mehta",
                "specialization": "Pulmonologist",
                "key_points": "Expert in lung diseases and respiratory disorders",
                "about": "Dr. Mehta is a renowned pulmonologist specializing in complex lung diseases and respiratory disorders. He has extensive experience in treating patients with chronic respiratory conditions.",
                "education": "MBBS, MD Internal Medicine, DM Pulmonary Medicine",
                "experience_years": 20,
                "rating": 4.7,
                "review_count": 250,
                "medical_license_number": "MED00112",
                "languages_spoken": "English, Hindi, Gujarati",
                "phone": "+91 98765 43230",
                "email": "dr.mehta@apollohospitals.com",
                "website": "https://www.apollohospitals.com/doctors/deepak-mehta",
                "profile_picture": "https://ui-avatars.com/api/?name=Deepak+Mehta&background=0D8ABC&color=fff"
            },
            {
                "name": "Dr. Ayşe Kaya",
                "specialization": "Dermatologist",
                "key_points": "Specialist in skin cancer and cosmetic dermatology",
                "about": "Dr. Kaya is a leading dermatologist with expertise in skin cancer treatment and advanced cosmetic dermatology procedures. She has published several research papers on dermatological conditions.",
                "education": "MD, Dermatology and Venereology, Fellowship in Dermatopathology",
                "experience_years": 17,
                "rating": 4.8,
                "review_count": 290,
                "medical_license_number": "MED11223",
                "languages_spoken": "English, Turkish",
                "phone": "+90 534 345 6789",
                "email": "dr.kaya@americanhospital.com.tr",
                "website": "https://www.americanhospital.com.tr/doctors/ayse-kaya",
                "profile_picture": "https://ui-avatars.com/api/?name=Ayse+Kaya&background=0D8ABC&color=fff"
            }
        ]
        
        # Create doctors
        doctors = []
        for doctor_data in doctors_data:
            doctor, _ = Doctor._default_manager.get_or_create(  # type: ignore
                name=doctor_data["name"],
                defaults=doctor_data
            )
            doctors.append(doctor)
            # Assign some treatments and hospitals to each doctor
            # Assign 3-7 random treatments to each doctor
            import random
            num_treatments = random.randint(3, 7)
            treatment_sample = random.sample(treatments, min(num_treatments, len(treatments)))
            doctor.treatments.set(treatment_sample)
            
            # Assign 2-5 random hospitals to each doctor
            num_hospitals = random.randint(2, 5)
            hospital_sample = random.sample(hospitals, min(num_hospitals, len(hospitals)))
            doctor.hospitals.set(hospital_sample)

        # Create some blog posts
        blog_posts_data = [
            {
                "title": "Knee Replacement: What to Expect Before, During, and After Surgery",
                "content": "A comprehensive guide to knee replacement surgery, covering preparation, procedure details, recovery timeline, and tips for optimal outcomes.",
                "treatment": treatments[0],  # Knee Replacement
                "doctor": doctors[0],  # Dr. Ramesh Sharma
                "hospital": hospitals[0]  # Apollo Hospitals
            },
            {
                "title": "Understanding Heart Bypass Surgery: A Patient's Guide",
                "content": "Detailed information about coronary artery bypass grafting (CABG), including indications, surgical process, recovery, and long-term care.",
                "treatment": treatments[6],  # Bypass Surgery
                "doctor": doctors[1],  # Dr. Priya Patel
                "hospital": hospitals[1]  # Fortis Healthcare
            },
            {
                "title": "The Ultimate Guide to Rhinoplasty: Achieving Natural Results",
                "content": "Everything you need to know about nose reshaping surgery, from consultation to recovery, with tips for choosing the right surgeon.",
                "treatment": treatments[20],  # Rhinoplasty
                "doctor": doctors[4],  # Dr. Rajesh Gupta
                "hospital": hospitals[4]  # Medanta
            },
            {
                "title": "Medical Tourism in India: Why It's the Preferred Destination",
                "content": "Exploring the benefits of medical tourism in India, including cost savings, quality care, and world-class facilities.",
                "is_medical_visa": True
            },
            {
                "title": "Hair Transplant Techniques: FUE vs FUT - Which is Right for You?",
                "content": "Comparing the two main hair transplant techniques, their benefits, recovery times, and ideal candidates for each procedure.",
                "treatment": treatments[24],  # FUE Hair Transplant
                "doctor": doctors[14],  # Dr. Burak Demir
                "hospital": hospitals[17]  # Sunny Beach Hospital
            },
            {
                "title": "Ayurvedic Panchakarma: Ancient Wisdom for Modern Wellness",
                "content": "Understanding the traditional Ayurvedic detoxification therapy and its benefits for holistic health and well-being.",
                "treatment": treatments[34],  # Panchakarma
                "doctor": doctors[19],  # Dr. Deepak Mehta
                "hospital": hospitals[13]  # Narayana Health
            },
            {
                "title": "Bariatric Surgery: A Life-Changing Decision for Weight Loss",
                "content": "Exploring the different types of weight loss surgeries, their effectiveness, and what to expect during the journey to better health.",
                "treatment": treatments[39],  # Bariatric Surgery
                "doctor": doctors[6],  # Dr. Mehmet Yilmaz
                "hospital": hospitals[6]  # American Hospital
            }
        ]
        
        # Create blog posts
        for blog_data in blog_posts_data:
            BlogPost._default_manager.get_or_create(  # type: ignore
                title=blog_data["title"],
                defaults=blog_data
            )

        # Create accommodations for hospitals
        accommodation_types = [
            "Luxury Hotel", "Boutique Hotel", "Serviced Apartment", 
            "Guest House", "Budget Hotel", "Resort"
        ]
        
        for hospital in hospitals:
            # Create 2-4 accommodations for each hospital
            import random
            num_accommodations = random.randint(2, 4)
            for i in range(num_accommodations):
                price = random.randint(2000, 15000)
                Accommodation._default_manager.get_or_create(  # type: ignore
                    hospital=hospital,
                    name=f"{random.choice(accommodation_types)} near {hospital.name}",
                    defaults={
                        "price_per_night": price
                    }
                )

        self.stdout.write(
            f"Demo data seeded: {len(treatments)} treatments, {len(hospitals)} hospitals, {len(doctors)} doctors"
        )
