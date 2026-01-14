# Invoice Generation

## Overview

Comprehensive guide to automated invoice generation for billing systems.

## Table of Contents

1. [Invoice Data Structure](#invoice-data-structure)
2. [PDF Generation](#pdf-generation)
3. [Invoice Templates](#invoice-templates)
4. [Line Items Calculation](#line-items-calculation)
5. [Tax Calculation](#tax-calculation)
6. [Invoice Numbering](#invoice-numbering)
7. [Storage and Retrieval](#storage-and-retrieval)
8. [Email Delivery](#email-delivery)
9. [Invoice Status Tracking](#invoice-status-tracking)
10. [Customization](#customization)
11. [Compliance Requirements](#compliance-requirements)

---

## Invoice Data Structure

### Invoice Model

```typescript
// invoice-model.ts

export interface Invoice {
  id: string;
  invoiceNumber: string;
  userId: string;
  subscriptionId?: string;
  status: InvoiceStatus;
  issueDate: Date;
  dueDate: Date;
  paidDate?: Date;
  subtotal: number;
  tax: number;
  total: number;
  currency: string;
  lineItems: InvoiceLineItem[];
  taxDetails: TaxDetails[];
  notes?: string;
  metadata?: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
}

export interface InvoiceLineItem {
  id: string;
  description: string;
  quantity: number;
  unitPrice: number;
  amount: number;
  taxRate?: number;
  taxAmount?: number;
  metadata?: Record<string, any>;
}

export interface TaxDetails {
  name: string;
  rate: number;
  amount: number;
  jurisdiction?: string;
}

export enum InvoiceStatus {
  DRAFT = 'draft',
  SENT = 'sent',
  VIEWED = 'viewed',
  PAID = 'paid',
  OVERDUE = 'overdue',
  CANCELLED = 'cancelled',
  REFUNDED = 'refunded'
}

export interface InvoiceTemplate {
  id: string;
  name: string;
  logo?: string;
  companyInfo: CompanyInfo;
  billingAddress?: Address;
  shippingAddress?: Address;
  terms?: string;
  footer?: string;
  colors: {
    primary: string;
    secondary: string;
    text: string;
    background: string;
  };
}

export interface CompanyInfo {
  name: string;
  address: Address;
  email: string;
  phone?: string;
  taxId?: string;
  vatNumber?: string;
}

export interface Address {
  line1: string;
  line2?: string;
  city: string;
  state: string;
  postalCode: string;
  country: string;
}
```

---

## PDF Generation

### Node.js (PDFKit)

```typescript
// pdfkit-generator.ts
import PDFDocument from 'pdfkit';
import { Invoice, InvoiceTemplate } from './invoice-model';
import * as fs from 'fs';

export class PDFKitInvoiceGenerator {
  async generatePDF(
    invoice: Invoice,
    template: InvoiceTemplate,
    outputPath: string
  ): Promise<void> {
    const doc = new PDFDocument({ size: 'A4', margin: 50 });
    const stream = fs.createWriteStream(outputPath);
    doc.pipe(stream);
    
    // Add company logo
    if (template.logo) {
      doc.image(template.logo, 50, 50, { width: 100 });
    }
    
    // Add company info
    this.addCompanyInfo(doc, template.companyInfo, template.logo ? 160 : 50, 50);
    
    // Add invoice details
    this.addInvoiceDetails(doc, invoice, 400, 50);
    
    // Add billing address
    if (invoice.metadata?.billingAddress) {
      this.addBillingAddress(doc, invoice.metadata.billingAddress, 50, 150);
    }
    
    // Add line items table
    this.addLineItemsTable(doc, invoice, 50, 220);
    
    // Add totals
    this.addTotals(doc, invoice, 400, 350);
    
    // Add notes
    if (invoice.notes) {
      this.addNotes(doc, invoice.notes, 50, 500);
    }
    
    // Add footer
    if (template.footer) {
      this.addFooter(doc, template.footer);
    }
    
    doc.end();
  }
  
  private addCompanyInfo(doc: PDFKit.PDFDocument, companyInfo: any, x: number, y: number): void {
    doc.fontSize(20).fillColor('#333333').text(companyInfo.name, x, y);
    
    doc.fontSize(10).fillColor('#666666');
    let yPos = y + 30;
    
    doc.text(companyInfo.address.line1, x, yPos);
    yPos += 15;
    
    if (companyInfo.address.line2) {
      doc.text(companyInfo.address.line2, x, yPos);
      yPos += 15;
    }
    
    doc.text(`${companyInfo.address.city}, ${companyInfo.address.state} ${companyInfo.address.postalCode}`, x, yPos);
    yPos += 15;
    doc.text(companyInfo.address.country, x, yPos);
    yPos += 15;
    doc.text(`Email: ${companyInfo.email}`, x, yPos);
    yPos += 15;
    
    if (companyInfo.phone) {
      doc.text(`Phone: ${companyInfo.phone}`, x, yPos);
    }
  }
  
  private addInvoiceDetails(doc: PDFKit.PDFDocument, invoice: Invoice, x: number, y: number): void {
    doc.fontSize(16).fillColor('#333333').text('INVOICE', x, y);
    
    doc.fontSize(10).fillColor('#666666');
    let yPos = y + 30;
    
    doc.text(`Invoice #: ${invoice.invoiceNumber}`, x, yPos);
    yPos += 15;
    doc.text(`Issue Date: ${invoice.issueDate.toLocaleDateString()}`, x, yPos);
    yPos += 15;
    doc.text(`Due Date: ${invoice.dueDate.toLocaleDateString()}`, x, yPos);
    yPos += 15;
    
    if (invoice.paidDate) {
      doc.text(`Paid Date: ${invoice.paidDate.toLocaleDateString()}`, x, yPos);
      yPos += 15;
    }
    
    doc.text(`Status: ${invoice.status.toUpperCase()}`, x, yPos);
  }
  
  private addBillingAddress(doc: PDFKit.PDFDocument, address: any, x: number, y: number): void {
    doc.fontSize(12).fillColor('#333333').text('Bill To:', x, y);
    
    doc.fontSize(10).fillColor('#666666');
    let yPos = y + 20;
    
    doc.text(address.name, x, yPos);
    yPos += 15;
    doc.text(address.line1, x, yPos);
    yPos += 15;
    
    if (address.line2) {
      doc.text(address.line2, x, yPos);
      yPos += 15;
    }
    
    doc.text(`${address.city}, ${address.state} ${address.postalCode}`, x, yPos);
    yPos += 15;
    doc.text(address.country, x, yPos);
  }
  
  private addLineItemsTable(doc: PDFKit.PDFDocument, invoice: Invoice, x: number, y: number): void {
    const tableWidth = 500;
    const colWidths = [50, 250, 80, 80, 40];
    const rowHeight = 25;
    
    // Table header
    doc.fontSize(10).fillColor('#333333');
    doc.text('#', x, y);
    doc.text('Description', x + colWidths[0], y);
    doc.text('Qty', x + colWidths[0] + colWidths[1], y);
    doc.text('Price', x + colWidths[0] + colWidths[1] + colWidths[2], y);
    doc.text('Total', x + colWidths[0] + colWidths[1] + colWidths[2] + colWidths[3], y);
    
    // Header line
    doc.moveTo(x, y + 20).lineTo(x + tableWidth, y + 20).stroke();
    
    // Line items
    let yPos = y + 30;
    invoice.lineItems.forEach((item, index) => {
      doc.text((index + 1).toString(), x, yPos);
      doc.text(item.description, x + colWidths[0], yPos);
      doc.text(item.quantity.toString(), x + colWidths[0] + colWidths[1], yPos);
      doc.text(`$${item.unitPrice.toFixed(2)}`, x + colWidths[0] + colWidths[1] + colWidths[2], yPos);
      doc.text(`$${item.amount.toFixed(2)}`, x + colWidths[0] + colWidths[1] + colWidths[2] + colWidths[3], yPos);
      
      yPos += rowHeight;
    });
    
    // Bottom line
    doc.moveTo(x, yPos).lineTo(x + tableWidth, yPos).stroke();
  }
  
  private addTotals(doc: PDFKit.PDFDocument, invoice: Invoice, x: number, y: number): void {
    doc.fontSize(10).fillColor('#666666');
    
    let yPos = y;
    doc.text('Subtotal:', x + 100, yPos);
    doc.text(`$${invoice.subtotal.toFixed(2)}`, x + 200, yPos);
    yPos += 20;
    
    invoice.taxDetails.forEach(tax => {
      doc.text(`${tax.name} (${(tax.rate * 100).toFixed(1)}%):`, x + 100, yPos);
      doc.text(`$${tax.amount.toFixed(2)}`, x + 200, yPos);
      yPos += 20;
    });
    
    doc.fontSize(12).fillColor('#333333');
    doc.text('Total:', x + 100, yPos);
    doc.text(`$${invoice.total.toFixed(2)}`, x + 200, yPos);
  }
  
  private addNotes(doc: PDFKit.PDFDocument, notes: string, x: number, y: number): void {
    doc.fontSize(10).fillColor('#666666');
    doc.text('Notes:', x, y);
    doc.text(notes, x, y + 15, { width: 500 });
  }
  
  private addFooter(doc: PDFKit.PDFDocument, footer: string): void {
    doc.fontSize(8).fillColor('#999999');
    doc.text(footer, 50, 750, { align: 'center', width: 500 });
  }
}
```

### Node.js (Puppeteer)

```typescript
// puppeteer-generator.ts
import puppeteer from 'puppeteer';
import { Invoice, InvoiceTemplate } from './invoice-model';

export class PuppeteerInvoiceGenerator {
  async generatePDF(
    invoice: Invoice,
    template: InvoiceTemplate,
    outputPath: string
  ): Promise<void> {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    const html = this.generateHTML(invoice, template);
    
    await page.setContent(html);
    await page.pdf({
      path: outputPath,
      format: 'A4',
      printBackground: true
    });
    
    await browser.close();
  }
  
  private generateHTML(invoice: Invoice, template: InvoiceTemplate): string {
    return `
      <!DOCTYPE html>
      <html>
        <head>
          <style>
            body {
              font-family: Arial, sans-serif;
              margin: 0;
              padding: 50px;
              color: #333;
            }
            .header {
              display: flex;
              justify-content: space-between;
              margin-bottom: 50px;
            }
            .company-info {
              max-width: 300px;
            }
            .company-name {
              font-size: 24px;
              font-weight: bold;
              margin-bottom: 10px;
            }
            .invoice-details {
              text-align: right;
            }
            .invoice-title {
              font-size: 20px;
              font-weight: bold;
              margin-bottom: 20px;
            }
            .invoice-info {
              font-size: 12px;
              color: #666;
              line-height: 1.8;
            }
            .billing-address {
              margin-bottom: 50px;
            }
            .address-title {
              font-size: 14px;
              font-weight: bold;
              margin-bottom: 10px;
            }
            .address-info {
              font-size: 12px;
              color: #666;
              line-height: 1.8;
            }
            table {
              width: 100%;
              border-collapse: collapse;
              margin-bottom: 30px;
            }
            th {
              background-color: #f5f5f5;
              padding: 10px;
              text-align: left;
              font-size: 12px;
              border-bottom: 2px solid #ddd;
            }
            td {
              padding: 10px;
              font-size: 12px;
              border-bottom: 1px solid #eee;
            }
            .totals {
              text-align: right;
              margin-bottom: 30px;
            }
            .total-row {
              display: flex;
              justify-content: flex-end;
              margin-bottom: 10px;
            }
            .total-label {
              width: 200px;
              font-size: 12px;
              color: #666;
            }
            .total-amount {
              width: 100px;
              font-size: 12px;
            }
            .grand-total {
              font-weight: bold;
              font-size: 14px;
            }
            .notes {
              margin-bottom: 50px;
            }
            .notes-title {
              font-size: 14px;
              font-weight: bold;
              margin-bottom: 10px;
            }
            .notes-content {
              font-size: 12px;
              color: #666;
              line-height: 1.6;
            }
            .footer {
              text-align: center;
              font-size: 10px;
              color: #999;
              margin-top: 50px;
            }
          </style>
        </head>
        <body>
          <div class="header">
            <div class="company-info">
              ${template.logo ? `<img src="${template.logo}" style="max-width: 100px; margin-bottom: 20px;">` : ''}
              <div class="company-name">${template.companyInfo.name}</div>
              <div class="address-info">
                ${template.companyInfo.address.line1}<br>
                ${template.companyInfo.address.line2 ? template.companyInfo.address.line2 + '<br>' : ''}
                ${template.companyInfo.address.city}, ${template.companyInfo.address.state} ${template.companyInfo.address.postalCode}<br>
                ${template.companyInfo.address.country}<br>
                Email: ${template.companyInfo.email}<br>
                ${template.companyInfo.phone ? 'Phone: ' + template.companyInfo.phone + '<br>' : ''}
              </div>
            </div>
            <div class="invoice-details">
              <div class="invoice-title">INVOICE</div>
              <div class="invoice-info">
                Invoice #: ${invoice.invoiceNumber}<br>
                Issue Date: ${invoice.issueDate.toLocaleDateString()}<br>
                Due Date: ${invoice.dueDate.toLocaleDateString()}<br>
                ${invoice.paidDate ? 'Paid Date: ' + invoice.paidDate.toLocaleDateString() + '<br>' : ''}
                Status: ${invoice.status.toUpperCase()}
              </div>
            </div>
          </div>
          
          ${invoice.metadata?.billingAddress ? `
          <div class="billing-address">
            <div class="address-title">Bill To:</div>
            <div class="address-info">
              ${invoice.metadata.billingAddress.name}<br>
              ${invoice.metadata.billingAddress.line1}<br>
              ${invoice.metadata.billingAddress.line2 ? invoice.metadata.billingAddress.line2 + '<br>' : ''}
              ${invoice.metadata.billingAddress.city}, ${invoice.metadata.billingAddress.state} ${invoice.metadata.billingAddress.postalCode}<br>
              ${invoice.metadata.billingAddress.country}
            </div>
          </div>
          ` : ''}
          
          <table>
            <thead>
              <tr>
                <th style="width: 50px;">#</th>
                <th>Description</th>
                <th style="width: 80px;">Qty</th>
                <th style="width: 80px;">Price</th>
                <th style="width: 80px;">Total</th>
              </tr>
            </thead>
            <tbody>
              ${invoice.lineItems.map((item, index) => `
              <tr>
                <td>${index + 1}</td>
                <td>${item.description}</td>
                <td>${item.quantity}</td>
                <td>$${item.unitPrice.toFixed(2)}</td>
                <td>$${item.amount.toFixed(2)}</td>
              </tr>
              `).join('')}
            </tbody>
          </table>
          
          <div class="totals">
            <div class="total-row">
              <div class="total-label">Subtotal:</div>
              <div class="total-amount">$${invoice.subtotal.toFixed(2)}</div>
            </div>
            ${invoice.taxDetails.map(tax => `
            <div class="total-row">
              <div class="total-label">${tax.name} (${(tax.rate * 100).toFixed(1)}%):</div>
              <div class="total-amount">$${tax.amount.toFixed(2)}</div>
            </div>
            `).join('')}
            <div class="total-row grand-total">
              <div class="total-label">Total:</div>
              <div class="total-amount">$${invoice.total.toFixed(2)}</div>
            </div>
          </div>
          
          ${invoice.notes ? `
          <div class="notes">
            <div class="notes-title">Notes:</div>
            <div class="notes-content">${invoice.notes}</div>
          </div>
          ` : ''}
          
          ${template.footer ? `
          <div class="footer">${template.footer}</div>
          ` : ''}
        </body>
      </html>
    `;
  }
}
```

### Python (ReportLab)

```python
# reportlab-generator.py
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_RIGHT
from datetime import datetime

class ReportLabInvoiceGenerator:
    def generate_pdf(self, invoice, template, output_path):
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Add company logo
        if template.get('logo'):
            # Add logo image
            pass
        
        # Add company info
        company_info = template['company_info']
        story.append(Paragraph(company_info['name'], styles['Heading1']))
        story.append(Spacer(1, 0.2 * inch))
        
        address = f"{company_info['address']['line1']}<br/>"
        if company_info['address'].get('line2'):
            address += f"{company_info['address']['line2']}<br/>"
        address += f"{company_info['address']['city']}, {company_info['address']['state']} {company_info['address']['postal_code']}<br/>"
        address += f"{company_info['address']['country']}<br/>"
        address += f"Email: {company_info['email']}"
        if company_info.get('phone'):
            address += f"<br/>Phone: {company_info['phone']}"
        
        story.append(Paragraph(address, styles['Normal']))
        story.append(Spacer(1, 0.3 * inch))
        
        # Add invoice details
        story.append(Paragraph("INVOICE", styles['Heading2']))
        invoice_info = f"""
        Invoice #: {invoice['invoice_number']}<br/>
        Issue Date: {invoice['issue_date'].strftime('%Y-%m-%d')}<br/>
        Due Date: {invoice['due_date'].strftime('%Y-%m-%d')}<br/>
        """
        if invoice.get('paid_date'):
            invoice_info += f"Paid Date: {invoice['paid_date'].strftime('%Y-%m-%d')}<br/>"
        invoice_info += f"Status: {invoice['status'].upper()}"
        
        story.append(Paragraph(invoice_info, styles['Normal']))
        story.append(Spacer(1, 0.3 * inch))
        
        # Add line items table
        data = [['#', 'Description', 'Qty', 'Price', 'Total']]
        for idx, item in enumerate(invoice['line_items'], 1):
            data.append([
                str(idx),
                item['description'],
                str(item['quantity']),
                f"${item['unit_price']:.2f}",
                f"${item['amount']:.2f}"
            ])
        
        table = Table(data, colWidths=[0.5 * inch, 3 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Add totals
        totals_data = [
            ['Subtotal:', f"${invoice['subtotal']:.2f}"]
        ]
        
        for tax in invoice['tax_details']:
            totals_data.append([
                f"{tax['name']} ({tax['rate'] * 100:.1f}%):",
                f"${tax['amount']:.2f}"
            ])
        
        totals_data.append(['Total:', f"${invoice['total']:.2f}"])
        
        totals_table = Table(totals_data, colWidths=[2 * inch, 1 * inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10)
        ]))
        
        story.append(totals_table)
        
        if invoice.get('notes'):
            story.append(Spacer(1, 0.3 * inch))
            story.append(Paragraph("Notes:", styles['Heading3']))
            story.append(Paragraph(invoice['notes'], styles['Normal']))
        
        doc.build(story)
```

### Python (WeasyPrint)

```python
# weasyprint-generator.py
from weasyprint import HTML, CSS
from datetime import datetime

class WeasyPrintInvoiceGenerator:
    def generate_pdf(self, invoice, template, output_path):
        html = self.generate_html(invoice, template)
        
        HTML(string=html).write_pdf(
            output_path,
            stylesheets=[CSS(string=self.get_css())]
        )
    
    def generate_html(self, invoice, template):
        line_items = ""
        for idx, item in enumerate(invoice['line_items'], 1):
            line_items += f"""
            <tr>
                <td>{idx}</td>
                <td>{item['description']}</td>
                <td>{item['quantity']}</td>
                <td>${item['unit_price']:.2f}</td>
                <td>${item['amount']:.2f}</td>
            </tr>
            """
        
        tax_details = ""
        for tax in invoice['tax_details']:
            tax_details += f"""
            <div class="total-row">
                <div class="total-label">{tax['name']} ({tax['rate'] * 100:.1f}%):</div>
                <div class="total-amount">${tax['amount']:.2f}</div>
            </div>
            """
        
        billing_address = ""
        if invoice.get('metadata', {}).get('billing_address'):
            addr = invoice['metadata']['billing_address']
            billing_address = f"""
            <div class="billing-address">
                <div class="address-title">Bill To:</div>
                <div class="address-info">
                    {addr['name']}<br/>
                    {addr['line1']}<br/>
                    {addr.get('line2', '') + '<br/>' if addr.get('line2') else ''}
                    {addr['city']}, {addr['state']} {addr['postal_code']}<br/>
                    {addr['country']}
                </div>
            </div>
            """
        
        notes = ""
        if invoice.get('notes'):
            notes = f"""
            <div class="notes">
                <div class="notes-title">Notes:</div>
                <div class="notes-content">{invoice['notes']}</div>
            </div>
            """
        
        footer = ""
        if template.get('footer'):
            footer = f'<div class="footer">{template["footer"]}</div>'
        
        return f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div class="header">
                    <div class="company-info">
                        {f'<img src="{template["logo"]}" class="logo">' if template.get('logo') else ''}
                        <div class="company-name">{template['company_info']['name']}</div>
                        <div class="address-info">
                            {template['company_info']['address']['line1']}<br/>
                            {template['company_info']['address'].get('line2', '') + '<br/>' if template['company_info']['address'].get('line2') else ''}
                            {template['company_info']['address']['city']}, {template['company_info']['address']['state']} {template['company_info']['address']['postal_code']}<br/>
                            {template['company_info']['address']['country']}<br/>
                            Email: {template['company_info']['email']}<br/>
                            {f"Phone: {template['company_info']['phone']}" if template['company_info'].get('phone') else ''}
                        </div>
                    </div>
                    <div class="invoice-details">
                        <div class="invoice-title">INVOICE</div>
                        <div class="invoice-info">
                            Invoice #: {invoice['invoice_number']}<br/>
                            Issue Date: {invoice['issue_date'].strftime('%Y-%m-%d')}<br/>
                            Due Date: {invoice['due_date'].strftime('%Y-%m-%d')}<br/>
                            {f"Paid Date: {invoice['paid_date'].strftime('%Y-%m-%d')}<br/>" if invoice.get('paid_date') else ''}
                            Status: {invoice['status'].upper()}
                        </div>
                    </div>
                </div>
                
                {billing_address}
                
                <table>
                    <thead>
                        <tr>
                            <th class="col-1">#</th>
                            <th>Description</th>
                            <th class="col-qty">Qty</th>
                            <th class="col-price">Price</th>
                            <th class="col-total">Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {line_items}
                    </tbody>
                </table>
                
                <div class="totals">
                    <div class="total-row">
                        <div class="total-label">Subtotal:</div>
                        <div class="total-amount">${invoice['subtotal']:.2f}</div>
                    </div>
                    {tax_details}
                    <div class="total-row grand-total">
                        <div class="total-label">Total:</div>
                        <div class="total-amount">${invoice['total']:.2f}</div>
                    </div>
                </div>
                
                {notes}
                
                {footer}
            </body>
        </html>
        """
    
    def get_css(self):
        return """
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 50px;
            color: #333;
        }
        .header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 50px;
        }
        .company-info {
            max-width: 300px;
        }
        .logo {
            max-width: 100px;
            margin-bottom: 20px;
        }
        .company-name {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .address-info {
            font-size: 12px;
            color: #666;
            line-height: 1.8;
        }
        .invoice-details {
            text-align: right;
        }
        .invoice-title {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .invoice-info {
            font-size: 12px;
            color: #666;
            line-height: 1.8;
        }
        .billing-address {
            margin-bottom: 50px;
        }
        .address-title {
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
        }
        th {
            background-color: #f5f5f5;
            padding: 10px;
            text-align: left;
            font-size: 12px;
            border-bottom: 2px solid #ddd;
        }
        td {
            padding: 10px;
            font-size: 12px;
            border-bottom: 1px solid #eee;
        }
        .col-1 { width: 50px; }
        .col-qty { width: 80px; }
        .col-price { width: 80px; }
        .col-total { width: 80px; }
        .totals {
            text-align: right;
            margin-bottom: 30px;
        }
        .total-row {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 10px;
        }
        .total-label {
            width: 200px;
            font-size: 12px;
            color: #666;
        }
        .total-amount {
            width: 100px;
            font-size: 12px;
        }
        .grand-total {
            font-weight: bold;
            font-size: 14px;
        }
        .notes {
            margin-bottom: 50px;
        }
        .notes-title {
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .notes-content {
            font-size: 12px;
            color: #666;
            line-height: 1.6;
        }
        .footer {
            text-align: center;
            font-size: 10px;
            color: #999;
            margin-top: 50px;
        }
        """
```

---

## Invoice Templates

### Template Management

```typescript
// template-manager.ts
import { InvoiceTemplate } from './invoice-model';
import { Pool } from 'pg';

export class InvoiceTemplateManager {
  constructor(private pool: Pool) {}
  
  async createTemplate(template: InvoiceTemplate): Promise<InvoiceTemplate> {
    const result = await this.pool.query(
      `INSERT INTO invoice_templates (name, logo, company_info, terms, footer, colors)
       VALUES ($1, $2, $3, $4, $5, $6)
       RETURNING *`,
      [
        template.name,
        template.logo,
        JSON.stringify(template.companyInfo),
        template.terms,
        template.footer,
        JSON.stringify(template.colors)
      ]
    );
    
    return this.mapRowToTemplate(result.rows[0]);
  }
  
  async getTemplate(id: string): Promise<InvoiceTemplate | null> {
    const result = await this.pool.query(
      'SELECT * FROM invoice_templates WHERE id = $1',
      [id]
    );
    
    if (result.rows.length === 0) return null;
    
    return this.mapRowToTemplate(result.rows[0]);
  }
  
  async getDefaultTemplate(): Promise<InvoiceTemplate | null> {
    const result = await this.pool.query(
      'SELECT * FROM invoice_templates WHERE is_default = true LIMIT 1'
    );
    
    if (result.rows.length === 0) return null;
    
    return this.mapRowToTemplate(result.rows[0]);
  }
  
  async updateTemplate(id: string, updates: Partial<InvoiceTemplate>): Promise<InvoiceTemplate> {
    const result = await this.pool.query(
      `UPDATE invoice_templates 
       SET name = COALESCE($1, name),
           logo = COALESCE($2, logo),
           company_info = COALESCE($3, company_info),
           terms = COALESCE($4, terms),
           footer = COALESCE($5, footer),
           colors = COALESCE($6, colors)
       WHERE id = $7
       RETURNING *`,
      [
        updates.name,
        updates.logo,
        updates.companyInfo ? JSON.stringify(updates.companyInfo) : null,
        updates.terms,
        updates.footer,
        updates.colors ? JSON.stringify(updates.colors) : null,
        id
      ]
    );
    
    return this.mapRowToTemplate(result.rows[0]);
  }
  
  async deleteTemplate(id: string): Promise<void> {
    await this.pool.query(
      'DELETE FROM invoice_templates WHERE id = $1',
      [id]
    );
  }
  
  async listTemplates(): Promise<InvoiceTemplate[]> {
    const result = await this.pool.query(
      'SELECT * FROM invoice_templates ORDER BY name'
    );
    
    return result.rows.map(row => this.mapRowToTemplate(row));
  }
  
  private mapRowToTemplate(row: any): InvoiceTemplate {
    return {
      id: row.id,
      name: row.name,
      logo: row.logo,
      companyInfo: JSON.parse(row.company_info),
      terms: row.terms,
      footer: row.footer,
      colors: JSON.parse(row.colors)
    };
  }
}

// SQL table
/*
CREATE TABLE invoice_templates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  logo TEXT,
  company_info JSONB NOT NULL,
  terms TEXT,
  footer TEXT,
  colors JSONB DEFAULT '{"primary":"#333333","secondary":"#666666","text":"#333333","background":"#ffffff"}',
  is_default BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
*/
```

---

## Line Items Calculation

### Line Item Calculator

```typescript
// line-item-calculator.ts
import { InvoiceLineItem } from './invoice-model';

export class LineItemCalculator {
  static calculateLineItem(
    description: string,
    quantity: number,
    unitPrice: number,
    taxRate?: number
  ): InvoiceLineItem {
    const amount = quantity * unitPrice;
    const taxAmount = taxRate ? amount * taxRate : 0;
    
    return {
      id: this.generateId(),
      description,
      quantity,
      unitPrice,
      amount,
      taxRate,
      taxAmount
    };
  }
  
  static calculateSubscriptionLineItem(
    planName: string,
    quantity: number,
    unitPrice: number,
    startDate: Date,
    endDate: Date,
    taxRate?: number
  ): InvoiceLineItem {
    const days = Math.ceil((endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24));
    const description = `${planName} (${days} days: ${startDate.toLocaleDateString()} - ${endDate.toLocaleDateString()})`;
    
    return this.calculateLineItem(description, quantity, unitPrice, taxRate);
  }
  
  static calculateProratedLineItem(
    planName: string,
    fullPrice: number,
    daysInPeriod: number,
    daysUsed: number,
    taxRate?: number
  ): InvoiceLineItem {
    const proratedPrice = (fullPrice / daysInPeriod) * daysUsed;
    const description = `${planName} (Prorated: ${daysUsed} of ${daysInPeriod} days)`;
    
    return this.calculateLineItem(description, 1, proratedPrice, taxRate);
  }
  
  static calculateUsageLineItem(
    metricName: string,
    quantity: number,
    unitPrice: number,
    period: string,
    taxRate?: number
  ): InvoiceLineItem {
    const description = `${metricName} usage (${period})`;
    
    return this.calculateLineItem(description, quantity, unitPrice, taxRate);
  }
  
  static calculateDiscountLineItem(
    description: string,
    amount: number
  ): InvoiceLineItem {
    return {
      id: this.generateId(),
      description,
      quantity: 1,
      unitPrice: -amount,
      amount: -amount
    };
  }
  
  static calculateCreditLineItem(
    description: string,
    amount: number
  ): InvoiceLineItem {
    return {
      id: this.generateId(),
      description,
      quantity: 1,
      unitPrice: -amount,
      amount: -amount
    };
  }
  
  static calculateLineItems(
    items: Array<{
      description: string;
      quantity: number;
      unitPrice: number;
      taxRate?: number
    }>
  ): InvoiceLineItem[] {
    return items.map(item =>
      this.calculateLineItem(
        item.description,
        item.quantity,
        item.unitPrice,
        item.taxRate
      )
    );
  }
  
  static calculateSubtotal(lineItems: InvoiceLineItem[]): number {
    return lineItems.reduce((sum, item) => sum + item.amount, 0);
  }
  
  private static generateId(): string {
    return `line_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
```

---

## Tax Calculation

### Tax Calculator

```typescript
// tax-calculator.ts
import { TaxDetails } from './invoice-model';

export interface TaxRate {
  name: string;
  rate: number;
  jurisdiction?: string;
  type: 'percentage' | 'fixed';
}

export class TaxCalculator {
  static calculateTax(
    amount: number,
    taxRates: TaxRate[]
  ): TaxDetails[] {
    return taxRates.map(taxRate => {
      const taxAmount = taxRate.type === 'percentage'
        ? amount * taxRate.rate
        : taxRate.rate;
      
      return {
        name: taxRate.name,
        rate: taxRate.rate,
        amount: taxAmount,
        jurisdiction: taxRate.jurisdiction
      };
    });
  }
  
  static calculateTotalTax(taxDetails: TaxDetails[]): number {
    return taxDetails.reduce((sum, tax) => sum + tax.amount, 0);
  }
  
  static calculateWithTax(
    subtotal: number,
    taxRates: TaxRate[]
  ): { subtotal: number; tax: number; total: number; taxDetails: TaxDetails[] } {
    const taxDetails = this.calculateTax(subtotal, taxRates);
    const tax = this.calculateTotalTax(taxDetails);
    const total = subtotal + tax;
    
    return { subtotal, tax, total, taxDetails };
  }
  
  static getTaxRatesForCountry(country: string, state?: string): TaxRate[] {
    // Simplified tax rate lookup
    const taxRates: Record<string, TaxRate[]> = {
      'US': [
        { name: 'Sales Tax', rate: 0.08, jurisdiction: 'US', type: 'percentage' }
      ],
      'CA': [
        { name: 'GST', rate: 0.05, jurisdiction: 'CA', type: 'percentage' },
        { name: 'PST', rate: 0.07, jurisdiction: 'CA', type: 'percentage' }
      ],
      'GB': [
        { name: 'VAT', rate: 0.20, jurisdiction: 'GB', type: 'percentage' }
      ],
      'DE': [
        { name: 'MwSt', rate: 0.19, jurisdiction: 'DE', type: 'percentage' }
      ]
    };
    
    return taxRates[country] || [];
  }
  
  static isTaxExempt(userId: string): boolean {
    // Implement tax exemption logic
    return false;
  }
}
```

---

## Invoice Numbering

### Invoice Number Generator

```typescript
// invoice-numbering.ts
import { Pool } from 'pg';

export class InvoiceNumberGenerator {
  constructor(private pool: Pool) {}
  
  async generateInvoiceNumber(prefix: string = 'INV'): Promise<string> {
    const result = await this.pool.query(
      `SELECT next_invoice_number FROM invoice_sequences WHERE prefix = $1 FOR UPDATE`,
      [prefix]
    );
    
    let nextNumber: number;
    
    if (result.rows.length === 0) {
      // Create new sequence
      nextNumber = 1;
      await this.pool.query(
        `INSERT INTO invoice_sequences (prefix, next_invoice_number) VALUES ($1, $2)`,
        [prefix, nextNumber + 1]
      );
    } else {
      nextNumber = result.rows[0].next_invoice_number;
      await this.pool.query(
        `UPDATE invoice_sequences SET next_invoice_number = next_invoice_number + 1 WHERE prefix = $1`,
        [prefix]
      );
    }
    
    return `${prefix}-${nextNumber.toString().padStart(6, '0')}`;
  }
  
  async generateInvoiceNumberWithDate(prefix: string = 'INV'): Promise<string> {
    const now = new Date();
    const year = now.getFullYear();
    const month = (now.getMonth() + 1).toString().padStart(2, '0');
    
    const result = await this.pool.query(
      `SELECT next_invoice_number FROM invoice_sequences 
       WHERE prefix = $1 AND year = $2 AND month = $3 FOR UPDATE`,
      [prefix, year, month]
    );
    
    let nextNumber: number;
    
    if (result.rows.length === 0) {
      nextNumber = 1;
      await this.pool.query(
        `INSERT INTO invoice_sequences (prefix, year, month, next_invoice_number) 
         VALUES ($1, $2, $3, $4)`,
        [prefix, year, month, nextNumber + 1]
      );
    } else {
      nextNumber = result.rows[0].next_invoice_number;
      await this.pool.query(
        `UPDATE invoice_sequences 
         SET next_invoice_number = next_invoice_number + 1 
         WHERE prefix = $1 AND year = $2 AND month = $3`,
        [prefix, year, month]
      );
    }
    
    return `${prefix}-${year}${month}-${nextNumber.toString().padStart(4, '0')}`;
  }
}

// SQL table
/*
CREATE TABLE invoice_sequences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  prefix VARCHAR(10) NOT NULL,
  year INTEGER,
  month INTEGER,
  next_invoice_number INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(prefix, year, month)
);
*/
```

---

## Storage and Retrieval

### Invoice Storage Service

```typescript
// invoice-storage.ts
import { Pool } from 'pg';
import { Invoice, InvoiceStatus } from './invoice-model';

export class InvoiceStorageService {
  constructor(private pool: Pool) {}
  
  async createInvoice(invoice: Omit<Invoice, 'id' | 'createdAt' | 'updatedAt'>): Promise<Invoice> {
    const result = await this.pool.query(
      `INSERT INTO invoices (
         invoice_number, user_id, subscription_id, status, issue_date, due_date, paid_date,
         subtotal, tax, total, currency, notes, metadata
       ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
       RETURNING *`,
      [
        invoice.invoiceNumber,
        invoice.userId,
        invoice.subscriptionId,
        invoice.status,
        invoice.issueDate,
        invoice.dueDate,
        invoice.paidDate,
        invoice.subtotal,
        invoice.tax,
        invoice.total,
        invoice.currency,
        invoice.notes,
        invoice.metadata ? JSON.stringify(invoice.metadata) : null
      ]
    );
    
    const createdInvoice = this.mapRowToInvoice(result.rows[0]);
    
    // Create line items
    for (const item of invoice.lineItems) {
      await this.createLineItem(createdInvoice.id, item);
    }
    
    // Create tax details
    for (const tax of invoice.taxDetails) {
      await this.createTaxDetail(createdInvoice.id, tax);
    }
    
    return createdInvoice;
  }
  
  async getInvoice(id: string): Promise<Invoice | null> {
    const result = await this.pool.query(
      'SELECT * FROM invoices WHERE id = $1',
      [id]
    );
    
    if (result.rows.length === 0) return null;
    
    const invoice = this.mapRowToInvoice(result.rows[0]);
    
    // Load line items
    invoice.lineItems = await this.getLineItems(id);
    
    // Load tax details
    invoice.taxDetails = await this.getTaxDetails(id);
    
    return invoice;
  }
  
  async getInvoiceByNumber(invoiceNumber: string): Promise<Invoice | null> {
    const result = await this.pool.query(
      'SELECT * FROM invoices WHERE invoice_number = $1',
      [invoiceNumber]
    );
    
    if (result.rows.length === 0) return null;
    
    const invoice = this.mapRowToInvoice(result.rows[0]);
    invoice.lineItems = await this.getLineItems(invoice.id);
    invoice.taxDetails = await this.getTaxDetails(invoice.id);
    
    return invoice;
  }
  
  async updateInvoiceStatus(id: string, status: InvoiceStatus): Promise<void> {
    await this.pool.query(
      'UPDATE invoices SET status = $1 WHERE id = $2',
      [status, id]
    );
  }
  
  async markInvoiceAsPaid(id: string, paidDate: Date = new Date()): Promise<void> {
    await this.pool.query(
      'UPDATE invoices SET status = $1, paid_date = $2 WHERE id = $3',
      [InvoiceStatus.PAID, paidDate, id]
    );
  }
  
  async listInvoicesByUser(
    userId: string,
    limit: number = 50,
    offset: number = 0
  ): Promise<Invoice[]> {
    const result = await this.pool.query(
      `SELECT * FROM invoices 
       WHERE user_id = $1 
       ORDER BY issue_date DESC 
       LIMIT $2 OFFSET $3`,
      [userId, limit, offset]
    );
    
    const invoices = result.rows.map(row => this.mapRowToInvoice(row));
    
    // Load line items and tax details for each invoice
    for (const invoice of invoices) {
      invoice.lineItems = await this.getLineItems(invoice.id);
      invoice.taxDetails = await this.getTaxDetails(invoice.id);
    }
    
    return invoices;
  }
  
  async getOverdueInvoices(): Promise<Invoice[]> {
    const result = await this.pool.query(
      `SELECT * FROM invoices 
       WHERE status = $1 AND due_date < NOW()
       ORDER BY due_date ASC`,
      [InvoiceStatus.SENT]
    );
    
    const invoices = result.rows.map(row => this.mapRowToInvoice(row));
    
    for (const invoice of invoices) {
      invoice.lineItems = await this.getLineItems(invoice.id);
      invoice.taxDetails = await this.getTaxDetails(invoice.id);
    }
    
    return invoices;
  }
  
  private async createLineItem(invoiceId: string, item: any): Promise<void> {
    await this.pool.query(
      `INSERT INTO invoice_line_items (invoice_id, description, quantity, unit_price, amount, tax_rate, tax_amount, metadata)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`,
      [
        invoiceId,
        item.description,
        item.quantity,
        item.unitPrice,
        item.amount,
        item.taxRate,
        item.taxAmount,
        item.metadata ? JSON.stringify(item.metadata) : null
      ]
    );
  }
  
  private async createTaxDetail(invoiceId: string, tax: any): Promise<void> {
    await this.pool.query(
      `INSERT INTO invoice_tax_details (invoice_id, name, rate, amount, jurisdiction)
       VALUES ($1, $2, $3, $4, $5)`,
      [invoiceId, tax.name, tax.rate, tax.amount, tax.jurisdiction]
    );
  }
  
  private async getLineItems(invoiceId: string): Promise<any[]> {
    const result = await this.pool.query(
      'SELECT * FROM invoice_line_items WHERE invoice_id = $1',
      [invoiceId]
    );
    
    return result.rows.map(row => ({
      id: row.id,
      description: row.description,
      quantity: row.quantity,
      unitPrice: row.unit_price,
      amount: row.amount,
      taxRate: row.tax_rate,
      taxAmount: row.tax_amount,
      metadata: row.metadata ? JSON.parse(row.metadata) : null
    }));
  }
  
  private async getTaxDetails(invoiceId: string): Promise<any[]> {
    const result = await this.pool.query(
      'SELECT * FROM invoice_tax_details WHERE invoice_id = $1',
      [invoiceId]
    );
    
    return result.rows.map(row => ({
      name: row.name,
      rate: row.rate,
      amount: row.amount,
      jurisdiction: row.jurisdiction
    }));
  }
  
  private mapRowToInvoice(row: any): Invoice {
    return {
      id: row.id,
      invoiceNumber: row.invoice_number,
      userId: row.user_id,
      subscriptionId: row.subscription_id,
      status: row.status,
      issueDate: row.issue_date,
      dueDate: row.due_date,
      paidDate: row.paid_date,
      subtotal: row.subtotal,
      tax: row.tax,
      total: row.total,
      currency: row.currency,
      lineItems: [],
      taxDetails: [],
      notes: row.notes,
      metadata: row.metadata ? JSON.parse(row.metadata) : null,
      createdAt: row.created_at,
      updatedAt: row.updated_at
    };
  }
}

// SQL tables
/*
CREATE TABLE invoices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_number VARCHAR(50) UNIQUE NOT NULL,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  subscription_id UUID REFERENCES subscriptions(id) ON DELETE SET NULL,
  status VARCHAR(20) NOT NULL CHECK (status IN ('draft', 'sent', 'viewed', 'paid', 'overdue', 'cancelled', 'refunded')),
  issue_date TIMESTAMP NOT NULL,
  due_date TIMESTAMP NOT NULL,
  paid_date TIMESTAMP,
  subtotal DECIMAL(10, 2) NOT NULL,
  tax DECIMAL(10, 2) NOT NULL,
  total DECIMAL(10, 2) NOT NULL,
  currency VARCHAR(3) DEFAULT 'USD',
  notes TEXT,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE invoice_line_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_id UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
  description TEXT NOT NULL,
  quantity INTEGER NOT NULL,
  unit_price DECIMAL(10, 2) NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  tax_rate DECIMAL(5, 4),
  tax_amount DECIMAL(10, 2),
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE invoice_tax_details (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_id UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  rate DECIMAL(5, 4) NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  jurisdiction VARCHAR(255)
);
*/
```

---

## Email Delivery

### Email Service

```typescript
// invoice-email-service.ts
import nodemailer from 'nodemailer';
import { Invoice } from './invoice-model';

export class InvoiceEmailService {
  private transporter: nodemailer.Transporter;
  
  constructor() {
    this.transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST,
      port: parseInt(process.env.SMTP_PORT || '587'),
      secure: false,
      auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS
      }
    });
  }
  
  async sendInvoice(
    invoice: Invoice,
    recipientEmail: string,
    pdfPath: string
  ): Promise<void> {
    const subject = `Invoice ${invoice.invoiceNumber} from ${invoice.metadata?.companyName || 'Our Company'}`;
    const html = this.generateEmailBody(invoice);
    
    await this.transporter.sendMail({
      from: process.env.SMTP_FROM,
      to: recipientEmail,
      subject,
      html,
      attachments: [
        {
          filename: `Invoice_${invoice.invoiceNumber}.pdf`,
          path: pdfPath
        }
      ]
    });
  }
  
  async sendInvoiceReminder(
    invoice: Invoice,
    recipientEmail: string,
    pdfPath: string
  ): Promise<void> {
    const subject = `Reminder: Invoice ${invoice.invoiceNumber} is due`;
    const html = this.generateReminderEmailBody(invoice);
    
    await this.transporter.sendMail({
      from: process.env.SMTP_FROM,
      to: recipientEmail,
      subject,
      html,
      attachments: [
        {
          filename: `Invoice_${invoice.invoiceNumber}.pdf`,
          path: pdfPath
        }
      ]
    });
  }
  
  async sendOverdueNotice(
    invoice: Invoice,
    recipientEmail: string,
    pdfPath: string
  ): Promise<void> {
    const subject = `Overdue: Invoice ${invoice.invoiceNumber}`;
    const html = this.generateOverdueEmailBody(invoice);
    
    await this.transporter.sendMail({
      from: process.env.SMTP_FROM,
      to: recipientEmail,
      subject,
      html,
      attachments: [
        {
          filename: `Invoice_${invoice.invoiceNumber}.pdf`,
          path: pdfPath
        }
      ]
    });
  }
  
  private generateEmailBody(invoice: Invoice): string {
    return `
      <html>
        <body>
          <h2>Invoice ${invoice.invoiceNumber}</h2>
          <p>Dear Customer,</p>
          <p>Please find attached your invoice for the billing period ${invoice.issueDate.toLocaleDateString()}.</p>
          <p><strong>Invoice Details:</strong></p>
          <ul>
            <li>Invoice Number: ${invoice.invoiceNumber}</li>
            <li>Issue Date: ${invoice.issueDate.toLocaleDateString()}</li>
            <li>Due Date: ${invoice.dueDate.toLocaleDateString()}</li>
            <li>Total Amount: ${invoice.currency} ${invoice.total.toFixed(2)}</li>
          </ul>
          <p>Please pay by the due date to avoid any late fees.</p>
          <p>If you have any questions, please contact us.</p>
          <p>Thank you for your business!</p>
        </body>
      </html>
    `;
  }
  
  private generateReminderEmailBody(invoice: Invoice): string {
    return `
      <html>
        <body>
          <h2>Reminder: Invoice ${invoice.invoiceNumber}</h2>
          <p>Dear Customer,</p>
          <p>This is a friendly reminder that invoice ${invoice.invoiceNumber} is due on ${invoice.dueDate.toLocaleDateString()}.</p>
          <p><strong>Invoice Details:</strong></p>
          <ul>
            <li>Invoice Number: ${invoice.invoiceNumber}</li>
            <li>Issue Date: ${invoice.issueDate.toLocaleDateString()}</li>
            <li>Due Date: ${invoice.dueDate.toLocaleDateString()}</li>
            <li>Total Amount: ${invoice.currency} ${invoice.total.toFixed(2)}</li>
          </ul>
          <p>Please ensure payment is made by the due date.</p>
          <p>Thank you!</p>
        </body>
      </html>
    `;
  }
  
  private generateOverdueEmailBody(invoice: Invoice): string {
    return `
      <html>
        <body>
          <h2>Overdue: Invoice ${invoice.invoiceNumber}</h2>
          <p>Dear Customer,</p>
          <p>Invoice ${invoice.invoiceNumber} is now overdue. The due date was ${invoice.dueDate.toLocaleDateString()}.</p>
          <p><strong>Invoice Details:</strong></p>
          <ul>
            <li>Invoice Number: ${invoice.invoiceNumber}</li>
            <li>Issue Date: ${invoice.issueDate.toLocaleDateString()}</li>
            <li>Due Date: ${invoice.dueDate.toLocaleDateString()}</li>
            <li>Total Amount: ${invoice.currency} ${invoice.total.toFixed(2)}</li>
          </ul>
          <p>Please make payment as soon as possible to avoid service interruption.</p>
          <p>If you have already paid, please disregard this notice.</p>
          <p>Thank you!</p>
        </body>
      </html>
    `;
  }
}
```

---

## Invoice Status Tracking

### Status Tracker

```typescript
// invoice-status-tracker.ts
import { InvoiceStatus } from './invoice-model';
import { Pool } from 'pg';

export class InvoiceStatusTracker {
  constructor(private pool: Pool) {}
  
  async trackStatusChange(
    invoiceId: string,
    oldStatus: InvoiceStatus,
    newStatus: InvoiceStatus,
    metadata?: Record<string, any>
  ): Promise<void> {
    await this.pool.query(
      `INSERT INTO invoice_status_history (invoice_id, old_status, new_status, metadata, changed_at)
       VALUES ($1, $2, $3, $4, NOW())`,
      [invoiceId, oldStatus, newStatus, metadata ? JSON.stringify(metadata) : null]
    );
  }
  
  async getStatusHistory(invoiceId: string): Promise<any[]> {
    const result = await this.pool.query(
      `SELECT * FROM invoice_status_history 
       WHERE invoice_id = $1 
       ORDER BY changed_at ASC`,
      [invoiceId]
    );
    
    return result.rows;
  }
  
  async updateInvoiceStatus(
    invoiceId: string,
    newStatus: InvoiceStatus,
    metadata?: Record<string, any>
  ): Promise<void> {
    const result = await this.pool.query(
      'SELECT status FROM invoices WHERE id = $1',
      [invoiceId]
    );
    
    if (result.rows.length === 0) {
      throw new Error('Invoice not found');
    }
    
    const oldStatus = result.rows[0].status;
    
    await this.pool.query(
      'UPDATE invoices SET status = $1 WHERE id = $2',
      [newStatus, invoiceId]
    );
    
    await this.trackStatusChange(invoiceId, oldStatus, newStatus, metadata);
  }
  
  async markAsSent(invoiceId: string): Promise<void> {
    await this.updateInvoiceStatus(invoiceId, InvoiceStatus.SENT, {
      method: 'email'
    });
  }
  
  async markAsViewed(invoiceId: string): Promise<void> {
    await this.updateInvoiceStatus(invoiceId, InvoiceStatus.VIEWED);
  }
  
  async markAsPaid(invoiceId: string, paymentMethod: string): Promise<void> {
    await this.pool.query(
      `UPDATE invoices 
       SET status = $1, paid_date = NOW() 
       WHERE id = $2`,
      [InvoiceStatus.PAID, invoiceId]
    );
    
    await this.updateInvoiceStatus(invoiceId, InvoiceStatus.PAID, {
      payment_method: paymentMethod
    });
  }
  
  async markAsOverdue(invoiceId: string): Promise<void> {
    await this.updateInvoiceStatus(invoiceId, InvoiceStatus.OVERDUE);
  }
}

// SQL table
/*
CREATE TABLE invoice_status_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_id UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
  old_status VARCHAR(20),
  new_status VARCHAR(20) NOT NULL,
  metadata JSONB,
  changed_at TIMESTAMP DEFAULT NOW()
);
*/
```

---

## Customization

### Custom Invoice Builder

```typescript
// custom-invoice-builder.ts
import { Invoice, InvoiceTemplate } from './invoice-model';

export class CustomInvoiceBuilder {
  private invoice: Partial<Invoice> = {};
  private template: Partial<InvoiceTemplate> = {};
  
  setInvoiceNumber(number: string): this {
    this.invoice.invoiceNumber = number;
    return this;
  }
  
  setUserId(userId: string): this {
    this.invoice.userId = userId;
    return this;
  }
  
  setSubscriptionId(subscriptionId: string): this {
    this.invoice.subscriptionId = subscriptionId;
    return this;
  }
  
  setIssueDate(date: Date): this {
    this.invoice.issueDate = date;
    return this;
  }
  
  setDueDate(date: Date): this {
    this.invoice.dueDate = date;
    return this;
  }
  
  setCurrency(currency: string): this {
    this.invoice.currency = currency;
    return this;
  }
  
  addLineItem(item: any): this {
    if (!this.invoice.lineItems) {
      this.invoice.lineItems = [];
    }
    this.invoice.lineItems.push(item);
    return this;
  }
  
  setNotes(notes: string): this {
    this.invoice.notes = notes;
    return this;
  }
  
  setMetadata(metadata: Record<string, any>): this {
    this.invoice.metadata = metadata;
    return this;
  }
  
  setTemplateName(name: string): this {
    this.template.name = name;
    return this;
  }
  
  setLogo(logo: string): this {
    this.template.logo = logo;
    return this;
  }
  
  setCompanyInfo(companyInfo: any): this {
    this.template.companyInfo = companyInfo;
    return this;
  }
  
  setTerms(terms: string): this {
    this.template.terms = terms;
    return this;
  }
  
  setFooter(footer: string): this {
    this.template.footer = footer;
    return this;
  }
  
  setColors(colors: any): this {
    this.template.colors = colors;
    return this;
  }
  
  build(): { invoice: Invoice; template: InvoiceTemplate } {
    // Calculate totals
    const subtotal = this.invoice.lineItems?.reduce((sum, item) => sum + item.amount, 0) || 0;
    
    // Calculate tax (simplified)
    const taxRate = 0.10; // 10% tax
    const tax = subtotal * taxRate;
    const total = subtotal + tax;
    
    const taxDetails = [
      {
        name: 'Sales Tax',
        rate: taxRate,
        amount: tax
      }
    ];
    
    return {
      invoice: {
        id: '',
        invoiceNumber: this.invoice.invoiceNumber || '',
        userId: this.invoice.userId || '',
        subscriptionId: this.invoice.subscriptionId,
        status: InvoiceStatus.DRAFT,
        issueDate: this.invoice.issueDate || new Date(),
        dueDate: this.invoice.dueDate || new Date(),
        paidDate: undefined,
        subtotal,
        tax,
        total,
        currency: this.invoice.currency || 'USD',
        lineItems: this.invoice.lineItems || [],
        taxDetails,
        notes: this.invoice.notes,
        metadata: this.invoice.metadata,
        createdAt: new Date(),
        updatedAt: new Date()
      },
      template: {
        id: '',
        name: this.template.name || 'Default',
        logo: this.template.logo,
        companyInfo: this.template.companyInfo || {
          name: 'Company Name',
          address: {
            line1: '123 Main St',
            city: 'San Francisco',
            state: 'CA',
            postalCode: '94107',
            country: 'US'
          },
          email: 'info@company.com'
        },
        terms: this.template.terms,
        footer: this.template.footer,
        colors: this.template.colors || {
          primary: '#333333',
          secondary: '#666666',
          text: '#333333',
          background: '#ffffff'
        }
      }
    };
  }
}
```

---

## Compliance Requirements

```markdown
## Invoice Compliance Checklist

### General Requirements
- [ ] Unique invoice number
- [ ] Invoice date (issue date)
- [ ] Due date
- [ ] Clear itemization of goods/services
- [ ] Quantities and unit prices
- [ ] Subtotal, taxes, and total
- [ ] Currency clearly stated
- [ ] Company name and address
- [ ] Customer name and address
- [ ] Tax registration numbers (VAT/GST)
- [ ] Payment terms and conditions

### Regional Compliance

#### United States
- [ ] Sales tax identification number
- [ ] State-specific tax requirements
- [ ] Federal tax ID (EIN)
- [ ] Payment terms clearly stated
- [ ] Late fee disclosure

#### European Union (VAT)
- [ ] VAT number of seller
- [ ] VAT number of buyer (for B2B)
- [ ] VAT rate applied
- [ ] Place of supply
- [ ] Reverse charge mechanism (if applicable)
- [ ] Invoice storage period (10 years)

#### Canada (GST/HST)
- [ ] GST/HST registration number
- [ ] Provincial tax requirements
- [ ] Tax breakdown by province
- [ ] Invoice storage period (6 years)

#### Australia (GST)
- [ ] ABN (Australian Business Number)
- [ ] GST amount clearly stated
- [ ] GST-inclusive pricing
- [ ] Invoice storage period (5 years)

### Digital Invoice Requirements
- [ ] PDF format with digital signature
- [ ] Tamper-evident format
- [ ] Secure delivery method
- [ ] Delivery confirmation
- [ ] Read receipt tracking

### Accessibility
- [ ] Screen reader compatible
- [ ] High contrast colors
- [ ] Clear font sizes
- [ ] Alternative text for images
- [ ] Structured data format

### Data Protection
- [ ] GDPR compliance (EU)
- [ ] PII protection
- [ ] Secure storage
- [ ] Access controls
- [ ] Data retention policies
```

---

## Additional Resources

- [PDFKit Documentation](https://pdfkit.org/)
- [Puppeteer Documentation](https://pptr.dev/)
- [ReportLab Documentation](https://www.reportlab.com/)
- [WeasyPrint Documentation](https://weasyprint.org/)
- [Invoice Compliance Guide](https://www.invoicehome.com/invoice-compliance/)
