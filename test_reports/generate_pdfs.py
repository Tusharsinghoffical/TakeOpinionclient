"""
Generate sample medical report PDFs for chatbot testing.
Run: python test_reports/generate_pdfs.py
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Styles ──────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    "ReportTitle",
    parent=styles["Title"],
    fontSize=16,
    textColor=colors.HexColor("#1a3c6e"),
    spaceAfter=4,
    alignment=TA_CENTER,
)
SUBTITLE_STYLE = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontSize=10,
    textColor=colors.HexColor("#555555"),
    alignment=TA_CENTER,
    spaceAfter=12,
)
SECTION_STYLE = ParagraphStyle(
    "Section",
    parent=styles["Heading2"],
    fontSize=11,
    textColor=colors.HexColor("#1a3c6e"),
    spaceBefore=10,
    spaceAfter=4,
    borderPad=2,
)
BODY_STYLE = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontSize=9,
    leading=14,
    spaceAfter=3,
)
BOLD_STYLE = ParagraphStyle(
    "Bold",
    parent=styles["Normal"],
    fontSize=9,
    leading=14,
    fontName="Helvetica-Bold",
)
HIGHLIGHT_STYLE = ParagraphStyle(
    "Highlight",
    parent=styles["Normal"],
    fontSize=9,
    leading=14,
    textColor=colors.HexColor("#c0392b"),
    fontName="Helvetica-Bold",
)


def header_block(patient_info: dict):
    """Returns flowables for the report header."""
    items = []
    items.append(Paragraph("TakeOpinion Medical Centre", TITLE_STYLE))
    items.append(Paragraph("Patient Medical Report", SUBTITLE_STYLE))
    items.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1a3c6e")))
    items.append(Spacer(1, 8))

    data = [
        [Paragraph(f"<b>Patient:</b> {patient_info['name']}", BODY_STYLE),
         Paragraph(f"<b>Report ID:</b> {patient_info['report_id']}", BODY_STYLE)],
        [Paragraph(f"<b>Age / Gender:</b> {patient_info['age']} / {patient_info['gender']}", BODY_STYLE),
         Paragraph(f"<b>Date:</b> {patient_info['date']}", BODY_STYLE)],
        [Paragraph(f"<b>Referring Doctor:</b> {patient_info['doctor']}", BODY_STYLE),
         Paragraph(f"<b>Department:</b> {patient_info['dept']}", BODY_STYLE)],
    ]
    t = Table(data, colWidths=[9 * cm, 9 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f0f4ff")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#1a3c6e")),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cccccc")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    items.append(t)
    items.append(Spacer(1, 10))
    return items


def section(title):
    return [Paragraph(title, SECTION_STYLE),
            HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#aaaaaa")),
            Spacer(1, 4)]


def lab_table(rows):
    """rows = list of (test, value, normal, flag)"""
    data = [[Paragraph("<b>Test</b>", BOLD_STYLE),
             Paragraph("<b>Result</b>", BOLD_STYLE),
             Paragraph("<b>Normal Range</b>", BOLD_STYLE),
             Paragraph("<b>Status</b>", BOLD_STYLE)]]
    for test, value, normal, flag in rows:
        style = HIGHLIGHT_STYLE if flag == "HIGH" or flag == "LOW" else BODY_STYLE
        data.append([
            Paragraph(test, BODY_STYLE),
            Paragraph(value, style),
            Paragraph(normal, BODY_STYLE),
            Paragraph(flag, style),
        ])
    t = Table(data, colWidths=[6 * cm, 4 * cm, 5 * cm, 3 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3c6e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7f9ff")]),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#aaaaaa")),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#dddddd")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def recommendation_box(specialist, followup):
    data = [
        [Paragraph("<b>Recommended Specialist</b>", BOLD_STYLE),
         Paragraph(specialist, HIGHLIGHT_STYLE)],
        [Paragraph("<b>Follow-up</b>", BOLD_STYLE),
         Paragraph(followup, BODY_STYLE)],
    ]
    t = Table(data, colWidths=[6 * cm, 12 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fff8e1")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#f39c12")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#f39c12")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def build_pdf(filename, flowables):
    path = os.path.join(OUTPUT_DIR, filename)
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
    )
    doc.build(flowables)
    print(f"  Created: {path}")


# ════════════════════════════════════════════════════════════════════════════
# 1. DIABETES REPORT
# ════════════════════════════════════════════════════════════════════════════
def make_diabetes():
    f = []
    f += header_block({"name": "Rajesh Kumar", "age": "52", "gender": "Male",
                        "date": "01-May-2026", "report_id": "MR-2026-001",
                        "doctor": "Dr. A. Mehta", "dept": "Internal Medicine"})

    f += section("CHIEF COMPLAINT")
    f.append(Paragraph("Increased thirst, frequent urination, fatigue, blurred vision for 3 months.", BODY_STYLE))

    f += section("DIAGNOSIS")
    f.append(Paragraph("<b>Type 2 Diabetes Mellitus</b> (ICD-10: E11.9)", HIGHLIGHT_STYLE))

    f += section("LABORATORY RESULTS")
    f.append(lab_table([
        ("Fasting Blood Glucose", "198 mg/dL", "70–100 mg/dL", "HIGH"),
        ("HbA1c", "9.2%", "< 5.7%", "HIGH"),
        ("Post-Prandial Glucose", "285 mg/dL", "< 140 mg/dL", "HIGH"),
        ("Serum Creatinine", "1.1 mg/dL", "0.7–1.2 mg/dL", "Normal"),
        ("Urine Microalbumin", "45 mg/24hr", "< 30 mg/24hr", "HIGH"),
        ("Serum Insulin", "3.2 µIU/mL", "2.6–24.9 µIU/mL", "Normal"),
    ]))

    f += section("CURRENT MEDICATIONS")
    for med in ["Metformin 500 mg — twice daily", "Glimepiride 2 mg — once daily"]:
        f.append(Paragraph(f"• {med}", BODY_STYLE))

    f += section("DOCTOR'S NOTES")
    notes = [
        "Patient has poorly controlled diabetes with HbA1c of 9.2%.",
        "Endocrinology consultation strongly recommended.",
        "Diabetic diet and lifestyle modification advised.",
        "Monitor kidney function (creatinine, microalbumin) every 3 months.",
        "Ophthalmology referral for diabetic retinopathy screening.",
    ]
    for n in notes:
        f.append(Paragraph(f"• {n}", BODY_STYLE))

    f.append(Spacer(1, 12))
    f.append(recommendation_box("Endocrinologist, Internal Medicine", "4 weeks"))
    build_pdf("diabetes_report.pdf", f)


# ════════════════════════════════════════════════════════════════════════════
# 2. CARDIAC REPORT
# ════════════════════════════════════════════════════════════════════════════
def make_cardiac():
    f = []
    f += header_block({"name": "Sunita Sharma", "age": "61", "gender": "Female",
                        "date": "01-May-2026", "report_id": "MR-2026-002",
                        "doctor": "Dr. P. Patel", "dept": "Cardiology"})

    f += section("CHIEF COMPLAINT")
    f.append(Paragraph("Chest pain, shortness of breath on exertion, palpitations for 6 weeks.", BODY_STYLE))

    f += section("DIAGNOSIS")
    f.append(Paragraph("<b>Coronary Artery Disease (CAD) — Hypertension Stage 2</b>", HIGHLIGHT_STYLE))

    f += section("LABORATORY RESULTS")
    f.append(lab_table([
        ("Blood Pressure", "168/102 mmHg", "< 120/80 mmHg", "HIGH"),
        ("Total Cholesterol", "245 mg/dL", "< 200 mg/dL", "HIGH"),
        ("LDL Cholesterol", "162 mg/dL", "< 100 mg/dL", "HIGH"),
        ("HDL Cholesterol", "38 mg/dL", "> 60 mg/dL", "LOW"),
        ("Troponin I", "0.04 ng/mL", "< 0.04 ng/mL", "HIGH"),
        ("BNP", "185 pg/mL", "< 100 pg/mL", "HIGH"),
    ]))

    f += section("ECHOCARDIOGRAM")
    echo = [
        ("Ejection Fraction", "48%", "55–70%", "LOW"),
        ("LV Hypertrophy", "Mild", "None", "HIGH"),
        ("Diastolic Dysfunction", "Grade I", "None", "HIGH"),
    ]
    f.append(lab_table(echo))

    f += section("ECG FINDINGS")
    f.append(Paragraph("ST depression in leads V4–V6. Left ventricular hypertrophy pattern.", BODY_STYLE))

    f += section("DOCTOR'S NOTES")
    notes = [
        "Patient requires urgent cardiac evaluation.",
        "Cardiology referral for possible coronary angiography.",
        "Blood pressure control is critical — target < 130/80 mmHg.",
        "Cardiac surgery consultation may be needed if angiography shows significant stenosis.",
        "Statin therapy and ACE inhibitor to be initiated.",
    ]
    for n in notes:
        f.append(Paragraph(f"• {n}", BODY_STYLE))

    f.append(Spacer(1, 12))
    f.append(recommendation_box("Cardiologist, Cardiac Surgery", "1 week (URGENT)"))
    build_pdf("cardiac_report.pdf", f)


# ════════════════════════════════════════════════════════════════════════════
# 3. KNEE / ORTHOPEDIC REPORT
# ════════════════════════════════════════════════════════════════════════════
def make_knee():
    f = []
    f += header_block({"name": "Mohan Verma", "age": "67", "gender": "Male",
                        "date": "01-May-2026", "report_id": "MR-2026-003",
                        "doctor": "Dr. R. Sharma", "dept": "Orthopedic Surgery"})

    f += section("CHIEF COMPLAINT")
    f.append(Paragraph("Severe knee pain, difficulty walking, swelling in both knees for 2 years.", BODY_STYLE))

    f += section("DIAGNOSIS")
    f.append(Paragraph("<b>Bilateral Knee Osteoarthritis — Grade IV (Bone-on-Bone)</b>", HIGHLIGHT_STYLE))
    f.append(Paragraph("<b>Medial Meniscus Complete Tear — Both Knees</b>", HIGHLIGHT_STYLE))

    f += section("X-RAY FINDINGS")
    findings = [
        "Complete loss of joint space in medial compartment (bilateral)",
        "Severe bone-on-bone contact",
        "Osteophyte formation at tibial and femoral margins",
        "Subchondral sclerosis and cyst formation",
        "Varus deformity: 8° (right), 6° (left)",
    ]
    for fi in findings:
        f.append(Paragraph(f"• {fi}", BODY_STYLE))

    f += section("MRI FINDINGS")
    f.append(lab_table([
        ("Medial Meniscus", "Complete tear", "Intact", "HIGH"),
        ("ACL", "Partial tear", "Intact", "HIGH"),
        ("Cartilage Grade", "Grade IV chondromalacia", "Grade 0", "HIGH"),
        ("Bone Marrow Edema", "Present", "Absent", "HIGH"),
        ("ROM — Flexion", "85°", "135°", "LOW"),
    ]))

    f += section("DOCTOR'S NOTES")
    notes = [
        "Patient is a candidate for bilateral total knee replacement surgery.",
        "Orthopedic Surgery consultation required immediately.",
        "Joint replacement surgery recommended — both knees.",
        "Pre-operative physiotherapy and quadriceps strengthening advised.",
        "Anaesthesia fitness evaluation required before surgery.",
    ]
    for n in notes:
        f.append(Paragraph(f"• {n}", BODY_STYLE))

    f.append(Spacer(1, 12))
    f.append(recommendation_box("Orthopedic Surgery, Joint Replacement", "2 weeks"))
    build_pdf("knee_orthopedic_report.pdf", f)


# ════════════════════════════════════════════════════════════════════════════
# 4. BRAIN / NEURO REPORT
# ════════════════════════════════════════════════════════════════════════════
def make_brain():
    f = []
    f += header_block({"name": "Priya Nair", "age": "45", "gender": "Female",
                        "date": "01-May-2026", "report_id": "MR-2026-004",
                        "doctor": "Dr. A. Khan", "dept": "Neurology"})

    f += section("CHIEF COMPLAINT")
    f.append(Paragraph("Severe headaches, dizziness, memory loss, occasional seizures for 2 months.", BODY_STYLE))

    f += section("DIAGNOSIS")
    f.append(Paragraph("<b>Intracranial Meningioma — Right Frontal Region (Brain Tumor)</b>", HIGHLIGHT_STYLE))

    f += section("MRI BRAIN WITH CONTRAST")
    f.append(lab_table([
        ("Tumor Size", "3.2 × 2.8 cm", "None", "HIGH"),
        ("Location", "Right frontal extra-axial", "—", "HIGH"),
        ("Enhancement", "Homogeneous on contrast", "—", "HIGH"),
        ("Surrounding Edema", "Mild", "None", "HIGH"),
        ("Midline Shift", "None currently", "None", "Normal"),
        ("Papilledema", "Early (fundoscopy)", "None", "HIGH"),
    ]))

    f += section("EEG REPORT")
    f.append(Paragraph("Focal slowing in right frontal region. Occasional epileptiform discharges noted.", BODY_STYLE))

    f += section("NEUROLOGICAL EXAMINATION")
    f.append(lab_table([
        ("GCS Score", "15/15", "15/15", "Normal"),
        ("Cognitive Function", "Mild impairment", "Normal", "HIGH"),
        ("Focal Deficit", "None detected", "None", "Normal"),
    ]))

    f += section("DOCTOR'S NOTES")
    notes = [
        "Brain tumor (meningioma) confirmed on MRI — neurosurgery consultation URGENT.",
        "Neurology follow-up for seizure management (anti-epileptic therapy).",
        "Surgical resection likely needed — craniotomy to be planned.",
        "Gamma knife radiosurgery to be discussed as alternative.",
        "Repeat MRI in 4 weeks if surgery is deferred.",
    ]
    for n in notes:
        f.append(Paragraph(f"• {n}", BODY_STYLE))

    f.append(Spacer(1, 12))
    f.append(recommendation_box("Neurosurgery, Neurology", "URGENT — within 3 days"))
    build_pdf("brain_neuro_report.pdf", f)


# ════════════════════════════════════════════════════════════════════════════
# 5. THYROID REPORT
# ════════════════════════════════════════════════════════════════════════════
def make_thyroid():
    f = []
    f += header_block({"name": "Anita Singh", "age": "38", "gender": "Female",
                        "date": "01-May-2026", "report_id": "MR-2026-005",
                        "doctor": "Dr. S. Kapoor", "dept": "Endocrinology"})

    f += section("CHIEF COMPLAINT")
    f.append(Paragraph("Weight gain (12 kg in 6 months), fatigue, hair loss, cold intolerance, depression.", BODY_STYLE))

    f += section("DIAGNOSIS")
    f.append(Paragraph("<b>Hypothyroidism — Hashimoto's Thyroiditis</b>", HIGHLIGHT_STYLE))
    f.append(Paragraph("<b>Thyroid Nodule — Right Lobe (TIRADS 4, Suspicious)</b>", HIGHLIGHT_STYLE))

    f += section("THYROID FUNCTION TESTS")
    f.append(lab_table([
        ("TSH", "12.4 mIU/L", "0.4–4.0 mIU/L", "HIGH"),
        ("Free T4", "0.6 ng/dL", "0.8–1.8 ng/dL", "LOW"),
        ("Free T3", "2.1 pg/mL", "2.3–4.2 pg/mL", "LOW"),
        ("Anti-TPO Antibodies", "485 IU/mL", "< 35 IU/mL", "HIGH"),
        ("Anti-Thyroglobulin", "320 IU/mL", "< 115 IU/mL", "HIGH"),
    ]))

    f += section("ULTRASOUND THYROID")
    f.append(lab_table([
        ("Right Lobe Nodule", "1.8 cm hypoechoic", "None", "HIGH"),
        ("Nodule Margins", "Irregular", "Well-defined", "HIGH"),
        ("TIRADS Score", "4 (Suspicious)", "1–2", "HIGH"),
        ("Left Lobe", "Normal", "Normal", "Normal"),
        ("FNAC Recommended", "Yes — right lobe", "—", "HIGH"),
    ]))

    f += section("DOCTOR'S NOTES")
    notes = [
        "Hashimoto's thyroiditis confirmed with markedly elevated antibodies.",
        "Endocrinology referral for thyroid hormone replacement therapy.",
        "Levothyroxine therapy to be initiated — dose titration required.",
        "FNAC of right lobe nodule to rule out malignancy — urgent.",
        "Repeat thyroid function tests after 6 weeks of treatment.",
    ]
    for n in notes:
        f.append(Paragraph(f"• {n}", BODY_STYLE))

    f.append(Spacer(1, 12))
    f.append(recommendation_box("Endocrinology", "6 weeks (FNAC urgent)"))
    build_pdf("thyroid_report.pdf", f)


# ════════════════════════════════════════════════════════════════════════════
# 6. LIVER / GASTRO REPORT
# ════════════════════════════════════════════════════════════════════════════
def make_liver():
    f = []
    f += header_block({"name": "Vikram Patel", "age": "49", "gender": "Male",
                        "date": "01-May-2026", "report_id": "MR-2026-006",
                        "doctor": "Dr. V. Mehta", "dept": "Gastroenterology"})

    f += section("CHIEF COMPLAINT")
    f.append(Paragraph("Abdominal pain (right upper quadrant), jaundice, nausea, loss of appetite for 3 months.", BODY_STYLE))

    f += section("DIAGNOSIS")
    f.append(Paragraph("<b>Chronic Liver Disease — Liver Cirrhosis (Child-Pugh Class B)</b>", HIGHLIGHT_STYLE))
    f.append(Paragraph("<b>Portal Hypertension with Mild Ascites</b>", HIGHLIGHT_STYLE))

    f += section("LIVER FUNCTION TESTS")
    f.append(lab_table([
        ("Total Bilirubin", "4.2 mg/dL", "0.2–1.2 mg/dL", "HIGH"),
        ("Direct Bilirubin", "2.8 mg/dL", "0–0.3 mg/dL", "HIGH"),
        ("SGOT (AST)", "185 U/L", "10–40 U/L", "HIGH"),
        ("SGPT (ALT)", "142 U/L", "7–56 U/L", "HIGH"),
        ("Serum Albumin", "2.8 g/dL", "3.5–5.0 g/dL", "LOW"),
        ("PT/INR", "1.8", "0.8–1.2", "HIGH"),
        ("AFP", "28 ng/mL", "< 10 ng/mL", "HIGH"),
    ]))

    f += section("ULTRASOUND ABDOMEN")
    findings = [
        "Liver: Coarse echotexture, nodular surface — consistent with cirrhosis",
        "Spleen: Enlarged — 14.5 cm (Normal < 12 cm)",
        "Mild ascites present in perihepatic region",
        "Portal vein diameter: 14 mm (dilated — Normal < 13 mm)",
        "No focal hepatic lesion detected on current scan",
    ]
    for fi in findings:
        f.append(Paragraph(f"• {fi}", BODY_STYLE))

    f += section("DOCTOR'S NOTES")
    notes = [
        "Liver cirrhosis with portal hypertension confirmed.",
        "Gastroenterology and Hepatology consultation required.",
        "Upper GI endoscopy for oesophageal varices screening.",
        "Diuretic therapy for ascites management.",
        "Liver transplant evaluation may be needed — refer to transplant centre.",
        "Avoid alcohol completely — patient counselling done.",
    ]
    for n in notes:
        f.append(Paragraph(f"• {n}", BODY_STYLE))

    f.append(Spacer(1, 12))
    f.append(recommendation_box("Gastroenterology, Hepatology", "2 weeks"))
    build_pdf("liver_gastro_report.pdf", f)


# ════════════════════════════════════════════════════════════════════════════
# 7. CANCER / ONCOLOGY REPORT
# ════════════════════════════════════════════════════════════════════════════
def make_cancer():
    f = []
    f += header_block({"name": "Meera Reddy", "age": "54", "gender": "Female",
                        "date": "01-May-2026", "report_id": "MR-2026-007",
                        "doctor": "Dr. S. Singh", "dept": "Oncology"})

    f += section("CHIEF COMPLAINT")
    f.append(Paragraph("Persistent cough, chest pain, weight loss (8 kg in 3 months), hemoptysis.", BODY_STYLE))

    f += section("DIAGNOSIS")
    f.append(Paragraph("<b>Non-Small Cell Lung Cancer (NSCLC) — Stage IIIA</b>", HIGHLIGHT_STYLE))
    f.append(Paragraph("<b>Adenocarcinoma — Right Upper Lobe</b>", HIGHLIGHT_STYLE))

    f += section("CT CHEST WITH CONTRAST")
    f.append(lab_table([
        ("Primary Tumor Size", "4.5 × 3.8 cm", "None", "HIGH"),
        ("Location", "Right upper lobe", "—", "HIGH"),
        ("Mediastinal Nodes", "Stations 2R, 4R enlarged", "Normal", "HIGH"),
        ("Distant Metastasis", "Not detected", "None", "Normal"),
        ("Pleural Effusion", "Minimal", "None", "HIGH"),
    ]))

    f += section("PET-CT FINDINGS")
    f.append(lab_table([
        ("Primary Tumor SUV max", "12.4", "< 2.5", "HIGH"),
        ("Right Hilar Nodes SUV", "8.2", "< 2.5", "HIGH"),
        ("Bone Metastasis", "Not detected", "None", "Normal"),
        ("Brain Metastasis", "Not detected", "None", "Normal"),
    ]))

    f += section("BIOPSY & MOLECULAR PROFILE")
    f.append(lab_table([
        ("Histology", "Adenocarcinoma", "—", "HIGH"),
        ("EGFR Mutation", "Negative", "—", "Normal"),
        ("ALK Rearrangement", "Negative", "—", "Normal"),
        ("PD-L1 Expression", "45%", "—", "HIGH"),
    ]))

    f += section("DOCTOR'S NOTES")
    notes = [
        "Locally advanced lung cancer — multimodal treatment required.",
        "Oncology consultation for chemotherapy / immunotherapy planning.",
        "Surgical Oncology evaluation for possible lobectomy.",
        "Radiation oncology referral for concurrent chemoradiation.",
        "Tumor board multidisciplinary discussion recommended.",
        "PD-L1 45% — immunotherapy (Pembrolizumab) may be considered.",
    ]
    for n in notes:
        f.append(Paragraph(f"• {n}", BODY_STYLE))

    f.append(Spacer(1, 12))
    f.append(recommendation_box("Oncology, Surgical Oncology", "URGENT — within 5 days"))
    build_pdf("cancer_oncology_report.pdf", f)


# ── Run all ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating medical report PDFs...")
    make_diabetes()
    make_cardiac()
    make_knee()
    make_brain()
    make_thyroid()
    make_liver()
    make_cancer()
    print("\nDone! All 7 PDFs created in test_reports/")
