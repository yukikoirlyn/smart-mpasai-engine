# import streamlit as st
# import json
# import os
# import sys

# # Tambahkan folder src ke path agar bisa di-import
# sys.path.append(os.path.abspath("src"))

# from src.text_cleaner import clean_text
# from src.biomedical_matcher import BiomedicalMatcher

# # Konfigurasi Halaman
# st.set_page_config(
#     page_title="Smart MPASI Engine",
#     page_icon="🍼",
#     layout="centered"
# )

# # Header
# st.title("🍼 Smart MPASI & Allergen Logic Engine")
# st.caption("Hybrid AI Engine: NLP Extraction + Deterministic Medical Guardrails")

# # Inisialisasi Matcher (Hanya sekali saat load)
# @st.cache_resource
# def load_matcher():
#     return BiomedicalMatcher("data/allergen_kb.json")

# matcher = load_matcher()

# # Area Input
# st.divider()
# st.subheader("📝 Input Analisis")
# user_input = st.text_area(
#     "Masukkan resep atau label makanan:",
#     placeholder="Contoh: Tumis ayam pakai unsalted butter, keju cheddar, dan sedikit kecap.",
#     height=100
# )

# # Tombol Aksi
# col1, col2 = st.columns([4, 1])
# with col1:
#     is_analyze = st.button("🔍 Analisis Alergen", type="primary", use_container_width=True)

# # Logika Utama
# if is_analyze and user_input:
#     with st.spinner("Sedang memproses pipeline..."):
#         # 1. Node 1: Text Sanitizer
#         clean_text_result = clean_text(user_input)
        
#         # 2. Node 3: Biomedical Matcher (Deterministik)
#         # (Di versi lanjutan, Node 2 LLM akan ada di sini)
#         results = matcher.analyze(clean_text_result)
        
#         # Tampilan Hasil
#         st.divider()
#         st.subheader(" Hasil Analisis")
        
#         if not results:
#             st.success("✅ **Aman!** Tidak ada alergen utama terdeteksi dalam database.")
#         else:
#             st.warning(f"⚠️ **Perhatian!** Ditemukan {len(results)} potensi alergen.")
            
#             for item in results:
#                 # Tentukan warna berdasarkan risiko
#                 if item["risk_level"] == "HIGH":
#                     color = "red"
#                     icon = "🚨"
#                 else:
#                     color = "orange"
#                     icon = "⚠️"
                    
#                 st.markdown(f"**{icon} {item['display_name']}** <span style='color:{color}; font-weight:bold;'>[{item['risk_level']} RISK]</span>", unsafe_allow_html=True)
                
#                 # Detail dalam expander agar rapi
#                 with st.expander(f"Lihat detail medis untuk {item['display_name']}"):
#                     st.write(f"**Kata terdeteksi:** `{item['keyword_matched']}`")
#                     st.info(item["medical_note"])
#                     st.caption(f"Referensi: {item['reference']}")

#         # Debug View (Untuk menunjukkan bahwa ini terstruktur)
#         with st.expander("🛠️ Technical View (JSON Output)"):
#             st.json({
#                 "input_raw": user_input,
#                 "input_cleaned": clean_text_result,
#                 "matches": results
#             })

# elif is_analyze and not user_input:
#     st.error("Mohon masukkan teks resep atau label makanan terlebih dahulu.")

import html
import os
import re
import sys

import streamlit as st

# Tambahkan folder src ke path agar bisa di-import
sys.path.append(os.path.abspath("src"))

from src.text_cleaner import clean_text
from src.biomedical_matcher import BiomedicalMatcher

# ----------------------------------------------------------------------------
# Konfigurasi halaman
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Smart MPASI Engine",
    page_icon="🍼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# Design tokens & CSS
