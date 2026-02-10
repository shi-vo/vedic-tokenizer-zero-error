"""
Automated Data Loader for Vedic Texts
======================================

Loads all Sanskrit texts from the data/ directory and builds comprehensive
vocabulary with frequency statistics.

Datasets:
- Atharvaveda (~20 kaandas)
- Valmiki Ramayana (7 kaandas, ~24,000 shlokas)
- Bhagavad Gita (18 chapters, 700 verses)
- Mahabharata (18 parvas, ~100,000 shlokas)
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import Counter
import re


class VedicCorpusLoader:
    """Loads and processes all Vedic texts."""
    
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.vocabulary: Counter = Counter()
        self.total_words = 0
        self.total_verses = 0
        self.dataset_stats = {}
        
    def load_all_datasets(self) -> Dict[str, any]:
        """Load all datasets and build unified vocabulary."""
        print("Loading Vedic Corpus...")
        
        # Load each dataset
        self._load_atharvaveda()
        self._load_ramayana()
        self._load_bhagavad_gita()
        self._load_mahabharata()
        
        print(f"\n✅ Corpus loaded successfully!")
        print(f"📊 Total verses: {self.total_verses:,}")
        print(f"📊 Total words: {self.total_words:,}")
        print(f"📊 Unique words: {len(self.vocabulary):,}")
        
        return {
            'vocabulary': dict(self.vocabulary),
            'total_words': self.total_words,
            'total_verses': self.total_verses,
            'dataset_stats': self.dataset_stats
        }
    
    def _load_atharvaveda(self):
        """Load Atharvaveda kaandas."""
        print("\n📖 Loading Atharvaveda...")
        dataset_dir = self.data_dir / "atharvaveda"
        
        verse_count = 0
        word_count = 0
        
        for json_file in sorted(dataset_dir.glob("*.json")):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for item in data:
                if 'text' in item:
                    verse_count += 1
                    words = self._extract_words(item['text'])
                    word_count += len(words)
                    self.vocabulary.update(words)
        
        self.dataset_stats['atharvaveda'] = {
            'verses': verse_count,
            'words': word_count
        }
        self.total_verses += verse_count
        self.total_words += word_count
        
        print(f"   ✓ Atharvaveda: {verse_count:,} verses, {word_count:,} words")
    
    def _load_ramayana(self):
        """Load Valmiki Ramayana."""
        print("\n📖 Loading Valmiki Ramayana...")
        dataset_dir = self.data_dir / "ValmikiRamayana"
        
        verse_count = 0
        word_count = 0
        
        for json_file in sorted(dataset_dir.glob("*.json")):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for item in data:
                if 'text' in item:
                    verse_count += 1
                    words = self._extract_words(item['text'])
                    word_count += len(words)
                    self.vocabulary.update(words)
        
        self.dataset_stats['ramayana'] = {
            'verses': verse_count,
            'words': word_count
        }
        self.total_verses += verse_count
        self.total_words += word_count
        
        print(f"   ✓ Ramayana: {verse_count:,} verses, {word_count:,} words")
    
    def _load_bhagavad_gita(self):
        """Load Bhagavad Gita."""
        print("\n📖 Loading Bhagavad Gita...")
        dataset_dir = self.data_dir / "SrimadBhagvadGita"
        
        verse_count = 0
        word_count = 0
        
        for json_file in sorted(dataset_dir.glob("*.json")):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle nested structure
            if 'BhagavadGitaChapter' in data:
                for verse in data['BhagavadGitaChapter']:
                    if 'text' in verse:
                        verse_count += 1
                        words = self._extract_words(verse['text'])
                        word_count += len(words)
                        self.vocabulary.update(words)
        
        self.dataset_stats['bhagavad_gita'] = {
            'verses': verse_count,
            'words': word_count
        }
        self.total_verses += verse_count
        self.total_words += word_count
        
        print(f"   ✓ Bhagavad Gita: {verse_count:,} verses, {word_count:,} words")
    
    def _load_mahabharata(self):
        """Load Mahabharata."""
        print("\n📖 Loading Mahabharata...")
        dataset_dir = self.data_dir / "Mahabharata"
        
        verse_count = 0
        word_count = 0
        
        for json_file in sorted(dataset_dir.glob("*.json")):
            with open(json_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except Exception as e:
                    print(f"   ⚠ Skipping {json_file.name}: {e}")
                    continue
            
            # Mahabharata structure may vary
            if isinstance(data, list):
                for item in data:
                    if 'text' in item or 'content' in item:
                        verse_count += 1
                        text = item.get('text', item.get('content', ''))
                        words = self._extract_words(text)
                        word_count += len(words)
                        self.vocabulary.update(words)
        
        self.dataset_stats['mahabharata'] = {
            'verses': verse_count,
            'words': word_count
        }
        self.total_verses += verse_count
        self.total_words += word_count
        
        print(f"   ✓ Mahabharata: {verse_count:,} verses, {word_count:,} words")
    
    def _extract_words(self, text: str) -> List[str]:
        """
        Extract Sanskrit words from text.
        
        Handles:
        - Devanagari script
        - Punctuation removal
        - Whitespace normalization
        - Accent marks preservation (for Vedic texts)
        """
        # Remove English/metadata
        text = re.sub(r'[a-zA-Z0-9।॥\n\r\.\,\?\!]+', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Split on spaces (preserving words with accent marks)
        words = text.split()
        
        # Filter out empty strings and very short tokens
        words = [w for w in words if len(w) >= 2]
        
        return words
    
    def get_top_words(self, n: int = 100) -> List[Tuple[str, int]]:
        """Get most frequent words."""
        return self.vocabulary.most_common(n)
    
    def save_vocabulary(self, output_file: str):
        """Save vocabulary to file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'vocabulary': dict(self.vocabulary),
                'stats': {
                    'total_words': self.total_words,
                    'total_verses': self.total_verses,
                    'unique_words': len(self.vocabulary),
                    'dataset_stats': self.dataset_stats
                }
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Vocabulary saved to: {output_file}")


if __name__ == '__main__':
    # Load all datasets
    loader = VedicCorpusLoader(data_dir='data')
    corpus_data = loader.load_all_datasets()
    
    # Show top 50 words
    print("\n📊 Top 50 Most Frequent Words:")
    print("=" * 60)
    for i, (word, count) in enumerate(loader.get_top_words(50), 1):
        print(f"{i:2d}. {word:20s} = {count:,} occurrences")
    
    # Save vocabulary
    loader.save_vocabulary('vedic_vocabulary.json')
    
    # Print summary by dataset
    print("\n📈 Dataset Summary:")
    print("=" * 60)
    for dataset, stats in corpus_data['dataset_stats'].items():
        print(f"{dataset.title():20s}: {stats['verses']:6,} verses, {stats['words']:8,} words")
