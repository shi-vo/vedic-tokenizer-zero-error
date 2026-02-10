"""
Lossless Verification Layer

Ensures zero-error guarantee by validating tokenization reversibility.
"""

from typing import List, Tuple, Dict


class TokenizationVerifier:
    """
    Verifies the lossless property of tokenization.
    
    This is the mathematical guarantee that distinguishes this tokenizer:
    detokenize(tokenize(text)) == text
    """
    
    def __init__(self):
        """Initialize verifier with metrics tracking."""
        self.total_verifications = 0
        self.successful_verifications = 0
        self.failed_verifications = 0
    
    def verify_integrity(
        self,
        original_text: str,
        tokens: List[str]
    ) -> Tuple[bool, Dict[str, any]]:
        """
        Verify that tokens can reconstruct original text.
        
        This is the CORE PATENT CLAIM: lossless tokenization.
        
        Args:
            original_text: Original input text
            tokens: Tokens produced by tokenizer
            
        Returns:
            Tuple of (is_valid, metrics_dict)
            
        Example:
            >>> verifier = TokenizationVerifier()
            >>> is_valid, metrics = verifier.verify_integrity(
            ...     "राम गच्छति",
            ...     ["राम", " ", "गच्छति"]
            ... )
            >>> assert is_valid == True
        """
        self.total_verifications += 1
        
        # Reconstruct text from tokens
        reconstructed = ''.join(tokens)
        
        # Check exact equality
        is_valid = (reconstructed == original_text)
        
        # Track statistics
        if is_valid:
            self.successful_verifications += 1
        else:
            self.failed_verifications += 1
        
        # Compute metrics
        metrics = {
            'is_valid': is_valid,
            'original_length': len(original_text),
            'reconstructed_length': len(reconstructed),
            'token_count': len(tokens),
            'character_accuracy': self._character_accuracy(original_text, reconstructed),
            'success_rate': self.get_success_rate()
        }
        
        return is_valid, metrics
    
    def _character_accuracy(self, original: str, reconstructed: str) -> float:
        """
        Compute character-level accuracy.
        
        Args:
            original: Original text
            reconstructed: Reconstructed text
            
        Returns:
            Accuracy percentage (0.0 to 1.0)
        """
        if not original:
            return 1.0 if not reconstructed else 0.0
        
        matches = sum(1 for o, r in zip(original, reconstructed) if o == r)
        total = max(len(original), len(reconstructed))
        
        return matches / total if total > 0 else 1.0
    
    def get_success_rate(self) -> float:
        """
        Get overall success rate of verifications.
        
        Returns:
            Success rate (0.0 to 1.0)
        """
        if self.total_verifications == 0:
            return 0.0
        
        return self.successful_verifications / self.total_verifications
    
    def get_metrics_summary(self) -> Dict[str, any]:
        """
        Get summary of all verifications performed.
        
        Returns:
            Dictionary of metrics
        """
        return {
            'total_verifications': self.total_verifications,
            'successful': self.successful_verifications,
            'failed': self.failed_verifications,
            'success_rate': self.get_success_rate()
        }
    
    def reset_metrics(self):
        """Reset all metrics counters."""
        self.total_verifications = 0
        self.successful_verifications = 0
        self.failed_verifications = 0