#   Primary  #005f73 / #0a9396   Danger #e63946   Warning #f4a261
#   Safe     #2a9d8f             Background #f8f9fa
# ----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
:root {
    --teal-900: #003d4a;
    --teal-700: #005f73;
    --teal-500: #0a9396;
    --danger: #e63946;
    --danger-text: #b4232f;
    --danger-tint: #fdecee;
    --warn: #f4a261;
    --warn-text: #a8570b;
    --warn-tint: #fef3e8;
    --safe: #2a9d8f;
    --safe-text: #1b6f65;
    --safe-tint: #e8f5f3;
    --bg: #f8f9fa;
    --surface: #ffffff;
    --ink: #1d2b36;
    --ink-soft: #5b6b79;
    --line: #e4e9ee;
    --font: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

/* ---------- Base ---------- */
.stApp { background: var(--bg); color: var(--ink); }
.stApp, .stMarkdown, .stMarkdown p, label, button, textarea, input,
.hero, .risk-card, .kpi, .banner, .panel, .empty {
    font-family: var(--font);
}
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1180px; }

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--line);
}
section[data-testid="stSidebar"] .block-container { padding-top: 1.4rem; }
.side-brand { display: flex; align-items: center; gap: .65rem; margin-bottom: 1.1rem; }
.side-brand .mark {
    width: 38px; height: 38px; border-radius: 10px; background: var(--teal-700);
    display: flex; align-items: center; justify-content: center; font-size: 1.25rem;
}
.side-brand .name { font-weight: 700; color: var(--teal-900); line-height: 1.15; }
.side-brand .sub { font-size: .78rem; color: var(--ink-soft); }
.side-hint {
    background: var(--safe-tint); border-radius: 10px; padding: .7rem .85rem;
    font-size: .84rem; color: var(--teal-900); line-height: 1.45; margin-bottom: 1rem;
}
.side-label { font-size: .8rem; color: var(--ink-soft); margin: 1rem 0 .35rem; font-weight: 600; }

section[data-testid="stSidebar"] textarea {
    border-radius: 10px; border: 1px solid var(--line); background: #fbfcfd; color: var(--ink);
    font-size: .93rem;
}
section[data-testid="stSidebar"] textarea:focus {
    border-color: var(--teal-500); box-shadow: 0 0 0 3px rgba(10,147,150,.16);
}

/* Primary button */
button[kind="primary"], button[data-testid="stBaseButton-primary"] {
    background: var(--teal-700); border: 1px solid var(--teal-700); color: #fff;
    border-radius: 10px; font-weight: 600; padding: .6rem 1rem;
    transition: background .15s ease, box-shadow .15s ease;
}
button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover {
    background: var(--teal-500); border-color: var(--teal-500); color: #fff;
    box-shadow: 0 4px 12px rgba(0,95,115,.25);
}
button[kind="primary"]:focus-visible, button[data-testid="stBaseButton-primary"]:focus-visible {
    outline: 3px solid rgba(10,147,150,.4); outline-offset: 2px;
}
/* Secondary (example) buttons */
button[kind="secondary"], button[data-testid="stBaseButton-secondary"] {
    background: var(--surface); border: 1px solid var(--line); color: var(--teal-700);
    border-radius: 999px; font-size: .82rem; padding: .25rem .8rem;
}
button[kind="secondary"]:hover, button[data-testid="stBaseButton-secondary"]:hover {
    border-color: var(--teal-500); color: var(--teal-500); background: var(--safe-tint);
}

