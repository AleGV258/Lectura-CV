from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(file_name):
    # Crea un objeto Canvas para el archivo PDF
    c = canvas.Canvas(file_name, pagesize=letter)

    # Agrega texto al PDF
    text = "¡Hola, este es un documento PDF generado con Python y reportlab!"
    c.drawString(100, 700, text)

    # Guarda el PDF
    c.save()

if __name__ == "__main__":
    pdf_file = "./datashets/ejemplo.pdf"
    create_pdf(pdf_file)
    print(f"PDF generado: {pdf_file}")