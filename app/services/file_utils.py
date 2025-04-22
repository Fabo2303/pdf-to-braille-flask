def save_text_to_file(text, output_file):
    """
    Guarda el texto extraído en un archivo.
    :param text: Lista de textos extraídos.
    :param output_file: Ruta al archivo de salida.
    """
    try:
        output_file = 'uploads/text/' + output_file
        with open(output_file, 'w', encoding='utf-8') as f:
            for page_text in text:
                f.write(page_text + '\n\n')
        print(f"Texto extraído guardado en {output_file}")
    except Exception as e:
        print(f"Error al guardar el texto en el archivo: {e}")
    
def save_braille_to_file(braille_text, output_file):
    """
    Guarda el texto en Braille en un archivo.
    :param braille_text: Texto en Braille.
    :param output_file: Ruta al archivo de salida.
    """
    try:
        output_file = 'uploads/braille/' + output_file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(braille_text)
        print(f"Texto en Braille guardado en {output_file}")
    except Exception as e:
        print(f"Error al guardar el texto en el archivo: {e}")
    
    