"""
Samasa (Compound) Analyzer for Sanskrit
========================================

Analyzes and decomposes Sanskrit compound words (samasa) into their
constituent parts.

Types of Samasa (6 main categories):
1. Dvandva (द्वन्द्व): Copulative compounds
2. Tatpurusha (तत्पुरुष): Determinative compounds  
3. Karmadharaya (कर्मधारय): Descriptive compounds
4. Dvigu (द्विगु): Numerical compounds
5. Bahuvrihi (बहुव्रीहि): Possessive compounds
6. Avyayibhava (अव्ययीभाव): Adverbial compounds

Uses longest-match algorithm + dictionary validation.
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

from .dictionary import SanskritDictionary


class SamasaType(Enum):
    """Types of Sanskrit compounds."""
    DVANDVA = "द्वन्द्व"              # Copulative (A and B)
    TATPURUSHA = "तत्पुरुष"           # Determinative (A of B)
    KARMADHARAYA = "कर्मधारय"         # Descriptive (Adjective + Noun)
    DVIGU = "द्विगु"                  # Numerical
    BAHUVRIHI = "बहुव्रीहि"           # Possessive
    AVYAYIBHAVA = "अव्ययीभाव"        # Adverbial


@dataclass
class SamasaAnalysis:
    """
    Result of compound analysis.
    
    Attributes:
        components: List of component words
        samasa_type: Type of compound (if identified)
        confidence: Confidence score (0.0-1.0)
        split_points: Character positions where splits occur
    """
    components: List[str]
    samasa_type: Optional[SamasaType]
    confidence: float
    split_points: List[int]
    
    def __repr__(self) -> str:
        return f"SamasaAnalysis({' + '.join(self.components)}, {self.samasa_type}, conf={self.confidence:.2f})"


class SamasaAnalyzer:
    """
    Analyzes and decomposes Sanskrit compounds.
    
    Uses a combination of:
    - Longest-match algorithm
    - Dictionary validation
    - Pattern recognition
    """
    
    def __init__(self, dictionary: SanskritDictionary):
        """
        Initialize the analyzer.
        
        Args:
            dictionary: Sanskrit dictionary for word validation
        """
        self.dictionary = dictionary
        
        # Common compound patterns
        self.common_prefixes = {
            "महा", "सु", "अ", "दुर्", "नि", "वि", "प्र", "सम्",
            "अति", "अनु", "उप", "परि", "अभि", "अव", "आ"
        }
        
        self.common_suffixes = {
            "त्व", "ता", "मत्", "वत्", "इक", "ईय", "य"
        }
    
    def analyze(self, compound: str, max_components: int = 5) -> List[SamasaAnalysis]:
        """
        Analyze a compound word and propose decompositions.
        
        Args:
            compound: The compound word to analyze
            max_components: Maximum number of components
        
        Returns:
            List of possible analyses, sorted by confidence
        """
        if len(compound) < 4:
            # Too short to be a meaningful compound
            return []
        
        # Try different splitting strategies
        analyses = []
        
        # Strategy 1: Greedy longest-match from left
        left_greedy = self._greedy_split_left(compound, max_components)
        if left_greedy:
            analyses.append(left_greedy)
        
        # Strategy 2: Greedy longest-match from right
        right_greedy = self._greedy_split_right(compound, max_components)
        if right_greedy:
            analyses.append(right_greedy)
        
        # Strategy 3: Balanced split (try to make equal-sized components)
        balanced = self._balanced_split(compound, max_components)
        if balanced:
            analyses.append(balanced)
        
        # Sort by confidence
        analyses.sort(key=lambda a: a.confidence, reverse=True)
        
        # Remove duplicates
        seen = set()
        unique_analyses = []
        for analysis in analyses:
            key = tuple(analysis.components)
            if key not in seen:
                seen.add(key)
                unique_analyses.append(analysis)
        
        return unique_analyses
    
    def decompose(self, compound: str) -> List[str]:
        """
        Get the best decomposition of a compound.
        
        Args:
            compound: The compound word
        
        Returns:
            List of component words (or [compound] if can't decompose)
        """
        analyses = self.analyze(compound, max_components=5)
        
        if analyses and analyses[0].confidence > 0.5:
            return analyses[0].components
        
        # Fallback: return as-is
        return [compound]
    
    def _greedy_split_left(self, compound: str, max_components: int) -> Optional[SamasaAnalysis]:
        """
        Greedy longest-match from left to right.
        
        Tries to find the longest valid word starting from the left,
        then recursively splits the remainder.
        """
        components = []
        split_points = []
        remaining = compound
        position = 0
        
        while remaining and len(components) < max_components:
            found = False
            
            # Try longest matches first
            for length in range(len(remaining), 0, -1):
                candidate = remaining[:length]
                
                if self.dictionary.has_word(candidate):
                    components.append(candidate)
                    split_points.append(position)
                    position += length
                    remaining = remaining[length:]
                    found = True
                    break
            
            if not found:
                # No valid word found, include remainder as-is
                if remaining:
                    components.append(remaining)
                    split_points.append(position)
                break
        
        if len(components) <= 1:
            return None
        
        # Calculate confidence based on dictionary coverage
        valid_count = sum(1 for c in components if self.dictionary.has_word(c))
        confidence = valid_count / len(components)
        
        return SamasaAnalysis(
            components=components,
            samasa_type=self._infer_type(components),
            confidence=confidence,
            split_points=split_points
        )
    
    def _greedy_split_right(self, compound: str, max_components: int) -> Optional[SamasaAnalysis]:
        """
        Greedy longest-match from right to left.
        
        Useful for compounds where the final component is more stable.
        """
        components = []
        split_points = []
        remaining = compound
        
        while remaining and len(components) < max_components:
            found = False
            
            # Try longest matches from the right
            for length in range(len(remaining), 0, -1):
                candidate = remaining[-length:]
                
                if self.dictionary.has_word(candidate):
                    components.insert(0, candidate)
                    split_points.insert(0, len(compound) - len(remaining))
                    remaining = remaining[:-length]
                    found = True
                    break
            
            if not found:
                if remaining:
                    components.insert(0, remaining)
                    split_points.insert(0, 0)
                break
        
        if len(components) <= 1:
            return None
        
        valid_count = sum(1 for c in components if self.dictionary.has_word(c))
        confidence = valid_count / len(components)
        
        return SamasaAnalysis(
            components=components,
            samasa_type=self._infer_type(components),
            confidence=confidence * 0.95,  # Slight penalty vs left-greedy
            split_points=split_points
        )
    
    def _balanced_split(self, compound: str, max_components: int) -> Optional[SamasaAnalysis]:
        """
        Try to split into roughly equal-sized components.
        
        Useful for dvandva compounds.
        """
        if max_components < 2:
            return None
        
        # Try binary split at midpoint
        mid = len(compound) // 2
        
        # Search around midpoint for valid split
        for offset in range(min(mid, len(compound) - mid)):
            for direction in [0, 1]:
                if direction == 0:
                    pos = mid - offset
                else:
                    pos = mid + offset
                
                if pos <= 0 or pos >= len(compound):
                    continue
                
                left = compound[:pos]
                right = compound[pos:]
                
                if self.dictionary.has_word(left) and self.dictionary.has_word(right):
                    return SamasaAnalysis(
                        components=[left, right],
                        samasa_type=SamasaType.DVANDVA,  # Likely copulative
                        confidence=0.8,
                        split_points=[0, pos]
                    )
        
        return None
    
    def _infer_type(self, components: List[str]) -> Optional[SamasaType]:
        """
        Try to infer the type of compound from its components.
        
        This is a simplified heuristic.
        """
        if len(components) == 2:
            # Check for common patterns
            first, second = components
            
            # Numerical compound (dvigu)
            numbers = {"एक", "द्वि", "त्रि", "चतुर्", "पञ्च", "षट्", "सप्त", "अष्ट", "नव", "दश"}
            if first in numbers:
                return SamasaType.DVIGU
            
            # Check for prefixes (likely tatpurusha or avyayibhava)
            if first in self.common_prefixes:
                return SamasaType.TATPURUSHA
            
            # Default to tatpurusha (most common)
            return SamasaType.TATPURUSHA
        
        elif len(components) > 2:
            # Multiple components likely dvandva
            return SamasaType.DVANDVA
        
        return None


def decompose_compound(dictionary: SanskritDictionary, compound: str) -> List[str]:
    """
    Convenience function to decompose a compound.
    
    Args:
        dictionary: Sanskrit dictionary
        compound: Compound word
    
    Returns:
        List of components
    """
    analyzer = SamasaAnalyzer(dictionary)
    return analyzer.decompose(compound)