/* ---------- Hero ---------- */
.hero {
    background: var(--teal-700); color: #fff; border-radius: 18px;
    padding: 1.5rem 1.75rem; display: flex; align-items: center; gap: 1.1rem;
    box-shadow: 0 6px 20px rgba(0,95,115,.18); margin-bottom: 1.4rem;
}
.hero .mark {
    flex: 0 0 56px; height: 56px; border-radius: 14px; background: rgba(255,255,255,.14);
    display: flex; align-items: center; justify-content: center; font-size: 1.8rem;
}
.hero .title { font-size: 1.55rem; font-weight: 700; line-height: 1.2; margin: 0; color: #fff; }
.hero .desc { margin: .3rem 0 0; color: rgba(255,255,255,.82); font-size: .95rem; }

/* ---------- Summary banner ---------- */
.banner {
    border-radius: 16px; padding: 1.2rem 1.4rem; display: flex; align-items: center;
    gap: 1rem; margin-bottom: 1rem; border: 1px solid transparent;
}
.banner .b-icon { font-size: 2rem; line-height: 1; }
.banner .b-title { font-size: 1.35rem; font-weight: 700; margin: 0; }
.banner .b-desc { margin: .15rem 0 0; font-size: .93rem; }
.banner.high { background: var(--danger-tint); border-color: #f6c3c8; }
.banner.high .b-title { color: var(--danger-text); }
.banner.moderate { background: var(--warn-tint); border-color: #f8d9bb; }
.banner.moderate .b-title { color: var(--warn-text); }
.banner.safe {
    background: var(--safe-tint); border-color: #b9e0db; padding: 2rem 1.6rem;
}
.banner.safe .b-icon { font-size: 3rem; }
.banner.safe .b-title { color: var(--safe-text); font-size: 1.7rem; }
.banner .b-desc { color: var(--ink-soft); }

/* ---------- KPI ---------- */
.kpi {
    background: var(--surface); border-radius: 14px; padding: .9rem 1.1rem;
    box-shadow: 0 1px 2px rgba(16,42,67,.05), 0 4px 14px rgba(16,42,67,.05);
    border: 1px solid var(--line);
}
.kpi .k-num { font-size: 1.9rem; font-weight: 700; line-height: 1.1; }
.kpi .k-label { font-size: .85rem; color: var(--ink-soft); margin-top: .15rem; }
.kpi.high .k-num { color: var(--danger); }
.kpi.moderate .k-num { color: var(--warn-text); }
.kpi.total .k-num { color: var(--teal-700); }

/* ---------- Result cards ---------- */
.section-title { font-size: 1.05rem; font-weight: 700; color: var(--teal-900); margin: 1.3rem 0 .7rem; }
.risk-card {
    background: var(--surface); border-radius: 14px; border-left: 6px solid var(--teal-500);
    padding: 1rem 1.25rem; margin-bottom: .9rem;
    box-shadow: 0 1px 2px rgba(16,42,67,.06), 0 6px 18px rgba(16,42,67,.06);
}
.risk-card.high { border-left-color: var(--danger); }
.risk-card.moderate { border-left-color: var(--warn); }
.risk-card .rc-head { display: flex; align-items: center; justify-content: space-between; gap: .75rem; flex-wrap: wrap; }
.risk-card .rc-title { display: flex; align-items: center; gap: .55rem; font-size: 1.08rem; font-weight: 700; color: var(--ink); }
.risk-card .rc-meta { margin-top: .45rem; font-size: .88rem; color: var(--ink-soft); }
.risk-card code {
    background: #eef3f6; color: var(--teal-900); padding: .1rem .45rem; border-radius: 6px; font-size: .85rem;
}
.badge { font-size: .78rem; font-weight: 700; padding: .22rem .65rem; border-radius: 999px; }
.badge.high { background: var(--danger-tint); color: var(--danger-text); }
.badge.moderate { background: var(--warn-tint); color: var(--warn-text); }
.risk-card details { margin-top: .7rem; border-top: 1px solid var(--line); padding-top: .6rem; }
.risk-card summary { cursor: pointer; font-size: .88rem; font-weight: 600; color: var(--teal-700); }
.risk-card summary:hover { color: var(--teal-500); }
.risk-card .rc-note {
    margin-top: .6rem; padding: .75rem .9rem; border-radius: 10px; background: #f1f7f9;
    color: var(--ink); font-size: .92rem; line-height: 1.55;
}
.risk-card .rc-ref { margin-top: .5rem; font-size: .8rem; color: var(--ink-soft); }

/* ---------- Side panel ---------- */
.panel {
    background: var(--surface); border-radius: 14px; border: 1px solid var(--line);
    padding: 1rem 1.2rem; margin-bottom: .9rem;
    box-shadow: 0 1px 2px rgba(16,42,67,.05), 0 4px 14px rgba(16,42,67,.05);
}
.panel .p-title { font-weight: 700; color: var(--teal-900); margin-bottom: .55rem; font-size: .98rem; }
.panel .p-text { font-size: .93rem; line-height: 1.7; color: var(--ink); word-break: break-word; }
.panel mark { padding: .05rem .3rem; border-radius: 5px; color: var(--ink); }
.panel mark.high { background: #f9c9ce; }
.panel mark.moderate { background: #fbdcc0; }
.panel .p-legend { margin-top: .7rem; font-size: .78rem; color: var(--ink-soft); }
.disclaimer {
    font-size: .82rem; color: var(--ink-soft); line-height: 1.5; padding: .8rem 1rem;
    border-radius: 12px; background: #f1f4f6; border: 1px dashed #cfd8df;
}

/* ---------- Empty state ---------- */
.empty {
    background: var(--surface); border: 1px solid var(--line); border-radius: 16px;
    padding: 1.6rem 1.8rem; box-shadow: 0 1px 2px rgba(16,42,67,.05), 0 4px 14px rgba(16,42,67,.05);
}
.empty .e-title { font-size: 1.15rem; font-weight: 700; color: var(--teal-900); margin-bottom: .8rem; }
.empty ol { margin: 0 0 1.1rem 1.1rem; padding: 0; color: var(--ink); line-height: 1.9; }
.legend { display: flex; gap: .6rem; flex-wrap: wrap; }
.legend span { font-size: .8rem; font-weight: 600; padding: .22rem .7rem; border-radius: 999px; }
.legend .l-high { background: var(--danger-tint); color: var(--danger-text); }
.legend .l-mod { background: var(--warn-tint); color: var(--warn-text); }
.legend .l-safe { background: var(--safe-tint); color: var(--safe-text); }

@media (prefers-reduced-motion: reduce) {
    button { transition: none !important; }
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# Inisialisasi Matcher (hanya sekali saat load)
# ----------------------------------------------------------------------------
@st.cache_resource
def load_matcher():
    return BiomedicalMatcher("data/allergen_kb.json")


matcher = load_matcher()


# ----------------------------------------------------------------------------
# Helper
# ----------------------------------------------------------------------------
EXAMPLES = {
    "🧈 Mentega & keju": "Tumis ayam pakai unsalted butter, keju cheddar, dan sedikit kecap.",
    "🥜 Selai kacang": "Puding susu dengan telur, tepung terigu, dan selai kacang.",
    "🥕 Bubur sayur": "Bubur beras dengan wortel, brokoli, dan minyak zaitun.",
}


def esc(value) -> str:
    """Escape teks agar aman disisipkan ke HTML."""
    return html.escape("" if value is None else str(value))


def risk_bucket(item: dict) -> str:
    """HIGH tetap HIGH; level lain diperlakukan sebagai MODERATE (sesuai logika awal)."""
    return "high" if str(item.get("risk_level", "")).upper() == "HIGH" else "moderate"


def set_example(text: str) -> None:
    st.session_state["user_input"] = text


def render_card(item: dict) -> str:
    bucket = risk_bucket(item)
    icon = "🚨" if bucket == "high" else "⚠️"
    label = "Risiko tinggi" if bucket == "high" else "Risiko sedang"
    note = esc(item.get("medical_note", "")).replace("\n", "<br>")
    open_attr = " open" if bucket == "high" else ""
    parts = [
        f'<div class="risk-card {bucket}">',
        '<div class="rc-head">',
        f'<div class="rc-title"><span>{icon}</span><span>{esc(item.get("display_name", "Alergen"))}</span></div>',
        f'<span class="badge {bucket}">{label}</span>',
        "</div>",
        f'<div class="rc-meta">Kata terdeteksi: <code>{esc(item.get("keyword_matched", "-"))}</code></div>',
        f"<details{open_attr}><summary>Catatan medis</summary>",
        f'<div class="rc-note">{note}</div>',
        f'<div class="rc-ref">Referensi: {esc(item.get("reference", "-"))}</div>',
        "</details>",
        "</div>",
    ]
    return "".join(parts)


def highlight_text(text: str, matches: list) -> str:
    """Escape teks lalu beri <mark> pada kata kunci yang terdeteksi."""
    levels = {}
    for item in matches:
        kw = str(item.get("keyword_matched", "")).strip().lower()
        if not kw:
            continue
        bucket = risk_bucket(item)
        if levels.get(kw) != "high":
            levels[kw] = bucket

    safe_text = esc(text)
    if not levels:
        return safe_text

    pattern = re.compile(
        "|".join(re.escape(esc(k)) for k in sorted(levels, key=len, reverse=True)),
        re.IGNORECASE,
    )

    def _wrap(m: re.Match) -> str:
        key = html.unescape(m.group(0)).lower()
        return f'<mark class="{levels.get(key, "moderate")}">{m.group(0)}</mark>'

    return pattern.sub(_wrap, safe_text)


def render_banner(high: int, moderate: int) -> str:
    if high == 0 and moderate == 0:
        return (
            '<div class="banner safe">'
            '<div class="b-icon">✅</div>'
            "<div>"
            '<div class="b-title">Aman, tidak ada alergen utama terdeteksi</div>'
            '<div class="b-desc">Tidak ada bahan dalam teks ini yang cocok dengan database alergen.</div>'
            "</div></div>"
        )
    if high > 0:
        title = f"{high} risiko tinggi ditemukan"
        if moderate:
            title += f" dan {moderate} risiko sedang"
        cls, icon = "high", "🚨"
    else:
        title = f"{moderate} risiko sedang ditemukan"
        cls, icon = "moderate", "⚠️"
    return (
        f'<div class="banner {cls}">'
        f'<div class="b-icon">{icon}</div>'
        "<div>"
        f'<div class="b-title">{title}</div>'
        '<div class="b-desc">Tinjau catatan medis pada setiap bahan di bawah sebelum menyajikan MPASI ini.</div>'
        "</div></div>"
    )


def kpi(number: int, label: str, cls: str) -> str:
    return f'<div class="kpi {cls}"><div class="k-num">{number}</div><div class="k-label">{label}</div></div>'


# ----------------------------------------------------------------------------
# Sidebar: area input
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div class="side-brand"><div class="mark">🍼</div>'
        '<div><div class="name">Smart MPASI</div>'
        '<div class="sub">Allergen Logic Engine</div></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="side-hint">Tempel resep atau label komposisi makanan bayi, '
        "lalu klik <b>Analisis alergen</b>. Bahan seperti susu, telur, kacang, dan gluten "
        "akan dicocokkan dengan database medis.</div>",
        unsafe_allow_html=True,
    )

    user_input = st.text_area(
        "Resep atau label makanan",
        key="user_input",
        placeholder="Contoh: Tumis ayam pakai unsalted butter, keju cheddar, dan sedikit kecap.",
        height=170,
        help="Tulis bahan dalam kalimat bebas. Bahasa Indonesia dan Inggris sama-sama didukung.",
    )

    is_analyze = st.button("🔍 Analisis alergen", type="primary", use_container_width=True)
    error_slot = st.empty()

    st.markdown('<div class="side-label">Coba contoh</div>', unsafe_allow_html=True)
    for label, text in EXAMPLES.items():
        st.button(label, key=f"ex_{label}", on_click=set_example, args=(text,))

    st.divider()
    st.caption("Pipeline: Text Sanitizer → Biomedical Matcher (deterministik)")


# ----------------------------------------------------------------------------
# Logika utama
# ----------------------------------------------------------------------------
if is_analyze:
    if not user_input.strip():
        error_slot.error("Masukkan teks resep atau label makanan terlebih dahulu.")
    else:
        with st.spinner("Memproses pipeline..."):
            try:
                # Node 1: Text Sanitizer
                cleaned = clean_text(user_input)
                # Node 3: Biomedical Matcher (deterministik)
                # (Di versi lanjutan, Node 2 LLM akan ada di sini)
                results = matcher.analyze(cleaned)
                st.session_state["analysis"] = {
                    "raw": user_input,
                    "clean": cleaned,
                    "results": results,
                }
            except Exception as exc:  # tampilkan error yang bisa ditindaklanjuti
                st.session_state.pop("analysis", None)
                error_slot.error(f"Analisis gagal: {exc}")


# ----------------------------------------------------------------------------
# Main dashboard
# ----------------------------------------------------------------------------
st.markdown(
    '<div class="hero"><div class="mark">🍼</div><div>'
    '<div class="title">Smart MPASI &amp; Allergen Logic Engine</div>'
    '<div class="desc">Ekstraksi NLP dan guardrail medis deterministik untuk menyaring alergen pada resep MPASI.</div>'
    "</div></div>",
    unsafe_allow_html=True,
)

analysis = st.session_state.get("analysis")

if not analysis:
    st.markdown(
        '<div class="empty">'
        '<div class="e-title">Mulai analisis pertama Anda</div>'
        "<ol>"
        "<li>Tempel resep atau label komposisi di panel kiri.</li>"
        "<li>Klik <b>Analisis alergen</b>.</li>"
        "<li>Baca ringkasan risiko dan catatan medis di sini.</li>"
        "</ol>"
        '<div class="legend">'
        '<span class="l-high">Risiko tinggi</span>'
        '<span class="l-mod">Risiko sedang</span>'
        '<span class="l-safe">Aman</span>'
        "</div></div>",
        unsafe_allow_html=True,
    )
else:
    results = analysis["results"] or []
    # Risiko tinggi tampil lebih dulu
    results = sorted(results, key=lambda it: 0 if risk_bucket(it) == "high" else 1)
    n_high = sum(1 for it in results if risk_bucket(it) == "high")
    n_mod = len(results) - n_high

    # Ringkasan risiko
    st.markdown(render_banner(n_high, n_mod), unsafe_allow_html=True)

    k1, k2, k3 = st.columns(3)
    k1.markdown(kpi(n_high, "Risiko tinggi", "high"), unsafe_allow_html=True)
    k2.markdown(kpi(n_mod, "Risiko sedang", "moderate"), unsafe_allow_html=True)
    k3.markdown(kpi(len(results), "Total alergen terdeteksi", "total"), unsafe_allow_html=True)

    left, right = st.columns([3, 2], gap="large")

    with left:
        if results:
            st.markdown('<div class="section-title">Detail alergen</div>', unsafe_allow_html=True)
            st.markdown("".join(render_card(it) for it in results), unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="section-title">Detail alergen</div>'
                '<div class="panel"><div class="p-text">Tidak ada alergen yang perlu ditinjau.</div></div>',
                unsafe_allow_html=True,
            )

    with right:
        st.markdown('<div class="section-title">Teks yang dianalisis</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="panel">'
            '<div class="p-title">Hasil pembersihan teks</div>'
            f'<div class="p-text">{highlight_text(analysis["clean"], results)}</div>'
            '<div class="p-legend">Kata yang disorot cocok dengan database alergen.</div>'
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="disclaimer">Alat ini membantu menyaring bahan, bukan pengganti saran medis. '
            "Konsultasikan dengan dokter anak atau ahli gizi sebelum mengenalkan makanan baru.</div>",
            unsafe_allow_html=True,
        )

    # Technical view (menunjukkan output terstruktur)
    st.markdown('<div style="height:.9rem"></div>', unsafe_allow_html=True)
    with st.expander("🛠️ Technical view (JSON output)"):
        st.json(
            {
                "input_raw": analysis["raw"],
                "input_cleaned": analysis["clean"],
                "matches": analysis["results"],
            }
        )