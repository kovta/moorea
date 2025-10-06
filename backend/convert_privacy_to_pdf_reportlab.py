#!/usr/bin/env python3
"""
Convert Moorea Privacy Policy from Markdown to PDF using ReportLab
"""

import markdown
import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, blue, green, orange
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def clean_text(text):
    """Clean text for PDF formatting."""
    # Remove markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    text = re.sub(r'`(.*?)`', r'<font name="Courier">\1</font>', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # Remove links, keep text
    return text

def convert_markdown_to_pdf():
    """Convert the privacy policy markdown file to a styled PDF."""
    
    # Read the markdown file
    with open('MOOREA_PRIVACY_POLICY.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML first to parse it
    html = markdown.markdown(markdown_content, extensions=['tables', 'toc'])
    
    # Create PDF
    pdf_filename = 'Moorea_Privacy_Policy.pdf'
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=HexColor('#2c3e50'),
        alignment=TA_CENTER
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12,
        spaceBefore=20,
        textColor=HexColor('#34495e'),
        borderWidth=1,
        borderColor=HexColor('#bdc3c7'),
        borderPadding=5
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=15,
        textColor=HexColor('#2c3e50')
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=8,
        spaceBefore=12,
        textColor=HexColor('#34495e')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    # Build the story (content)
    story = []
    
    # Add header
    story.append(Paragraph("Moorea Privacy Policy", title_style))
    story.append(Spacer(1, 12))
    
    # Add compliance badges
    compliance_text = """
    <para align="center">
    <font color="green" size="10"><b>✅ Pinterest API Compliant</b></font> &nbsp;&nbsp;
    <font color="green" size="10"><b>✅ GDPR Compliant</b></font> &nbsp;&nbsp;
    <font color="green" size="10"><b>✅ CCPA Compliant</b></font>
    </para>
    """
    story.append(Paragraph(compliance_text, normal_style))
    story.append(Spacer(1, 20))
    
    # Parse the markdown content
    lines = markdown_content.split('\n')
    current_section = []
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_section:
                # Process accumulated section
                section_text = ' '.join(current_section)
                if section_text:
                    story.append(Paragraph(clean_text(section_text), normal_style))
                current_section = []
            continue
            
        # Handle headers
        if line.startswith('# '):
            if current_section:
                section_text = ' '.join(current_section)
                if section_text:
                    story.append(Paragraph(clean_text(section_text), normal_style))
                current_section = []
            story.append(Paragraph(clean_text(line[2:]), heading1_style))
            
        elif line.startswith('## '):
            if current_section:
                section_text = ' '.join(current_section)
                if section_text:
                    story.append(Paragraph(clean_text(section_text), normal_style))
                current_section = []
            story.append(Paragraph(clean_text(line[3:]), heading2_style))
            
        elif line.startswith('### '):
            if current_section:
                section_text = ' '.join(current_section)
                if section_text:
                    story.append(Paragraph(clean_text(section_text), normal_style))
                current_section = []
            story.append(Paragraph(clean_text(line[4:]), heading3_style))
            
        elif line.startswith('#### '):
            if current_section:
                section_text = ' '.join(current_section)
                if section_text:
                    story.append(Paragraph(clean_text(section_text), normal_style))
                current_section = []
            story.append(Paragraph(clean_text(line[5:]), heading3_style))
            
        elif line.startswith('- ') or line.startswith('* '):
            # Handle bullet points
            if current_section:
                section_text = ' '.join(current_section)
                if section_text:
                    story.append(Paragraph(clean_text(section_text), normal_style))
                current_section = []
            bullet_text = f"• {clean_text(line[2:])}"
            story.append(Paragraph(bullet_text, normal_style))
            
        else:
            current_section.append(line)
    
    # Process any remaining content
    if current_section:
        section_text = ' '.join(current_section)
        if section_text:
            story.append(Paragraph(clean_text(section_text), normal_style))
    
    # Add footer information
    story.append(Spacer(1, 30))
    story.append(Paragraph("Contact Information", heading2_style))
    story.append(Paragraph("<b>Email:</b> annaszilviakennedy@gmail.com", normal_style))
    story.append(Paragraph("<b>Website:</b> Moorea.mood.com", normal_style))
    story.append(Paragraph("<b>Privacy Policy:</b> Moorea.mood.com/privacy", normal_style))
    
    story.append(Spacer(1, 20))
    note_text = """
    <para>
    <font color="orange"><b>Note:</b></font> This privacy policy is designed to comply with Pinterest API requirements, 
    GDPR, and CCPA regulations. For the most up-to-date version, please visit our website.
    </para>
    """
    story.append(Paragraph(note_text, normal_style))
    
    # Build PDF
    doc.build(story)
    
    print(f"✅ PDF created successfully: {pdf_filename}")
    print(f"📄 File size: {os.path.getsize(pdf_filename) / 1024:.1f} KB")
    print(f"📍 Location: {os.path.abspath(pdf_filename)}")
    
    return pdf_filename

if __name__ == "__main__":
    try:
        pdf_file = convert_markdown_to_pdf()
        print(f"\n🎉 Privacy Policy PDF is ready!")
        print(f"📁 You can find it at: {os.path.abspath(pdf_file)}")
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        import traceback
        traceback.print_exc()
