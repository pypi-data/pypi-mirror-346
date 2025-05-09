import pandas as pd
import glob
import os
from fpdf import FPDF
from pathlib import Path

def generate_invoice_pdf(invoice_path, pdf_path, image_path, product_id, product_name, amount_purchased, price_per_unit, total_price):
        """
        Convert Excel invoices to PDF format.
        """
        filepaths = glob.glob(f"{invoice_path}/*.xlsx")

        for filepath in filepaths:
                pdf = FPDF(orientation="P", unit="mm", format="A4")
                pdf.add_page()

                filename = Path(filepath).stem
                invoice_no, date = filename.split("-")

                pdf.set_font(family="Times", size=16, style="B")
                pdf.cell(w=50, h=8, txt=f"Invoice no. {invoice_no}", ln=1)

                pdf.set_font(family="Times", size=16, style="B")
                pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)
                
                df = pd.read_excel(filepath, sheet_name="Sheet 1")

                # Header in the table
                columns = df.columns
                columns = [item.replace("_", " ").title() for item in columns]
                pdf.set_font(family="Times", size=10, style="B")
                pdf.set_text_color(80, 80, 80)
                pdf.cell(w=30, h=8, txt=columns[0], border=1)
                pdf.cell(w=70, h=8, txt=columns[1], border=1)
                pdf.cell(w=30, h=8, txt=columns[2], border=1)
                pdf.cell(w=30, h=8, txt=columns[3], border=1)
                pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

                # Rows in the table
                for index, row in df.iterrows():
                        pdf.set_font(family="Times", size=10)
                        pdf.set_text_color(80, 80, 80)
                        pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
                        pdf.cell(w=70, h=8, txt=str(row[product_name]), border=1)
                        pdf.cell(w=30, h=8, txt=str(row[amount_purchased]), border=1)
                        pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
                        pdf.cell(w=30, h=8, txt=str(row[total_price]), border=1, ln=1)
                
                total_sum = df[total_price].sum()

                pdf.set_font(family="Times", size=10)
                pdf.set_text_color(80, 80, 80)
                pdf.cell(w=30, h=8, txt="", border=1)
                pdf.cell(w=70, h=8, txt="", border=1)
                pdf.cell(w=30, h=8, txt="", border=1)
                pdf.cell(w=30, h=8, txt="", border=1)
                pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)

                # Total sum sentence
                pdf.set_font(family="Times", size=10)
                pdf.cell(w=30, h=8, txt=f"The total price of this order is {total_sum}", ln=1)

                # Company name and logo
                pdf.set_font(family="Times", size=14, style="B")
                pdf.cell(w=25, h=8, txt=f"PythonHow")
                pdf.image(image_path, w=10)

                if not os.path.exists(pdf_path):   
                        os.mkdir(pdf_path)
                pdf.output(f"{pdf_path}/{filename}.pdf")