import streamlit as st
from PIL import Image
import pytesseract
import pdfplumber
import io

st.title("Extraktor údajů z výpisu z KN")

uploaded_file = st.file_uploader("Nahraj výpis z KN (PDF nebo obrázek)", type=["pdf", "png", "jpg", "jpeg"])

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

def extract_text_from_image(file):
    image = Image.open(file)
    return pytesseract.image_to_string(image, lang='ces')

if uploaded_file:
    file_type = uploaded_file.type

    if "pdf" in file_type:
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = extract_text_from_image(uploaded_file)

    st.subheader("Extrahovaný text")
    st.text_area("Výpis", value=text, height=300)

    if st.button("Vygeneruj prompt pro ChatGPT"):
        prompt = f"""
Z následujícího textu výpisu z katastru nemovitostí prosím extrahuj tyto údaje:

- Parcelní číslo
- Druh pozemku
- Výměra
- Vlastník
- Číslo LV
- Katastrální území

Text výpisu:
{text}
"""
        st.subheader("Prompt pro ChatGPT")
        st.text_area("Prompt", value=prompt, height=400)
