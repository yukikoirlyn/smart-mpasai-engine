# test_matcher.py
from src.biomedical_matcher import BiomedicalMatcher

# 1. Inisialisasi
matcher = BiomedicalMatcher("data/allergen_kb.json")

# 2. Test Case 1: Input Normal
text_1 = "Resep hari ini: Tumis ayam pakai unsalted butter dan keju cheddar."
result_1 = matcher.analyze(text_1)
print(f"Test 1 - Ditemukan: {len(result_1)} alergen")
for r in result_1:
    print(f"  - {r['display_name']} (ditemukan: '{r['keyword_matched']}')")

# 3. Test Case 2: False Positive Check (Harusnya aman)
text_2 = "Anak saya suka makan donat cokelat."
result_2 = matcher.analyze(text_2)
print(f"\nTest 2 - Donat (Seharusnya 0 alergen kacang): {len(result_2)} alergen")

# 4. Test Case 3: Input Kosong
result_3 = matcher.analyze("")
print(f"\nTest 3 - Input Kosong: {len(result_3)} alergen")