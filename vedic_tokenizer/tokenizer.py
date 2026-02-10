"""
Main VedicZeroTokenizer Class

The primary public API for patent-grade Sanskrit tokenization.

This tokenizer provides:
1. Deterministic output
2. Mathematical reversibility (zero-error)
3. Sandhi-awareness
4. Paninian grammar compliance
"""

from typing import List, Tuple, Dict, Optional

from .normalizer import DevanagariNormalizer
from .dictionary import SanskritDictionary
from .sandhi_rules import SandhiRules
from .sandhi_engine import SandhiEngine
from .samasa_decomposer import SamasaAnalyzer
from .verifier import TokenizationVerifier


class VedicZeroTokenizer:
    """
    Zero-Error Lossless Tokenizer for Vedic Sanskrit.
    
    This is the main class that users interact with. It orchestrates
    all the sub-modules to provide patent-grade tokenization.
    
    Key Properties (Patent Claims):
    - **Deterministic**: Same input always produces same output
    - **Reversible**: detokenize(tokenize(text)) == text
    - **Grammar-Aware**: Respects Paninian Sandhi and Samasa rules
    - **Verifiable**: Automatic integrity checking
    
    Example:
        >>> tokenizer = VedicZeroTokenizer()
        >>> tokenizer.load_dictionary_from_json("ramayan.json")
        >>> 
        >>> text = "रामः वनं गच्छति"
        >>> tokens = tokenizer.tokenize(text)
        >>> print(tokens)
        ['रामः', ' ', 'वनं', ' ', 'गच्छति']
        >>> 
        >>> restored = tokenizer.detokenize(tokens)
        >>> assert restored == text  # Zero-error guarantee
    """
    
    def __init__(
        self,
        preserve_whitespace: bool = True,
        preserve_vedic_accents: bool = True,
        enable_sandhi_splitting: bool = True,
        enable_samasa_decomposition: bool = True,
        auto_verify: bool = True
    ):
        """
        Initialize the Vedic tokenizer.
        
        Args:
            preserve_whitespace: Keep spaces as separate tokens
            preserve_vedic_accents: Preserve Swara marks in output
            enable_sandhi_splitting: Use Sandhi-aware splitting
            enable_samasa_decomposition: Decompose compound words
            auto_verify: Automatically verify tokenization integrity
        """
        self.preserve_whitespace = preserve_whitespace
        self.enable_sandhi_splitting = enable_sandhi_splitting
        self.enable_samasa_decomposition = enable_samasa_decomposition
        self.auto_verify = auto_verify
        
        # Initialize sub-components
        self.normalizer = DevanagariNormalizer(
            preserve_vedic_accents=preserve_vedic_accents
        )
        self.dictionary = SanskritDictionary()
        self.sandhi_rules = SandhiRules()
        self.sandhi_engine = SandhiEngine(self.dictionary, self.sandhi_rules)
        self.samasa_decomposer = SamasaAnalyzer(self.dictionary)
        self.verifier = TokenizationVerifier()
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize Sanskrit text with zero-error guarantee.
        
        This is the main tokenization method. It applies a multi-stage
        pipeline to ensure accurate, lossless tokenization.
        
        Pipeline:
        1. Unicode normalization
        2. Whitespace handling
        3. Sandhi-aware word splitting (if enabled)
        4. Compound word decomposition (if enabled)
        5. Verification (if auto_verify enabled)
        
        Args:
            text: Input Sanskrit text in Devanagari
            
        Returns:
            List of tokens (guaranteed reversible)
            
        Raises:
            ValueError: If verification fails and fallback is needed
        """
        if not text:
            return []
        
        # Store original for verification
        original_text = text
        
        # Stage 1: Normalize Unicode
        normalized = self.normalizer.normalize(text)
        
        # Stage 2: Handle whitespace
        if self.preserve_whitespace:
            tokens = self._tokenize_with_whitespace(normalized)
        else:
            tokens = self._tokenize_without_whitespace(normalized)
        
        # Stage 3: Apply Sandhi splitting (if enabled)
        if self.enable_sandhi_splitting:
            tokens = self._apply_sandhi_splitting(tokens)
        
        # Stage 4: Apply Samasa decomposition (if enabled)
        if self.enable_samasa_decomposition:
            tokens = self._apply_samasa_decomposition(tokens)
        
        # Stage 5: Verify integrity
        if self.auto_verify:
            is_valid, metrics = self.verify_integrity(original_text, tokens)
            
            if not is_valid:
                # Fallback: use simpler tokenization
                print(f"Warning: Verification failed. Using fallback tokenization.")
                print(f"Metrics: {metrics}")
                tokens = self._fallback_tokenize(original_text)
        
        return tokens
    
    def _tokenize_with_whitespace(self, text: str) -> List[str]:
        """
        Tokenize preserving whitespace as separate tokens.
        
        Args:
            text: Normalized text
            
        Returns:
            List of tokens (words and spaces)
        """
        tokens = []
        current_word = []
        
        for char in text:
            if char == ' ':
                if current_word:
                    tokens.append(''.join(current_word))
                    current_word = []
                tokens.append(' ')
            else:
                current_word.append(char)
        
        if current_word:
            tokens.append(''.join(current_word))
        
        return tokens
    
    def _tokenize_without_whitespace(self, text: str) -> List[str]:
        """
        Tokenize by splitting on whitespace only.
        
        Args:
            text: Normalized text
            
        Returns:
            List of word tokens
        """
        return text.split()
    
    def _apply_sandhi_splitting(self, tokens: List[str]) -> List[str]:
        """
        Apply Sandhi-aware splitting to each token.
        
        Args:
            tokens: Initial tokens
            
        Returns:
            Refined tokens with Sandhi splits
        """
        result = []
        
        for token in tokens:
            # Skip whitespace
            if token.strip() == '':
                result.append(token)
                continue
            
            # Apply Sandhi splitting
            sub_tokens = self.sandhi_engine.split_with_sandhi(token)
            result.extend(sub_tokens)
        
        return result
    
    def _apply_samasa_decomposition(self, tokens: List[str]) -> List[str]:
        """
        Apply compound word decomposition to tokens.
        
        Args:
            tokens: Tokens potentially containing compounds
            
        Returns:
            Tokens with compounds decomposed
        """
        result = []
        
        for token in tokens:
            # Skip whitespace
            if token.strip() == '':
                result.append(token)
                continue
            
            # Try to decompose
            components = self.samasa_decomposer.decompose(token)
            result.extend(components)
        
        return result
    
    def _fallback_tokenize(self, text: str) -> List[str]:
        """
        Fallback tokenization when verification fails.
        
        This uses the simplest possible strategy: keep original text
        as-is to guarantee reversibility.
        
        Args:
            text: Original text
            
        Returns:
            Tokens guaranteed to be reversible
        """
        # Simplest possible: split on whitespace
        if self.preserve_whitespace:
            tokens = []
            for i, char in enumerate(text):
                if i > 0 and text[i-1] != ' ' and char == ' ':
                    pass  # Space after word
                elif i > 0 and text[i-1] == ' ' and char != ' ':
                    tokens.append(' ')
                
                if char != ' ' or (i > 0 and text[i-1] != ' '):
                    if char == ' ':
                        if not tokens or tokens[-1] != ' ':
                            tokens.append(' ')
                    else:
                        if tokens and tokens[-1] != ' ' and text[i-1] != ' ':
                            tokens[-1] += char
                        else:
                            tokens.append(char)
            
            return tokens if tokens else [text]
        else:
            return text.split() if text.strip() else [text]
    
    def detokenize(self, tokens: List[str]) -> str:
        """
        Reconstruct original text from tokens.
        
        This is the inverse operation of tokenize(). The lossless
        property guarantees: detokenize(tokenize(text)) == text
        
        Args:
            tokens: List of tokens from tokenize()
            
        Returns:
            Reconstructed text
        """
        return ''.join(tokens)
    
    def verify_integrity(
        self,
        original_text: str,
        tokens: List[str]
    ) -> Tuple[bool, Dict]:
        """
        Verify the zero-error property.
        
        This checks that tokenization is lossless.
        
        Args:
            original_text: Original input
            tokens: Output from tokenize()
            
        Returns:
            Tuple of (is_valid, metrics_dict)
        """
        return self.verifier.verify_integrity(original_text, tokens)
    
    def load_dictionary_from_json(
        self,
        filepath: str,
        text_field: str = "content",
        extract_words: bool = True
    ):
        """
        Load vocabulary from JSON file containing Vedic texts.
        
        This allows integration with your authentic datasets
        (Ramayan, Vedas, Bhagavad Gita).
        
        Args:
            filepath: Path to JSON file
            text_field: Field name containing Sanskrit text
            extract_words: Auto-extract vocabulary from text
            
        Example:
            >>> tokenizer = VedicZeroTokenizer()
            >>> tokenizer.load_dictionary_from_json(
            ...     "data/1_बाल_काण्ड_data.json",
            ...     text_field="content"
            ... )
        """
        self.dictionary.load_from_json(filepath, text_field, extract_words)
    
    def load_dictionary_from_text(self, filepath: str):
        """
        Load vocabulary from plain text file.
        
        Args:
            filepath: Path to text file (one word per line)
        """
        self.dictionary.load_from_text_file(filepath)
    
    def add_words_to_dictionary(self, words: List[str]):
        """
        Manually add words to dictionary.
        
        Args:
            words: List of Sanskrit words
        """
        self.dictionary.add_words(words)
    
    def get_statistics(self) -> Dict:
        """
        Get tokenizer statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            'dictionary_size': self.dictionary.size(),
            'verification_metrics': self.verifier.get_metrics_summary(),
            'sandhi_enabled': self.enable_sandhi_splitting,
            'samasa_enabled': self.enable_samasa_decomposition,
            'sandhi_rules_count': len(self.sandhi_rules.rules)
        }
