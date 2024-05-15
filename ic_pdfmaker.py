from reportlab.pdfgen import canvas 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase import pdfmetrics 
from reportlab.lib import colors 
import os
from datetime import datetime
from fetcher import Fetch
import string

fetch = Fetch()
try:
    class IcPdfMaker:
        def __init__(self) -> None:
            print('IcPdf running')
        
        def lspacer(self, amt=4):
            return ' '*amt

        def add_footer(self, pdf, nums):
            page_number = pdf.getPageNumber()
            pdf.setFont("Helvetica", 10)
            pdf.drawCentredString(300, 15, f"[ITEM CRATE MaG] Factura #{nums} @ {os.getlogin()} | Pg.{page_number}")

        def makePdf(self):
            directory = "Log Facturas"

            current_datetime = datetime.now()
            day_shortened = current_datetime.strftime("%a")
            month_shortened = current_datetime.strftime("%B")
            formatted_time = current_datetime.strftime("%I:%M %p")

            if not os.path.exists(directory):
                os.makedirs(directory)

            all_items = os.listdir(directory)
            num_items = len(all_items)

            pdf_filename = f"ItemCrate_FACTURA({num_items})[{month_shortened},{day_shortened}{current_datetime.day},{current_datetime.year}].pdf"
            pdf_file_path = os.path.join(directory, pdf_filename)

            inv_items: dict = fetch.get_allContent().items()
            title = f"Item Crate Factura #{num_items}"

            pdf = canvas.Canvas(pdf_file_path)
            pdf.setTitle(pdf_filename)
            pdf.setFont('Helvetica-Bold', 25)
            pdf.drawCentredString(300, 770, title)
            pdf.setFont("Helvetica", 14)
            pdf.drawCentredString(300, 745, f"{day_shortened} {current_datetime.day} of {month_shortened}, {current_datetime.year} @ {formatted_time}")
            pdf.setFont("Helvetica", 12)
            pdf.drawCentredString(300, 723, f"AUTH: {os.getlogin()}")
            pdf.line(30, 710, 550, 710)

            start_info = pdf.beginText(40, 662)
            start_info.setFont("Helvetica", 18)
            start_info.textLine(f"Total Items: {str(fetch.get_keysAmount())}")
            pdf.drawText(start_info)

            text = pdf.beginText(40, 635)
            text.setFont("Helvetica", 15)

            for item_name, item_details in inv_items:
                if item_name != 'ITEM_ORIGIN':
                    text.textLine()
                    text.setFont("Helvetica-Bold", 17)
                    text.textLine(item_name)
                    text.setFont("Helvetica", 15)
                    text.textLine(f"'{item_details['description']}'")

                    for wildcard in ['sizes', 'colors', 'quantity']:
                        try:
                            if item_details[wildcard] is not None:
                                if wildcard != 'sizes':
                                    text.setFont("Helvetica-Oblique", 15)
                                    text.textLine(f">{self.lspacer(2)}{string.capwords(wildcard)}:")
                                    text.setFont("Helvetica", 15)
                                    text.textLine(f'''{self.lspacer(8)}{str(item_details[wildcard]).replace("'", '').replace('[', '').replace(']', '')}''')
                        except:
                            pass
                    text.textLine()

                    if text.getY() < 50:
                        pdf.drawText(text)
                        self.add_footer(pdf, num_items)
                        pdf.showPage()
                        text = pdf.beginText(40, 800)
                        text.setFont("Helvetica", 15)

            pdf.drawText(text)
            self.add_footer(pdf, num_items)
            pdf.save()
except Exception as e:
    print(e)
    input('Press enter to continue...')
