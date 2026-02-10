"""
Dictionary and Vocabulary Management

Provides interfaces for:
- Mock dictionary (for development)
- JSON file loading (for authentic Vedic datasets)
- Custom vocabulary objects
- Caching for performance
"""

import json
import re
from typing import Set, List, Optional, Dict
from pathlib import Path


class SanskritDictionary:
    """
    Sanskrit word dictionary with multiple loading mechanisms.
    
    This class provides the vocabulary needed for Sandhi validation.
    It supports both mock data (for testing) and real Vedic datasets.
    """
    
    def __init__(self):
        """Initialize empty dictionary."""
        self.words: Set[str] = set()
        self.word_frequencies: Dict[str, int] = {}  # Track word frequencies
        self._load_mock_words()
    
    def _load_mock_words(self):
        """
        Load a small set of common Sanskrit words for testing.
        
        This mock implementation provides basic vocabulary until
        authentic Vedic datasets are loaded.
        """
        mock_vocabulary = {
            # Common nouns
            "राम", "सीता", "लक्ष्मण", "हनुमान्",
            "गज", "इन्द्र", "गजेन्द्र",
            "धर्म", "अर्थ", "काम", "मोक्ष",
            
            # Pronouns
            "अहम्", "त्वम्", "सः", "सा", "तत्",
            
            # Verbs (roots)
            "गच्छ", "पठ्", "लिख्", "कृ",
            
            # Common adjectives
            "सुन्दर", "महान्", "छोट", "बड़",
            
            # Numbers
            "एक", "द्वि", "त्रि", "चतुर्",
            
            # Particles
            "च", "वा", "अपि", "एव",
        }
        
        self.words.update(mock_vocabulary)
    
    def contains(self, word: str) -> bool:
        """
        Check if a word exists in the dictionary.
        
        Args:
            word: Sanskrit word to check
            
        Returns:
            True if word is in dictionary
        """
        return word in self.words
    
    def add_word(self, word: str):
        """
        Add a single word to dictionary.
        
        Args:
            word: Sanskrit word to add
        """
        if word and word.strip():
            cleaned = word.strip()
            self.words.add(cleaned)
            # Track frequency
            self.word_frequencies[cleaned] = self.word_frequencies.get(cleaned, 0) + 1
    
    def add_words(self, words: List[str]):
        """
        Add multiple words to dictionary.
        
        Args:
            words: List of Sanskrit words
        """
        for word in words:
            self.add_word(word)
    
    def load_from_json(
        self,
        filepath: str,
        text_field: str = "content",
        extract_words: bool = True
    ):
        """
        Load vocabulary from JSON file (e.g., Ramayan, Veda data).
        
        This method parses your authentic Vedic datasets and extracts
        the vocabulary needed for Sandhi validation.
        
        Args:
            filepath: Path to JSON file
            text_field: JSON field containing Sanskrit text
            extract_words: If True, automatically extract words from text
            
        Example:
            >>> dict = SanskritDictionary()
            >>> dict.load_from_json(
            ...     "data/1_बाल_काण्ड_data.json",
            ...     text_field="content"
            ... )
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"JSON file not found: {filepath}")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle list of verses (like Ramayan data)
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and text_field in item:
                    text = item[text_field]
                    if extract_words:
                        self._extract_words_from_text(text)
                    else:
                        self.add_word(text)
        
        # Handle structured format with nested keys
        elif isinstance(data, dict):
            self._recursive_extract(data, text_field, extract_words)
    
    def _recursive_extract(
        self,
        data: Dict,
        text_field: str,
        extract_words: bool
    ):
        """
        Recursively extract text from nested JSON structure.
        
        Args:
            data: JSON data (dict or list)
            text_field: Field name to extract
            extract_words: Whether to tokenize text into words
        """
        if isinstance(data, dict):
            if text_field in data:
                text = data[text_field]
                if isinstance(text, str):
                    if extract_words:
                        self._extract_words_from_text(text)
                    else:
                        self.add_word(text)
            
            # Recurse into nested structures
            for value in data.values():
                if isinstance(value, (dict, list)):
                    self._recursive_extract(value, text_field, extract_words)
        
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    self._recursive_extract(item, text_field, extract_words)
    
    def _extract_words_from_text(self, text: str):
        """
        Extract individual words from a text passage.
        
        This uses simple whitespace splitting plus some heuristics
        to identify word boundaries in Devanagari.
        
        Args:
            text: Sanskrit text passage
        """
        # Remove punctuation marks
        text = re.sub(r'[।॥\.,\n]', ' ', text)
        
        # Split on whitespace
        words = text.split()
        
        for word in words:
            word = word.strip()
            if word:
                self.add_word(word)
                
                # Also add sub-words (for compound analysis)
                # This is a heuristic - real compound breaking is complex
                if len(word) > 6:  # Likely a compound
                    # Add potential component words (simplified)
                    for i in range(2, len(word) - 1):
                        self.add_word(word[:i])
                        self.add_word(word[i:])
    
    def load_from_text_file(self, filepath: str):
        """
        Load words from a plain text file (one word per line).
        
        Args:
            filepath: Path to text file
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Text file not found: {filepath}")
        
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word and not word.startswith('#'):  # Skip comments
                    self.add_word(word)
    
    def size(self) -> int:
        """
        Get number of words in dictionary.
        
        Returns:
            Dictionary size
        """
        return len(self.words)
    
    def get_words_starting_with(self, prefix: str) -> List[str]:
        """
        Get all words starting with a given prefix.
        
        Useful for compound word analysis.
        
        Args:
            prefix: Word prefix to search
            
        Returns:
            List of matching words
        """
        return [w for w in self.words if w.startswith(prefix)]
    
    def get_words_ending_with(self, suffix: str) -> List[str]:
        """
        Get all words ending with a given suffix.
        
        Args:
            suffix: Word suffix to search
            
        Returns:
            List of matching words
        """
        return [w for w in self.words if w.endswith(suffix)]
    
    def get_word_frequency(self, word: str) -> int:
        """
        Get the frequency count for a word.
        
        Args:
            word: Sanskrit word
            
        Returns:
            Frequency count (0 if word not in dictionary)
        """
        return self.word_frequencies.get(word, 0)
    
    def has_word(self, word: str) -> bool:
        """
        Check if word exists in dictionary (alias for contains).
        
        Args:
            word: Sanskrit word
            
        Returns:
            True if word exists
        """
        return word in self.words
