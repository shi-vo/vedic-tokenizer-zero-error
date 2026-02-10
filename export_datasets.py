"""
Dataset Exporter for Vedic Tokenizer
=====================================

Creates comprehensive, reusable datasets from the tokenizer for:
- Machine learning training
- Linguistic research
- Sanskrit NLP applications
- Grammar rule validation

Export Formats:
- JSON (structured data)
- CSV (tabular data)
- SQLite (queryable database)
"""

import json
import csv
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from vedic_tokenizer.sandhi_rules import (
    ALL_SANDHI_RULES, 
    SandhiCategory,
    get_rules_by_category
)


class DatasetExporter:
    """Exports tokenizer datasets in multiple formats."""
    
    def __init__(self, vocabulary_file: str, output_dir: str):
        self.vocabulary_file = Path(vocabulary_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Load vocabulary
        with open(self.vocabulary_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.vocabulary = self.data['vocabulary']
        self.stats = self.data['stats']
    
    def export_all(self):
        """Export all datasets in all formats."""
        print("=" * 70)
        print("VEDIC TOKENIZER - DATASET EXPORT")
        print("=" * 70)
        print(f"Export Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Unique Words: {len(self.vocabulary):,}")
        print(f"Total Word Occurrences: {self.stats['total_words']:,}")
        print(f"Total Verses: {self.stats['total_verses']:,}")
        print("=" * 70)
        
        # 1. Vocabulary exports
        self._export_vocabulary_json()
        self._export_vocabulary_csv()
        
        # 2. Sandhi rules export
        self._export_sandhi_rules_json()
        self._export_sandhi_rules_csv()
        
        # 3. Dataset statistics
        self._export_statistics_json()
        
        # 4. Grammar reference
        self._export_grammar_reference()
        
        # 5. SQLite database
        self._export_sqlite_database()
        
        # 6. README documentation
        self._export_readme()
        
        print("\n" + "=" * 70)
        print("✅ EXPORT COMPLETE!")
        print("=" * 70)
        print(f"Output directory: {self.output_dir.absolute()}")
    
    def _export_vocabulary_json(self):
        """Export vocabulary as structured JSON."""
        output_file = self.output_dir / "vocabulary.json"
        
        # Create enriched format
        vocab_list = []
        for word, frequency in sorted(
            self.vocabulary.items(), 
            key=lambda x: x[1], 
            reverse=True
        ):
            vocab_list.append({
                'word': word,
                'frequency': frequency,
                'rank': len(vocab_list) + 1,
                'length': len(word),
                'percentage': round(frequency / self.stats['total_words'] * 100, 4)
            })
        
        export_data = {
            'metadata': {
                'export_date': datetime.now().isoformat(),
                'total_unique_words': len(self.vocabulary),
                'total_occurrences': self.stats['total_words'],
                'total_verses': self.stats['total_verses'],
                'datasets': list(self.stats['dataset_stats'].keys())
            },
            'vocabulary': vocab_list
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Vocabulary JSON: {output_file.name} ({len(vocab_list):,} words)")
    
    def _export_vocabulary_csv(self):
        """Export vocabulary as CSV for easy analysis."""
        output_file = self.output_dir / "vocabulary.csv"
        
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'rank', 'word', 'frequency', 'percentage', 
                'length', 'devanagari_codepoints'
            ])
            
            for rank, (word, freq) in enumerate(
                sorted(self.vocabulary.items(), key=lambda x: x[1], reverse=True),
                start=1
            ):
                percentage = round(freq / self.stats['total_words'] * 100, 4)
                codepoints = ','.join(f"U+{ord(c):04X}" for c in word)
                
                writer.writerow([
                    rank, word, freq, percentage, len(word), codepoints
                ])
        
        print(f"✓ Vocabulary CSV: {output_file.name}")
    
    def _export_sandhi_rules_json(self):
        """Export all Sandhi rules as structured JSON."""
        output_file = self.output_dir / "sandhi_rules.json"
        
        rules_data = {
            'metadata': {
                'export_date': datetime.now().isoformat(),
                'total_rules': len(ALL_SANDHI_RULES),
                'categories': {
                    'vowel': len(get_rules_by_category(SandhiCategory.VOWEL)),
                    'consonant': len(get_rules_by_category(SandhiCategory.CONSONANT)),
                    'visarga': len(get_rules_by_category(SandhiCategory.VISARGA)),
                    'special': len(get_rules_by_category(SandhiCategory.SPECIAL))
                }
            },
            'rules': []
        }
        
        for rule in ALL_SANDHI_RULES:
            rule_dict = {
                'rule_id': rule.rule_id,
                'category': rule.category.value,
                'left_pattern': rule.left_pattern,
                'right_pattern': rule.right_pattern,
                'result': rule.result,
                'priority': rule.priority,
                'vedic_only': rule.vedic_only,
                'panini_sutra': rule.panini_sutra,
                'description': rule.description,
                'examples': [
                    {
                        'left': ex[0],
                        'right': ex[1],
                        'combined': ex[2]
                    } for ex in (rule.examples or [])
                ]
            }
            rules_data['rules'].append(rule_dict)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(rules_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Sandhi Rules JSON: {output_file.name} ({len(ALL_SANDHI_RULES)} rules)")
    
    def _export_sandhi_rules_csv(self):
        """Export Sandhi rules as CSV."""
        output_file = self.output_dir / "sandhi_rules.csv"
        
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'rule_id', 'category', 'left_pattern', 'right_pattern', 
                'result', 'priority', 'vedic_only', 'panini_sutra', 'description'
            ])
            
            for rule in ALL_SANDHI_RULES:
                writer.writerow([
                    rule.rule_id,
                    rule.category.value,
                    rule.left_pattern,
                    rule.right_pattern,
                    rule.result,
                    rule.priority,
                    rule.vedic_only,
                    rule.panini_sutra or '',
                    rule.description
                ])
        
        print(f"✓ Sandhi Rules CSV: {output_file.name}")
    
    def _export_statistics_json(self):
        """Export detailed statistics."""
        output_file = self.output_dir / "statistics.json"
        
        # Calculate additional statistics
        word_lengths = [len(word) for word in self.vocabulary.keys()]
        
        stats_data = {
            'export_date': datetime.now().isoformat(),
            'corpus_statistics': {
                'total_verses': self.stats['total_verses'],
                'total_words': self.stats['total_words'],
                'unique_words': len(self.vocabulary),
                'vocabulary_diversity': round(
                    len(self.vocabulary) / self.stats['total_words'], 4
                )
            },
            'dataset_breakdown': self.stats['dataset_stats'],
            'word_length_statistics': {
                'min_length': min(word_lengths),
                'max_length': max(word_lengths),
                'avg_length': round(sum(word_lengths) / len(word_lengths), 2)
            },
            'frequency_distribution': {
                'top_1_percent': sum(
                    freq for freq in sorted(
                        self.vocabulary.values(), 
                        reverse=True
                    )[:int(len(self.vocabulary) * 0.01)]
                ),
                'top_10_percent': sum(
                    freq for freq in sorted(
                        self.vocabulary.values(), 
                        reverse=True
                    )[:int(len(self.vocabulary) * 0.1)]
                ),
            }
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Statistics JSON: {output_file.name}")
    
    def _export_grammar_reference(self):
        """Export comprehensive grammar reference."""
        output_file = self.output_dir / "grammar_reference.md"
        
        content = f"""# Sanskrit Grammar Reference
*Generated from Vedic Tokenizer*

## Sandhi Rules Catalog

This document contains all {len(ALL_SANDHI_RULES)} Sandhi (phonetic transformation) rules 
implemented in the tokenizer, organized by category.

---

"""
        
        for category in SandhiCategory:
            rules = get_rules_by_category(category)
            if not rules:
                continue
            
            content += f"## {category.value.upper()} SANDHI ({len(rules)} rules)\n\n"
            
            for rule in sorted(rules, key=lambda r: r.rule_id):
                content += f"### {rule.rule_id}: {rule.description}\n\n"
                
                if rule.panini_sutra:
                    content += f"**Pāṇini Sūtra**: {rule.panini_sutra}\n\n"
                
                content += f"**Pattern**: `{rule.left_pattern}` + `{rule.right_pattern}` → `{rule.result}`\n\n"
                content += f"**Priority**: {rule.priority}/10\n\n"
                
                if rule.vedic_only:
                    content += "**Vedic Only**: Yes\n\n"
                
                if rule.examples:
                    content += "**Examples**:\n"
                    for left, right, combined in rule.examples:
                        content += f"- `{left}` + `{right}` → `{combined}`\n"
                    content += "\n"
                
                content += "---\n\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Grammar Reference: {output_file.name}")
    
    def _export_sqlite_database(self):
        """Export as queryable SQLite database."""
        output_file = self.output_dir / "vedic_tokenizer.db"
        
        # Remove existing database
        if output_file.exists():
            output_file.unlink()
        
        conn = sqlite3.connect(output_file)
        cursor = conn.cursor()
        
        # Create vocabulary table
        cursor.execute("""
            CREATE TABLE vocabulary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL UNIQUE,
                frequency INTEGER NOT NULL,
                rank INTEGER NOT NULL,
                length INTEGER NOT NULL,
                percentage REAL NOT NULL
            )
        """)
        
        # Create sandhi_rules table
        cursor.execute("""
            CREATE TABLE sandhi_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_id TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                left_pattern TEXT,
                right_pattern TEXT,
                result TEXT,
                priority INTEGER NOT NULL,
                vedic_only BOOLEAN NOT NULL,
                panini_sutra TEXT,
                description TEXT
            )
        """)
        
        # Create datasets table
        cursor.execute("""
            CREATE TABLE datasets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                verses INTEGER NOT NULL,
                words INTEGER NOT NULL
            )
        """)
        
        # Insert vocabulary
        for rank, (word, freq) in enumerate(
            sorted(self.vocabulary.items(), key=lambda x: x[1], reverse=True),
            start=1
        ):
            percentage = freq / self.stats['total_words'] * 100
            cursor.execute(
                "INSERT INTO vocabulary (word, frequency, rank, length, percentage) VALUES (?, ?, ?, ?, ?)",
                (word, freq, rank, len(word), percentage)
            )
        
        # Insert Sandhi rules
        for rule in ALL_SANDHI_RULES:
            cursor.execute(
                """INSERT INTO sandhi_rules 
                   (rule_id, category, left_pattern, right_pattern, result, 
                    priority, vedic_only, panini_sutra, description) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (rule.rule_id, rule.category.value, rule.left_pattern,
                 rule.right_pattern, rule.result, rule.priority,
                 rule.vedic_only, rule.panini_sutra, rule.description)
            )
        
        # Insert dataset info
        for dataset_name, stats in self.stats['dataset_stats'].items():
            cursor.execute(
                "INSERT INTO datasets (name, verses, words) VALUES (?, ?, ?)",
                (dataset_name, stats['verses'], stats['words'])
            )
        
        # Create indexes
        cursor.execute("CREATE INDEX idx_word_frequency ON vocabulary(frequency DESC)")
        cursor.execute("CREATE INDEX idx_word_rank ON vocabulary(rank)")
        cursor.execute("CREATE INDEX idx_rule_category ON sandhi_rules(category)")
        cursor.execute("CREATE INDEX idx_rule_priority ON sandhi_rules(priority DESC)")
        
        conn.commit()
        conn.close()
        
        print(f"✓ SQLite Database: {output_file.name}")
    
    def _export_readme(self):
        """Export README with usage instructions."""
        output_file = self.output_dir / "README.md"
        
        content = f"""# Vedic Tokenizer - Exported Datasets

**Export Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

This package contains comprehensive datasets extracted from the Vedic Tokenizer project,
including vocabulary from authentic Sanskrit texts, complete Sandhi rule catalogs, and
linguistic statistics.

## Corpus Statistics

- **Total Verses**: {self.stats['total_verses']:,}
- **Total Words**: {self.stats['total_words']:,}
- **Unique Words**: {len(self.vocabulary):,}
- **Vocabulary Diversity**: {round(len(self.vocabulary) / self.stats['total_words'], 4)}

## Source Texts

| Dataset | Verses | Words |
|---------|--------|-------|
"""
        
        for dataset, stats in self.stats['dataset_stats'].items():
            content += f"| {dataset.replace('_', ' ').title()} | {stats['verses']:,} | {stats['words']:,} |\n"
        
        content += f"""
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
    print(f"{{word_info['rank']}}. {{word_info['word']}} = {{word_info['frequency']:,}}")
```

#### `vocabulary.csv` (Tabular Format)
Same data in CSV for spreadsheet analysis.

**Columns**: rank, word, frequency, percentage, length, devanagari_codepoints

---

### 2. Sandhi Rules

#### `sandhi_rules.json` (Structured Format)
All {len(ALL_SANDHI_RULES)} Sandhi transformation rules:
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
print(f"Vowel Sandhi rules: {{len(vowel_rules)}}")
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
Total Corpus: {self.stats['total_verses']:,} verses, {self.stats['total_words']:,} words
Year: {datetime.now().year}
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
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ README: {output_file.name}")


if __name__ == '__main__':
    exporter = DatasetExporter(
        vocabulary_file='vedic_vocabulary.json',
        output_dir='exported_datasets'
    )
    exporter.export_all()
