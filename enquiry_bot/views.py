from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
import json
import requests
import urllib.parse
from PIL import Image
import base64
from io import BytesIO
from .models import Enquiry, FAQ, ChatMessage


def enquiry_bot_view(request):
    """Main view for the enquiry bot"""
    faqs = FAQ.objects.filter(is_active=True)[:10]  # Show top 10 FAQs
    recent_enquiries = Enquiry.objects.filter(user=request.user) if request.user.is_authenticated else []
    
    context = {
        'faqs': faqs,
        'recent_enquiries': recent_enquiries,
    }
    return render(request, 'enquiry_bot/bot_interface.html', context)


@csrf_exempt
def chat_message_api(request):
    """API endpoint to handle chat messages"""
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        enquiry_id = data.get('enquiry_id')
        
        # Get or create enquiry
        if enquiry_id:
            enquiry = get_object_or_404(Enquiry, id=enquiry_id)
        else:
            # Create new enquiry if not provided
            enquiry = Enquiry.objects.create(
                name=request.user.username if request.user.is_authenticated else "Guest",
                email=request.user.email if request.user.is_authenticated else "",
                subject="Chat Inquiry",
                message=user_message
            )
        
        # Save user message
        ChatMessage.objects.create(
            enquiry=enquiry,
            sender_type='user',
            message=user_message
        )
        
        # Check if the message contains request for medical report analysis
        if any(keyword in user_message.lower() for keyword in ['medical report', 'analyze report', 'upload report', 'report analysis']):
            bot_response = "You can upload your medical report for analysis. I'll analyze it and provide information about precautions, treatments, effects, and side effects. Please use the upload button in the interface to share your report."
        else:
            # Generate bot response based on the message
            bot_response = generate_bot_response(user_message, enquiry)
        
        # Save bot response
        bot_message = ChatMessage.objects.create(
            enquiry=enquiry,
            sender_type='bot',
            message=bot_response
        )
        
        return JsonResponse({
            'success': True,
            'response': bot_response,
            'enquiry_id': enquiry.id,
            'timestamp': bot_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def generate_bot_response(message, enquiry):
    """Generate enhanced bot response based on user message and website information"""
    message_lower = message.lower().strip()
    
    # Handle numeric inputs by mapping them to common topics
    if message.isdigit():
        num = int(message)
        if num == 1:
            return "TakeOpinion offers a comprehensive healthcare platform with these services:\n\n• Doctor consultations and profiles with detailed information\n• Hospital information and booking with comparisons\n• Medical treatment details with success rates and costs\n• Appointment scheduling and management\n• Patient portal with medical history tracking\n• Feedback and review system\n• Medical tourism support including hotel booking\n• Secure payment integration\n\nWhat specific service would you like to know more about?"
        elif num == 2:
            return "You can search for treatments, doctors, and hospitals that match your needs using our platform. Enter specific medical conditions, doctor specializations, or hospital locations to find the best options."
        elif num == 3:
            return "Booking appointments on TakeOpinion is simple:\n\n1. Search for doctors or hospitals\n2. Select your preferred date and time\n3. Fill in your details\n4. Confirm your booking\n5. Receive confirmation via email/SMS\n\nYou can also manage your appointments, reschedule, or cancel through your patient portal."
        elif num == 4:
            return "I can help you analyze medical reports. Please use the upload button in the bot interface to upload your medical report (PDF, JPG, JPEG, PNG, GIF) for comprehensive analysis. I'll extract information about precautions, treatments, effects, and suggest relevant doctors."
        elif num == 5:
            return "TakeOpinion specializes in medical tourism, helping international patients access quality healthcare. We offer special packages including doctor appointments, hospital stays, hotel accommodations, and local support services."
        elif num == 6:
            return "Our platform offers comprehensive health checkup packages for preventive care. We have various packages tailored to different age groups and health needs. You can book health checkups directly through our platform and get recommendations based on your age and medical history."
        elif num == 7:
            return "We provide 24/7 customer support through multiple channels:\n\n• Email: support@takeopinion.com\n• Phone: +91-XXX-XXX-XXXX\n• Live chat: Available on our website\n• WhatsApp: Coming soon\n\nOur support team is trained to assist with medical queries, appointment scheduling, and platform navigation."
        elif num == 8:
            return "TakeOpinion ensures your medical data security with advanced encryption and privacy measures:\n\n• End-to-end encryption for all communications\n• HIPAA compliant data storage\n• Strict access controls and authentication\n• Regular security audits and updates\n• GDPR compliance for international users\n\nYour medical information is never shared without explicit consent."
        elif num == 9:
            return "We offer specialized services for international patients:\n\n• Medical visa assistance\n• Airport pickup and drop\n• Language interpretation services\n• Hotel and accommodation arrangements\n• City tour and local support\n• Follow-up care coordination\n\nOur medical tourism package includes comprehensive support throughout your treatment journey."
        elif num == 10:
            return "TakeOpinion provides insurance and financing options:\n\n• Insurance claim assistance\n• EMI options for major treatments\n• Healthcare credit lines\n• Partnership with leading insurers\n• Transparent cost breakdowns\n\nWe aim to make quality healthcare accessible to everyone regardless of financial constraints."
        else:
            return "I'm your TakeOpinion assistant. I can help you with:\n• Finding hospitals, doctors, and treatments\n• Analyzing medical reports (upload using the button)\n• Getting information about pricing and support\n• Booking appointments and consultations\n• Learning about our medical tourism services\nWhat would you like to know?"
    
    # Define responses based on common inquiries about the website
    if 'hello' in message_lower or 'hi' in message_lower or 'hey' in message_lower:
        return "Hello! I'm your TakeOpinion assistant. I can help you with:\n• Finding hospitals, doctors, and treatments\n• Analyzing medical reports (upload using the button)\n• Getting information about pricing and support\n• Booking appointments and consultations\n• Learning about our medical tourism services\nWhat would you like to know?"
    
    elif 'health checkup' in message_lower or 'checkup' in message_lower or 'preventive' in message_lower:
        return "TakeOpinion offers comprehensive health checkup packages for preventive care. We have various packages tailored to different age groups and health needs:\n\n• Basic Health Screening\n• Executive Health Checkup\n• Comprehensive Cardiac Package\n• Women's Wellness Package\n• Senior Citizen Package\n\nYou can book health checkups directly through our platform and get recommendations based on your age and medical history. Early detection helps in preventing serious health issues."
    
    elif 'insurance' in message_lower or 'finance' in message_lower or 'emi' in message_lower:
        return "TakeOpinion provides various insurance and financing options to make healthcare accessible:\n\n• Insurance claim assistance for cashless treatments\n• EMI options for major treatments with flexible repayment\n• Healthcare credit lines with competitive interest rates\n• Partnership with leading insurers like HDFC ERGO, ICICI Lombard, Star Health\n• Transparent cost breakdowns with no hidden charges\n\nWe believe quality healthcare should be accessible to everyone regardless of financial constraints. Contact our support team for more information on financing options."
    
    elif 'security' in message_lower or 'privacy' in message_lower or 'data' in message_lower:
        return "TakeOpinion takes your medical data security seriously with these measures:\n\n• End-to-end encryption for all communications\n• HIPAA compliant data storage and handling\n• Strict access controls and multi-factor authentication\n• Regular security audits and penetration testing\n• GDPR compliance for international users\n• Data anonymization for research purposes\n\nYour medical information is never shared without explicit consent. We follow industry best practices to protect your privacy."
    
    elif 'support' in message_lower or 'help' in message_lower or 'contact' in message_lower:
        return "TakeOpinion offers 24/7 customer support through multiple channels:\n\n• Email: support@takeopinion.com\n• Phone: +91-XXX-XXX-XXXX (Available 24/7)\n• Live chat: Available on our website\n• WhatsApp: Coming soon\n• Help Center: Detailed articles and tutorials\n\nOur support team is trained to assist with medical queries, appointment scheduling, platform navigation, and post-treatment care. We aim to respond to all queries within 2 hours."
    
    elif 'international' in message_lower or 'tourism' in message_lower or 'visa' in message_lower or 'travel' in message_lower:
        return "TakeOpinion provides specialized services for international patients:\n\n• Medical visa assistance and documentation\n• Airport pickup and drop services\n• Language interpretation and translation\n• Hotel and accommodation arrangements\n• City tour and local support\n• Currency exchange guidance\n• Follow-up care coordination\n\nOur medical tourism package includes comprehensive support throughout your treatment journey. We partner with leading hospitals and hotels to ensure a comfortable experience."
    
    elif 'appointment' in message_lower or 'slot' in message_lower or 'schedule' in message_lower:
        return "Our appointment scheduling system is designed for convenience:\n\n• Online booking with real-time availability\n• Option to reschedule or cancel appointments\n• Automated reminders via SMS and email\n• Video consultation options available\n• Priority booking for returning patients\n• Emergency appointment slots reserved\n\nYou can manage all your appointments through your patient dashboard. We recommend booking at least 24 hours in advance for non-emergency consultations."

    elif 'service' in message_lower or 'feature' in message_lower:
        response = "TakeOpinion offers a comprehensive healthcare platform with these services:\n\n• Doctor consultations and profiles with detailed information\n• Hospital information and booking with comparisons\n• Medical treatment details with success rates and costs\n• Appointment scheduling and management\n• Patient portal with medical history tracking\n• Feedback and review system\n• Medical tourism support including hotel booking\n• Secure payment integration\n\nWhat specific service would you like to know more about?"
        if any(word in message_lower for word in ['medical tourism', 'tourism', 'international']):
            response += "\n\nFor medical tourism, we offer special packages including doctor appointments, hospital stays, hotel accommodations, and local support services."
        return response

    elif any(word in message_lower for word in ['doctor', 'doctors', 'expert', 'experts', 'physician', 'physicians']):
        response = "Our platform provides detailed doctor profiles with qualifications, specialties, experience, awards, languages spoken, and patient reviews."
        if any(word in message_lower for word in ['search', 'find', 'locate']):
            response += " You can search for doctors by specialty, location, hospital affiliation, or experience."
        elif any(word in message_lower for word in ['book', 'appointment', 'consult', 'consultation']):
            response += " You can book consultations directly through our system."
        elif any(word in message_lower for word in ['orthopedic', 'orthopaedic', 'knee', 'bone', 'joint']):
            response += " Our orthopedic surgeons include specialists in joint replacement and bone procedures."
        elif any(word in message_lower for word in ['neuro', 'brain', 'nervous']):
            response += " Our neurosurgeons specialize in brain and nervous system procedures."
        elif any(word in message_lower for word in ['cardio', 'heart']):
            response += " Our cardiologists and cardiac surgeons specialize in heart procedures."
        elif any(word in message_lower for word in ['pediatric', 'child']):
            response += " Our pediatric surgeons specialize in children's procedures."
        response += " Would you like to know how to search for doctors or book a consultation?"
        return response

    elif any(word in message_lower for word in ['hospital', 'hospitals', 'medical facility', 'facilities']):
        response = "We offer comprehensive hospital information including facilities, specialties, awards, patient reviews, and booking options."
        if any(word in message_lower for word in ['search', 'find', 'locate']):
            response += " You can search for hospitals by location, specialty, or specific treatments offered."
        elif any(word in message_lower for word in ['compare', 'comparison']):
            response += " Our platform provides hospital comparisons to help you make informed decisions."
        if any(word in message_lower for word in ['near', 'closest', 'location', 'find']):
            response += " You can explore hospitals by location and specialty through our platform."
        response += " Our verified hospitals include MediCare Heart Institute, OrthoPlus Joint Center, and Indraprastha Apollo Hospitals."
        return response

    elif 'booking' in message_lower or 'appointment' in message_lower:
        response = "Booking appointments on TakeOpinion is simple:\n\n1. Search for doctors or hospitals\n2. Select your preferred date and time\n3. Fill in your details\n4. Confirm your booking\n5. Receive confirmation via email/SMS\n\nYou can also manage your appointments, reschedule, or cancel through your patient portal."
        if any(word in message_lower for word in ['medical tourism', 'tourism', 'international']):
            response += " For medical tourists, we can also arrange hotel bookings and local support services."
        return response

    elif any(word in message_lower for word in ['treatment', 'treatments', 'procedure', 'procedures']):
        response = "Our platform provides detailed information about various medical treatments including:\n\n• Treatment procedures and protocols\n• Cost estimates\n• Recovery time\n• Risks and benefits\n• Success rates\n• Doctor recommendations\n\nYou can browse treatments by category or search for specific procedures."
        if any(word in message_lower for word in ['orthopedic', 'knee', 'joint']):
            response += " Our orthopedic treatments include knee replacement, joint repair, and other bone/joint procedures."
        elif any(word in message_lower for word in ['cosmetic', 'aesthetic', 'plastic']):
            response += " Our cosmetic treatments include rhinoplasty, facelifts, and other aesthetic procedures."
        elif any(word in message_lower for word in ['ayurveda', 'ayurvedic']):
            response += " Our Ayurvedic treatments include Panchakarma and traditional healing methods."
        elif any(word in message_lower for word in ['surgery', 'surgical']):
            response += " Our surgical treatments cover various specialties with expert surgeons."
        return response

    elif 'price' in message_lower or 'cost' in message_lower or 'payment' in message_lower:
        response = "TakeOpinion integrates secure payment gateways including Razorpay and Stripe for convenient transactions. We offer transparent pricing with our best price guarantee. Payment options include credit/debit cards, net banking, UPI, and wallets."
        if any(word in message_lower for word in ['discount', 'offer', 'deal']):
            response += " We also offer special packages and discounts for medical tourism."
        response += " For detailed pricing of specific services, please contact our support team or check the respective service page."
        return response

    elif 'contact' in message_lower or 'support' in message_lower:
        response = "For immediate assistance:\n\n• Email: support@takeopinion.com\n• Phone: +91-XXX-XXX-XXXX\n• Live chat: Available on our website\n• Support hours: 24/7\n\nYou can also submit an enquiry through our form, and our team will get back to you within 24 hours."
        if any(word in message_lower for word in ['language', 'multilingual', 'translate']):
            response += "\n\nWe provide multilingual support to ensure clear communication with medical professionals."
        return response

    elif 'about' in message_lower or 'company' in message_lower:
        response = "TakeOpinion is your trusted partner for medical travel and treatment decisions. We connect you with verified experts, provide best price guarantee, and offer 24/7 support."
        if any(word in message_lower for word in ['process', 'work', 'how']):
            response += " Our process includes search, consult, booking, and recovery support."
        elif any(word in message_lower for word in ['medical tourism', 'tourism']):
            response += " We specialize in medical tourism, helping international patients access quality healthcare."
        return response

    elif 'review' in message_lower or 'feedback' in message_lower:
        return "We value patient feedback greatly! You can submit reviews and feedback for doctors, hospitals, and treatments you've experienced. Your feedback helps other patients make informed decisions and helps healthcare providers improve their services. To submit feedback, visit the respective profile or service page and click on the 'Submit Review' button."

    elif 'faq' in message_lower or 'help' in message_lower:
        faqs = FAQ.objects.filter(is_active=True)[:3]  # Get top 3 FAQs
        faq_text = "Here are some frequently asked questions:\n\n"
        for faq in faqs:
            faq_text += f"Q: {faq.question}\nA: {faq.answer}\n\n"
        return faq_text + "If you have more specific questions, please ask me directly!"

    elif 'login' in message_lower or 'register' in message_lower or 'account' in message_lower:
        return "To access personalized features:\n\n1. Click on 'Sign Up' to create an account\n2. Verify your email address\n3. Complete your profile\n4. Access your dashboard to manage appointments, medical records, and preferences\n\nRegistered users can book appointments, view medical history, receive personalized recommendations, and track their health journey."

    elif 'thank' in message_lower:
        return "You're welcome! Is there anything else I can help you with today?"

    elif any(word in message_lower for word in ['medical report', 'analyze', 'pdf', 'report', 'analysis', 'scan', 'upload', 'medical file']):
        return "I can help you analyze medical reports. Please use the upload button in the bot interface to upload your medical report (PDF, JPG, JPEG, PNG, GIF) for comprehensive analysis. I'll extract information about precautions, treatments, effects, and suggest relevant doctors."

    elif any(word in message_lower for word in ['search', 'find', 'locate']):
        return "You can search for treatments, doctors, and hospitals that match your needs using our platform. Enter specific medical conditions, doctor specializations, or hospital locations to find the best options."

    elif 'suggest' in message_lower and ('doctor' in message_lower or 'doctors' in message_lower):
        # Check if there are previous medical report analysis messages in the conversation
        # This is a simplified approach - in a real system, you'd have more sophisticated context tracking
        all_messages = ChatMessage.objects.filter(enquiry=enquiry).order_by('-timestamp')[:10]  # Last 10 messages
        has_medical_analysis = False
        
        for msg in all_messages:
            if 'Medical Report Analysis:' in msg.message or any(keyword in msg.message.lower() for keyword in ['hypertension', 'diabetes', 'cardiac', 'heart', 'cancer', 'treatment plan', 'medication', 'consultation']):
                has_medical_analysis = True
                break
        
        if has_medical_analysis:
            return "Based on your previous medical report analysis, I recommend consulting with specialists relevant to your conditions. You can book appointments with cardiologists, endocrinologists, or other specialists as indicated in your report. Our platform shows doctor profiles with qualifications, experience, and patient reviews to help you choose the right specialist."
        else:
            return "I can suggest doctors based on your medical needs. If you've uploaded a medical report, I can recommend specialists relevant to your condition. Otherwise, you can search for doctors by specialty, location, or hospital affiliation through our platform. Our doctors are verified professionals with detailed profiles showing qualifications, experience, and patient reviews."

    elif any(word in message_lower for word in ['book', 'appointment', 'schedule']):
        return "You can book appointments with the best doctors and hospitals through our platform. Our booking system helps you find available slots and complete the reservation process seamlessly."

    elif any(word in message_lower for word in ['recover', 'recovery', 'after', 'post']):
        return "We provide world-class treatment and comprehensive post-care support to ensure your complete recovery. Our support continues even after your procedure is completed."

    else:
        # Default response with more specific help options
        return "I'm your TakeOpinion assistant. I can help you with:\n• Finding hospitals, doctors, and treatments\n• Analyzing medical reports (upload using the button)\n• Getting information about pricing and support\n• Booking appointments and consultations\n• Learning about our medical tourism services\nWhat would you like to know?"


def submit_enquiry(request):
    """Handle enquiry submission"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Validate required fields
        if not name or not email or not subject or not message:
            # Return specific error about which field is missing
            missing_fields = []
            if not name:
                missing_fields.append('Name')
            if not email:
                missing_fields.append('Email')
            if not subject:
                missing_fields.append('Subject')
            if not message:
                missing_fields.append('Message')
            
            return JsonResponse({
                'success': False,
                'error': f'The following required fields are missing: {", ".join(missing_fields)}'
            })
        
        enquiry = Enquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        
        # Create initial bot response
        ChatMessage.objects.create(
            enquiry=enquiry,
            sender_type='bot',
            message="Thank you for your enquiry! Our support team will review your query and get back to you within 24 hours. In the meantime, I can answer common questions about our platform. Feel free to ask anything!"
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Your enquiry has been submitted successfully!',
            'enquiry_id': enquiry.id
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def get_chat_history(request, enquiry_id):
    """Get chat history for a specific enquiry"""
    enquiry = get_object_or_404(Enquiry, id=enquiry_id)
    messages = ChatMessage.objects.filter(enquiry=enquiry).order_by('timestamp')
    
    chat_data = []
    for msg in messages:
        chat_data.append({
            'sender': msg.sender_type,
            'message': msg.message,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return JsonResponse({
        'success': True,
        'messages': chat_data,
        'enquiry_status': enquiry.status
    })


def analyze_medical_report(request):
    """Analyze uploaded medical report using local processing"""
    if request.method == 'POST' and request.FILES.get('medical_report'):
        medical_report = request.FILES['medical_report']
        
        # For non-image files like PDF, we'll extract text first
        file_content = medical_report.read()
        
        if medical_report.content_type == 'application/pdf':
            # Extract text from PDF
            import PyPDF2
            from io import BytesIO
            
            try:
                pdf_file = BytesIO(file_content)
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                pdf_text = ""
                for page in pdf_reader.pages:
                    pdf_text += page.extract_text() + "\n"
            except Exception as e:
                pdf_text = "Error extracting text from PDF: " + str(e)
        elif medical_report.content_type.startswith('image'):
            # For image files, we need to handle differently
            # For local processing, we'll use a simple placeholder
            encoded_content = base64.b64encode(file_content).decode('utf-8')
            pdf_text = f"Image file received (type: {medical_report.content_type}). Local processing applied."
        else:
            # For other text-based files
            pdf_text = file_content.decode('utf-8', errors='ignore')
        
        # Local analysis using rule-based approach
        analysis = local_medical_analysis(pdf_text)
        
        # Process the analysis to suggest relevant doctors
        suggested_doctors = []
        
        # Improved doctor matching based on medical conditions
        # Extract key terms from the analysis to match with doctor specializations
        analysis_lower = analysis.lower()
        
        from doctors.models import Doctor
        from django.db.models import Q
        
        # Match based on conditions found in the analysis
        # First, check if any specific conditions are mentioned in the analysis
        matched_condition = False
        
        if any(word in analysis_lower for word in ['heart', 'cardiac', 'cardiology', 'cardiovascular', 'cardiac surgery', 'hypertension', 'blood pressure']):
            # Find cardiologists
            doctor_queryset = Doctor.objects.prefetch_related('hospitals').filter(
                Q(specialization__icontains='cardiology') | Q(specialization__icontains='cardiac') | Q(specialization__icontains='cardiovascular') | Q(specialization__icontains='heart')
            )[:3]
            matched_condition = True
        elif any(word in analysis_lower for word in ['brain', 'neuro', 'nervous', 'neurology', 'neurosurgery', 'psychiatry']):
            # Find neurologists/neurosurgeons/psychiatrists
            doctor_queryset = Doctor.objects.prefetch_related('hospitals').filter(
                Q(specialization__icontains='neurology') | Q(specialization__icontains='neurosurgery') | Q(specialization__icontains='psychiatry')
            )[:3]
            matched_condition = True
        elif any(word in analysis_lower for word in ['bone', 'joint', 'orthopedic', 'orthopaedic', 'orthopedics', 'arthritis']):
            # Find orthopedic surgeons
            doctor_queryset = Doctor.objects.prefetch_related('hospitals').filter(
                Q(specialization__icontains='orthopedic') | Q(specialization__icontains='orthopaedic') | Q(specialization__icontains='joint')
            )[:3]
            matched_condition = True
        elif any(word in analysis_lower for word in ['diabetes', 'thyroid', 'hormone', 'endocrine', 'metabolism']):
            # Find endocrinologists or general physicians for diabetes
            doctor_queryset = Doctor.objects.prefetch_related('hospitals').filter(
                Q(specialization__icontains='endocrinology') | Q(specialization__icontains='diabetes') | Q(specialization__icontains='internal medicine') | Q(specialization__icontains='general') | Q(specialization__icontains='MBBS')
            )[:3]
            matched_condition = True
        elif any(word in analysis_lower for word in ['cancer', 'tumor', 'oncology', 'chemotherapy', 'radiation']):
            # Find oncologists
            doctor_queryset = Doctor.objects.prefetch_related('hospitals').filter(
                Q(specialization__icontains='oncology') | Q(specialization__icontains='hematology')
            )[:3]
            matched_condition = True
        elif any(word in analysis_lower for word in ['kidney', 'urine', 'bladder', 'urology']):
            # Find urologists
            doctor_queryset = Doctor.objects.prefetch_related('hospitals').filter(
                Q(specialization__icontains='urology') | Q(specialization__icontains='nephrology')
            )[:3]
            matched_condition = True
        elif any(word in analysis_lower for word in ['liver', 'stomach', 'intestine', 'gastro', 'digestive']):
            # Find gastroenterologists
            doctor_queryset = Doctor.objects.prefetch_related('hospitals').filter(
                Q(specialization__icontains='gastroenterology') | Q(specialization__icontains='hepatology')
            )[:3]
            matched_condition = True
        elif any(word in analysis_lower for word in ['lung', 'breathing', 'asthma', 'pulmonary', 'respiratory']):
            # Find pulmonologists
            doctor_queryset = Doctor.objects.prefetch_related('hospitals').filter(
                Q(specialization__icontains='pulmonology') | Q(specialization__icontains='respiratory')
            )[:3]
            matched_condition = True
        elif any(word in analysis_lower for word in ['skin', 'rash', 'dermatitis', 'acne', 'dermatology']):
            # Find dermatologists
            doctor_queryset = Doctor.objects.prefetch_related('hospitals').filter(
                Q(specialization__icontains='dermatology') | Q(specialization__icontains='skin')
            )[:3]
            matched_condition = True
        else:
            # If no specific conditions found, get general physicians
            doctor_queryset = Doctor.objects.prefetch_related('hospitals').filter(
                Q(specialization__icontains='general medicine') | Q(specialization__icontains='internal medicine') | Q(specialization__icontains='family medicine')
            )[:3]
            matched_condition = False
        
        # Build the suggested doctors list
        suggested_doctors = []
        for doctor in doctor_queryset:
            try:
                hospitals_list = [hospital.name for hospital in doctor.hospitals.all()]
                hospitals_str = ', '.join(hospitals_list)
            except:
                hospitals_str = "Hospital information not available"
            suggested_doctors.append({
                'id': doctor.id,
                'name': doctor.name,
                'specialization': doctor.specialization,
                'experience_years': doctor.experience_years,
                'hospitals': hospitals_str,
                'profile_url': f'/doctors/{getattr(doctor, "slug", "")}/' if getattr(doctor, 'slug', None) else f'/doctors/profile/{doctor.id}/',
                'meeting_link': f'/video-call/{doctor.id}/'
            })
        
        # If no doctors found from condition matching, try general physicians
        if not suggested_doctors and not matched_condition:
            doctor_queryset = Doctor.objects.prefetch_related('hospitals').filter(
                Q(specialization__icontains='general medicine') | Q(specialization__icontains='internal medicine') | Q(specialization__icontains='family medicine')
            )[:3]
            for doctor in doctor_queryset:
                try:
                    hospitals_list = [hospital.name for hospital in doctor.hospitals.all()]
                    hospitals_str = ', '.join(hospitals_list)
                except:
                    hospitals_str = "Hospital information not available"
                suggested_doctors.append({
                    'id': doctor.id,
                    'name': doctor.name,
                    'specialization': doctor.specialization,
                    'experience_years': doctor.experience_years,
                    'hospitals': hospitals_str,
                    'profile_url': f'/doctors/{getattr(doctor, "slug", "")}/' if getattr(doctor, 'slug', None) else f'/doctors/profile/{doctor.id}/',
                    'meeting_link': f'/video-call/{doctor.id}/'
                })
        

        
        return JsonResponse({
            'success': True,
            'analysis': analysis,
            'suggested_doctors': suggested_doctors
        })
    
    return JsonResponse({
        'success': False,
        'error': 'No medical report uploaded'
    })


def local_medical_analysis(text_content):
    """Perform local medical analysis using rule-based approach"""
    # Define common medical terms and their associated recommendations
    precautions_keywords = ['diabetes', 'hypertension', 'cholesterol', 'heart', 'cardiac', 'stroke', 'kidney', 'liver', 'lung', 'asthma', 'arthritis', 'thyroid', 'cancer', 'osteoporosis', 'depression', 'anxiety']
    treatment_keywords = ['medication', 'therapy', 'surgery', 'injection', 'procedure', 'treatment', 'prescription', 'tablet', 'capsule', 'dose', 'chemotherapy', 'radiation', 'physical therapy', 'occupational therapy']
    effect_keywords = ['side effect', 'reaction', 'complication', 'outcome', 'result', 'response', 'change', 'improvement', 'worsening', 'adverse effect']
    symptom_keywords = ['pain', 'fever', 'headache', 'fatigue', 'nausea', 'dizziness', 'shortness of breath', 'chest pain', 'swelling', 'rash', 'bleeding', 'numbness', 'tingling', 'weakness']
    
    analysis_parts = []
    
    # Identify conditions and suggest precautions
    found_conditions = [word for word in precautions_keywords if word.lower() in text_content.lower()]
    if found_conditions:
        analysis_parts.append(f"• Precautions to take: Based on identified conditions ({', '.join(found_conditions)}), follow your doctor's advice, maintain a healthy diet, exercise regularly, monitor vital signs, and take prescribed medications on time.")
    
    # Identify treatments mentioned
    found_treatments = [word for word in treatment_keywords if word.lower() in text_content.lower()]
    if found_treatments:
        analysis_parts.append(f"• Recommended treatments/cures: The report mentions {', '.join(found_treatments)}. Ensure you follow the prescribed treatment plan as directed by your healthcare provider.")
    
    # Identify potential effects
    found_effects = [word for word in effect_keywords if word.lower() in text_content.lower()]
    if found_effects:
        analysis_parts.append(f"• Potential effects: Monitor for {', '.join(found_effects)} as mentioned in your report, and report any concerns to your doctor.")
    
    # Identify symptoms
    found_symptoms = [word for word in symptom_keywords if word.lower() in text_content.lower()]
    if found_symptoms:
        analysis_parts.append(f"• Side effects/symptoms to watch for: Be aware of {', '.join(found_symptoms)} and consult your doctor if they worsen or persist.")
    
    # Add general recommendations
    analysis_parts.append("• Follow-up recommendations: Schedule regular check-ups with your healthcare provider, maintain a healthy lifestyle, stay hydrated, get adequate rest, and keep track of your symptoms. Following your treatment plan consistently is crucial for the best outcomes.")
    
    # Return the combined analysis
    return "\n".join(analysis_parts) if analysis_parts else "Local analysis completed. Please consult with a healthcare professional for detailed medical advice based on your report."


def full_bot_interface(request):
    """Full screen bot interface view"""
    return render(request, 'enquiry_bot/full_bot_interface.html')



def video_call_view(request, doctor_id=None):
    """Video call/meeting page for doctor consultations"""
    from doctors.models import Doctor
    
    try:
        doctor = Doctor.objects.get(id=doctor_id) if doctor_id else None
    except Doctor.DoesNotExist:
        doctor = None
    
    context = {
        'doctor': doctor,
        'doctor_id': doctor_id,
    }
    return render(request, 'enquiry_bot/video_call.html', context)


def user_enquiries(request):
    """View for user's enquiries"""
    enquiries = Enquiry.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(enquiries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'enquiry_bot/user_enquiries.html', {'page_obj': page_obj})