# Vedic Tokenizer - Exported Datasets

**Export Date**: 2026-01-27 01:20:39

## Overview

This package contains comprehensive datasets extracted from the Vedic Tokenizer project,
including vocabulary from authentic Sanskrit texts, complete Sandhi rule catalogs, and
linguistic statistics.

## Corpus Statistics

- **Total Verses**: 98,000
- **Total Words**: 1,130,149
- **Unique Words**: 348,231
- **Vocabulary Diversity**: 0.3081

## Source Texts

| Dataset | Verses | Words |
|---------|--------|-------|
| Atharvaveda | 736 | 71,922 |
| Ramayana | 22,742 | 261,203 |
| Bhagavad Gita | 701 | 5,382 |
| Mahabharata | 73,821 | 791,642 |

## Files Included

### 1. Vocabulary Data

#### `vocabulary.json` (Structured Format)
Complete vocabulary with metadata:
- Word
- Frequency (occurrence count)
- Rank (by frequency)
- Length (character count)
- Percentage (of corpus)

**Example Usage (Python)**:
```python
import json

with open('vocabulary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Top 10 words
for word_info in data['vocabulary'][:10]:
    print(f"{word_info['rank']}. {word_info['word']} = {word_info['frequency']:,}")
```

#### `vocabulary.csv` (Tabular Format)
Same data in CSV for spreadsheet analysis.

**Columns**: rank, word, frequency, percentage, length, devanagari_codepoints

---

### 2. Sandhi Rules

#### `sandhi_rules.json` (Structured Format)
All 46 Sandhi transformation rules:
- Rule ID
- Category (vowel/consonant/visarga/special)
- Patterns (left/right)
- Result
- Priority (1-10)
- Paninian sutra reference
- Examples

**Example Usage (Python)**:
```python
import json

with open('sandhi_rules.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find all vowel sandhi rules
vowel_rules = [r for r in data['rules'] if r['category'] == 'svara']
print(f"Vowel Sandhi rules: {len(vowel_rules)}")
```

#### `sandhi_rules.csv`
Same data in CSV format.

---

### 3. Statistics

#### `statistics.json`
Detailed corpus statistics:
- Corpus totals
- Dataset breakdown
- Word length statistics
- Frequency distribution

---

### 4. Reference Documentation

#### `grammar_reference.md`
Complete catalog of all Sandhi rules with:
- Descriptions
- Paninian sutra references
- Pattern explanations
- Examples

---

### 5. Database

#### `vedic_tokenizer.db` (SQLite)
Queryable database with tables:
- `vocabulary` - All words with metadata
- `sandhi_rules` - All transformation rules
- `datasets` - Source text information

**Example Queries**:

```sql
-- Top 50 most frequent words
SELECT word, frequency FROM vocabulary ORDER BY frequency DESC LIMIT 50;

-- All high-priority Guna sandhi rules
SELECT * FROM sandhi_rules 
WHERE category = 'svara' 
  AND description LIKE '%guna%' 
  AND priority >= 8;

-- Words longer than 15 characters
SELECT word, length FROM vocabulary WHERE length > 15 ORDER BY frequency DESC;
```

---

## Use Cases

### 1. Machine Learning / NLP
- Train Sanskrit word embeddings
- Build language models
- Create tokenization datasets
- Develop grammar checkers

### 2. Linguistic Research
- Study word frequency distributions
- Analyze Sandhi patterns
- Compare Vedic vs. Epic Sanskrit
- Validate grammar rules

### 3. Educational Tools
- Create Sanskrit learning apps
- Build rule-based parsers
- Generate practice exercises
- Develop interactive tutorials

### 4. Text Processing
- Implement custom tokenizers
- Build spell checkers
- Create autocomplete systems
- Develop translation tools

---

## Technical Details

### Sandhi Rule Format

Each rule can be applied in two directions:

**Forward** (Combining):
```
left_word + right_word → combined_form
Example: "महा" + "इन्द्रः" → "महेन्द्रः"
```

**Reverse** (Splitting):
```
combined_form → left_word + right_word
Example: "महेन्द्रः" → "महा" + "इन्द्रः"
```

### Priority Levels

Rules are prioritized 1-10:
- **10**: Extremely common (e.g., a+a→ā)
- **7-9**: Common
- **4-6**: Moderate
- **1-3**: Rare/specialized

Use high-priority rules in fast mode for performance.

---

## Citation

If you use this dataset in research, please cite:

```
Vedic Zero-Error Tokenizer Dataset
Extracted from: Atharvaveda, Valmiki Ramayana, Bhagavad Gita, Mahabharata
Total Corpus: 98,000 verses, 1,130,149 words
Year: 2026
```

---

## License

This dataset is derived from public domain Sanskrit texts and grammar rules
documented in classical sources (Panini's Ashtadhyayi, Siddhanta Kaumudi).

---

## Contact & Support

For questions or issues with this dataset, please refer to the main
Vedic Tokenizer project repository.

---

*Generated automatically by Vedic Tokenizer Dataset Exporter*
