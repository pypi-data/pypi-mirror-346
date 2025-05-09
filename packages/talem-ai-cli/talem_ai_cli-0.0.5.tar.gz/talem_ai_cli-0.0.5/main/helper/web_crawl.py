import requests
from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfReader

filename = "source.pdf"

def crawler(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

    soup = BeautifulSoup(response.text, 'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text(separator='\n', strip=True)

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 50

    for line in text.splitlines():
        if y < 50:
            c.showPage()
            y = height - 50
        c.drawString(50, y, line[:90])  # Limit line width
        y -= 15

    c.save()
