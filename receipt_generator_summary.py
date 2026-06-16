from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# Create PDF document
doc = SimpleDocTemplate("receipt_generator_summary.pdf", pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
elements = []

# Define styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=28,
    textColor=colors.HexColor('#1f4788'),
    spaceAfter=12,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

subtitle_style = ParagraphStyle(
    'Subtitle',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#333333'),
    spaceAfter=12,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=12,
    textColor=colors.HexColor('#1f4788'),
    spaceAfter=8,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontSize=10,
    textColor=colors.HexColor('#333333'),
    spaceAfter=6,
    alignment=TA_JUSTIFY,
    leading=14
)

bullet_style = ParagraphStyle(
    'Bullet',
    parent=styles['Normal'],
    fontSize=10,
    textColor=colors.HexColor('#333333'),
    spaceAfter=4,
    leftIndent=20,
    leading=12
)

# Title
elements.append(Paragraph("Receipt Generator Summary", title_style))
elements.append(Paragraph("File: receipt_generator.py", subtitle_style))
elements.append(Spacer(1, 0.2*inch))

# Overview Section
elements.append(Paragraph("Overview", heading_style))
elements.append(Paragraph(
    "The <b>ReceiptGenerator</b> class is a comprehensive Python utility that creates, manages, and generates professional PDF receipts for financial transactions. It provides a complete receipt management system with data persistence, PDF generation, and search capabilities.",
    body_style
))
elements.append(Spacer(1, 0.15*inch))

# Core Features Section
elements.append(Paragraph("Core Features", heading_style))

features = [
    "<b>Data Management:</b> Loads and saves receipt records to JSON files with automatic sequential receipt numbering",
    "<b>Receipt Creation:</b> Creates new receipt records with recipient name, bank, amount, and description fields",
    "<b>PDF Generation:</b> Converts receipts to professional PDF documents with styled tables, formatted currency, and custom typography",
    "<b>Viewing:</b> Displays individual or all receipts in formatted console output with totals and summaries",
    "<b>Search Functionality:</b> Searches receipts by recipient name with case-insensitive matching"
]

for feature in features:
    elements.append(Paragraph(f"• {feature}", bullet_style))

elements.append(Spacer(1, 0.15*inch))

# Key Methods Section
elements.append(Paragraph("Key Methods", heading_style))

methods_data = [
    ["Method", "Description"],
    ["load_receipts()", "Loads receipt data from JSON file"],
    ["save_receipts()", "Persists receipts to JSON file"],
    ["get_next_receipt_number()", "Generates sequential receipt numbers"],
    ["create_receipt()", "Creates and stores new receipt records"],
    ["generate_pdf()", "Creates professional PDF receipt documents"],
    ["view_receipt()", "Displays individual receipt details"],
    ["view_all_receipts()", "Shows all receipts with summary totals"],
    ["search_receipts()", "Searches receipts by recipient name"]
]

methods_table = Table(methods_data, colWidths=[2*inch, 3.5*inch])
methods_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 11),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
]))

elements.append(methods_table)
elements.append(Spacer(1, 0.2*inch))

# PDF Formatting Section
elements.append(Paragraph("PDF Formatting Features", heading_style))

formatting_features = [
    "Centered company header with custom branding",
    "Professional color scheme with navy blue headers (#1f4788)",
    "Structured layout with Receipt Details and Payment Details sections",
    "Styled tables with alternating row backgrounds and borders",
    "Formatted currency display (Nigerian Naira - ₦)",
    "Multiple custom paragraph styles for different content types",
    "Thank you message and auto-generation footer",
    "Configurable output directory for PDF files"
]

for feature in formatting_features:
    elements.append(Paragraph(f"• {feature}", bullet_style))

elements.append(Spacer(1, 0.15*inch))

# Use Case Section
elements.append(Paragraph("Primary Use Case", heading_style))
elements.append(Paragraph(
    "This system is designed for financial transaction tracking in Nigeria, specifically for managing bank transfers and payments. The example usage demonstrates creating receipts for three sample transactions, then generating professional PDF receipts for record-keeping and audit purposes.",
    body_style
))

elements.append(Spacer(1, 0.15*inch))

# Example Usage Section
elements.append(Paragraph("Example Workflow", heading_style))

example_steps = [
    "Initialize ReceiptGenerator with company name",
    "Create multiple receipt records with transaction details",
    "View all receipts in a formatted table with totals",
    "Generate PDF files for archival and distribution"
]

for i, step in enumerate(example_steps, 1):
    elements.append(Paragraph(f"{i}. {step}", bullet_style))

elements.append(Spacer(1, 0.2*inch))

# Technical Details Section
elements.append(Paragraph("Technical Details", heading_style))

tech_info = [
    "Language: Python",
    "Primary Library: ReportLab (PDF generation)",
    "Data Storage: JSON file format",
    "Receipt Number Range: Starting from 1001",
    "Currency: Nigerian Naira (₦)"
]

for info in tech_info:
    elements.append(Paragraph(f"• {info}", bullet_style))

# Build PDF
doc.build(elements)
print("✓ PDF Summary generated: receipt_generator_summary.pdf")
