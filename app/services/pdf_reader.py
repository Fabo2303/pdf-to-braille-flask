import fitz  # PyMuPDF
from app.services.file_utils import save_text_to_file
from PIL import Image
import pytesseract
import io
import os
import re

# Especifica la ruta al ejecutable de Tesseract (solo en Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def convert_pdf_to_images(pdf_path, zoom=2):
    """
    Convierte cada página del PDF en una imagen con una calidad mejorada.
    :param pdf_path: Ruta al archivo PDF.
    :param zoom: Factor de zoom para mejorar la calidad de la imagen (por defecto 2).
    :return: Lista de imágenes (PIL.Image).
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"El archivo PDF no existe: {pdf_path}")

    try:
        # Abre el PDF
        pdf_document = fitz.open(pdf_path)
        images = []
        
        # Itera sobre cada página del PDF
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            
            # Define la matriz de transformación para mejorar la calidad de la imagen
            mat = fitz.Matrix(zoom, zoom)  # Aumenta la resolución
            
            # Renderiza la página como una imagen (PNG)
            pix = page.get_pixmap(matrix=mat)
            image = Image.open(io.BytesIO(pix.tobytes()))
            images.append(image)

        return images
    except Exception as e:
        print(f"Error al convertir el PDF a imágenes: {e}")
        return []


def ocr_on_images(images):
    """
    Aplica OCR a una lista de imágenes.
    :param images: Lista de imágenes (PIL.Image).
    :return: Lista de textos extraídos.
    """
    if not images:
        print("No hay imágenes para procesar.")
        return []

    extracted_text = []
    
    for image in images:
        try:
            # Preprocesamiento de la imagen (opcional)
            image = image.convert('L')  # Convertir a escala de grises
            image = image.point(lambda x: 0 if x < 128 else 255)  # Binarización

            # Aplicar OCR
            text = pytesseract.image_to_string(image, lang='spa')
            extracted_text.append(text)
        except Exception as e:
            print(f"Error al aplicar OCR a la imagen: {e}")
            extracted_text.append("")

    return extracted_text


def remove_accents(text):
        """
        Elimina las tildes de las vocales.
        :param text: Texto con tildes.
        :return: Texto sin tildes.
        """
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'
        }
        for key, value in replacements.items():
            text = text.replace(key, value)
        return text


def clean_text(extracted_text):
    """
    Limpia el texto extraído eliminando caracteres no deseados y arreglando el encoding.
    :param extracted_text: Lista de textos extraídos (OCR).
    :return: Texto limpio y legible.
    """
    cleaned_text = []

    for page_text in extracted_text:

        page_text = remove_accents(page_text)
        page_text = re.sub(r'[^\w\sñÑ.,;:¿?¡!()\-"\']', '', page_text)

        page_text = re.sub(r'\n+', '\n', page_text)
        page_text = re.sub(r'\s+', ' ', page_text).strip()
        
        cleaned_text.append(page_text)

    return cleaned_text


def extract_text_from_pdf(pdf_path, output_file='texto_extraido.txt', zoom=2):
    """
    Extrae texto de un PDF (escaneado) utilizando OCR y lo guarda en un archivo.
    :param pdf_path: Ruta al archivo PDF.
    :param output_file: Ruta al archivo de salida donde se guardará el texto (por defecto 'texto_extraido.txt').
    :param zoom: Factor de zoom para mejorar la calidad de las imágenes convertidas del PDF.
    """
    # Convertir el PDF a imágenes
    images = convert_pdf_to_images(pdf_path, zoom)
    
    # Si la conversión fue exitosa, aplicar OCR
    if images:
        extracted_text = ocr_on_images(images)
        cleaned_text = clean_text(extracted_text)
        save_text_to_file(cleaned_text, output_file)
        return cleaned_text
    else:
        print(f"Hubo un error al convertir el PDF a imágenes, no se pudo extraer texto.")
