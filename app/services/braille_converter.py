from app.services.file_utils import save_braille_to_file

# Diccionario con mapeo de caracteres al Braille
braille_map = {
    # Letras básicas (igual que en inglés)
    'a': '100000', 'b': '101000', 'c': '110000', 'd': '110100', 'e': '100100',
    'f': '111000', 'g': '111100', 'h': '101100', 'i': '011000', 'j': '011100',
    'k': '100010', 'l': '101010', 'm': '110010', 'n': '110110', 'o': '100110', 
    'p': '111010', 'q': '111110', 'r': '101110', 's': '011010', 't': '011110', 
    'u': '100011', 'v': '101011', 'w': '011101', 'x': '110011','y': '110111', 
    'z': '100111',
    
    # Números (precedidos por ⠼)
    '1': '100000', '2': '101000', '3': '110000', '4': '110100', '5': '100100',
    '6': '111000', '7': '111100', '8': '101100', '9': '011000', '0': '011100',
    
    # Signos de puntuación y especiales
    ' ': '000000', '\n': '000000',
    '.': '000010', ',': '001000', ';': '001010', ':': '001100',
    '!': '001110', '¡': '001110', '?': '001001', '¿': '001001',
    '(': '101001', ')': '010110', '+': '001110', 'X': '001011',
    '-': '000011', '=': '001111',
    
    # Caracteres específicos del español
    'á': '101111', 'é': '011011', 'í': '010010',
    'ó': '010011', 'ú': '011111', 'ü': '101101',
    'ñ': '111101',
    
    # Signos compuestos (necesarios antes de letras mayúsculas y números)
    'mayúscula': '010001',  # Prefijo para mayúsculas
    'número': '010111',     # Prefijo para números
}

def text_to_braille(text : str, filename: str = 'braille_output.txt') -> str:
    """
    Convierte texto a Braille utilizando el diccionario braille_map.
    :param text: Texto a convertir.
    :return: Texto en Braille.
    """
    braille_text = ''
    
    for char in text.lower():
        if char in braille_map:
            braille_text += braille_map[char] + ' '  # Concatenar Braille por cada carácter
        else:
            braille_text += '000000 '  # Si no se encuentra en el diccionario, poner un espacio
    
    braille_text = braille_text.strip()
    save_braille_to_file(braille_text, filename)
    return braille_text