from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from decimal import Decimal
import random


class Command(BaseCommand):
    help = "Seed full realistic medical data into the database"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting full database seed..."))
        with transaction.atomic():
            self._seed_countries_states()
            self._seed_treatment_categories()
            self._seed_treatments()
            self._seed_hospitals()
            self._seed_doctors()
            self._seed_patient_users()
            self._seed_blogs()
            self._seed_feedbacks()
            self._update_ratings()
        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))

    def _seed_countries_states(self):
        from core.models import Country, State
        self.stdout.write("  Seeding countries and states...")
        countries = [
            {"name": "India", "code": "IN"},
            {"name": "Malaysia", "code": "MY"},
            {"name": "Thailand", "code": "TH"},
            {"name": "Turkey", "code": "TR"},
            {"name": "Germany", "code": "DE"},
        ]
        for c in countries:
            Country.objects.get_or_create(code=c["code"], defaults={"name": c["name"]})
        india = Country.objects.get(code="IN")
        my = Country.objects.get(code="MY")
        th = Country.objects.get(code="TH")
        tr = Country.objects.get(code="TR")
        states = [
            (india, "Maharashtra", "MH"),
            (india, "Delhi", "DL"),
            (india, "Karnataka", "KA"),
            (india, "Tamil Nadu", "TN"),
            (india, "Kerala", "KL"),
            (india, "Haryana", "HR"),
            (india, "West Bengal", "WB"),
            (my, "Kuala Lumpur", "KL"),
            (my, "Penang", "PG"),
            (th, "Bangkok", "BK"),
            (tr, "Istanbul", "IST"),
        ]
        for country, name, code in states:
            State.objects.get_or_create(country=country, name=name, defaults={"code": code})
        self.stdout.write("    Countries and states done.")

    def _seed_treatment_categories(self):
        from treatments.models import TreatmentCategory
        self.stdout.write("  Seeding treatment categories...")
        cats = [
            ("Cardiology", "medical"),
            ("Orthopedics", "medical"),
            ("Neurology", "medical"),
            ("Oncology", "medical"),
            ("Endocrinology", "medical"),
            ("Gastroenterology", "medical"),
            ("Pulmonology", "medical"),
            ("Ophthalmology", "medical"),
            ("Urology", "medical"),
            ("Fertility", "medical"),
            ("Cosmetic Surgery", "aesthetic"),
            ("Dental", "medical"),
            ("Wellness", "wellness"),
        ]
        for name, typ in cats:
            TreatmentCategory.objects.get_or_create(name=name, defaults={"type": typ})
        self.stdout.write("    Treatment categories done.")

    def _seed_treatments(self):
        from treatments.models import Treatment, TreatmentCategory
        self.stdout.write("  Seeding treatments...")
        def get_cat(name):
            return TreatmentCategory.objects.get(name=name)
        treatments_data = [
            # Cardiology
            ("Coronary Angioplasty", get_cat("Cardiology"), "A minimally invasive procedure to open blocked coronary arteries using a balloon catheter and stent.", "2-3 hours", "Local", "1-2 days", Decimal("180000")),
            ("Bypass Surgery (CABG)", get_cat("Cardiology"), "Coronary artery bypass grafting to restore blood flow to the heart by creating new pathways around blocked arteries.", "4-6 hours", "General", "7-10 days", Decimal("350000")),
            ("Heart Valve Replacement", get_cat("Cardiology"), "Surgical replacement of a damaged heart valve with a mechanical or biological prosthetic valve.", "4-5 hours", "General", "10-14 days", Decimal("420000")),
            ("Pacemaker Implantation", get_cat("Cardiology"), "Implantation of a small electronic device to regulate abnormal heart rhythms.", "1-2 hours", "Local", "2-3 days", Decimal("150000")),
            ("Cardiac Ablation", get_cat("Cardiology"), "A procedure to correct heart rhythm problems by scarring or destroying tissue that triggers abnormal electrical signals.", "3-4 hours", "Local", "1-2 days", Decimal("200000")),
            ("Angiography", get_cat("Cardiology"), "Diagnostic imaging procedure to visualize blood vessels and detect blockages using contrast dye and X-ray.", "1 hour", "Local", "Same day", Decimal("25000")),
            # Orthopedics
            ("Knee Replacement", get_cat("Orthopedics"), "Total or partial replacement of the knee joint with an artificial implant to relieve pain and restore mobility.", "2-3 hours", "Spinal/General", "5-7 days", Decimal("280000")),
            ("Hip Replacement", get_cat("Orthopedics"), "Surgical replacement of the hip joint with a prosthetic implant to relieve arthritis pain and improve mobility.", "2-3 hours", "Spinal/General", "5-7 days", Decimal("300000")),
            ("Spinal Fusion", get_cat("Orthopedics"), "Surgical procedure to permanently connect two or more vertebrae to eliminate painful motion and restore stability.", "3-5 hours", "General", "7-10 days", Decimal("350000")),
            ("Arthroscopic Surgery", get_cat("Orthopedics"), "Minimally invasive joint surgery using a small camera and instruments to diagnose and treat joint problems.", "1-2 hours", "General/Spinal", "1-2 days", Decimal("80000")),
            ("Shoulder Replacement", get_cat("Orthopedics"), "Replacement of the damaged shoulder joint with an artificial implant to relieve pain and restore function.", "2-3 hours", "General", "3-5 days", Decimal("280000")),
            ("Spine Surgery", get_cat("Orthopedics"), "Surgical correction of spinal disorders including disc herniation, spinal stenosis, and deformities.", "3-6 hours", "General", "7-14 days", Decimal("320000")),
            # Neurology
            ("Brain Tumor Removal", get_cat("Neurology"), "Neurosurgical procedure to remove benign or malignant brain tumors using advanced microsurgical techniques.", "6-10 hours", "General", "10-14 days", Decimal("500000")),
            ("Deep Brain Stimulation", get_cat("Neurology"), "Surgical implantation of electrodes in specific brain areas to treat movement disorders like Parkinson disease.", "4-6 hours", "Local/General", "5-7 days", Decimal("600000")),
            ("Epilepsy Surgery", get_cat("Neurology"), "Surgical removal of the brain area causing seizures in patients with drug-resistant epilepsy.", "4-8 hours", "General", "7-10 days", Decimal("450000")),
            ("Stroke Rehabilitation", get_cat("Neurology"), "Comprehensive rehabilitation program to help stroke survivors regain lost functions and improve quality of life.", "4-6 weeks", "None", "Outpatient", Decimal("80000")),
            ("Spinal Cord Surgery", get_cat("Neurology"), "Surgical treatment of spinal cord injuries, tumors, and compression to restore neurological function.", "4-8 hours", "General", "10-14 days", Decimal("480000")),
            # Oncology
            ("Chemotherapy", get_cat("Oncology"), "Systemic cancer treatment using powerful drugs to destroy cancer cells or stop their growth.", "3-6 months", "None", "Outpatient cycles", Decimal("150000")),
            ("Radiation Therapy", get_cat("Oncology"), "High-energy radiation treatment to destroy cancer cells and shrink tumors with precision targeting.", "6-8 weeks", "None", "Outpatient", Decimal("200000")),
            ("Immunotherapy", get_cat("Oncology"), "Treatment that uses the body immune system to fight cancer by boosting or changing how it works.", "6-12 months", "None", "Outpatient", Decimal("300000")),
            ("Targeted Therapy", get_cat("Oncology"), "Cancer treatment using drugs that target specific genes or proteins involved in cancer cell growth.", "Ongoing", "None", "Outpatient", Decimal("250000")),
            ("Stem Cell Transplant", get_cat("Oncology"), "Replacement of diseased bone marrow with healthy stem cells to treat blood cancers and disorders.", "4-6 weeks", "None", "21-30 days", Decimal("800000")),
            # Endocrinology
            ("Diabetes Management", get_cat("Endocrinology"), "Comprehensive diabetes care program including medication, diet counseling, and lifestyle modification.", "Ongoing", "None", "Outpatient", Decimal("15000")),
            ("Thyroid Treatment", get_cat("Endocrinology"), "Medical management of thyroid disorders including hypothyroidism, hyperthyroidism, and thyroid nodules.", "3-6 months", "None", "Outpatient", Decimal("10000")),
            ("Thyroidectomy", get_cat("Endocrinology"), "Surgical removal of all or part of the thyroid gland to treat thyroid cancer, goiter, or hyperthyroidism.", "2-3 hours", "General", "2-3 days", Decimal("120000")),
            ("Insulin Pump Therapy", get_cat("Endocrinology"), "Continuous subcutaneous insulin infusion therapy for better blood glucose control in diabetes patients.", "Ongoing", "None", "Outpatient", Decimal("80000")),
            # Gastroenterology
            ("Liver Transplant", get_cat("Gastroenterology"), "Surgical replacement of a diseased liver with a healthy donor liver to treat end-stage liver disease.", "8-12 hours", "General", "21-30 days", Decimal("1500000")),
            ("Colonoscopy", get_cat("Gastroenterology"), "Endoscopic examination of the large intestine to detect polyps, cancer, and other abnormalities.", "30-60 min", "Sedation", "Same day", Decimal("8000")),
            ("Bariatric Surgery", get_cat("Gastroenterology"), "Weight loss surgery to reduce stomach size and help patients achieve significant and sustained weight loss.", "2-3 hours", "General", "3-5 days", Decimal("250000")),
            ("Liver Biopsy", get_cat("Gastroenterology"), "Minimally invasive procedure to obtain a small sample of liver tissue for diagnosis of liver diseases.", "30 min", "Local", "Same day", Decimal("15000")),
            # Pulmonology
            ("Lung Cancer Treatment", get_cat("Pulmonology"), "Comprehensive treatment for lung cancer including surgery, chemotherapy, radiation, and targeted therapy.", "3-6 months", "General/None", "Varies", Decimal("400000")),
            ("Bronchoscopy", get_cat("Pulmonology"), "Endoscopic procedure to examine the airways and lungs for diagnosis and treatment of lung conditions.", "30-60 min", "Sedation", "Same day", Decimal("12000")),
            ("COPD Management", get_cat("Pulmonology"), "Comprehensive management of chronic obstructive pulmonary disease with medication and pulmonary rehabilitation.", "Ongoing", "None", "Outpatient", Decimal("20000")),
            ("Asthma Treatment", get_cat("Pulmonology"), "Personalized asthma management plan with controller medications, rescue inhalers, and trigger avoidance.", "Ongoing", "None", "Outpatient", Decimal("10000")),
            # Ophthalmology
            ("LASIK Surgery", get_cat("Ophthalmology"), "Laser eye surgery to correct refractive errors including myopia, hyperopia, and astigmatism.", "15-30 min", "Eye drops", "1-2 days", Decimal("45000")),
            ("Cataract Surgery", get_cat("Ophthalmology"), "Removal of the clouded natural lens and replacement with a clear artificial intraocular lens.", "30-45 min", "Local", "Same day", Decimal("35000")),
            ("Retinal Surgery", get_cat("Ophthalmology"), "Surgical repair of retinal detachment, macular holes, and other retinal conditions.", "1-3 hours", "Local/General", "1-3 days", Decimal("120000")),
            ("Glaucoma Treatment", get_cat("Ophthalmology"), "Medical and surgical management of glaucoma to prevent optic nerve damage and vision loss.", "Ongoing", "Local", "Outpatient", Decimal("25000")),
            # Urology
            ("Kidney Stone Removal", get_cat("Urology"), "Minimally invasive procedures including ESWL, ureteroscopy, and PCNL to remove kidney stones.", "1-2 hours", "General/Spinal", "1-3 days", Decimal("60000")),
            ("Prostate Surgery", get_cat("Urology"), "Surgical treatment of benign prostatic hyperplasia or prostate cancer using TURP or robotic prostatectomy.", "2-4 hours", "Spinal/General", "3-5 days", Decimal("180000")),
            ("Kidney Transplant", get_cat("Urology"), "Surgical replacement of a failed kidney with a healthy donor kidney to restore normal kidney function.", "3-4 hours", "General", "10-14 days", Decimal("700000")),
            # Fertility
            ("IVF Treatment", get_cat("Fertility"), "In vitro fertilization treatment involving egg retrieval, fertilization in laboratory, and embryo transfer.", "4-6 weeks", "Sedation", "Outpatient", Decimal("150000")),
            ("Egg Freezing", get_cat("Fertility"), "Oocyte cryopreservation to preserve fertility by freezing eggs for future use.", "2-3 weeks", "Sedation", "Outpatient", Decimal("80000")),
            ("ICSI Treatment", get_cat("Fertility"), "Intracytoplasmic sperm injection for male factor infertility where a single sperm is injected into an egg.", "4-6 weeks", "Sedation", "Outpatient", Decimal("160000")),
            # Cosmetic Surgery
            ("Rhinoplasty", get_cat("Cosmetic Surgery"), "Surgical reshaping of the nose to improve appearance or correct breathing problems.", "2-3 hours", "General", "7-10 days", Decimal("120000")),
            ("Breast Augmentation", get_cat("Cosmetic Surgery"), "Surgical enhancement of breast size and shape using implants or fat transfer.", "1-2 hours", "General", "5-7 days", Decimal("150000")),
            ("Liposuction", get_cat("Cosmetic Surgery"), "Surgical removal of excess fat deposits to reshape and contour specific areas of the body.", "1-3 hours", "General/Local", "3-5 days", Decimal("80000")),
            ("Facelift", get_cat("Cosmetic Surgery"), "Surgical procedure to reduce visible signs of aging in the face and neck.", "3-5 hours", "General", "10-14 days", Decimal("200000")),
            ("FUE Hair Transplant", get_cat("Cosmetic Surgery"), "Follicular unit extraction hair transplant for natural-looking permanent hair restoration.", "6-8 hours", "Local", "7-10 days", Decimal("80000")),
            # Dental
            ("Dental Implants", get_cat("Dental"), "Permanent titanium implants surgically placed in the jawbone to replace missing teeth.", "3-6 months", "Local", "3-5 days", Decimal("40000")),
            ("Teeth Whitening", get_cat("Dental"), "Professional teeth whitening treatment to remove stains and brighten smile by several shades.", "1-2 hours", "None", "Same day", Decimal("8000")),
            ("Veneers", get_cat("Dental"), "Thin porcelain shells bonded to the front of teeth to improve appearance and correct imperfections.", "2-3 visits", "Local", "Same day", Decimal("15000")),
            ("Invisalign", get_cat("Dental"), "Clear aligner orthodontic treatment to straighten teeth without traditional metal braces.", "12-18 months", "None", "Outpatient", Decimal("120000")),
            ("Root Canal", get_cat("Dental"), "Endodontic treatment to remove infected pulp from inside a tooth and seal it to prevent reinfection.", "1-2 hours", "Local", "Same day", Decimal("8000")),
            # Wellness
            ("Panchakarma", get_cat("Wellness"), "Traditional Ayurvedic detoxification and rejuvenation therapy consisting of five therapeutic treatments.", "7-21 days", "None", "Outpatient", Decimal("25000")),
            ("Yoga Retreat", get_cat("Wellness"), "Immersive yoga and meditation program for physical and mental wellness.", "7-14 days", "None", "Outpatient", Decimal("15000")),
            ("Abhyanga", get_cat("Wellness"), "Traditional Ayurvedic full-body warm oil massage for relaxation and detoxification.", "1-2 hours", "None", "Same day", Decimal("3000")),
        ]
        for name, cat, desc, dur, anes, rec, price in treatments_data:
            Treatment.objects.update_or_create(
                name=name,
                defaults={
                    "category": cat,
                    "description": desc,
                    "duration": dur,
                    "anesthesia_type": anes,
                    "recovery_time": rec,
                    "starting_price": price,
                    "procedure_details": f"This {name} procedure is performed by highly qualified specialists using the latest technology and evidence-based protocols. Our team ensures the highest standards of patient safety and care throughout the treatment process.",
                    "preparation_guidelines": "Consult your specialist,Complete pre-operative tests,Stop blood thinners if advised,Fast 6-8 hours before procedure,Arrange post-procedure transport",
                    "aftercare_instructions": "Follow medication schedule,Attend all follow-up appointments,Rest as advised,Avoid strenuous activity,Contact doctor if complications arise",
                    "review_count": random.randint(50, 500),
                }
            )
        self.stdout.write(f"    {len(treatments_data)} treatments done.")

    def _seed_hospitals(self):
        from hospitals.models import Hospital
        from treatments.models import Treatment
        from core.models import Country, State
        self.stdout.write("  Seeding hospitals...")
        india = Country.objects.get(code="IN")
        my = Country.objects.get(code="MY")
        th = Country.objects.get(code="TH")
        tr = Country.objects.get(code="TR")
        def st(country, name):
            return State.objects.get(country=country, name=name)
        hospitals_data = [
            {
                "name": "Apollo Hospitals Delhi",
                "country": india, "state": st(india,"Delhi"), "city": "New Delhi",
                "about": "Apollo Hospitals Delhi is one of India premier multi-specialty hospitals with over 710 beds. Established in 1996, it offers world-class healthcare across 52 specialties with JCI and NABH accreditation. The hospital is equipped with the latest medical technology including robotic surgery, proton therapy, and advanced cardiac care.",
                "rating": Decimal("4.9"), "starting_price": Decimal("5000"),
                "established_year": 1996, "beds_count": 710, "staff_count": 3500,
                "departments_count": 52, "awards_count": 25,
                "jci_accredited": True, "nabh_accredited": True, "iso_certified": True,
                "phone": "+91-11-71791090", "email": "delhi@apollohospitals.com",
                "website": "https://www.apollohospitals.com",
                "profile_picture": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=400",
                "treatments": ["Coronary Angioplasty","Bypass Surgery (CABG)","Heart Valve Replacement","Knee Replacement","Hip Replacement","Brain Tumor Removal","Chemotherapy","Diabetes Management","Thyroid Treatment","Liver Transplant","LASIK Surgery","Kidney Transplant","IVF Treatment","Rhinoplasty","Dental Implants"],
            },
            {
                "name": "Fortis Memorial Research Institute",
                "country": india, "state": st(india,"Haryana"), "city": "Gurugram",
                "about": "Fortis Memorial Research Institute is a 1000-bed quaternary care hospital in Gurugram, recognized as one of the best hospitals in India. It is JCI and NABH accredited and offers advanced treatments in cardiac sciences, neurosciences, oncology, and orthopedics.",
                "rating": Decimal("4.8"), "starting_price": Decimal("6000"),
                "established_year": 2001, "beds_count": 1000, "staff_count": 4000,
                "departments_count": 45, "awards_count": 30,
                "jci_accredited": True, "nabh_accredited": True, "iso_certified": True,
                "phone": "+91-124-4921021", "email": "fmri@fortishealthcare.com",
                "website": "https://www.fortishealthcare.com",
                "profile_picture": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=400",
                "treatments": ["Bypass Surgery (CABG)","Cardiac Ablation","Knee Replacement","Spinal Fusion","Brain Tumor Removal","Epilepsy Surgery","Chemotherapy","Radiation Therapy","Bariatric Surgery","Rhinoplasty","FUE Hair Transplant","Kidney Stone Removal"],
            },
            {
                "name": "AIIMS New Delhi",
                "country": india, "state": st(india,"Delhi"), "city": "New Delhi",
                "about": "All India Institute of Medical Sciences (AIIMS) New Delhi is India premier medical institution and hospital. Established in 1956, it is a NABH-accredited hospital with 2478 beds offering cutting-edge treatment across all medical specialties. AIIMS is renowned for its research, education, and patient care.",
                "rating": Decimal("4.9"), "starting_price": Decimal("2000"),
                "established_year": 1956, "beds_count": 2478, "staff_count": 8000,
                "departments_count": 60, "awards_count": 50,
                "jci_accredited": False, "nabh_accredited": True, "iso_certified": True,
                "phone": "+91-11-26588500", "email": "director@aiims.edu",
                "website": "https://www.aiims.edu",
                "profile_picture": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=400",
                "treatments": ["Bypass Surgery (CABG)","Heart Valve Replacement","Knee Replacement","Hip Replacement","Brain Tumor Removal","Deep Brain Stimulation","Spinal Cord Surgery","Chemotherapy","Stem Cell Transplant","Kidney Transplant","Liver Transplant","Thyroidectomy","Prostate Surgery"],
            },
            {
                "name": "Medanta The Medicity",
                "country": india, "state": st(india,"Haryana"), "city": "Gurugram",
                "about": "Medanta The Medicity is a 1250-bed multi-super-speciality hospital in Gurugram founded by Dr. Naresh Trehan. It is JCI and NABH accredited and is known for its excellence in cardiac surgery, neurosciences, and organ transplants. The hospital has performed over 50,000 cardiac surgeries.",
                "rating": Decimal("4.8"), "starting_price": Decimal("7000"),
                "established_year": 2009, "beds_count": 1250, "staff_count": 5000,
                "departments_count": 45, "awards_count": 35,
                "jci_accredited": True, "nabh_accredited": True, "iso_certified": True,
                "phone": "+91-124-4141414", "email": "info@medanta.org",
                "website": "https://www.medanta.org",
                "profile_picture": "https://images.unsplash.com/photo-1551190822-a9333d879b1f?w=400",
                "treatments": ["Coronary Angioplasty","Bypass Surgery (CABG)","Heart Valve Replacement","Pacemaker Implantation","Knee Replacement","Brain Tumor Removal","Liver Transplant","Kidney Transplant","Diabetes Management","Thyroid Treatment","IVF Treatment"],
            },
            {
                "name": "Kokilaben Dhirubhai Ambani Hospital",
                "country": india, "state": st(india,"Maharashtra"), "city": "Mumbai",
                "about": "Kokilaben Dhirubhai Ambani Hospital is a 750-bed JCI and NABH accredited hospital in Mumbai. It is equipped with the da Vinci robotic surgery system and offers advanced treatments in oncology, cardiac sciences, neurosciences, and orthopedics.",
                "rating": Decimal("4.7"), "starting_price": Decimal("8000"),
                "established_year": 2009, "beds_count": 750, "staff_count": 3000,
                "departments_count": 40, "awards_count": 20,
                "jci_accredited": True, "nabh_accredited": True, "iso_certified": True,
                "phone": "+91-22-30999999", "email": "info@kokilabenhospital.com",
                "website": "https://www.kokilabenhospital.com",
                "profile_picture": "https://images.unsplash.com/photo-1587351021759-3e566b6af7cc?w=400",
                "treatments": ["Bypass Surgery (CABG)","Cardiac Ablation","Knee Replacement","Shoulder Replacement","Brain Tumor Removal","Chemotherapy","Radiation Therapy","Rhinoplasty","Breast Augmentation","Liposuction","Dental Implants"],
            },
            {
                "name": "Manipal Hospital Bangalore",
                "country": india, "state": st(india,"Karnataka"), "city": "Bangalore",
                "about": "Manipal Hospital Bangalore is a 600-bed NABH accredited multi-specialty hospital. It is one of the leading hospitals in South India offering advanced treatments in cardiac care, neurosciences, oncology, and orthopedics with state-of-the-art technology.",
                "rating": Decimal("4.7"), "starting_price": Decimal("5500"),
                "established_year": 1991, "beds_count": 600, "staff_count": 2500,
                "departments_count": 38, "awards_count": 18,
                "jci_accredited": False, "nabh_accredited": True, "iso_certified": True,
                "phone": "+91-80-25024444", "email": "info@manipalhospitals.com",
                "website": "https://www.manipalhospitals.com",
                "profile_picture": "https://images.unsplash.com/photo-1516549655169-df83a0774514?w=400",
                "treatments": ["Coronary Angioplasty","Knee Replacement","Hip Replacement","Arthroscopic Surgery","Brain Tumor Removal","Chemotherapy","Bariatric Surgery","LASIK Surgery","Cataract Surgery","Kidney Stone Removal"],
            },
            {
                "name": "Tata Memorial Hospital",
                "country": india, "state": st(india,"Maharashtra"), "city": "Mumbai",
                "about": "Tata Memorial Hospital is India premier cancer hospital and research centre. Established in 1941, it is NABH accredited with 629 beds dedicated entirely to cancer care. It is one of the largest cancer centres in Asia offering comprehensive oncology services.",
                "rating": Decimal("4.8"), "starting_price": Decimal("3000"),
                "established_year": 1941, "beds_count": 629, "staff_count": 3000,
                "departments_count": 20, "awards_count": 40,
                "jci_accredited": False, "nabh_accredited": True, "iso_certified": True,
                "phone": "+91-22-24177000", "email": "info@tmc.gov.in",
                "website": "https://tmc.gov.in",
                "profile_picture": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=400",
                "treatments": ["Chemotherapy","Radiation Therapy","Immunotherapy","Targeted Therapy","Stem Cell Transplant","Lung Cancer Treatment","Surgical Oncology"],
            },
            {
                "name": "Narayana Health City",
                "country": india, "state": st(india,"Karnataka"), "city": "Bangalore",
                "about": "Narayana Health City is a 3000-bed multi-specialty hospital campus in Bangalore founded by Dr. Devi Shetty. It is NABH accredited and is known for making world-class cardiac surgery affordable. The hospital performs over 30 cardiac surgeries daily.",
                "rating": Decimal("4.7"), "starting_price": Decimal("4000"),
                "established_year": 2000, "beds_count": 3000, "staff_count": 6000,
                "departments_count": 30, "awards_count": 25,
                "jci_accredited": False, "nabh_accredited": True, "iso_certified": True,
                "phone": "+91-80-71222222", "email": "info@narayanahealth.org",
                "website": "https://www.narayanahealth.org",
                "profile_picture": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=400",
                "treatments": ["Bypass Surgery (CABG)","Heart Valve Replacement","Pacemaker Implantation","Coronary Angioplasty","Kidney Transplant","Liver Transplant","Stem Cell Transplant"],
            },
            {
                "name": "Bumrungrad International Hospital",
                "country": th, "state": st(th,"Bangkok"), "city": "Bangkok",
                "about": "Bumrungrad International Hospital is Thailand most internationally recognized hospital with JCI accreditation. It serves over 1.1 million patients annually from 190 countries. The hospital offers world-class medical care with English-speaking staff and international patient services.",
                "rating": Decimal("4.9"), "starting_price": Decimal("8000"),
                "established_year": 1980, "beds_count": 580, "staff_count": 4000,
                "departments_count": 35, "awards_count": 30,
                "jci_accredited": True, "nabh_accredited": False, "iso_certified": True,
                "phone": "+66-2-667-1000", "email": "info@bumrungrad.com",
                "website": "https://www.bumrungrad.com",
                "profile_picture": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=400",
                "treatments": ["Coronary Angioplasty","Knee Replacement","Brain Tumor Removal","Chemotherapy","IVF Treatment","Rhinoplasty","Dental Implants","LASIK Surgery","Bariatric Surgery"],
            },
            {
                "name": "Prince Court Medical Centre",
                "country": my, "state": st(my,"Kuala Lumpur"), "city": "Kuala Lumpur",
                "about": "Prince Court Medical Centre is Malaysia premier private hospital with JCI accreditation. It offers 257 beds and is known for its excellence in cardiac care, oncology, and orthopedics. The hospital provides comprehensive medical tourism services.",
                "rating": Decimal("4.8"), "starting_price": Decimal("7000"),
                "established_year": 2008, "beds_count": 257, "staff_count": 1500,
                "departments_count": 30, "awards_count": 15,
                "jci_accredited": True, "nabh_accredited": False, "iso_certified": True,
                "phone": "+60-3-2160-0000", "email": "info@princecourt.com",
                "website": "https://www.princecourt.com",
                "profile_picture": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=400",
                "treatments": ["Bypass Surgery (CABG)","Knee Replacement","Hip Replacement","Chemotherapy","IVF Treatment","Rhinoplasty","Dental Implants"],
            },
            {
                "name": "Max Super Speciality Hospital Delhi",
                "country": india, "state": st(india,"Delhi"), "city": "New Delhi",
                "about": "Max Super Speciality Hospital is a 500-bed NABH accredited hospital in Delhi known for its excellence in cardiac sciences, neurosciences, and oncology. It has performed over 10,000 cardiac surgeries and 5,000 joint replacements.",
                "rating": Decimal("4.7"), "starting_price": Decimal("5500"),
                "established_year": 2006, "beds_count": 500, "staff_count": 2000,
                "departments_count": 35, "awards_count": 15,
                "jci_accredited": False, "nabh_accredited": True, "iso_certified": True,
                "phone": "+91-11-26515050", "email": "info@maxhealthcare.in",
                "website": "https://www.maxhealthcare.in",
                "profile_picture": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=400",
                "treatments": ["Coronary Angioplasty","Bypass Surgery (CABG)","Knee Replacement","Spinal Fusion","Brain Tumor Removal","Chemotherapy","Bariatric Surgery","Kidney Stone Removal"],
            },
            {
                "name": "Sankara Nethralaya",
                "country": india, "state": st(india,"Tamil Nadu"), "city": "Chennai",
                "about": "Sankara Nethralaya is India leading eye hospital with NABH accreditation. Established in 1978, it has performed over 3 million eye surgeries. The hospital is renowned for its expertise in corneal transplants, retinal surgery, and glaucoma treatment.",
                "rating": Decimal("4.8"), "starting_price": Decimal("15000"),
                "established_year": 1978, "beds_count": 500, "staff_count": 1500,
                "departments_count": 15, "awards_count": 20,
                "jci_accredited": False, "nabh_accredited": True, "iso_certified": True,
                "phone": "+91-44-28271616", "email": "info@sankaranethralaya.org",
                "website": "https://www.sankaranethralaya.org",
                "profile_picture": "https://images.unsplash.com/photo-1551190822-a9333d879b1f?w=400",
                "treatments": ["LASIK Surgery","Cataract Surgery","Retinal Surgery","Glaucoma Treatment"],
            },
            {
                "name": "Christian Medical College Vellore",
                "country": india, "state": st(india,"Tamil Nadu"), "city": "Vellore",
                "about": "Christian Medical College Vellore is one of India oldest and most respected medical institutions with 2700 beds. NABH accredited, it is known for its excellence in organ transplants, neurosciences, and infectious diseases. CMC Vellore has pioneered many medical firsts in India.",
                "rating": Decimal("4.8"), "starting_price": Decimal("3000"),
                "established_year": 1900, "beds_count": 2700, "staff_count": 7000,
                "departments_count": 55, "awards_count": 45,
                "jci_accredited": False, "nabh_accredited": True, "iso_certified": True,
                "phone": "+91-416-2281000", "email": "info@cmcvellore.ac.in",
                "website": "https://www.cmch-vellore.edu",
                "profile_picture": "https://images.unsplash.com/photo-1587351021759-3e566b6af7cc?w=400",
                "treatments": ["Kidney Transplant","Liver Transplant","Stem Cell Transplant","Brain Tumor Removal","Spinal Cord Surgery","Chemotherapy","Thyroidectomy"],
            },
            {
                "name": "Rajiv Gandhi Cancer Institute",
                "country": india, "state": st(india,"Delhi"), "city": "New Delhi",
                "about": "Rajiv Gandhi Cancer Institute and Research Centre is a 330-bed NABH accredited cancer hospital in Delhi. It is one of the leading cancer centres in North India offering comprehensive oncology services including bone marrow transplants and robotic surgery.",
                "rating": Decimal("4.7"), "starting_price": Decimal("4000"),
                "established_year": 1996, "beds_count": 330, "staff_count": 1200,
                "departments_count": 18, "awards_count": 12,
                "jci_accredited": False, "nabh_accredited": True, "iso_certified": True,
                "phone": "+91-11-47022222", "email": "info@rgcirc.org",
                "website": "https://www.rgcirc.org",
                "profile_picture": "https://images.unsplash.com/photo-1516549655169-df83a0774514?w=400",
                "treatments": ["Chemotherapy","Radiation Therapy","Immunotherapy","Targeted Therapy","Stem Cell Transplant","Lung Cancer Treatment"],
            },
            {
                "name": "Acibadem Hospital Istanbul",
                "country": tr, "state": st(tr,"Istanbul"), "city": "Istanbul",
                "about": "Acibadem Hospital is Turkey leading JCI-accredited hospital chain. The Istanbul flagship has 400 beds and is known for its excellence in cardiac surgery, oncology, and orthopedics. It serves thousands of international patients annually with multilingual staff.",
                "rating": Decimal("4.8"), "starting_price": Decimal("6000"),
                "established_year": 1991, "beds_count": 400, "staff_count": 2000,
                "departments_count": 35, "awards_count": 20,
                "jci_accredited": True, "nabh_accredited": False, "iso_certified": True,
                "phone": "+90-212-304-4444", "email": "info@acibadem.com",
                "website": "https://www.acibadem.com",
                "profile_picture": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=400",
                "treatments": ["Bypass Surgery (CABG)","Knee Replacement","Brain Tumor Removal","Chemotherapy","Rhinoplasty","Hair Transplant","Dental Implants","IVF Treatment"],
            },
        ]
        for hdata in hospitals_data:
            treatment_names = hdata.pop("treatments")
            hospital, _ = Hospital.objects.update_or_create(
                name=hdata["name"],
                defaults=hdata
            )
            from treatments.models import Treatment
            for tname in treatment_names:
                try:
                    t = Treatment.objects.get(name=tname)
                    hospital.treatments.add(t)
                except Treatment.DoesNotExist:
                    pass
        self.stdout.write(f"    {len(hospitals_data)} hospitals done.")

    def _seed_doctors(self):
        from doctors.models import Doctor
        from hospitals.models import Hospital
        from treatments.models import Treatment
        self.stdout.write("  Seeding doctors...")
        def hosp(*names):
            return [Hospital.objects.get(name=n) for n in names if Hospital.objects.filter(name=n).exists()]
        def treat(*names):
            return [Treatment.objects.get(name=n) for n in names if Treatment.objects.filter(name=n).exists()]
        doctors_data = [
            {
                "name": "Dr. Naresh Trehan",
                "specialization": "Cardiac Surgeon",
                "about": "Dr. Naresh Trehan is one of India most celebrated cardiac surgeons and the founder of Medanta The Medicity. With over 40 years of experience, he has performed more than 48,000 cardiac surgeries. He trained at NYU Medical Center and is credited with revolutionizing cardiac care in India.",
                "education": "MBBS - AIIMS New Delhi; MS (Surgery) - AIIMS; Fellowship in Cardiothoracic Surgery - NYU Medical Center, USA",
                "experience_years": 40,
                "rating": Decimal("4.9"), "review_count": 1250,
                "awards": "Padma Bhushan 2001\nPadma Vibhushan 2021\nDr. B.C. Roy Award\nLal Bahadur Shastri National Award",
                "languages_spoken": "Hindi, English",
                "key_points": "48000+ cardiac surgeries performed, Pioneer of minimally invasive cardiac surgery in India, Founder of Medanta The Medicity, Former Chief of Cardiothoracic Surgery at NYU",
                "phone": "+91-124-4141414",
                "email": "dr.trehan@medanta.org",
                "medical_license_number": "DMC-12345",
                "profile_picture": "https://ui-avatars.com/api/?name=Naresh+Trehan&background=1a3c6e&color=fff&size=200",
                "hospitals": hosp("Medanta The Medicity","Apollo Hospitals Delhi"),
                "treatments": treat("Bypass Surgery (CABG)","Coronary Angioplasty","Heart Valve Replacement","Pacemaker Implantation","Cardiac Ablation"),
            },
            {
                "name": "Dr. Devi Shetty",
                "specialization": "Cardiac Surgeon",
                "about": "Dr. Devi Shetty is a world-renowned cardiac surgeon and philanthropist who founded Narayana Health. He has performed over 15,000 open heart surgeries and is known for making cardiac surgery affordable for the masses. He was Mother Teresa personal physician.",
                "education": "MBBS - Kasturba Medical College Mangalore; MS - Kasturba Medical College; Fellowship in Cardiac Surgery - Guy Hospital London",
                "experience_years": 35,
                "rating": Decimal("4.9"), "review_count": 1100,
                "awards": "Padma Bhushan 2012\nCNBC Asia Business Leader Award\nErnst & Young Entrepreneur of the Year",
                "languages_spoken": "Kannada, Hindi, English",
                "key_points": "15000+ open heart surgeries, Founder of Narayana Health, Made cardiac surgery affordable, Mother Teresa personal physician",
                "phone": "+91-80-71222222",
                "email": "dr.shetty@narayanahealth.org",
                "medical_license_number": "KMC-23456",
                "profile_picture": "https://ui-avatars.com/api/?name=Devi+Shetty&background=1a3c6e&color=fff&size=200",
                "hospitals": hosp("Narayana Health City"),
                "treatments": treat("Bypass Surgery (CABG)","Heart Valve Replacement","Coronary Angioplasty","Pacemaker Implantation"),
            },
            {
                "name": "Dr. Priya Patel",
                "specialization": "Cardiac Surgeon",
                "about": "Dr. Priya Patel is a highly skilled cardiac surgeon with 20 years of experience in interventional cardiology and cardiac surgery. She specializes in minimally invasive cardiac procedures and has performed over 5,000 successful cardiac interventions.",
                "education": "MBBS - Grant Medical College Mumbai; MD (Cardiology) - KEM Hospital Mumbai; Fellowship in Interventional Cardiology - Cleveland Clinic USA",
                "experience_years": 20,
                "rating": Decimal("4.8"), "review_count": 680,
                "awards": "Best Cardiologist Award - IMA 2019\nWomen in Medicine Award 2020",
                "languages_spoken": "Hindi, English, Gujarati",
                "key_points": "5000+ cardiac interventions, Specialist in minimally invasive cardiac surgery, Expert in hypertension management, Blood pressure specialist",
                "phone": "+91-11-71791090",
                "email": "dr.priya@apollohospitals.com",
                "medical_license_number": "MMC-34567",
                "profile_picture": "https://ui-avatars.com/api/?name=Priya+Patel&background=e74c3c&color=fff&size=200",
                "hospitals": hosp("Apollo Hospitals Delhi","Fortis Memorial Research Institute"),
                "treatments": treat("Coronary Angioplasty","Cardiac Ablation","Angiography","Pacemaker Implantation"),
            },
            {
                "name": "Dr. Ramesh Sharma",
                "specialization": "Orthopedic Surgeon",
                "about": "Dr. Ramesh Sharma is a leading orthopedic surgeon with 22 years of experience specializing in joint replacement surgery. He has performed over 8,000 knee and hip replacement surgeries and is a pioneer of computer-assisted joint replacement in India.",
                "education": "MBBS - AIIMS New Delhi; MS (Orthopedics) - AIIMS; Fellowship in Joint Replacement - Hospital for Special Surgery New York",
                "experience_years": 22,
                "rating": Decimal("4.9"), "review_count": 920,
                "awards": "Best Orthopedic Surgeon - Times Health Awards 2020\nNational Award for Excellence in Orthopedics",
                "languages_spoken": "Hindi, English",
                "key_points": "8000+ joint replacement surgeries, Pioneer of computer-assisted surgery in India, Expert in knee and hip replacement, Bone and joint specialist",
                "phone": "+91-11-26588500",
                "email": "dr.ramesh@aiims.edu",
                "medical_license_number": "DMC-45678",
                "profile_picture": "https://ui-avatars.com/api/?name=Ramesh+Sharma&background=27ae60&color=fff&size=200",
                "hospitals": hosp("AIIMS New Delhi","Apollo Hospitals Delhi"),
                "treatments": treat("Knee Replacement","Hip Replacement","Arthroscopic Surgery","Shoulder Replacement","Spinal Fusion"),
            },
            {
                "name": "Dr. Smith Singh",
                "specialization": "Orthopedic Surgeon",
                "about": "Dr. Smith Singh is an experienced orthopedic surgeon with 18 years of expertise in sports medicine and joint replacement. He has treated numerous national and international athletes and has performed over 4,000 arthroscopic procedures.",
                "education": "MBBS - Maulana Azad Medical College Delhi; MS (Orthopedics) - PGIMER Chandigarh; Fellowship in Sports Medicine - Hospital for Special Surgery New York",
                "experience_years": 18,
                "rating": Decimal("4.7"), "review_count": 540,
                "awards": "Sports Medicine Excellence Award 2018\nBest Young Orthopedic Surgeon 2015",
                "languages_spoken": "Hindi, English, Punjabi",
                "key_points": "4000+ arthroscopic procedures, Sports medicine specialist, Expert in knee ligament reconstruction, Bone and joint specialist",
                "phone": "+91-124-4921021",
                "email": "dr.smith@fortishealthcare.com",
                "medical_license_number": "DMC-56789",
                "profile_picture": "https://ui-avatars.com/api/?name=Smith+Singh&background=27ae60&color=fff&size=200",
                "hospitals": hosp("Fortis Memorial Research Institute","Max Super Speciality Hospital Delhi"),
                "treatments": treat("Knee Replacement","Arthroscopic Surgery","Shoulder Replacement","Spine Surgery"),
            },
            {
                "name": "Dr. Ahmed Khan",
                "specialization": "Neurosurgeon",
                "about": "Dr. Ahmed Khan is a distinguished neurosurgeon with 28 years of experience in brain and spine surgery. He has performed over 6,000 neurosurgical procedures including complex brain tumor removals and deep brain stimulation surgeries for Parkinson disease.",
                "education": "MBBS - AIIMS New Delhi; MCh (Neurosurgery) - AIIMS; Fellowship in Functional Neurosurgery - Toronto Western Hospital Canada",
                "experience_years": 28,
                "rating": Decimal("4.9"), "review_count": 780,
                "awards": "Dr. B.C. Roy Award 2015\nBest Neurosurgeon - India Today Medical Excellence Awards 2019",
                "languages_spoken": "Hindi, English, Urdu",
                "key_points": "6000+ neurosurgical procedures, Expert in brain tumor removal, Pioneer of DBS surgery in India, Spine and brain specialist",
                "phone": "+91-11-26588500",
                "email": "dr.ahmed@aiims.edu",
                "medical_license_number": "DMC-67890",
                "profile_picture": "https://ui-avatars.com/api/?name=Ahmed+Khan&background=8e44ad&color=fff&size=200",
                "hospitals": hosp("AIIMS New Delhi","Apollo Hospitals Delhi"),
                "treatments": treat("Brain Tumor Removal","Deep Brain Stimulation","Epilepsy Surgery","Spinal Cord Surgery","Stroke Rehabilitation"),
            },
            {
                "name": "Dr. Paresh Doshi",
                "specialization": "Neurosurgeon",
                "about": "Dr. Paresh Doshi is a leading neurosurgeon specializing in functional neurosurgery and movement disorders. He has performed over 3,000 deep brain stimulation surgeries and is internationally recognized for his work in treating Parkinson disease and epilepsy.",
                "education": "MBBS - Seth GS Medical College Mumbai; MCh (Neurosurgery) - KEM Hospital; Fellowship in Functional Neurosurgery - University of Toronto",
                "experience_years": 30,
                "rating": Decimal("4.8"), "review_count": 620,
                "awards": "International Movement Disorder Society Award\nBest Neurosurgeon - Maharashtra Medical Council",
                "languages_spoken": "Hindi, English, Marathi, Gujarati",
                "key_points": "3000+ DBS surgeries, World expert in movement disorders, Parkinson disease specialist, Brain tumor specialist",
                "phone": "+91-22-30999999",
                "email": "dr.doshi@kokilabenhospital.com",
                "medical_license_number": "MMC-78901",
                "profile_picture": "https://ui-avatars.com/api/?name=Paresh+Doshi&background=8e44ad&color=fff&size=200",
                "hospitals": hosp("Kokilaben Dhirubhai Ambani Hospital"),
                "treatments": treat("Deep Brain Stimulation","Brain Tumor Removal","Epilepsy Surgery","Spinal Cord Surgery"),
            },
            {
                "name": "Dr. Anil Heroor",
                "specialization": "Surgical Oncologist",
                "about": "Dr. Anil Heroor is a leading surgical oncologist with 25 years of experience in cancer surgery. He specializes in robotic and laparoscopic cancer surgery and has performed over 5,000 cancer surgeries. He is known for his expertise in gastrointestinal and breast cancer surgery.",
                "education": "MBBS - Grant Medical College Mumbai; MS (Surgery) - KEM Hospital; MCh (Surgical Oncology) - Tata Memorial Hospital; Fellowship in Robotic Surgery - USA",
                "experience_years": 25,
                "rating": Decimal("4.9"), "review_count": 850,
                "awards": "Best Oncosurgeon - India Cancer Congress 2020\nExcellence in Robotic Surgery Award",
                "languages_spoken": "Hindi, English, Marathi",
                "key_points": "5000+ cancer surgeries, Robotic surgery pioneer, Expert in GI and breast cancer, Lung cancer specialist",
                "phone": "+91-22-30999999",
                "email": "dr.heroor@kokilabenhospital.com",
                "medical_license_number": "MMC-89012",
                "profile_picture": "https://ui-avatars.com/api/?name=Anil+Heroor&background=c0392b&color=fff&size=200",
                "hospitals": hosp("Kokilaben Dhirubhai Ambani Hospital","Fortis Memorial Research Institute"),
                "treatments": treat("Chemotherapy","Radiation Therapy","Immunotherapy","Targeted Therapy","Lung Cancer Treatment"),
            },
            {
                "name": "Dr. Sara Kapoor",
                "specialization": "Endocrinologist",
                "about": "Dr. Sara Kapoor is a highly regarded endocrinologist with 18 years of experience in managing diabetes, thyroid disorders, and hormonal conditions. She has treated over 20,000 patients with diabetes and is known for her patient-centered approach to endocrine care.",
                "education": "MBBS - Lady Hardinge Medical College Delhi; MD (Internal Medicine) - AIIMS; DM (Endocrinology) - AIIMS",
                "experience_years": 18,
                "rating": Decimal("4.8"), "review_count": 760,
                "awards": "Best Endocrinologist - Endocrine Society of India 2019\nWomen in Medicine Excellence Award",
                "languages_spoken": "Hindi, English",
                "key_points": "20000+ diabetes patients treated, Thyroid disorder specialist, Expert in insulin pump therapy, Diabetes and thyroid specialist",
                "phone": "+91-11-26588500",
                "email": "dr.sara@aiims.edu",
                "medical_license_number": "DMC-90123",
                "profile_picture": "https://ui-avatars.com/api/?name=Sara+Kapoor&background=e67e22&color=fff&size=200",
                "hospitals": hosp("AIIMS New Delhi","Medanta The Medicity"),
                "treatments": treat("Diabetes Management","Thyroid Treatment","Thyroidectomy","Insulin Pump Therapy"),
            },
            {
                "name": "Dr. Niranjan Kumar",
                "specialization": "Gastroenterologist",
                "about": "Dr. Niranjan Kumar is a senior gastroenterologist and hepatologist with 20 years of experience. He specializes in liver diseases, inflammatory bowel disease, and advanced endoscopic procedures. He has performed over 15,000 endoscopic procedures.",
                "education": "MBBS - Maulana Azad Medical College Delhi; MD (Medicine) - PGIMER Chandigarh; DM (Gastroenterology) - SGPGI Lucknow",
                "experience_years": 20,
                "rating": Decimal("4.8"), "review_count": 590,
                "awards": "Best Gastroenterologist - Indian Society of Gastroenterology 2018",
                "languages_spoken": "Hindi, English",
                "key_points": "15000+ endoscopic procedures, Liver disease specialist, Expert in liver transplant evaluation, Gastroenterology and hepatology specialist",
                "phone": "+91-124-4141414",
                "email": "dr.niranjan@medanta.org",
                "medical_license_number": "DMC-01234",
                "profile_picture": "https://ui-avatars.com/api/?name=Niranjan+Kumar&background=16a085&color=fff&size=200",
                "hospitals": hosp("Medanta The Medicity","Apollo Hospitals Delhi"),
                "treatments": treat("Liver Transplant","Colonoscopy","Bariatric Surgery","Liver Biopsy"),
            },
            {
                "name": "Dr. Arjun Mehta",
                "specialization": "MBBS",
                "about": "Dr. Arjun Mehta is an experienced general physician and diabetologist with 15 years of practice. He provides comprehensive primary care and specializes in managing chronic conditions including diabetes, hypertension, and metabolic disorders.",
                "education": "MBBS - Grant Medical College Mumbai; MD (General Medicine) - KEM Hospital Mumbai; Diploma in Diabetology - RSSDI",
                "experience_years": 15,
                "rating": Decimal("4.7"), "review_count": 480,
                "awards": "Best General Physician - IMA Mumbai Branch 2018",
                "languages_spoken": "Hindi, English, Marathi, Gujarati",
                "key_points": "Diabetes and hypertension specialist, Comprehensive primary care, Preventive medicine expert, General medicine and diabetes",
                "phone": "+91-11-71791090",
                "email": "dr.arjun@apollohospitals.com",
                "medical_license_number": "MMC-11223",
                "profile_picture": "https://ui-avatars.com/api/?name=Arjun+Mehta&background=2980b9&color=fff&size=200",
                "hospitals": hosp("Apollo Hospitals Delhi"),
                "treatments": treat("Diabetes Management","Thyroid Treatment","Asthma Treatment","COPD Management"),
            },
            {
                "name": "Dr. Rajesh Gupta",
                "specialization": "Plastic Surgeon",
                "about": "Dr. Rajesh Gupta is a board-certified plastic and reconstructive surgeon with 22 years of experience. He specializes in cosmetic surgery, hair transplantation, and reconstructive procedures. He has performed over 6,000 cosmetic surgeries.",
                "education": "MBBS - AIIMS New Delhi; MS (Surgery) - AIIMS; MCh (Plastic Surgery) - PGIMER Chandigarh; Fellowship in Aesthetic Surgery - Paris",
                "experience_years": 22,
                "rating": Decimal("4.8"), "review_count": 720,
                "awards": "Best Plastic Surgeon - Association of Plastic Surgeons of India 2019",
                "languages_spoken": "Hindi, English",
                "key_points": "6000+ cosmetic surgeries, Hair transplant specialist, Expert in rhinoplasty and facelift, Cosmetic and reconstructive surgery",
                "phone": "+91-11-71791090",
                "email": "dr.rajesh@apollohospitals.com",
                "medical_license_number": "DMC-22334",
                "profile_picture": "https://ui-avatars.com/api/?name=Rajesh+Gupta&background=9b59b6&color=fff&size=200",
                "hospitals": hosp("Apollo Hospitals Delhi","Fortis Memorial Research Institute"),
                "treatments": treat("Rhinoplasty","Breast Augmentation","Liposuction","Facelift","FUE Hair Transplant"),
            },
            {
                "name": "Dr. Maria Gonzalez",
                "specialization": "Gynecologist",
                "about": "Dr. Maria Gonzalez is a senior gynecologist and fertility specialist with 20 years of experience. She specializes in IVF, reproductive medicine, and high-risk obstetrics. She has helped over 3,000 couples achieve successful pregnancies through assisted reproduction.",
                "education": "MBBS - St. John Medical College Bangalore; MD (Obstetrics & Gynecology) - AIIMS; Fellowship in Reproductive Medicine - ESHRE Belgium",
                "experience_years": 20,
                "rating": Decimal("4.8"), "review_count": 650,
                "awards": "Best Fertility Specialist - Indian Fertility Society 2020",
                "languages_spoken": "Hindi, English, Spanish",
                "key_points": "3000+ successful IVF cycles, High-risk pregnancy specialist, Expert in reproductive medicine, Fertility and IVF specialist",
                "phone": "+91-11-71791090",
                "email": "dr.maria@apollohospitals.com",
                "medical_license_number": "KMC-33445",
                "profile_picture": "https://ui-avatars.com/api/?name=Maria+Gonzalez&background=e91e63&color=fff&size=200",
                "hospitals": hosp("Apollo Hospitals Delhi","Kokilaben Dhirubhai Ambani Hospital"),
                "treatments": treat("IVF Treatment","Egg Freezing","ICSI Treatment"),
            },
            {
                "name": "Dr. Deepak Mehta",
                "specialization": "Pulmonologist",
                "about": "Dr. Deepak Mehta is a leading pulmonologist and thoracic oncologist with 22 years of experience. He specializes in lung cancer treatment, COPD management, and interventional pulmonology. He has treated over 5,000 lung cancer patients.",
                "education": "MBBS - Grant Medical College Mumbai; MD (Pulmonary Medicine) - KEM Hospital; Fellowship in Thoracic Oncology - MD Anderson Cancer Center USA",
                "experience_years": 22,
                "rating": Decimal("4.8"), "review_count": 580,
                "awards": "Best Pulmonologist - Indian Chest Society 2019\nExcellence in Lung Cancer Treatment Award",
                "languages_spoken": "Hindi, English, Marathi",
                "key_points": "5000+ lung cancer patients treated, COPD and asthma specialist, Expert in bronchoscopy, Lung and pulmonary specialist",
                "phone": "+91-22-24177000",
                "email": "dr.deepak@tmc.gov.in",
                "medical_license_number": "MMC-44556",
                "profile_picture": "https://ui-avatars.com/api/?name=Deepak+Mehta&background=00897b&color=fff&size=200",
                "hospitals": hosp("Tata Memorial Hospital","Apollo Hospitals Delhi"),
                "treatments": treat("Lung Cancer Treatment","Bronchoscopy","COPD Management","Asthma Treatment","Chemotherapy"),
            },
            {
                "name": "Dr. Anita Sharma",
                "specialization": "Ophthalmologist",
                "about": "Dr. Anita Sharma is a renowned ophthalmologist with 18 years of experience specializing in refractive surgery, cataract surgery, and retinal diseases. She has performed over 10,000 eye surgeries and is known for her expertise in LASIK and advanced cataract surgery.",
                "education": "MBBS - Madras Medical College Chennai; MS (Ophthalmology) - Sankara Nethralaya; Fellowship in Vitreoretinal Surgery - Moorfields Eye Hospital London",
                "experience_years": 18,
                "rating": Decimal("4.8"), "review_count": 690,
                "awards": "Best Ophthalmologist - All India Ophthalmological Society 2019",
                "languages_spoken": "Tamil, Hindi, English",
                "key_points": "10000+ eye surgeries, LASIK specialist, Expert in retinal surgery, Eye and vision specialist",
                "phone": "+91-44-28271616",
                "email": "dr.anita@sankaranethralaya.org",
                "medical_license_number": "TNM-55667",
                "profile_picture": "https://ui-avatars.com/api/?name=Anita+Sharma&background=0288d1&color=fff&size=200",
                "hospitals": hosp("Sankara Nethralaya"),
                "treatments": treat("LASIK Surgery","Cataract Surgery","Retinal Surgery","Glaucoma Treatment"),
            },
            {
                "name": "Dr. Preecha Srisuwan",
                "specialization": "Dental Surgeon",
                "about": "Dr. Preecha Srisuwan is a highly skilled dental surgeon with 20 years of experience at Bumrungrad International Hospital. He specializes in dental implants, cosmetic dentistry, and full mouth rehabilitation. He has treated thousands of international patients.",
                "education": "BDS - Mahidol University Bangkok; MDS (Prosthodontics) - Chulalongkorn University; Fellowship in Implantology - ITI Switzerland",
                "experience_years": 20,
                "rating": Decimal("4.8"), "review_count": 520,
                "awards": "Best Dental Surgeon - Thailand Dental Association 2018",
                "languages_spoken": "Thai, English",
                "key_points": "Dental implant specialist, Expert in cosmetic dentistry, Full mouth rehabilitation, Dental and oral surgery",
                "phone": "+66-2-667-1000",
                "email": "dr.preecha@bumrungrad.com",
                "medical_license_number": "TH-66778",
                "profile_picture": "https://ui-avatars.com/api/?name=Preecha+Srisuwan&background=f39c12&color=fff&size=200",
                "hospitals": hosp("Bumrungrad International Hospital"),
                "treatments": treat("Dental Implants","Teeth Whitening","Veneers","Invisalign","Root Canal"),
            },
            {
                "name": "Dr. Kavita Desai",
                "specialization": "Pediatric Surgeon",
                "about": "Dr. Kavita Desai is a senior pediatric surgeon with 15 years of experience at AIIMS. She specializes in neonatal surgery, pediatric oncology, and minimally invasive pediatric procedures. She has performed over 3,000 pediatric surgeries.",
                "education": "MBBS - AIIMS New Delhi; MS (Surgery) - AIIMS; MCh (Pediatric Surgery) - AIIMS",
                "experience_years": 15,
                "rating": Decimal("4.7"), "review_count": 380,
                "awards": "Best Pediatric Surgeon - Indian Association of Pediatric Surgeons 2019",
                "languages_spoken": "Hindi, English",
                "key_points": "3000+ pediatric surgeries, Neonatal surgery specialist, Pediatric oncology expert, Children surgery specialist",
                "phone": "+91-11-26588500",
                "email": "dr.kavita@aiims.edu",
                "medical_license_number": "DMC-77889",
                "profile_picture": "https://ui-avatars.com/api/?name=Kavita+Desai&background=ad1457&color=fff&size=200",
                "hospitals": hosp("AIIMS New Delhi"),
                "treatments": treat("Chemotherapy","Stem Cell Transplant"),
            },
            {
                "name": "Dr. Rajiv Sinha",
                "specialization": "Urologist",
                "about": "Dr. Rajiv Sinha is a leading urologist with 20 years of experience specializing in robotic urology, kidney transplants, and urological oncology. He has performed over 2,000 kidney transplants and 1,500 robotic urological procedures.",
                "education": "MBBS - AIIMS New Delhi; MS (Surgery) - AIIMS; MCh (Urology) - PGIMER Chandigarh; Fellowship in Robotic Urology - Johns Hopkins USA",
                "experience_years": 20,
                "rating": Decimal("4.7"), "review_count": 450,
                "awards": "Best Urologist - Urological Society of India 2019",
                "languages_spoken": "Hindi, English",
                "key_points": "2000+ kidney transplants, Robotic urology pioneer, Kidney stone specialist, Urology and kidney specialist",
                "phone": "+91-11-71791090",
                "email": "dr.rajiv@apollohospitals.com",
                "medical_license_number": "DMC-88990",
                "profile_picture": "https://ui-avatars.com/api/?name=Rajiv+Sinha&background=546e7a&color=fff&size=200",
                "hospitals": hosp("Apollo Hospitals Delhi","AIIMS New Delhi"),
                "treatments": treat("Kidney Transplant","Kidney Stone Removal","Prostate Surgery"),
            },
        ]
        for ddata in doctors_data:
            hospitals_list = ddata.pop("hospitals")
            treatments_list = ddata.pop("treatments")
            doctor, _ = Doctor.objects.update_or_create(
                name=ddata["name"],
                defaults=ddata
            )
            doctor.hospitals.set(hospitals_list)
            doctor.treatments.set(treatments_list)
        self.stdout.write(f"    {len(doctors_data)} doctors done.")

    def _seed_patient_users(self):
        from accounts.models import UserProfile
        self.stdout.write("  Seeding patient users...")
        patients = [
            ("patient_rahul", "Rahul", "Verma", "rahul.verma@email.com", "Mumbai"),
            ("patient_sunita", "Sunita", "Sharma", "sunita.sharma@email.com", "Delhi"),
            ("patient_mohan", "Mohan", "Patel", "mohan.patel@email.com", "Ahmedabad"),
            ("patient_priya", "Priya", "Singh", "priya.singh@email.com", "Bangalore"),
            ("patient_amit", "Amit", "Kumar", "amit.kumar@email.com", "Chennai"),
            ("patient_neha", "Neha", "Gupta", "neha.gupta@email.com", "Hyderabad"),
            ("patient_vikram", "Vikram", "Joshi", "vikram.joshi@email.com", "Pune"),
            ("patient_ananya", "Ananya", "Reddy", "ananya.reddy@email.com", "Kolkata"),
            ("patient_suresh", "Suresh", "Nair", "suresh.nair@email.com", "Kochi"),
            ("patient_meera", "Meera", "Iyer", "meera.iyer@email.com", "Jaipur"),
        ]
        self.patient_profiles = []
        for username, first, last, email, city in patients:
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={"first_name": first, "last_name": last, "email": email}
            )
            if _:
                user.set_password("Patient@123")
                user.save()
            profile, _ = UserProfile.objects.get_or_create(
                user=user,
                defaults={"user_type": "patient", "city": city}
            )
            self.patient_profiles.append(profile)
        self.stdout.write(f"    {len(patients)} patient users done.")

    def _seed_blogs(self):
        from blogs.models import BlogPost
        from treatments.models import Treatment
        from doctors.models import Doctor
        from hospitals.models import Hospital
        self.stdout.write("  Seeding blog posts...")
        def get_t(name):
            return Treatment.objects.filter(name=name).first()
        def get_d(name):
            return Doctor.objects.filter(name=name).first()
        def get_h(name):
            return Hospital.objects.filter(name=name).first()
        blogs = [
            ("Understanding Coronary Artery Disease: Symptoms and Treatment Options",
             "cardiac-artery-disease-guide",
             """Coronary artery disease (CAD) is the most common type of heart disease and the leading cause of death worldwide. It occurs when the coronary arteries that supply blood to the heart muscle become hardened and narrowed due to plaque buildup.\n\nSymptoms of CAD include chest pain or discomfort (angina), shortness of breath, heart attack, and in some cases, no symptoms at all. Risk factors include high blood pressure, high cholesterol, smoking, diabetes, obesity, and family history.\n\nDiagnosis involves ECG, stress tests, echocardiogram, and coronary angiography. Treatment options range from lifestyle changes and medications to interventional procedures like angioplasty and bypass surgery.\n\nAt Apollo Hospitals Delhi, our cardiac team has performed over 10,000 successful cardiac interventions. Dr. Priya Patel, our senior cardiologist, emphasizes that early detection and lifestyle modification can significantly reduce the risk of heart attacks.\n\nIf you experience chest pain, shortness of breath, or palpitations, consult a cardiologist immediately. Early intervention can save lives.""",
             get_t("Coronary Angioplasty"), get_d("Dr. Priya Patel"), get_h("Apollo Hospitals Delhi")),
            ("Bypass Surgery vs Angioplasty: Which is Right for You?",
             "bypass-vs-angioplasty-guide",
             """When coronary arteries are blocked, two main treatment options are available: coronary angioplasty (PCI) and bypass surgery (CABG). Understanding the differences helps patients make informed decisions.\n\nAngioplasty is a minimally invasive procedure where a balloon catheter is used to open blocked arteries, often with a stent placement. It requires shorter hospital stay (1-2 days) and faster recovery. It is ideal for single or double vessel disease.\n\nBypass surgery creates new pathways around blocked arteries using blood vessels from other parts of the body. It is more invasive but provides better long-term outcomes for patients with multiple vessel disease or diabetes.\n\nDr. Naresh Trehan, founder of Medanta and one of India most celebrated cardiac surgeons, recommends bypass surgery for patients with three-vessel disease or left main coronary artery disease. For single vessel disease, angioplasty is often the preferred choice.\n\nThe decision depends on the number of blocked arteries, overall heart function, presence of diabetes, and patient preference. A thorough evaluation by a cardiac team is essential.""",
             get_t("Bypass Surgery (CABG)"), get_d("Dr. Naresh Trehan"), get_h("Medanta The Medicity")),
            ("Knee Replacement Surgery: Complete Guide for Patients",
             "knee-replacement-complete-guide",
             """Knee replacement surgery (arthroplasty) is one of the most successful orthopedic procedures, relieving pain and restoring function in patients with severe knee arthritis. Over 700,000 knee replacements are performed annually in India.\n\nWho needs knee replacement? Patients with severe osteoarthritis (Grade III-IV), rheumatoid arthritis, or post-traumatic arthritis who have failed conservative treatment including medications, physiotherapy, and injections.\n\nThe procedure involves removing damaged cartilage and bone from the knee joint and replacing it with metal and plastic components. Total knee replacement replaces the entire joint, while partial replacement addresses only the damaged compartment.\n\nDr. Ramesh Sharma at AIIMS Delhi, who has performed over 8,000 joint replacements, explains that modern implants last 20-25 years and allow patients to return to normal activities including walking, swimming, and cycling.\n\nRecovery involves physiotherapy starting the day after surgery. Most patients walk with support within 24 hours and return home in 5-7 days. Full recovery takes 3-6 months.\n\nCost of knee replacement in India ranges from Rs. 2-4 lakhs, making it significantly more affordable than in Western countries.""",
             get_t("Knee Replacement"), get_d("Dr. Ramesh Sharma"), get_h("AIIMS New Delhi")),
            ("Brain Tumor Treatment: What to Expect",
             "brain-tumor-treatment-guide",
             """A brain tumor diagnosis can be overwhelming, but advances in neurosurgery and oncology have significantly improved outcomes. Understanding the treatment process helps patients and families prepare.\n\nBrain tumors are classified as primary (originating in the brain) or secondary (metastatic). Common types include gliomas, meningiomas, and pituitary adenomas. Treatment depends on tumor type, location, size, and patient health.\n\nSurgery is often the first treatment for accessible tumors. Modern neurosurgery uses advanced techniques including awake craniotomy, intraoperative MRI, and fluorescence-guided surgery to maximize tumor removal while preserving brain function.\n\nDr. Ahmed Khan at AIIMS Delhi, with over 6,000 neurosurgical procedures, explains that minimally invasive approaches have reduced complications and recovery time significantly. Many patients are discharged within 7-10 days.\n\nPost-surgery treatment may include radiation therapy, chemotherapy, or targeted therapy depending on tumor type. Regular MRI monitoring is essential for detecting recurrence.\n\nAt Apollo Hospitals Delhi, our multidisciplinary neuro-oncology team provides comprehensive care from diagnosis through rehabilitation.""",
             get_t("Brain Tumor Removal"), get_d("Dr. Ahmed Khan"), get_h("AIIMS New Delhi")),
            ("Cancer Treatment in India: World-Class Care at Affordable Costs",
             "cancer-treatment-india-guide",
             """India has emerged as a global destination for cancer treatment, offering world-class oncology care at a fraction of the cost compared to Western countries. Leading cancer hospitals like Tata Memorial Hospital and Rajiv Gandhi Cancer Institute provide comprehensive cancer care.\n\nIndia cancer treatment costs are 60-80% lower than in the USA or UK. A chemotherapy cycle that costs $10,000 in the USA costs approximately Rs. 50,000-1,50,000 in India. Radiation therapy, immunotherapy, and targeted therapy are similarly affordable.\n\nDr. Anil Heroor, a leading surgical oncologist at Kokilaben Hospital, notes that Indian oncologists are trained at the best institutions worldwide and use the same protocols as international cancer centers.\n\nModern cancer treatments available in India include immunotherapy with checkpoint inhibitors, CAR-T cell therapy, proton therapy, robotic surgery, and precision medicine based on molecular profiling.\n\nFor international patients, India offers medical visa facilitation, language interpretation, accommodation assistance, and post-treatment follow-up through telemedicine.""",
             get_t("Chemotherapy"), get_d("Dr. Anil Heroor"), get_h("Tata Memorial Hospital")),
            ("Managing Type 2 Diabetes: Diet, Exercise and Medication",
             "type2-diabetes-management-guide",
             """Type 2 diabetes affects over 77 million people in India, making it the diabetes capital of the world. Effective management requires a comprehensive approach combining diet, exercise, and medication.\n\nDiet is the cornerstone of diabetes management. A low glycemic index diet rich in vegetables, whole grains, and lean proteins helps control blood sugar. Avoid refined carbohydrates, sugary drinks, and processed foods. Portion control is essential.\n\nRegular physical activity improves insulin sensitivity and helps control blood sugar. Aim for 150 minutes of moderate exercise weekly including brisk walking, cycling, or swimming. Resistance training is also beneficial.\n\nMedications range from metformin (first-line treatment) to newer agents like SGLT2 inhibitors and GLP-1 agonists that also provide cardiovascular and kidney protection. Insulin therapy may be needed for poorly controlled diabetes.\n\nDr. Sara Kapoor, endocrinologist at AIIMS Delhi, emphasizes that HbA1c below 7% is the target for most patients. Regular monitoring of blood sugar, HbA1c, kidney function, and eye health is essential.\n\nWith proper management, people with type 2 diabetes can live long, healthy lives and prevent complications including kidney disease, blindness, and cardiovascular disease.""",
             get_t("Diabetes Management"), get_d("Dr. Sara Kapoor"), get_h("AIIMS New Delhi")),
            ("Hypothyroidism: Symptoms, Diagnosis and Treatment",
             "hypothyroidism-complete-guide",
             """Hypothyroidism, or underactive thyroid, affects millions of people worldwide, particularly women. The thyroid gland produces insufficient thyroid hormones, slowing down many body functions.\n\nCommon symptoms include fatigue, weight gain, cold intolerance, dry skin, hair loss, constipation, depression, and brain fog. Many people live with undiagnosed hypothyroidism for years.\n\nDiagnosis is confirmed by blood tests measuring TSH (thyroid stimulating hormone) and free T4 levels. TSH above 4.0 mIU/L with low free T4 confirms hypothyroidism. Anti-TPO antibodies indicate Hashimoto thyroiditis, the most common cause.\n\nTreatment with levothyroxine (synthetic T4) is highly effective. The dose is adjusted based on TSH levels measured every 6-8 weeks until stable. Most patients feel significantly better within 2-3 months of starting treatment.\n\nDr. Sara Kapoor at AIIMS Delhi notes that thyroid nodules require ultrasound evaluation and sometimes fine needle aspiration cytology (FNAC) to rule out malignancy. Most nodules are benign.\n\nWith proper treatment, hypothyroidism is completely manageable and patients can lead normal, healthy lives.""",
             get_t("Thyroid Treatment"), get_d("Dr. Sara Kapoor"), get_h("AIIMS New Delhi")),
            ("Liver Cirrhosis: Causes, Symptoms and Treatment Options",
             "liver-cirrhosis-treatment-guide",
             """Liver cirrhosis is a late stage of liver disease where healthy liver tissue is replaced by scar tissue, permanently damaging the liver. It is caused by chronic liver diseases including alcoholic liver disease, hepatitis B and C, and non-alcoholic fatty liver disease.\n\nSymptoms include fatigue, jaundice, abdominal swelling (ascites), easy bruising, confusion, and in advanced cases, liver failure. The Child-Pugh score and MELD score are used to assess severity.\n\nTreatment focuses on treating the underlying cause, managing complications, and preventing further damage. Alcohol abstinence is essential for alcoholic cirrhosis. Antiviral therapy treats hepatitis B and C. Diuretics manage ascites.\n\nDr. Niranjan Kumar, hepatologist at Medanta, explains that liver transplant is the only cure for end-stage liver disease. India has excellent liver transplant programs with success rates comparable to international standards.\n\nAt Medanta The Medicity, the liver transplant team has performed over 1,000 successful liver transplants. The 1-year survival rate exceeds 90%.\n\nEarly diagnosis and treatment can slow progression and prevent complications. Regular monitoring with liver function tests, ultrasound, and endoscopy is essential.""",
             get_t("Liver Transplant"), get_d("Dr. Niranjan Kumar"), get_h("Medanta The Medicity")),
            ("Rhinoplasty in India: What You Need to Know",
             "rhinoplasty-india-guide",
             """Rhinoplasty, or nose reshaping surgery, is one of the most popular cosmetic procedures worldwide. India has become a leading destination for rhinoplasty due to its skilled surgeons, advanced facilities, and affordable costs.\n\nRhinoplasty can address aesthetic concerns (shape, size, symmetry) and functional issues (deviated septum, breathing problems). The procedure can reduce or increase nose size, change the shape of the tip or bridge, narrow nostrils, or change the angle between nose and upper lip.\n\nDr. Rajesh Gupta, plastic surgeon at Apollo Hospitals Delhi, uses advanced 3D imaging to show patients their expected results before surgery. This helps set realistic expectations and plan the procedure precisely.\n\nThe procedure takes 2-3 hours under general anesthesia. Recovery involves swelling and bruising for 2-3 weeks. Final results are visible after 6-12 months when all swelling subsides.\n\nCost of rhinoplasty in India ranges from Rs. 80,000-2,00,000, compared to $8,000-15,000 in the USA. The quality of care and outcomes are comparable to international standards.\n\nChoosing a board-certified plastic surgeon with extensive rhinoplasty experience is crucial for achieving natural-looking results.""",
             get_t("Rhinoplasty"), get_d("Dr. Rajesh Gupta"), get_h("Apollo Hospitals Delhi")),
            ("IVF Treatment: Step by Step Process Explained",
             "ivf-treatment-step-by-step",
             """In vitro fertilization (IVF) is the most effective assisted reproductive technology, helping millions of couples worldwide achieve pregnancy. Understanding the IVF process helps patients prepare mentally and physically.\n\nStep 1 - Ovarian Stimulation: Fertility medications are given for 8-14 days to stimulate the ovaries to produce multiple eggs. Regular monitoring with ultrasound and blood tests tracks follicle development.\n\nStep 2 - Egg Retrieval: Under sedation, eggs are retrieved from the ovaries using a thin needle guided by ultrasound. The procedure takes 20-30 minutes.\n\nStep 3 - Fertilization: Retrieved eggs are fertilized with sperm in the laboratory. ICSI (intracytoplasmic sperm injection) may be used for male factor infertility.\n\nStep 4 - Embryo Culture: Fertilized eggs develop into embryos over 3-5 days in the laboratory. Preimplantation genetic testing (PGT) may be performed to select healthy embryos.\n\nStep 5 - Embryo Transfer: One or two healthy embryos are transferred into the uterus. The procedure is painless and takes 15-20 minutes.\n\nDr. Maria Gonzalez at Apollo Hospitals Delhi reports a success rate of 45-55% per cycle for women under 35. Multiple cycles may be needed.\n\nCost of IVF in India ranges from Rs. 1-2 lakhs per cycle, significantly more affordable than in Western countries.""",
             get_t("IVF Treatment"), get_d("Dr. Maria Gonzalez"), get_h("Apollo Hospitals Delhi")),
            ("LASIK Surgery: Freedom from Glasses and Contact Lenses",
             "lasik-surgery-complete-guide",
             """LASIK (Laser-Assisted In Situ Keratomileusis) is the world most popular refractive surgery, permanently correcting vision problems including myopia, hyperopia, and astigmatism. Over 700,000 LASIK procedures are performed in India annually.\n\nCandidates for LASIK must be at least 18 years old with stable prescription for at least 1 year, adequate corneal thickness, and no significant eye diseases. A comprehensive pre-operative evaluation determines suitability.\n\nThe procedure takes only 15 minutes for both eyes. A thin flap is created in the cornea, laser reshapes the underlying tissue, and the flap is repositioned. Most patients achieve 20/20 vision or better.\n\nDr. Anita Sharma at Sankara Nethralaya, who has performed over 10,000 eye surgeries, explains that modern LASIK using wavefront-guided technology provides superior outcomes with minimal side effects.\n\nRecovery is rapid - most patients see clearly within 24 hours and return to work in 1-2 days. Mild dryness and glare are common initially but resolve within weeks.\n\nCost of LASIK in India ranges from Rs. 25,000-60,000 per eye, compared to $2,000-3,000 per eye in the USA.""",
             get_t("LASIK Surgery"), get_d("Dr. Anita Sharma"), get_h("Sankara Nethralaya")),
            ("Dental Implants: The Permanent Solution for Missing Teeth",
             "dental-implants-complete-guide",
             """Dental implants are the gold standard for replacing missing teeth, providing a permanent, natural-looking solution that functions like real teeth. Unlike dentures or bridges, implants are anchored directly into the jawbone.\n\nA dental implant consists of three parts: a titanium post (implant) surgically placed in the jawbone, an abutment connecting the implant to the crown, and a ceramic crown that looks and functions like a natural tooth.\n\nThe procedure involves multiple stages over 3-6 months. The implant is placed under local anesthesia and allowed to integrate with the bone (osseointegration) over 3-4 months. The crown is then attached.\n\nDr. Preecha Srisuwan at Bumrungrad International Hospital, a leading implantologist, notes that modern implants have a 95-98% success rate over 10 years. Proper oral hygiene and regular dental check-ups ensure longevity.\n\nCost of dental implants in India ranges from Rs. 25,000-50,000 per tooth, compared to $3,000-5,000 in the USA. Thailand and Malaysia also offer competitive pricing for dental tourism.\n\nImplants are suitable for most adults with good general health and adequate bone density. Bone grafting may be needed if bone loss has occurred.""",
             get_t("Dental Implants"), get_d("Dr. Preecha Srisuwan"), get_h("Bumrungrad International Hospital")),
        ]
        for title, slug, content, treatment, doctor, hospital in blogs:
            BlogPost.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "content": content,
                    "treatment": treatment,
                    "doctor": doctor,
                    "hospital": hospital,
                }
            )
        self.stdout.write(f"    {len(blogs)} blog posts done.")

    def _seed_feedbacks(self):
        from feedbacks.models import Feedback
        from doctors.models import Doctor
        from hospitals.models import Hospital
        from treatments.models import Treatment
        self.stdout.write("  Seeding feedbacks...")
        if not hasattr(self, "patient_profiles") or not self.patient_profiles:
            from accounts.models import UserProfile
            self.patient_profiles = list(UserProfile.objects.filter(user_type="patient")[:10])
        if not self.patient_profiles:
            self.stdout.write("    No patient profiles found, skipping feedbacks.")
            return
        def pat(i):
            return self.patient_profiles[i % len(self.patient_profiles)]
        doctor_feedbacks = [
            ("Dr. Naresh Trehan", 5, "Life-saving bypass surgery", "Dr. Trehan performed my bypass surgery with exceptional skill. I was back home in 8 days and feel completely transformed. His team is world-class and the care at Medanta is outstanding. I am forever grateful.", 0),
            ("Dr. Naresh Trehan", 5, "Best cardiac surgeon in India", "After being told I needed bypass surgery, I was terrified. Dr. Trehan explained everything clearly and performed a flawless triple bypass. Six months later I am walking 5km daily. Truly a miracle worker.", 1),
            ("Dr. Naresh Trehan", 5, "Exceptional expertise and care", "My father had a complex cardiac condition that other hospitals refused to operate on. Dr. Trehan took the case and performed a successful surgery. His expertise is unmatched in India.", 2),
            ("Dr. Devi Shetty", 5, "Affordable world-class cardiac care", "Dr. Devi Shetty performed my heart valve replacement at a fraction of what it would cost abroad. The quality of care at Narayana Health is exceptional. He is truly making healthcare accessible.", 3),
            ("Dr. Devi Shetty", 5, "Compassionate and brilliant surgeon", "Dr. Shetty operated on my mother who had a complex congenital heart defect. His compassion and surgical skill are extraordinary. The entire team at Narayana Health was wonderful.", 4),
            ("Dr. Priya Patel", 5, "Excellent cardiologist", "Dr. Priya Patel diagnosed my hypertension and coronary artery disease early. Her treatment plan has completely controlled my blood pressure. She is thorough, caring, and always available for questions.", 5),
            ("Dr. Priya Patel", 4, "Very knowledgeable and caring", "I had an angioplasty done by Dr. Patel. The procedure was smooth and recovery was quick. She explained every step clearly. Highly recommend her for cardiac issues.", 6),
            ("Dr. Ramesh Sharma", 5, "Knee replacement changed my life", "I suffered from severe knee arthritis for 10 years. Dr. Ramesh Sharma performed bilateral knee replacement and I am now pain-free. His surgical precision is remarkable. I can walk, climb stairs, and even dance!", 7),
            ("Dr. Ramesh Sharma", 5, "Outstanding orthopedic surgeon", "Dr. Sharma performed my hip replacement using computer-assisted surgery. The alignment is perfect and recovery was faster than expected. I was walking without support in 3 weeks.", 8),
            ("Dr. Ramesh Sharma", 4, "Highly skilled and professional", "My spinal fusion surgery by Dr. Sharma was a complete success. The chronic back pain I had for 7 years is gone. His team is professional and the post-operative care was excellent.", 9),
            ("Dr. Smith Singh", 5, "Expert in sports injuries", "Dr. Smith Singh performed my ACL reconstruction after a sports injury. His expertise in arthroscopic surgery is exceptional. I returned to playing cricket within 6 months.", 0),
            ("Dr. Smith Singh", 4, "Great orthopedic surgeon", "Had my knee arthroscopy done by Dr. Singh. Minimally invasive procedure with quick recovery. He is very patient in explaining the condition and treatment options.", 1),
            ("Dr. Ahmed Khan", 5, "Brilliant neurosurgeon", "Dr. Ahmed Khan removed a brain tumor that other surgeons said was inoperable. His skill and courage saved my life. The surgery was 8 hours long and he performed it flawlessly. I am forever in his debt.", 2),
            ("Dr. Ahmed Khan", 5, "Life-changing DBS surgery", "My father had severe Parkinson disease. Dr. Khan performed deep brain stimulation surgery and the improvement is miraculous. He can now walk, eat, and live independently. Dr. Khan is a true hero.", 3),
            ("Dr. Ahmed Khan", 5, "Best neurosurgeon in India", "After my stroke, I had significant neurological deficits. Dr. Khan performed spinal cord surgery and supervised my rehabilitation. His expertise and dedication are unparalleled.", 4),
            ("Dr. Paresh Doshi", 5, "World-class DBS specialist", "Dr. Doshi performed deep brain stimulation for my essential tremor. The results are incredible - my tremors have reduced by 90%. He is one of the best DBS surgeons in the world.", 5),
            ("Dr. Anil Heroor", 5, "Exceptional cancer surgeon", "Dr. Heroor performed robotic surgery for my colon cancer. The procedure was minimally invasive and I was discharged in 4 days. He is a master of robotic oncological surgery.", 6),
            ("Dr. Anil Heroor", 5, "Saved my life from lung cancer", "Diagnosed with stage 3 lung cancer, I was devastated. Dr. Heroor designed a comprehensive treatment plan and performed surgery followed by chemotherapy. I am now in remission.", 7),
            ("Dr. Sara Kapoor", 5, "Best endocrinologist I have met", "Dr. Sara Kapoor has been managing my Type 2 diabetes for 3 years. My HbA1c has come down from 11% to 6.8% under her care. She is thorough, empathetic, and always up-to-date with latest treatments.", 8),
            ("Dr. Sara Kapoor", 5, "Excellent thyroid specialist", "I had Hashimoto thyroiditis with a suspicious nodule. Dr. Kapoor managed my case expertly - the nodule turned out benign and my thyroid levels are now perfectly controlled.", 9),
            ("Dr. Niranjan Kumar", 5, "Outstanding gastroenterologist", "Dr. Niranjan Kumar diagnosed my liver cirrhosis early and put me on the right treatment. His expertise in hepatology is exceptional. He is always available and explains everything clearly.", 0),
            ("Dr. Niranjan Kumar", 4, "Very skilled endoscopist", "Had a colonoscopy and endoscopy done by Dr. Kumar. The procedures were smooth and painless. He found and removed polyps that could have become cancerous. Excellent preventive care.", 1),
            ("Dr. Arjun Mehta", 5, "Wonderful general physician", "Dr. Arjun Mehta has been my family doctor for 5 years. He is thorough, caring, and always takes time to explain. His management of my diabetes and hypertension has been excellent.", 2),
            ("Dr. Rajesh Gupta", 5, "Natural-looking rhinoplasty", "Dr. Rajesh Gupta performed my rhinoplasty and the results are absolutely natural. He understood exactly what I wanted and delivered beyond my expectations. His artistic eye is remarkable.", 3),
            ("Dr. Rajesh Gupta", 5, "Excellent hair transplant results", "I had FUE hair transplant by Dr. Gupta. 18 months later, the results are amazing - full, natural-looking hair. His technique is precise and the hairline design is perfect.", 4),
            ("Dr. Maria Gonzalez", 5, "Made our dream come true", "After 5 years of trying to conceive, Dr. Maria Gonzalez helped us achieve pregnancy through IVF. She is compassionate, knowledgeable, and supported us through every step. We now have a beautiful baby girl.", 5),
            ("Dr. Maria Gonzalez", 5, "Best fertility specialist", "Dr. Gonzalez performed ICSI for my husband severe male factor infertility. On the second cycle, we achieved pregnancy. Her expertise and emotional support made a difficult journey bearable.", 6),
            ("Dr. Deepak Mehta", 5, "Expert lung cancer treatment", "Dr. Deepak Mehta treated my stage 3 lung cancer with a combination of chemotherapy and immunotherapy. I am now in complete remission. His expertise in thoracic oncology is world-class.", 7),
            ("Dr. Anita Sharma", 5, "Perfect LASIK results", "Dr. Anita Sharma performed LASIK on both my eyes. I had -6.5 power and now have 20/20 vision. The procedure was painless and I was seeing clearly the next morning. Life-changing!", 8),
            ("Dr. Preecha Srisuwan", 5, "Excellent dental implants", "Dr. Preecha placed 4 dental implants for me at Bumrungrad. The procedure was painless and the implants look and feel exactly like natural teeth. His skill and attention to detail are exceptional.", 9),
        ]
        count = 0
        for dname, rating, title, comment, pat_idx in doctor_feedbacks:
            doctor = Doctor.objects.filter(name=dname).first()
            if doctor:
                Feedback.objects.get_or_create(
                    patient=pat(pat_idx),
                    doctor=doctor,
                    title=title,
                    defaults={
                        "feedback_type": "doctor",
                        "rating": rating,
                        "comment": comment,
                        "is_approved": True,
                    }
                )
                count += 1
        hospital_feedbacks = [
            ("Apollo Hospitals Delhi", 5, "World-class hospital", "Apollo Hospitals Delhi is truly world-class. The facilities are excellent, staff is professional and caring, and the medical care is outstanding. I came from the UK for my knee replacement and could not be happier.", 0),
            ("Apollo Hospitals Delhi", 5, "Best hospital in India", "From admission to discharge, every aspect of care at Apollo Delhi was exceptional. The doctors, nurses, and support staff all work seamlessly as a team. The hospital is clean, modern, and well-organized.", 1),
            ("Apollo Hospitals Delhi", 4, "Excellent facilities and care", "Had my cardiac procedure at Apollo Delhi. The cath lab is state-of-the-art and the cardiac team is highly skilled. The only minor issue was waiting time for some tests.", 2),
            ("Fortis Memorial Research Institute", 5, "Outstanding hospital", "Fortis FMRI is one of the best hospitals I have visited. The infrastructure is world-class, doctors are highly qualified, and the nursing care is excellent. My bypass surgery here was a complete success.", 3),
            ("Fortis Memorial Research Institute", 4, "Very good hospital", "Had my knee replacement at Fortis FMRI. The orthopedic team is excellent and the physiotherapy department is outstanding. Recovery was smooth and well-supported.", 4),
            ("AIIMS New Delhi", 5, "India premier medical institution", "AIIMS Delhi is in a class of its own. The doctors are among the best in the world and the research-driven approach to treatment is evident. Despite being a government hospital, the care quality is exceptional.", 5),
            ("AIIMS New Delhi", 5, "Excellent care at affordable cost", "My brain tumor surgery at AIIMS was performed by Dr. Ahmed Khan with exceptional skill. The cost was a fraction of private hospitals. AIIMS proves that excellent healthcare need not be expensive.", 6),
            ("Medanta The Medicity", 5, "Truly world-class hospital", "Medanta is a world-class hospital in every sense. The infrastructure rivals the best hospitals globally, the doctors are internationally trained, and the patient care is exceptional. My cardiac surgery here was flawless.", 7),
            ("Tata Memorial Hospital", 5, "Best cancer hospital in India", "Tata Memorial Hospital is India best cancer hospital. The oncology team is world-class, the treatment protocols are evidence-based, and the support services are excellent. My cancer treatment here gave me a second chance at life.", 8),
            ("Bumrungrad International Hospital", 5, "Best hospital in Asia", "Bumrungrad is truly the best hospital in Asia. The facilities are luxurious, the doctors are internationally trained, and the service is impeccable. My dental treatment here was perfect.", 9),
            ("Sankara Nethralaya", 5, "Best eye hospital in India", "Sankara Nethralaya is the gold standard for eye care in India. Dr. Anita Sharma performed my LASIK with perfect results. The hospital is dedicated entirely to eye care and the expertise shows.", 0),
            ("Kokilaben Dhirubhai Ambani Hospital", 5, "Excellent hospital", "Kokilaben Hospital is one of Mumbai best hospitals. The robotic surgery facilities are state-of-the-art and the oncology team is excellent. My cancer surgery here was performed with minimal invasiveness.", 1),
        ]
        for hname, rating, title, comment, pat_idx in hospital_feedbacks:
            hospital = Hospital.objects.filter(name=hname).first()
            if hospital:
                Feedback.objects.get_or_create(
                    patient=pat(pat_idx),
                    hospital=hospital,
                    title=title,
                    defaults={
                        "feedback_type": "hospital",
                        "rating": rating,
                        "comment": comment,
                        "is_approved": True,
                    }
                )
                count += 1
        treatment_feedbacks = [
            ("Knee Replacement", 5, "Pain-free life after knee replacement", "After 10 years of knee pain, my total knee replacement has given me a completely pain-free life. I can walk, climb stairs, and even play with my grandchildren. The procedure was smooth and recovery was well-supported.", 2),
            ("Knee Replacement", 5, "Excellent outcome", "My bilateral knee replacement was performed with computer-assisted technology. The alignment is perfect and both knees feel completely natural. I am back to my normal activities within 4 months.", 3),
            ("Bypass Surgery (CABG)", 5, "Life-saving surgery", "My triple bypass surgery was performed flawlessly. I was back home in 8 days and feel 20 years younger. The cardiac team was exceptional throughout.", 4),
            ("Chemotherapy", 4, "Effective treatment with good support", "My chemotherapy for breast cancer was well-managed. The oncology team monitored me closely and managed side effects effectively. I completed 6 cycles and am now in remission.", 5),
            ("IVF Treatment", 5, "IVF gave us our miracle baby", "After 4 failed IUI cycles, IVF worked on the first attempt. The fertility team was supportive throughout the emotional journey. We now have a healthy baby boy.", 6),
            ("Brain Tumor Removal", 5, "Successful tumor removal", "My meningioma was successfully removed with no neurological deficits. The neurosurgery team was exceptional. I was discharged in 10 days and have made a complete recovery.", 7),
            ("Diabetes Management", 5, "Excellent diabetes care program", "The diabetes management program at Apollo has transformed my health. My HbA1c has come down from 10% to 6.5% in 6 months. The dietitian, educator, and doctor work as a team.", 8),
            ("LASIK Surgery", 5, "Perfect vision after LASIK", "I had -7.0 myopia and now have 20/20 vision after LASIK. The procedure took 15 minutes and I was seeing clearly the next day. Best decision I ever made.", 9),
            ("Liver Transplant", 5, "Liver transplant saved my life", "I had end-stage liver disease and was given 6 months to live. The liver transplant team at Medanta performed a successful living donor transplant. I am now 2 years post-transplant and living a normal life.", 0),
            ("Rhinoplasty", 5, "Natural-looking results", "My rhinoplasty results are absolutely natural. The surgeon understood my aesthetic goals perfectly. The swelling resolved in 3 months and the final result is exactly what I wanted.", 1),
            ("Dental Implants", 5, "Implants feel like natural teeth", "I had 3 dental implants placed and they feel completely natural. The procedure was done in stages over 4 months. The final crowns match my natural teeth perfectly.", 2),
            ("Thyroid Treatment", 5, "Thyroid condition well-managed", "My Hashimoto thyroiditis is now perfectly controlled with levothyroxine. The endocrinologist monitored my levels carefully and adjusted the dose until optimal. I feel completely normal now.", 3),
        ]
        for tname, rating, title, comment, pat_idx in treatment_feedbacks:
            treatment = Treatment.objects.filter(name=tname).first()
            if treatment:
                Feedback.objects.get_or_create(
                    patient=pat(pat_idx),
                    treatment=treatment,
                    title=title,
                    defaults={
                        "feedback_type": "treatment",
                        "rating": rating,
                        "comment": comment,
                        "is_approved": True,
                    }
                )
                count += 1
        self.stdout.write(f"    {count} feedbacks done.")

    def _update_ratings(self):
        from feedbacks.models import Feedback
        from doctors.models import Doctor
        from hospitals.models import Hospital
        from django.db.models import Avg, Count
        self.stdout.write("  Updating ratings...")
        for doctor in Doctor.objects.all():
            agg = Feedback.objects.filter(doctor=doctor, is_approved=True).aggregate(avg=Avg("rating"), cnt=Count("id"))
            if agg["avg"]:
                doctor.rating = round(agg["avg"], 2)
                doctor.review_count = agg["cnt"]
                doctor.save(update_fields=["rating", "review_count"])
        for hospital in Hospital.objects.all():
            agg = Feedback.objects.filter(hospital=hospital, is_approved=True).aggregate(avg=Avg("rating"), cnt=Count("id"))
            if agg["avg"]:
                hospital.rating = round(agg["avg"], 2)
                hospital.save(update_fields=["rating"])
        self.stdout.write("    Ratings updated.")
