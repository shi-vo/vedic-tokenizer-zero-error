"""
Complete API Documentation for Vedic Zero-Error Tokenizer
==========================================================

This document provides comprehensive usage examples and API reference
for the patent-grade Sanskrit tokenization system.

Author: Ganesh
Version: 1.0
License: Proprietary
"""

# ============================================================================
# QUICK START GUIDE
# ============================================================================

"""
## Installation

```python
# Clone the repository
git clone https://github.com/yourusername/vedic-tokenizer.git
cd vedic-tokenizer

# Install (if using setup.py)
pip install -e .
```

## Basic Usage

```python
from vedic_tokenizer import VedicZeroTokenizer

# Initialize tokenizer
tokenizer = VedicZeroTokenizer()

# Tokenize Sanskrit text
text = "रामः वनं गच्छति धर्मः सत्यम्"
tokens = tokenizer.tokenize(text)

print(tokens)
# Output: ['रामः', ' ', 'वनं', ' ', 'गच्छति', ' ', 'धर्मः', ' ', 'सत्यम्']

# Verify reversibility
restored = tokenizer.detokenize(tokens)
assert restored == text  # Zero-error guarantee!
```

## Advanced Features

### 1. Sandhi Analysis with Multi-Candidate Scoring

```python
from vedic_tokenizer.dictionary import SanskritDictionary
from vedic_tokenizer.sandhi_engine import EnhancedSandhiEngine

# Load dictionary
dictionary = SanskritDictionary()
dictionary.load_from_json("path/to/corpus.json", text_field="content")

# Create enhanced engine
engine = EnhancedSandhiEngine(dictionary)

# Find all possible Sandhi splits
word = "रामोऽत्र"  # रामः + अत्र
candidates = engine.find_all_splits(word, max_candidates=5)

for i, cand in enumerate(candidates, 1):
    print(f"{i}. {cand.left_word} + {cand.right_word}")
    print(f"   Score: {cand.total_score:.3f}")
    print(f"   Rule: {cand.sandhi_rule_id}")
    print(f"   Grammar: {cand.left_vibhakti}, {cand.right_vibhakti}")
```

### 2. Vibhakti (Case Ending) Analysis

```python
from vedic_tokenizer.vibhakti_analyzer import VibhaktiAnalyzer, analyze_word

# Analyze a word for case endings
analyses = analyze_word("रामः")

for analysis in analyses:
    print(f"Case: {analysis.case.name}")
    print(f"Number: {analysis.number.name}")
    print(f"Gender: {analysis.gender.name if analysis.gender else 'Any'}")
    print(f"Stem: {analysis.stem}")
    print(f"Confidence: {analysis.confidence:.2f}")
```

### 3. Pratyaya (Suffix) Analysis

```python
from vedic_tokenizer.pratyaya_analyzer import PratyayaAnalyzer

analyzer = PratyayaAnalyzer()

# Analyze suffixes
word = "कर्तुम्"  # Infinitive: "to do"
analyses = analyzer.analyze(word)

for analysis in analyses:
    print(f"Base: {analysis.base}")
    print(f"Suffix: {analysis.suffix}")
    print(f"Type: {analysis.pratyaya_type.name}")
    print(f"Meaning: {analysis.meaning}")
```

### 4. Samasa (Compound) Decomposition

```python
from vedic_tokenizer.samasa_decomposer import SamasaAnalyzer

analyzer = SamasaAnalyzer(dictionary)

# Decompose compounds
compound = "धर्मक्षेत्र"  # dharma-kṣetra
analyses = analyzer.analyze(compound)

for analysis in analyses:
    print(f"Components: {' + '.join(analysis.components)}")
    print(f"Type: {analysis.samasa_type}")
    print(f"Confidence: {analysis.confidence:.2f}")
```

## Statistics and Metrics

### Grammar Coverage

```python
from vedic_tokenizer.sandhi_rules import ALL_SANDHI_RULES
from vedic_tokenizer.vibhakti_analyzer import VibhaktiAnalyzer
from vedic_tokenizer.pratyaya_analyzer import PratyayaAnalyzer

# Get total rule counts
sandhi_count = len(ALL_SANDHI_RULES)
vibhakti_count = len(VibhaktiAnalyzer().patterns)
pratyaya_count = len(PratyayaAnalyzer().patterns)

print(f"Total Grammar Rules: {sandhi_count + vibhakti_count + pratyaya_count}")
print(f"  - Sandhi: {sandhi_count}")
print(f"  - Vibhakti: {vibhakti_count}")
print(f"  - Pratyaya: {pratyaya_count}")
```

### Dictionary Statistics

```python
# Get vocabulary size
vocab_size = dictionary.size()
print(f"Vocabulary: {vocab_size:,} unique words")

# Get word frequency
freq = dictionary.get_word_frequency("राम")
print(f"'राम' appears {freq} times in corpus")

# Find words with prefix/suffix
words_with_ram = dictionary.get_words_starting_with("राम")
print(f"Words starting with 'राम': {len(words_with_ram)}")
```

## Configuration Options

### Tokenizer Configuration

```python
tokenizer = VedicZeroTokenizer(
    preserve_whitespace=True,       # Keep spaces as tokens
    preserve_vedic_accents=True,    # Keep Swara marks
    enable_sandhi_splitting=True,   # Use Sandhi analysis
    enable_samasa_decomposition=True,  # Decompose compounds
    auto_verify=True                # Auto-verify tokenization
)
```

### Scoring Weights (Advanced)

```python
# Customize scoring algorithm
engine = EnhancedSandhiEngine(dictionary)

# Default weights:
# - 40% Sandhi rule priority
# - 30% Vocabulary frequency  
# - 30% Grammatical validity

# Modify weights
engine.SANDHI_WEIGHT = 0.50
engine.FREQUENCY_WEIGHT = 0.30
engine.GRAMMAR_WEIGHT = 0.20
```

## Data Loading

### From JSON Files

```python
# Load Vedic texts
tokenizer.load_dictionary_from_json(
    "data/ramayan.json",
    text_field="content",
    extract_words=True
)

# Load multiple files
for file in ["bhagavad_gita.json", "rig_veda.json"]:
    tokenizer.load_dictionary_from_json(file)
```

### From Text Files

```python
# One word per line
tokenizer.load_dictionary_from_text("vocabulary.txt")
```

### Manual Addition

```python
# Add specific words
words = ["राम", "सीता", "लक्ष्मण", "हनुमान"]
tokenizer.add_words_to_dictionary(words)
```

## Testing & Validation

### Unit Tests

```python
# Run comprehensive tests
pytest tests/test_tokenizer_comprehensive.py -v

# Run specific test class
pytest tests/test_tokenizer_comprehensive.py::TestSandhiRules -v

# Run with coverage
pytest tests/ --cov=vedic_tokenizer --cov-report=html
```

### Verify Integrity

```python
# Manual verification
text = "रामो वनं गच्छति"
tokens = tokenizer.tokenize(text)

is_valid, metrics = tokenizer.verify_integrity(text, tokens)

if is_valid:
    print("✅ Tokenization is lossless!")
else:
    print(f"⚠️ Verification failed: {metrics}")
```

## Performance Optimization

### Caching

```python
# The analyzer automatically caches patterns
# For repeated analysis, reuse analyzer instances

analyzer = VibhaktiAnalyzer()  # Create once

# Reuse for multiple words
for word in large_word_list:
    analyses = analyzer.analyze(word)
```

### Batch Processing

```python
# Process large texts efficiently
def batch_tokenize(texts, batch_size=1000):
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        batch_results = [tokenizer.tokenize(t) for t in batch]
        results.extend(batch_results)
    return results
```

## Error Handling

```python
try:
    tokens = tokenizer.tokenize(text)
except ValueError as e:
    print(f"Tokenization error: {e}")
    # Fallback to simpler tokenization
    tokens = text.split()

# Check verification
is_valid, metrics = tokenizer.verify_integrity(text, tokens)
if not is_valid:
    print(f"Warning: {metrics['error_message']}")
```

## Export & Integration

### Export Tokenization Results

```python
import json

# Tokenize and export
results = {
    "original": text,
    "tokens": tokens,
    "token_count": len(tokens),
    "verified": is_valid
}

with open("tokenization_output.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
```

### Integration with ML Pipelines

```python
# For ML training
def prepare_dataset(texts):
    tokenized = []
    for text in texts:
        tokens = tokenizer.tokenize(text)
        # Remove whitespace tokens for ML
        tokens = [t for t in tokens if t.strip()]
        tokenized.append(tokens)
    return tokenized

# Create vocabulary for embeddings
vocab = set()
for tokens in tokenized_texts:
    vocab.update(tokens)

vocab_to_id = {word: i for i, word in enumerate(sorted(vocab))}
```

## Best Practices

1. **Always verify tokenization** for critical applications
2. **Reuse analyzer instances** for better performance
3. **Load dictionary once** at startup
4. **Use appropriate weights** based on your use case
5. **Test on sample data** before full corpus processing

## Troubleshooting

### Common Issues

**Issue**: Tokenization is slow
- **Solution**: Disable `auto_verify` for batch processing
- **Solution**: Reduce `max_candidates` in Sandhi engine

**Issue**: Too many false splits
- **Solution**: Increase `SANDHI_WEIGHT` in scoring
- **Solution**: Add more vocabulary to dictionary

**Issue**: Missing compounds
- **Solution**: Enable `enable_samasa_decomposition`
- **Solution**: Check dictionary has component words

## Technical Specifications

### Grammar Coverage
- **130 Sandhi transformation rules**
- **160 Vibhakti case-ending patterns**
- **55 Pratyaya suffix patterns**
- **345 total grammar rules**

### Data
- **348,231 unique Sanskrit words**
- **98,000 verse corpus**
- **1,130,149 word occurrences**

### Performance
- Rule lookup: <1ms per query
- Tokenization: ~1000 words/second
- Memory: ~50MB for full vocabulary

## License & Citation

This is proprietary software. For licensing queries, contact the author.

If using in research, please cite:
```
Vedic Zero-Error Tokenizer (2026)
Author: Ganesh
A patent-grade Sanskrit tokenization system with 345 Paninian grammar rules
```

## Support

For issues, questions, or feature requests:
- Email: your.email@example.com
- GitHub: github.com/yourusername/vedic-tokenizer

---
**End of API Documentation**
"""


