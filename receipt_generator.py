import json
import os
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

class ReceiptGenerator:
    def __init__(self, company_name="Receipt System", data_file="receipts_data.json"):
        self.company_name = company_name
        self.data_file = data_file
        self.receipts = self.load_receipts()
    
    def load_receipts(self):
        """Load receipts from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_receipts(self):
        """Save receipts to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.receipts, f, indent=4)
    
    def get_next_receipt_number(self):
        """Generate next receipt number based on existing receipts"""
        if not self.receipts:
            return 1001
        last_number = max(receipt['receipt_number'] for receipt in self.receipts)
        return last_number + 1
    
    def create_receipt(self, recipient_name, bank_name, amount, description=""):
        """Create a new receipt"""
        receipt_number = self.get_next_receipt_number()
        receipt = {
            'receipt_number': receipt_number,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'recipient_name': recipient_name,
            'bank_name': bank_name,
            'amount': amount,
            'description': description,
            'status': 'Active'
        }
        self.receipts.append(receipt)
        self.save_receipts()
        return receipt
    
    def generate_pdf(self, receipt_number, output_dir="receipts"):
        """Generate PDF receipt"""
        receipt = next((r for r in self.receipts if r['receipt_number'] == receipt_number), None)
        
        if not receipt:
            print(f"Receipt {receipt_number} not found")
            return None
        
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(exist_ok=True)
        
        filename = f"{output_dir}/Receipt_{receipt_number}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            spaceAfter=4,
            alignment=TA_CENTER
        )
        
        label_style = ParagraphStyle(
            'Label',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#555555'),
            fontName='Helvetica-Bold'
        )
        
        value_style = ParagraphStyle(
            'Value',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#000000')
        )
        
        elements = []
        
        # Header
        elements.append(Paragraph(self.company_name, title_style))
        elements.append(Paragraph("Official Receipt", heading_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Receipt details table
        receipt_data = [
            [Paragraph("<b>Receipt Number:</b>", label_style), Paragraph(str(receipt['receipt_number']), value_style)],
            [Paragraph("<b>Date:</b>", label_style), Paragraph(receipt['date'], value_style)],
            [Paragraph("<b>Status:</b>", label_style), Paragraph(receipt['status'], value_style)]
        ]
        
        receipt_table = Table(receipt_data, colWidths=[2*inch, 3*inch])
        receipt_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0'))
        ]))
        
        elements.append(receipt_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Payment details
        elements.append(Paragraph("<b>Payment Details</b>", heading_style))
        elements.append(Spacer(1, 0.1*inch))
        
        payment_data = [
            [Paragraph("<b>Recipient Name:</b>", label_style), Paragraph(receipt['recipient_name'], value_style)],
            [Paragraph("<b>Bank Name:</b>", label_style), Paragraph(receipt['bank_name'], value_style)],
            [Paragraph("<b>Amount:</b>", label_style), Paragraph(f"₦{receipt['amount']:,.2f}", value_style)],
            [Paragraph("<b>Description:</b>", label_style), Paragraph(receipt['description'] or "N/A", value_style)]
        ]
        
        payment_table = Table(payment_data, colWidths=[2*inch, 3*inch])
        payment_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0'))
        ]))
        
        elements.append(payment_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#999999'),
            alignment=TA_CENTER
        )
        elements.append(Paragraph("Thank you for your business", footer_style))
        elements.append(Paragraph("This is an automatically generated receipt", footer_style))
        
        doc.build(elements)
        print(f"PDF receipt generated: {filename}")
        return filename
    
    def view_receipt(self, receipt_number):
        """View a specific receipt"""
        receipt = next((r for r in self.receipts if r['receipt_number'] == receipt_number), None)
        if receipt:
            print("\n" + "="*60)
            print(f"Receipt #{receipt['receipt_number']}")
            print("="*60)
            print(f"Date: {receipt['date']}")
            print(f"Recipient: {receipt['recipient_name']}")
            print(f"Bank: {receipt['bank_name']}")
            print(f"Amount: ₦{receipt['amount']:,.2f}")
            print(f"Description: {receipt['description']}")
            print(f"Status: {receipt['status']}")
            print("="*60 + "\n")
        else:
            print(f"Receipt {receipt_number} not found")
    
    def view_all_receipts(self):
        """Display all receipts"""
        if not self.receipts:
            print("No receipts found")
            return
        
        print("\n" + "="*100)
        print(f"{'Receipt #':<12} {'Date':<20} {'Recipient':<20} {'Bank':<20} {'Amount':<15} {'Status':<10}")
        print("="*100)
        
        for receipt in self.receipts:
            print(f"{receipt['receipt_number']:<12} {receipt['date']:<20} {receipt['recipient_name']:<20} {receipt['bank_name']:<20} ₦{receipt['amount']:>13,.2f} {receipt['status']:<10}")
        
        print("="*100 + "\n")
        print(f"Total Receipts: {len(self.receipts)}")
        total_amount = sum(r['amount'] for r in self.receipts)
        print(f"Total Amount: ₦{total_amount:,.2f}\n")
    
    def search_receipts(self, search_term):
        """Search receipts by recipient name"""
        results = [r for r in self.receipts if search_term.lower() in r['recipient_name'].lower()]
        
        if results:
            print(f"\nSearch results for '{search_term}':")
            for receipt in results:
                print(f"Receipt #{receipt['receipt_number']}: {receipt['recipient_name']} - ₦{receipt['amount']:,.2f}")
        else:
            print(f"No receipts found for '{search_term}'")

# Example usage
if __name__ == "__main__":
    # Create receipt generator
    generator = ReceiptGenerator(company_name="Naira Vault")
    
    # Create sample receipts
    print("Creating receipts...\n")
    
    receipt1 = generator.create_receipt(
        recipient_name="John Adeyemi",
        bank_name="First Bank of Nigeria",
        amount=8000.00,
        description="Transfer for services rendered"
    )
    print(f"Created Receipt #{receipt1['receipt_number']}")
    
    receipt2 = generator.create_receipt(
        recipient_name="Maria Okonkwo",
        bank_name="Zenith Bank",
        amount=8000.00,
        description="Monthly allowance"
    )
    print(f"Created Receipt #{receipt2['receipt_number']}")
    
    receipt3 = generator.create_receipt(
        recipient_name="Ahmed Hassan",
        bank_name="GTBank",
        amount=8000.00,
        description="Consultation fee"
    )
    print(f"Created Receipt #{receipt3['receipt_number']}")
    
    # View all receipts
    print("\n" + "="*60)
    print("ALL RECEIPTS")
    print("="*60)
    generator.view_all_receipts()
    
    # View individual receipt
    print("\nViewing Receipt #1001:")
    generator.view_receipt(1001)
    
    # Generate PDFs
    print("\nGenerating PDF receipts...\n")
    for receipt in generator.receipts:
        generator.generate_pdf(receipt['receipt_number'])
    
    print("\n✓ Receipt system setup complete!")
    print("PDFs saved in 'receipts/' folder")
