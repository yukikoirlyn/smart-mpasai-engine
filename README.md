# 🍼 Smart MPASI & Allergen Logic Engine

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Promptflow](https://img.shields.io/badge/Orchestration-Promptflow-0078D4.svg)](https://microsoft.github.io/promptflow/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📖 Overview
**Smart MPASI** is an open-source AI engine designed to analyze infant/toddler food compositions and recipes, automatically extracting ingredients and mapping them to medically verified allergen warnings. 

Built with a hybrid architecture, it combines **deterministic logic** (regex cleaning, static biomedical knowledge base) with **probabilistic AI** (LLM-powered entity extraction) to ensure accurate, structured, and hallucination-free outputs.

## ✨ Key Features
- 🔍 **Dual Input Modes:** Parses dense packaged food labels & unstructured natural language recipes.
- 🛡️ **AI Guardrails:** Strict JSON schema enforcement; prevents LLM hallucinations by cross-referencing with a curated biomedical database.
- 🧠 **Hybrid Pipeline:** Separates data sanitization from AI inference for optimal token usage and reliability.
- 📊 **Risk Mapping:** Automatically classifies allergens by medical risk level (High/Moderate/Low) based on pediatric guidelines.
- 🖥️ **Interactive UI:** Clean, responsive Streamlit interface for real-time testing and visualization.

## 🏗️ System Architecture (Promptflow DAG)
The pipeline is designed to separate data cleaning from AI inference:
| Node | Component | Function |
|------|-----------|----------|
| `1` | **Text Sanitizer** (`Python & Regex`) | Strips special characters, standardizes formatting, removes marketing fluff |
| `2` | **Entity Extraction** (`LLM`) | Identifies pure ingredients from raw text |
| `3` | **Biomedical Cross-Referencing** (`Python`) | Deterministic matching against `allergen_kb.json` to fetch allergen class & medical risk |
| `4` | **JSON Output Formatter** (`LLM`) | Forces structured, nested JSON output ready for API/frontend consumption |

## 🧪 Use Cases
| Scenario | Input Example | Output Focus |
|---|---|---|
| **Packaged Food Label** | `"Ingredients: Whey protein, casein, maltodextrin, natural flavors"` | Chemical derivative mapping (e.g., Whey → Cow's Milk Protein) |
| **Home Recipe (NLP)** | `"Tumis ayam pakai unsalted butter dan keju cheddar"` | Hidden allergen detection in conversational text |

## 🛠️ Tech Stack
- **Backend:** Python 3.10+, Promptflow, Regex
- **AI/LLM:** OpenAI / Azure OpenAI (or local via Ollama)
- **Database:** Static JSON Knowledge Base (`allergen_kb.json`)
- **Frontend/UI:** Streamlit
- **Testing:** `pytest`, JSON Schema Validation

## 🚀 Quick Start
### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/smart-mpasai-engine.git
cd smart-mpasai-engine
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install streamlit
```
### 2. Run the App
```bash
streamlit run app.py
```