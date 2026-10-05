import re

def clean_text(raw_text: str) -> str:
    """
    Membersihkan teks dari karakter khusus, emoji, dan menstandarkan spasi.
    """
    if not raw_text:
        return ""
    
    # 1. Lowercase
    text = raw_text.lower()
    
    # 2. Hapus karakter khusus & tanda baca
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # 3. Hapus spasi berlebih
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text