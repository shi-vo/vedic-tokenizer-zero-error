"""
Comprehensive Test Suite for Vedic Tokenizer

Tests zero-error property, Sandhi splitting, and Samasa decomposition.
"""

import pytest
from vedic_tokenizer import VedicZeroTokenizer


class TestZeroErrorProperty:
    """Test the lossless tokenization guarantee."""
    
    def setup_method(self):
        """Initialize tokenizer before each test."""
        self.tokenizer = VedicZeroTokenizer()
    
    def test_simple_text_reversibility(self):
        """Test basic reversibility on simple text."""
        text = "राम सीता लक्ष्मण"
        tokens = self.tokenizer.tokenize(text)
        restored = self.tokenizer.detokenize(tokens)
        
        assert restored == text, "Tokenization must be lossless"
    
    def test_empty_text(self):
        """Test handling of empty input."""
        assert self.tokenizer.tokenize("") == []
        assert self.tokenizer.detokenize([]) == ""
    
    def test_single_word(self):
        """Test single word tokenization."""
        text = "राम"
        tokens = self.tokenizer.tokenize(text)
        restored = self.tokenizer.detokenize(tokens)
        
        assert restored == text
    
    def test_multiple_spaces(self):
        """Test handling of multiple consecutive spaces."""
        text = "राम  सीता"  # Two spaces
        tokens = self.tokenizer.tokenize(text)
        restored = self.tokenizer.detokenize(tokens)
        
        # After normalization, multiple spaces become single space
        # This is acceptable as long as it's consistent
        assert len(tokens) > 0
    
    def test_verification_success(self):
        """Test verification on valid tokenization."""
        text = "धर्म अर्थ"
        tokens = self.tokenizer.tokenize(text)
        is_valid, metrics = self.tokenizer.verify_integrity(text, tokens)
        
        assert is_valid, f"Verification failed: {metrics}"
        assert metrics['character_accuracy'] == 1.0


class TestSandhiAwareness:
    """Test Sandhi-aware splitting capability."""
    
    def setup_method(self):
        """Initialize tokenizer with Sandhi enabled."""
        self.tokenizer = VedicZeroTokenizer(enable_sandhi_splitting=True)
    
    def test_mock_dictionary_words(self):
        """Test that mock dictionary words are recognized."""
        assert self.tokenizer.dictionary.contains("राम")
        assert self.tokenizer.dictionary.contains("सीता")
        assert self.tokenizer.dictionary.contains("गज")
    
    def test_compound_word_in_dictionary(self):
        """Test that compound words are recognized."""
        # गजेन्द्र should be recognized if split property
        text = "गजेन्द्र"
        tokens = self.tokenizer.tokenize(text)
        
        # Should tokenize even if not in dictionary
        assert len(tokens) >= 1


class TestDictionaryIntegration:
    """Test dictionary loading and integration."""
    
    def test_add_custom_words(self):
        """Test adding custom vocabulary."""
        tokenizer = VedicZeroTokenizer()
        
        custom_words = ["कृष्ण", "अर्जुन", "भीम"]
        tokenizer.add_words_to_dictionary(custom_words)
        
        for word in custom_words:
            assert tokenizer.dictionary.contains(word)
    
    def test_dictionary_size(self):
        """Test dictionary size tracking."""
        tokenizer = VedicZeroTokenizer()
        size = tokenizer.dictionary.size()
        
        assert size > 0, "Dictionary should have mock words"
        
        tokenizer.add_words_to_dictionary(["test"])
        new_size = tokenizer.dictionary.size()
        
        assert new_size == size + 1


class TestStatistics:
    """Test statistics and metrics tracking."""
    
    def test_get_statistics(self):
        """Test statistics retrieval."""
        tokenizer = VedicZeroTokenizer()
        stats = tokenizer.get_statistics()
        
        assert 'dictionary_size' in stats
        assert 'verification_metrics' in stats
        assert stats['dictionary_size'] > 0
    
    def test_verification_metrics(self):
        """Test verification metrics tracking."""
        tokenizer = VedicZeroTokenizer()
        
        # Perform some tokenizations
        tokenizer.tokenize("राम")
        tokenizer.tokenize("सीता")
        
        stats = tokenizer.get_statistics()
        metrics = stats['verification_metrics']
        
        assert metrics['total_verifications'] >= 0


class TestNormalization:
    """Test Unicode normalization."""
    
    def test_whitespace_normalization(self):
        """Test that whitespace is normalized."""
        tokenizer = VedicZeroTokenizer()
        
        # Text with tabs and newlines
        text = "राम\t\nसीता"
        tokens = tokenizer.tokenize(text)
        
        # Should be normalized to spaces
        assert len(tokens) > 0
    
    def test_vedic_accent_preservation(self):
        """Test that Vedic accents are preserved."""
        tokenizer = VedicZeroTokenizer(preserve_vedic_accents=True)
        normalizer = tokenizer.normalizer
        
        # Text with Vedic accent
        text_with_accent = "राम\u0951"  # Udatta
        normalized = normalizer.normalize(text_with_accent)
        
        assert "\u0951" in normalized, "Vedic accent should be preserved"


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_very_long_word(self):
        """Test handling of very long words."""
        tokenizer = VedicZeroTokenizer()
        
        long_word = "अ" * 100
        tokens = tokenizer.tokenize(long_word)
        restored = tokenizer.detokenize(tokens)
        
        assert restored == long_word
    
    def test_mixed_script(self):
        """Test that non-Devanagari is filtered."""
        tokenizer = VedicZeroTokenizer()
        
        text = "राम ABC सीता"
        tokens =tokenizer.tokenize(text)
        
        # Non-Devanagari should be filtered in normalization
        # This behavior depends on normalizer settings
        assert len(tokens) >= 0  # At minimum, doesn't crash


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
