"""
Unicode Normalization Module for Devanagari Text

Handles:
- NFC/NFD normalization
- Vedic accent mark preservation
- Whitespace standardization
- Non-Vedic symbol filtering
"""

import unicodedata
from typing import Set


class DevanagariNormalizer:
    """
    Normalizes Devanagari text for consistent tokenization.
    
    This module ensures that different Unicode representations of the same
    Devanagari character are treated identically, while preserving authentic
    Vedic accent marks (Swara) that appear in ancient manuscripts.
    """
    
    # Vedic accent marks to preserve (Sw ara - tone marks)
    VEDIC_ACCENTS: Set[str] = {
        '\u0951',  # Udatta
        '\u0952',  # Anudatta
        '\u1CD0',  # Vedic tone karshana
        '\u1CD1',  # Vedic tone shara
        '\u1CD2',  # Vedic tone prenkha
        '\u1CD3',  # Vedic sign nihshvasa
    }
    
    # Devanagari range
    DEVANAGARI_START = 0x0900
    DEVANAGARI_END = 0x097F
    
    def __init__(self, preserve_vedic_accents: bool = True):
        """
        Initialize normalizer.
        
        Args:
            preserve_vedic_accents: If True, keeps Vedic tone marks in output
        """
        self.preserve_vedic_accents = preserve_vedic_accents
    
    def normalize(self, text: str) -> str:
        """
        Normalize Devanagari text to canonical form.
        
        Args:
            text: Input Sanskrit text in Devanagari
            
        Returns:
            Normalized text with consistent Unicode representation
            
        Example:
            >>> normalizer = DevanagariNormalizer()
            >>> text = "राम"  # Could be NFC or NFD
            >>> normalized = normalizer.normalize(text)
        """
        # Step 1: Apply NFC normalization (Canonical Composition)
        text = unicodedata.normalize('NFC', text)
        
        # Step 2: Standardize whitespace
        text = self._standardize_whitespace(text)
        
        # Step 3: Filter non-Devanagari characters (but keep Vedic marks)
        text = self._filter_non_vedic(text)
        
        return text
    
    def _standardize_whitespace(self, text: str) -> str:
        """
        Convert all whitespace variations to single space.
        
        Args:
            text: Input text
            
        Returns:
            Text with standardized whitespace
        """
        # Replace multiple spaces/tabs/newlines with single space
        import re
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _filter_non_vedic(self, text: str) -> str:
        """
        Remove non-Devanagari characters while preserving Vedic marks.
        
        Args:
            text: Input text
            
        Returns:
            Filtered text containing only Devanagari + Vedic marks + space
        """
        filtered_chars = []
        
        for char in text:
            # Allow space
            if char == ' ':
                filtered_chars.append(char)
                continue
            
            # Allow Vedic accent marks if preservation is enabled
            if self.preserve_vedic_accents and char in self.VEDIC_ACCENTS:
                filtered_chars.append(char)
                continue
            
            # Allow Devanagari characters
            char_code = ord(char)
            if self.DEVANAGARI_START <= char_code <= self.DEVANAGARI_END:
                filtered_chars.append(char)
                continue
            
            # Allow Devanagari extended blocks
            if 0xA8E0 <= char_code <= 0xA8FF:  # Devanagari Extended
                filtered_chars.append(char)
                continue
        
        return ''.join(filtered_chars)
    
    def is_devanagari(self, char: str) -> bool:
        """
        Check if a character is Devanagari.
        
        Args:
            char: Single character to check
            
        Returns:
            True if character is Devanagari
        """
        if len(char) != 1:
            return False
        
        char_code = ord(char)
        return (self.DEVANAGARI_START <= char_code <= self.DEVANAGARI_END or
                0xA8E0 <= char_code <= 0xA8FF)
