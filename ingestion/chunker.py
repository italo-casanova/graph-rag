import re


def chunk_text(text, max_chars=800, overlap=100):
    """
    Divide el texto en chunks respetando límites naturales del lenguaje.

    - Primero intenta dividir por párrafos (doble salto de línea)
    - Si un párrafo es demasiado largo, lo divide por oraciones
    - Aplica overlap entre chunks para no perder contexto
    - Nunca corta en medio de una palabra

    Args:
        text:      Texto completo del documento
        max_chars: Máximo de caracteres por chunk (default 800)
        overlap:   Caracteres de solapamiento entre chunks (default 100)
    """

    if not text or not text.strip():
        return []

    # --- 1. Normalizar saltos de línea ---
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # --- 2. Dividir por párrafos ---
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    # --- 3. Si un párrafo supera max_chars, dividir por oraciones ---
    segments = []

    for paragraph in paragraphs:
        if len(paragraph) <= max_chars:
            segments.append(paragraph)
        else:
            # dividir por oraciones (punto, signo de interrogación, exclamación)
            sentences = re.split(r"(?<=[.!?])\s+", paragraph)
            current = ""

            for sentence in sentences:
                if len(current) + len(sentence) + 1 <= max_chars:
                    current = (current + " " + sentence).strip()
                else:
                    if current:
                        segments.append(current)
                    # si una sola oración supera el límite, la incluimos igual
                    current = sentence

            if current:
                segments.append(current)

    # --- 4. Combinar segmentos cortos y aplicar overlap ---
    chunks = []
    current_chunk = ""

    for segment in segments:
        if len(current_chunk) + len(segment) + 2 <= max_chars:
            current_chunk = (current_chunk + "\n\n" + segment).strip()
        else:
            if current_chunk:
                chunks.append(current_chunk)

            # overlap: tomar los últimos N caracteres del chunk anterior
            if chunks and overlap > 0:
                prev = chunks[-1]
                overlap_text = prev[-overlap:].strip()
                current_chunk = (overlap_text + "\n\n" + segment).strip()
            else:
                current_chunk = segment

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
