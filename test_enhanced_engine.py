"""
Test script for Enhanced Sandhi Engine

Tests the multi-candidate analysis with real Sanskrit words.
"""

import sys
sys.path.insert(0, '.')

from vedic_tokenizer.dictionary import SanskritDictionary
from vedic_tokenizer.sandhi_engine import EnhancedSandhiEngine

# Initialize
print("Initializing Enhanced Sand hi Engine...")
dictionary = SanskritDictionary()

# Add some test vocabulary with frequencies
test_vocab = {
    "राम": 1500,
    "रामः": 1200,
    "वन": 800,
    "वनम्": 600,
    "गच्छति": 500,
    "अत्र": 400,
    "सुर": 300,
    "उत्तम": 250,
    "उत्तमः": 200,
    "तत्र": 350,
    "आगच्छति": 450,
}

for word, freq in test_vocab.items():
    for _ in range(freq):
        dictionary.add_word(word)

print(f"Loaded {len(test_vocab)} words with frequencies\n")

# Create engine
engine = EnhancedSandhiEngine(dictionary)

# Test cases
test_words = [
    "रामोऽत्र",      # रामः + अत्र
    "तत्रागच्छति",   # तत्र + आगच्छति
    "सुरोत्तमः",     # सुर + उत्तमः
]

print("=" * 60)
print("TESTING MULTI-CANDIDATE SANDHI ANALYSIS")
print("=" * 60)

for word in test_words:
    print(f"\n🔍 Analyzing: {word}")
    print("-" * 60)
    
    candidates = engine.find_all_splits(word, max_candidates=5)
    
    if not candidates:
        print("  ⚠️  No splits found")
        continue
    
    print(f"  Found {len(candidates)} candidate(s):\n")
    
    for i, cand in enumerate(candidates, 1):
        print(f"  {i}. {cand.left_word} + {cand.right_word}")
        print(f"     Score: {cand.total_score:.3f}")
        print(f"     Rule: {cand.sandhi_rule_id} (priority={cand.sandhi_priority})")
        print(f"     Frequencies: {cand.left_frequency}, {cand.right_frequency}")
        
        grammar_info = []
        if cand.left_vibhakti:
            grammar_info.append(f"L:{cand.left_vibhakti}")
        if cand.right_vibhakti:
            grammar_info.append(f"R:{cand.right_vibhakti}")
        if cand.left_pratyaya:
            grammar_info.append(f"L:{cand.left_pratyaya}")
        if cand.right_pratyaya:
            grammar_info.append(f"R:{cand.right_pratyaya}")
        
        if grammar_info:
            print(f"     Grammar: {', '.join(grammar_info)}")
        
        print()
    
    # Show best split
    best = engine.get_best_split(word)
    print(f"  ✅ Best split: {best[0]} + {best[1]}")

print("\n" + "=" * 60)
print("✅ Enhanced Sandhi Engine test complete!")
print("=" * 60)
