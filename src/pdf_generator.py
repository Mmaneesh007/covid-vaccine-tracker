"""
PDF generation utilities for COVID-19 Vaccine Tracker
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io


def create_symptom_assessment_pdf(
    symptoms_data,
    risk_level,
    exposure,
    vaccination_status
):
    """
    Generate a PDF report for COVID-19 symptom assessment.
    
    Args:
        symptoms_data (dict): Dictionary of symptoms with bool values
        risk_level (str): "HIGH", "MODERATE", or "LOW"
        exposure (str): Exposure history
        vaccination_status (str): Vaccination status
        
    Returns:
        io.BytesIO: PDF file as bytes
    """
    # Create a BytesIO buffer
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER,
        bold=True
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12,
        spaceBefore=12,
        bold=True
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#666666'),
        spaceAfter=12,
    )
    
    # Title
    title = Paragraph("COVID-19 Symptom Assessment Report", title_style)
    elements.append(title)
    
    # Date and disclaimer
    date_text = f"Assessment Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
    date_para = Paragraph(date_text, normal_style)
    elements.append(date_para)
    elements.append(Spacer(1, 0.2*inch))
    
    # Medical Disclaimer Box
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.red,
        borderWidth=1,
        borderColor=colors.red,
        borderPadding=10,
        backColor=colors.HexColor('#fff5f5'),
        spaceAfter=20
    )
    
    disclaimer = Paragraph(
        "<b>MEDICAL DISCLAIMER:</b> This is NOT a medical diagnosis. "
        "This assessment is for informational purposes only and does not replace "
        "professional medical advice, diagnosis, or treatment. Please consult a "
        "healthcare provider if you have symptoms.",
        disclaimer_style
    )
    elements.append(disclaimer)
    elements.append(Spacer(1, 0.3*inch))
    
    # Risk Assessment Result
    risk_heading = Paragraph("Risk Assessment Result", heading_style)
    elements.append(risk_heading)
    
    # Risk level with color coding
    risk_colors = {
        "HIGH": colors.HexColor('#dc3545'),
        "MODERATE": colors.HexColor('#fd7e14'),
        "LOW": colors.HexColor('#28a745')
    }
    
    risk_color = risk_colors.get(risk_level, colors.gray)
    
    risk_box_style = ParagraphStyle(
        'RiskBox',
        parent=styles['Normal'],
        fontSize=16,
        textColor=colors.white,
        backColor=risk_color,
        borderPadding=15,
        alignment=TA_CENTER,
        spaceAfter=20,
        bold=True
    )
    
    risk_text = Paragraph(f"{risk_level} RISK", risk_box_style)
    elements.append(risk_text)
    elements.append(Spacer(1, 0.2*inch))
    
    # Reported Symptoms
    symptoms_heading = Paragraph("Reported Symptoms", heading_style)
    elements.append(symptoms_heading)
    
    # Create symptoms table
    primary_symptoms = []
    other_symptoms = []
    
    symptom_names = {
        'fever': '🌡️ Fever (>100.4°F / 38°C)',
        'cough': '🤧 New continuous cough',
        'breathing': '😮‍💨 Difficulty breathing',
        'taste_smell': '👃 Loss of taste or smell',
        'fatigue': '😴 Unusual tiredness',
        'body_aches': '💪 Muscle or body aches',
        'sore_throat': '🗣️ Sore throat',
        'headache': '🤕 Headache',
        'congestion': '🤧 Nasal congestion',
        'nausea': '🤢 Nausea or vomiting',
        'diarrhea': '🚽 Diarrhea'
    }
    
    primary_keys = ['fever', 'cough', 'breathing', 'taste_smell']
    
    for key, name in symptom_names.items():
        if symptoms_data.get(key, False):
            if key in primary_keys:
                primary_symptoms.append(name)
            else:
                other_symptoms.append(name)
    
    if primary_symptoms:
        elements.append(Paragraph("<b>Primary Symptoms:</b>", normal_style))
        for symptom in primary_symptoms:
            elements.append(Paragraph(f"• {symptom}", normal_style))
    
    if other_symptoms:
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph("<b>Other Symptoms:</b>", normal_style))
        for symptom in other_symptoms:
            elements.append(Paragraph(f"• {symptom}", normal_style))
    
    if not primary_symptoms and not other_symptoms:
        elements.append(Paragraph("No symptoms reported", normal_style))
    
    elements.append(Spacer(1, 0.2*inch))
    
    # Additional Information
    info_heading = Paragraph("Additional Information", heading_style)
    elements.append(info_heading)
    
    info_data = [
        ['Exposure History:', exposure],
        ['Vaccination Status:', vaccination_status],
    ]
    
    info_table = Table(info_data, colWidths=[2.5*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Recommendations
    rec_heading = Paragraph("Recommendations", heading_style)
    elements.append(rec_heading)
    
    if risk_level == "HIGH":
        recommendations = [
            "✅ Get tested immediately at a COVID-19 testing center",
            "🏠 Self-isolate - Stay away from others, including household members",
            "😷 Wear a mask if you must be around others",
            "📞 Contact your healthcare provider if symptoms worsen",
            "🚨 Seek emergency care if you experience severe symptoms"
        ]
    elif risk_level == "MODERATE":
        recommendations = [
            "✅ Get tested for COVID-19",
            "🏠 Stay home - Avoid contact with others until you get tested",
            "😷 Wear a mask around others",
            "👁️ Monitor symptoms - Watch for worsening symptoms",
            "📞 Contact your healthcare provider if symptoms worsen"
        ]
    else:
        recommendations = [
            "💉 Stay up-to-date with vaccinations",
            "😷 Wear masks in crowded indoor spaces",
            "👐 Wash hands frequently",
            "📏 Maintain social distance when possible",
            "👁️ Monitor for new symptoms"
        ]
    
    for rec in recommendations:
        elements.append(Paragraph(rec, normal_style))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Emergency Warning (for high risk)
    if risk_level == "HIGH":
        emergency_style = ParagraphStyle(
            'Emergency',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#721c24'),
            backColor=colors.HexColor('#f8d7da'),
            borderWidth=1,
            borderColor=colors.HexColor('#f5c6cb'),
            borderPadding=10,
            spaceAfter=20
        )
        
        emergency = Paragraph(
            "<b>SEEK EMERGENCY CARE IF YOU EXPERIENCE:</b><br/>"
            "• Trouble breathing<br/>"
            "• Persistent chest pain or pressure<br/>"
            "• New confusion<br/>"
            "• Inability to wake or stay awake<br/>"
            "• Pale, gray, or blue-colored skin, lips, or nail beds",
            emergency_style
        )
        elements.append(emergency)
    
    # Testing Resources
    resources_heading = Paragraph("Testing Resources", heading_style)
    elements.append(resources_heading)
    
    resources = Paragraph(
        "<b>India:</b> ICMR Testing Centers (icmr.gov.in) | COVID Helpline: 1075<br/>"
        "<b>United States:</b> COVID.gov Testing Locator | Call: 211<br/>"
        "<b>United Kingdom:</b> NHS COVID-19 Testing | Call: 119<br/>"
        "<b>Global:</b> WHO COVID-19 Resources (who.int)",
        normal_style
    )
    elements.append(resources)
    
    # Footer
    elements.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    
    footer = Paragraph(
        "This report was generated by COVID-19 Vaccine Tracker<br/>"
        "For more information, visit: github.com/Mmaneesh007/covid-vaccine-tracker<br/>"
        f"Report ID: {datetime.now().strftime('%Y%m%d%H%M%S')}",
        footer_style
    )
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf
