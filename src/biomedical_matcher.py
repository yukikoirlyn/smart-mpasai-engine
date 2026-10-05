import json
import os
import re
from typing import List, Dict

class BiomedicalMatcher:
    """
    Engine deterministik untuk mencocokkan teks resep dengan database alergen.
    """

    def __init__(self, db_path: str):
        """
        Inisialisasi matcher dengan memuat database JSON.
        """
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database alergen tidak ditemukan di: {db_path}")

        with open(db_path, "r", encoding="utf-8") as f:
            self.kb = json.load(f)

        # Hapus metadata dari list pencarian agar tidak bentrok
        self.allergens = {k: v for k, v in self.kb.items() if k != "metadata"}

    def analyze(self, clean_text: str) -> List[Dict]:
        """
        Menganalisis teks bersih dan mengembalikan daftar alergen yang terdeteksi.
        """
        if not clean_text:
            return []

        detected_allergens = []

        for category, data in self.allergens.items():
            for keyword in data["keywords"]:
                # Regex \b memastikan pencocokan kata utuh
                pattern = r'\b' + re.escape(keyword) + r'\b'
                
                if re.search(pattern, clean_text, re.IGNORECASE):
                    detected_allergens.append({
                        "category": category,
                        "display_name": data.get("display_name", category),
                        "keyword_matched": keyword,
                        "risk_level": data["risk_level"],
                        "medical_note": data["medical_note"],
                        "reference": data.get("reference", "Internal KB")
                    })
                    break 

        # Urutkan berdasarkan risiko (HIGH dulu)
        risk_order = {"HIGH": 0, "MODERATE": 1, "LOW": 2}
        detected_allergens.sort(key=lambda x: risk_order.get(x["risk_level"], 3))

        return detected_allergens