import streamlit as st
import json
import os
import sys

# Tambahkan folder src ke path agar bisa di-import
sys.path.append(os.path.abspath("src"))

from src.text_cleaner import clean_text
from src.biomedical_matcher import BiomedicalMatcher

# Konfigurasi Halaman
st.set_page_config(
    page_title="Smart MPASI Engine",
    page_icon="🍼",
    layout="centered"
)

# Header
st.title("🍼 Smart MPASI & Allergen Logic Engine")
st.caption("Hybrid AI Engine: NLP Extraction + Deterministic Medical Guardrails")

# Inisialisasi Matcher (Hanya sekali saat load)
@st.cache_resource
def load_matcher():
    return BiomedicalMatcher("data/allergen_kb.json")

matcher = load_matcher()

# Area Input
st.divider()
st.subheader("📝 Input Analisis")
user_input = st.text_area(
    "Masukkan resep atau label makanan:",
    placeholder="Contoh: Tumis ayam pakai unsalted butter, keju cheddar, dan sedikit kecap.",
    height=100
)

# Tombol Aksi
col1, col2 = st.columns([4, 1])
with col1:
    is_analyze = st.button("🔍 Analisis Alergen", type="primary", use_container_width=True)

# Logika Utama
if is_analyze and user_input:
    with st.spinner("Sedang memproses pipeline..."):
        # 1. Node 1: Text Sanitizer
        clean_text_result = clean_text(user_input)
        
        # 2. Node 3: Biomedical Matcher (Deterministik)
        # (Di versi lanjutan, Node 2 LLM akan ada di sini)
        results = matcher.analyze(clean_text_result)
        
        # Tampilan Hasil
        st.divider()
        st.subheader(" Hasil Analisis")
        
        if not results:
            st.success("✅ **Aman!** Tidak ada alergen utama terdeteksi dalam database.")
        else:
            st.warning(f"⚠️ **Perhatian!** Ditemukan {len(results)} potensi alergen.")
            
            for item in results:
                # Tentukan warna berdasarkan risiko
                if item["risk_level"] == "HIGH":
                    color = "red"
                    icon = "🚨"
                else:
                    color = "orange"
                    icon = "⚠️"
                    
                st.markdown(f"**{icon} {item['display_name']}** <span style='color:{color}; font-weight:bold;'>[{item['risk_level']} RISK]</span>", unsafe_allow_html=True)
                
                # Detail dalam expander agar rapi
                with st.expander(f"Lihat detail medis untuk {item['display_name']}"):
                    st.write(f"**Kata terdeteksi:** `{item['keyword_matched']}`")
                    st.info(item["medical_note"])
                    st.caption(f"Referensi: {item['reference']}")

        # Debug View (Untuk menunjukkan bahwa ini terstruktur)
        with st.expander("🛠️ Technical View (JSON Output)"):
            st.json({
                "input_raw": user_input,
                "input_cleaned": clean_text_result,
                "matches": results
            })

elif is_analyze and not user_input:
    st.error("Mohon masukkan teks resep atau label makanan terlebih dahulu.")