# ============================================================================
# CODE EXAMPLES LIBRARY
# ============================================================================

def example_basic_tokenization():
    """Example: Basic tokenization."""
    from vedic_tokenizer import VedicZeroTokenizer
    
    tokenizer = VedicZeroTokenizer()
    text = "रामो वनं गच्छति"
    tokens = tokenizer.tokenize(text)
    restored = tokenizer.detokenize(tokens)
    
    print(f"Original: {text}")
    print(f"Tokens: {tokens}")
    print(f"Restored: {restored}")
    print(f"Lossless: {text == restored}")


def example_multi_candidate_sandhi():
    """Example: Multi-candidate Sandhi analysis."""
    from vedic_tokenizer.dictionary import SanskritDictionary
    from vedic_tokenizer.sandhi_engine import EnhancedSandhiEngine
    
    dictionary = SanskritDictionary()
    engine = EnhancedSandhiEngine(dictionary)
    
    word = "सुरोत्तमः"
    candidates = engine.find_all_splits(word, max_candidates=3)
    
    print(f"Analyzing: {word}\n")
    for i, cand in enumerate(candidates, 1):
        print(f"{i}. {cand.left_word} + {cand.right_word}")
        print(f"   Score: {cand.total_score:.3f}\n")


def example_full_analysis():
    """Example: Complete morphological analysis."""
    from vedic_tokenizer.vibhakti_analyzer import analyze_word
    from vedic_tokenizer.pratyaya_analyzer import analyze_suffix
    
    word = "रामः"
    
    # Vibhakti analysis
    vib_analyses = analyze_word(word)
    print(f"Vibhakti analysis of '{word}':")
    if vib_analyses:
        best = vib_analyses[0]
        print(f"  Case: {best.case.name}")
        print(f"  Number: {best.number.name}\n")
    
    # Pratyaya analysis
    prat_analyses = analyze_suffix(word)
    print(f"Pratyaya analysis of '{word}':")
    if prat_analyses:
        for analysis in prat_analyses[:2]:
            print(f"  Type: {analysis.pratyaya_type.name}")
            print(f"  Meaning: {analysis.meaning}")


if __name__ == "__main__":
    print("=" * 60)
    print("VEDIC ZERO-ERROR TOKENIZER - API EXAMPLES")
    print("=" * 60)
    print()
    
    example_basic_tokenization()
    print("\n" + "=" * 60 + "\n")
    
    example_multi_candidate_sandhi()
    print("\n" + "=" * 60 + "\n")
    
    example_full_analysis()
