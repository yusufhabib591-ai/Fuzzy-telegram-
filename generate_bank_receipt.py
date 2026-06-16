from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Line, HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime

# Create PDF document
doc = SimpleDocTemplate("bank_receipt.pdf", pagesize=letter, topMargin=0.3*inch, bottomMargin=0.3*inch, leftMargin=0.4*inch, rightMargin=0.4*inch)
elements = []

# Define styles
styles = getSampleStyleSheet()

# Bank header style
bank_name_style = ParagraphStyle(
    'BankName',
    parent=styles['Heading1'],
    fontSize=20,
    textColor=colors.HexColor('#003366'),
    spaceAfter=2,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

receipt_title_style = ParagraphStyle(
    'ReceiptTitle',
    parent=styles['Normal'],
    fontSize=12,
    textColor=colors.HexColor('#333333'),
    spaceAfter=8,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

info_label_style = ParagraphStyle(
    'InfoLabel',
    parent=styles['Normal'],
    fontSize=9,
    textColor=colors.HexColor('#555555'),
    spaceAfter=2,
    fontName='Helvetica'
)

info_value_style = ParagraphStyle(
    'InfoValue',
    parent=styles['Normal'],
    fontSize=9,
    textColor=colors.HexColor('#000000'),
    spaceAfter=2,
    fontName='Helvetica-Bold'
)

transaction_label_style = ParagraphStyle(
    'TransactionLabel',
    parent=styles['Normal'],
    fontSize=9,
    textColor=colors.HexColor('#555555'),
    spaceAfter=4,
    fontName='Helvetica'
)

transaction_value_style = ParagraphStyle(
    'TransactionValue',
    parent=styles['Normal'],
    fontSize=10,
    textColor=colors.HexColor('#000000'),
    spaceAfter=4,
    fontName='Helvetica-Bold'
)

amount_style = ParagraphStyle(
    'Amount',
    parent=styles['Normal'],
    fontSize=14,
    textColor=colors.HexColor('#003366'),
    spaceAfter=6,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

footer_style = ParagraphStyle(
    'Footer',
    parent=styles['Normal'],
    fontSize=8,
    textColor=colors.HexColor('#999999'),
    spaceAfter=3,
    alignment=TA_CENTER
)

# Bank Logo/Header
elements.append(Paragraph("FIRST BANK OF NIGERIA PLC", bank_name_style))
elements.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", receipt_title_style))
elements.append(Paragraph("TRANSACTION RECEIPT", receipt_title_style))
elements.append(Spacer(1, 0.15*inch))

# Receipt Information Section
receipt_info_data = [
    [Paragraph("Receipt No:", info_label_style), Paragraph("FBN0124561789", info_value_style), Paragraph("Date:", info_label_style), Paragraph(datetime.now().strftime("%d/%m/%Y"), info_value_style)],
    [Paragraph("Terminal ID:", info_label_style), Paragraph("ATM001234", info_value_style), Paragraph("Time:", info_label_style), Paragraph(datetime.now().strftime("%H:%M:%S"), info_value_style)],
]

receipt_info_table = Table(receipt_info_data, colWidths=[1.2*inch, 1.3*inch, 1.2*inch, 1.3*inch])
receipt_info_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 2),
    ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ('TOPPADDING', (0, 0), (-1, -1), 2),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
]))

elements.append(receipt_info_table)
elements.append(Spacer(1, 0.15*inch))

# Transaction Details
elements.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", footer_style))
elements.append(Spacer(1, 0.1*inch))

elements.append(Paragraph("FROM ACCOUNT:", transaction_label_style))
elements.append(Paragraph("John Adeyemi", transaction_value_style))
elements.append(Paragraph("Account: 0000123456789 | USSD: *326*", info_label_style))
elements.append(Spacer(1, 0.1*inch))

elements.append(Paragraph("TRANSACTION TYPE:", transaction_label_style))
elements.append(Paragraph("Fund Transfer - Domestic", transaction_value_style))
elements.append(Spacer(1, 0.1*inch))

elements.append(Paragraph("TO ACCOUNT:", transaction_label_style))
elements.append(Paragraph("Maria Okonkwo", transaction_value_style))
elements.append(Paragraph("Zenith Bank - 1000000000 | Account Name Verified ✓", info_label_style))
elements.append(Spacer(1, 0.1*inch))

elements.append(Paragraph("DESCRIPTION:", transaction_label_style))
elements.append(Paragraph("Monthly Allowance", transaction_value_style))
elements.append(Spacer(1, 0.15*inch))

# Amount Section
elements.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", footer_style))
elements.append(Spacer(1, 0.1*inch))

elements.append(Paragraph("AMOUNT", amount_style))
elements.append(Paragraph("₦ 8,000.00", amount_style))
elements.append(Spacer(1, 0.08*inch))

# Charges Section
charges_data = [
    [Paragraph("Transfer Charge:", info_label_style), Paragraph("₦50.00", info_label_style)],
    [Paragraph("Narration Fee:", info_label_style), Paragraph("₦0.00", info_label_style)],
    [Paragraph("Total Debit:", transaction_label_style), Paragraph("₦ 8,050.00", transaction_value_style)],
]

charges_table = Table(charges_data, colWidths=[3*inch, 1.5*inch])
charges_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 2),
    ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ('TOPPADDING', (0, 0), (-1, -1), 2),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ('GRID', (0, 2), (-1, 2), 1, colors.HexColor('#CCCCCC')),
]))

elements.append(charges_table)
elements.append(Spacer(1, 0.15*inch))

# Status Section
elements.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", footer_style))
elements.append(Spacer(1, 0.1*inch))

status_data = [
    [Paragraph("TRANSACTION STATUS:", transaction_label_style), Paragraph("✓ SUCCESSFUL", Paragraph("TransactionStatus", parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#008000'), fontName='Helvetica-Bold'))],
    [Paragraph("Reference No:", info_label_style), Paragraph("FBN2024061612345678901", info_value_style)],
]

status_table = Table(status_data, colWidths=[2*inch, 3*inch])
status_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 2),
    ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ('TOPPADDING', (0, 0), (-1, -1), 2),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
]))

elements.append(status_table)
elements.append(Spacer(1, 0.15*inch))

# Footer
elements.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", footer_style))
elements.append(Spacer(1, 0.1*inch))

elements.append(Paragraph("Thank you for banking with us", footer_style))
elements.append(Paragraph("Please keep this receipt for your records", footer_style))
elements.append(Paragraph("For inquiries, call: 07001000000 | www.firstbanknigeria.com", footer_style))
elements.append(Spacer(1, 0.08*inch))
elements.append(Paragraph("This is an electronically generated receipt. No signature required.", footer_style))

# Build PDF
doc.build(elements)
print("✓ Bank Receipt PDF generated: bank_receipt.pdf")
