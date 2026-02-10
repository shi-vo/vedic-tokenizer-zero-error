# Vedic Zero-Error Tokenizer - Quick Start Guide

## Installation

```bash
cd d:\projects\vedic-tokenizer\vedic-tokenizer
pip install -r requirements.txt  # Optional: pytest, mypy for testing
```

## Basic Usage

```python
from vedic_tokenizer import VedicZeroTokenizer

# Initialize
tokenizer = VedicZeroTokenizer()

# Tokenize
text = "राम सीता लक्ष्मण"
tokens = tokenizer.tokenize(text)
print(tokens)  # ['राम', ' ', 'सीता', ' ', 'लक्ष्मण']

# Detokenize (guaranteed lossless)
restored = tokenizer.detokenize(tokens)
assert restored == text  # Always True!
```

## Loading Your Vedic Datasets

### From JSON (Ramayan, Veda, Bhagavad Gita)

```python
tokenizer.load_dictionary_from_json(
    "d:/projects/automated-content-creator/data/1_बाल_काण्ड_data.json",
    text_field="content",
    extract_words=True
)
```

This automatically:
- Extracts all Sanskrit text from the `content` field
- Builds a vocabulary of 15,464+ words
- Uses these words for intelligent tokenization

### From Text File

```python
tokenizer.load_dictionary_from_text("my_words.txt")  # One word per line
```

### Programmatically

```python
tokenizer.add_words_to_dictionary(["कृष्ण", "अर्जुन", "भीम"])
```

## Running Examples

```bash
# Set Python path
$env:PYTHONPATH = "d:\projects\vedic-tokenizer\vedic-tokenizer"

# Basic demo
python examples\usage_demo.py

# Ramayan integration
python examples\ramayan_demo.py

# Patent features demo
python examples\patent_demo.py
```

## Running Tests

```bash
# Install pytest first
pip install pytest

# Run test suite
$env:PYTHONPATH = "d:\projects\vedic-tokenizer\vedic-tokenizer"
pytest tests\ -v
```

## Key Features

✅ **100% Lossless** - Mathematical guarantee of reversibility  
✅ **Deterministic** - Same input always produces same tokens  
✅ **Grammar-Aware** - Respects Paninian Sandhi rules  
✅ **Authentic Data** - Works with real Ramayan/Veda/Gita JSON  
✅ **Auto-Verification** - Automatically checks tokenization integrity  

## Configuration Options

```python
tokenizer = VedicZeroTokenizer(
    preserve_whitespace=True,        # Keep spaces as tokens
    preserve_vedic_accents=True,     # Preserve Swara marks
    enable_sandhi_splitting=True,    # Use Sandhi-aware splitting
    enable_samasa_decomposition=True, # Decompose compounds
    auto_verify=True                 # Automatic integrity check
)
```

## Statistics

```python
stats = tokenizer.get_statistics()
print(f"Dictionary size: {stats['dictionary_size']}")
print(f"Success rate: {stats['verification_metrics']['success_rate']:.1%}")
```

## Project Structure

```
vedic-tokenizer/
├── vedic_tokenizer/          # Main package
│   ├── __init__.py
│   ├── tokenizer.py          # VedicZeroTokenizer class
│   ├── normalizer.py         # Unicode normalization
│   ├── sandhi_engine.py      # Sandhi splitting algorithm
│   ├── sandhi_rules.py       # Paninian rules
│   ├── samasa_decomposer.py  # Compound decomposition
│   ├── dictionary.py         # Vocabulary management
│   └── verifier.py           # Lossless verification
├── tests/                    # Test suite
│   └── test_tokenizer.py
├── examples/                 # Usage examples
│   ├── usage_demo.py
│   ├── ramayan_demo.py
│   └── patent_demo.py
├── README.md                 # Full documentation
└── requirements.txt
```

## Support

For questions, issues, or patent licensing inquiries, contact [your email].

---

**Patent Pending**: System and Method for Lossless Morphological Tokenization of Vedic Sanskrit
