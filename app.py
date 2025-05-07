import streamlit as st
from PIL import Image
import pytesseract
import pdfplumber
import io

st.title("Extraktor údajů z výpisu z KN")

uploaded_file = st.file_uploader("Nahraj výpis z KN (PDF nebo obrázek)", type=["pdf", "png", "jpg", "jpeg"])

def extract_text_from_image(image):
    return pytesseract.image_to_string(image, lang='ces')

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            # OCR fallback: převede stránku na obrázek a použije pytesseract
            image = page.to_image(resolution=300).original
            text += extract_text_from_image(image) + "\n"
    return text

if uploaded_file:
    file_type = uploaded_file.type

    if "pdf" in file_type:
        text = extract_text_from_pdf(uploaded_file)
    else:
        image = Image.open(uploaded_file)
        text = extract_text_from_image(image)

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
