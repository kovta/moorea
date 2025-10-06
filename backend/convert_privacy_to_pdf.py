#!/usr/bin/env python3
"""
Convert Moorea Privacy Policy from Markdown to PDF
"""

import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import os

def convert_markdown_to_pdf():
    """Convert the privacy policy markdown file to a styled PDF."""
    
    # Read the markdown file
    with open('MOOREA_PRIVACY_POLICY.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML
    html = markdown.markdown(markdown_content, extensions=['tables', 'toc'])
    
    # Create a complete HTML document with styling
    html_document = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Moorea Privacy Policy</title>
        <style>
            @page {{
                size: A4;
                margin: 2cm;
                @bottom-center {{
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 10px;
                    color: #666;
                }}
            }}
            
            body {{
                font-family: 'Helvetica', 'Arial', sans-serif;
                line-height: 1.6;
                color: #333;
                font-size: 11px;
            }}
            
            h1 {{
                color: #2c3e50;
                font-size: 24px;
                margin-bottom: 20px;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }}
            
            h2 {{
                color: #34495e;
                font-size: 18px;
                margin-top: 25px;
                margin-bottom: 15px;
                border-bottom: 1px solid #bdc3c7;
                padding-bottom: 5px;
            }}
            
            h3 {{
                color: #2c3e50;
                font-size: 14px;
                margin-top: 20px;
                margin-bottom: 10px;
            }}
            
            h4 {{
                color: #34495e;
                font-size: 12px;
                margin-top: 15px;
                margin-bottom: 8px;
            }}
            
            p {{
                margin-bottom: 10px;
                text-align: justify;
            }}
            
            ul, ol {{
                margin-bottom: 15px;
                padding-left: 20px;
            }}
            
            li {{
                margin-bottom: 5px;
            }}
            
            strong {{
                color: #2c3e50;
                font-weight: bold;
            }}
            
            code {{
                background-color: #f8f9fa;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 10px;
            }}
            
            blockquote {{
                border-left: 4px solid #3498db;
                margin: 15px 0;
                padding-left: 15px;
                color: #555;
                font-style: italic;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
                font-size: 10px;
            }}
            
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            
            .header-info {{
                background-color: #ecf0f1;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
                border-left: 5px solid #3498db;
            }}
            
            .contact-info {{
                background-color: #e8f5e8;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
                border-left: 3px solid #27ae60;
            }}
            
            .important {{
                background-color: #fff3cd;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
                border-left: 3px solid #ffc107;
            }}
            
            .compliance-badge {{
                background-color: #d4edda;
                color: #155724;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 10px;
                font-weight: bold;
                display: inline-block;
                margin: 5px 0;
            }}
        </style>
    </head>
    <body>
        <div class="header-info">
            <h1>Moorea Privacy Policy</h1>
            <p><strong>Last Updated:</strong> October 6, 2025</p>
            <p><strong>Website:</strong> Moorea.mood.com</p>
            <p><strong>Contact:</strong> annaszilviakennedy@gmail.com</p>
            <div class="compliance-badge">✅ Pinterest API Compliant</div>
            <div class="compliance-badge">✅ GDPR Compliant</div>
            <div class="compliance-badge">✅ CCPA Compliant</div>
        </div>
        
        {html}
        
        <div class="contact-info">
            <h3>Contact Information</h3>
            <p><strong>Email:</strong> annaszilviakennedy@gmail.com</p>
            <p><strong>Website:</strong> Moorea.mood.com</p>
            <p><strong>Privacy Policy:</strong> Moorea.mood.com/privacy</p>
        </div>
        
        <div class="important">
            <p><strong>Note:</strong> This privacy policy is designed to comply with Pinterest API requirements, GDPR, and CCPA regulations. For the most up-to-date version, please visit our website.</p>
        </div>
    </body>
    </html>
    """
    
    # Create PDF
    font_config = FontConfiguration()
    html_doc = HTML(string=html_document)
    
    # Generate PDF
    pdf_filename = 'Moorea_Privacy_Policy.pdf'
    html_doc.write_pdf(pdf_filename, font_config=font_config)
    
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
