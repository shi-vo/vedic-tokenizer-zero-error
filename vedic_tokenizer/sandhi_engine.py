"""
Enhanced Sandhi Engine with Multi-Candidate Analysis
=====================================================

Integrates Sandhi, Vibhakti, and Pratyaya analyzers for comprehensive
morphological analysis with intelligent ambiguity resolution.

Scoring Algorithm:
- 40%: Sandhi rule priority (how common/specific the Sandhi pattern is)
- 30%: Vocabulary frequency (how common the resulting words are)
- 30%: Grammatical validity (Vibhakti + Pratyaya recognition)
"""

from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
import math

from .sandhi_rules import get_applicable_rules, ALL_SANDHI_RULES
from .vibhakti_analyzer import VibhaktiAnalyzer
from .pratyaya_analyzer import PratyayaAnalyzer
from .dictionary import SanskritDictionary


@dataclass
class SandhiCandidate:
    """
    Represents a possible Sandhi split with analysis.
    
    Attributes:
        left_word: First component after split
        right_word: Second component after split
        sandhi_rule_id: Which Sandhi rule was applied
        sandhi_priority: Priority of the Sandhi rule (1-10)
        left_frequency: Corpus frequency of left word
        right_frequency: Corpus frequency of right word
        left_vibhakti: Vibhakti analysis of left word (if any)
        right_vibhakti: Vibhakti analysis of right word (if any)
        left_pratyaya: Pratyaya analysis of left word (if any)
        right_pratyaya: Pratyaya analysis of right word (if any)
        total_score: Combined confidence score (0.0-1.0)
    """
    left_word: str
    right_word: str
    sandhi_rule_id: str
    sandhi_priority: int
    left_frequency: int
    right_frequency: int
    left_vibhakti: Optional[str]
    right_vibhakti: Optional[str]
    left_pratyaya: Optional[str]
    right_pratyaya: Optional[str]
    total_score: float
    
    def __repr__(self) -> str:
        return (f"SandhiCandidate({self.left_word} + {self.right_word}, "
                f"score={self.total_score:.3f}, rule={self.sandhi_rule_id})")


class EnhancedSandhiEngine:
    """
    Advanced Sandhi engine with comprehensive morphological analysis.
    
    This engine uses all 344 grammar rules to intelligently split
    Sanskrit text and score multiple candidates.
    """
    
    def __init__(self, dictionary: SanskritDictionary):
        """
        Initialize the enhanced engine.
        
        Args:
            dictionary: Sanskrit dictionary with word frequencies
        """
        self.dictionary = dictionary
        self.vibhakti_analyzer = VibhaktiAnalyzer()
        self.pratyaya_analyzer = PratyayaAnalyzer()
        
        # Scoring weights
        self.SANDHI_WEIGHT = 0.40
        self.FREQUENCY_WEIGHT = 0.30
        self.GRAMMAR_WEIGHT = 0.30
    
    def find_all_splits(self, word: str, max_candidates: int = 10) -> List[SandhiCandidate]:
        """
        Find all possible Sandhi splits for a word.
        
        This uses the comprehensive Sandhi rules to generate multiple
        candidates, then scores each using frequency + grammar analysis.
        
        Args:
            word: Combined word to split
            max_candidates: Maximum number of candidates to return
        
        Returns:
            List of candidates sorted by score (best first)
        """
        candidates = []
        
        # Try splitting at each position
        for i in range(1, len(word)):
            left_part = word[:i]
            right_part = word[i:]
            
            # Find applicable Sandhi rules
            applicable_rules = get_applicable_rules(left_part, right_part, vedic_mode=False)
            
            for rule in applicable_rules:
                # Try to reverse-apply the rule
                splits = rule.apply_reverse(word)
                
                for left, right in splits:
                    # Create candidate and score it
                    candidate = self._create_and_score_candidate(
                        left, right, rule.rule_id, rule.priority
                    )
                    candidates.append(candidate)
        
        # Also try no-split option (word as-is)
        if self.dictionary.has_word(word):
            no_split = self._create_no_split_candidate(word)
            candidates.append(no_split)
        
        # Sort by score and return top candidates
        candidates.sort(key=lambda c: c.total_score, reverse=True)
        return candidates[:max_candidates]
    
    def get_best_split(self, word: str) -> Tuple[str, str]:
        """
        Get the most likely Sandhi split for a word.
        
        Args:
            word: Combined word to split
        
        Returns:
            Tuple of (left_word, right_word). Returns (word, "") if no split found.
        """
        candidates = self.find_all_splits(word, max_candidates=1)
        
        if not candidates:
            return (word, "")
        
        best = candidates[0]
        
        # If best candidate is no-split, return as-is
        if best.right_word == "":
            return (word, "")
        
        return (best.left_word, best.right_word)
    
    def split_with_sandhi(self, text: str) -> List[str]:
        """
        Split text using Sandhi rules (maintains compatibility with old API).
        
        Args:
            text: Text to split
        
        Returns:
            List of tokens
        """
        # Simple implementation: try to split once at best position
        left, right = self.get_best_split(text)
        
        if right:
            return [left, right]
        else:
            return [text]
    
    def _create_and_score_candidate(
        self,
        left: str,
        right: str,
        rule_id: str,
        rule_priority: int
    ) -> SandhiCandidate:
        """Create a candidate and calculate its score."""
        
        # Get word frequencies
        left_freq = self.dictionary.get_word_frequency(left)
        right_freq = self.dictionary.get_word_frequency(right)
        
        # Analyze grammatically
        left_vib = self._analyze_vibhakti(left)
        right_vib = self._analyze_vibhakti(right)
        left_prat = self._analyze_pratyaya(left)
        right_prat = self._analyze_pratyaya(right)
        
        # Calculate component scores
        sandhi_score = rule_priority / 10.0  # Normalize to 0-1
        
        # Frequency score (log-normalized)
        freq_score = self._calculate_frequency_score(left_freq, right_freq)
        
        # Grammar score (bonus for recognized patterns)
        grammar_score = self._calculate_grammar_score(
            left_vib, right_vib, left_prat, right_prat
        )
        
        # Weighted total
        total_score = (
            self.SANDHI_WEIGHT * sandhi_score +
            self.FREQUENCY_WEIGHT * freq_score +
            self.GRAMMAR_WEIGHT * grammar_score
        )
        
        return SandhiCandidate(
            left_word=left,
            right_word=right,
            sandhi_rule_id=rule_id,
            sandhi_priority=rule_priority,
            left_frequency=left_freq,
            right_frequency=right_freq,
            left_vibhakti=left_vib,
            right_vibhakti=right_vib,
            left_pratyaya=left_prat,
            right_pratyaya=right_prat,
            total_score=total_score
        )
    
    def _create_no_split_candidate(self, word: str) -> SandhiCandidate:
        """Create a candidate for keeping the word as-is."""
        freq = self.dictionary.get_word_frequency(word)
        vib = self._analyze_vibhakti(word)
        prat = self._analyze_pratyaya(word)
        
        # High frequency/grammar scores compensate for no Sandhi rule
        freq_score = min(1.0, (freq / 1000.0) if freq > 0 else 0.0)
        grammar_score = 0.8 if (vib or prat) else 0.3
        
        total_score = (
            self.SANDHI_WEIGHT * 0.5 +  # No Sandhi rule penalty
            self.FREQUENCY_WEIGHT * freq_score +
            self.GRAMMAR_WEIGHT * grammar_score
        )
        
        return SandhiCandidate(
            left_word=word,
            right_word="",
            sandhi_rule_id="NO_SPLIT",
            sandhi_priority=5,
            left_frequency=freq,
            right_frequency=0,
            left_vibhakti=vib,
            right_vibhakti=None,
            left_pratyaya=prat,
            right_pratyaya=None,
            total_score=total_score
        )
    
    def _analyze_vibhakti(self, word: str) -> Optional[str]:
        """Analyze word for vibhakti patterns."""
        analyses = self.vibhakti_analyzer.analyze(word)
        if analyses:
            best = analyses[0]
            return f"{best.case.name}_{best.number.name}"
        return None
    
    def _analyze_pratyaya(self, word: str) -> Optional[str]:
        """Analyze word for pratyaya patterns."""
        analyses = self.pratyaya_analyzer.analyze(word)
        if analyses:
            best = analyses[0]
            return f"{best.pratyaya_type.name}"
        return None
    
    def _calculate_frequency_score(self, left_freq: int, right_freq: int) -> float:
        """
        Calculate frequency-based score.
        
        Uses logarithmic scaling to avoid over-weighting very common words.
        """
        if left_freq == 0 or right_freq == 0:
            return 0.0
        
        # Geometric mean of log frequencies
        log_left = math.log(left_freq + 1)
        log_right = math.log(right_freq + 1)
        
        combined = math.sqrt(log_left * log_right)
        
        # Normalize to 0-1 range (assuming max frequency ~10000)
        max_log = math.log(10000)
        return min(1.0, combined / max_log)
    
    def _calculate_grammar_score(
        self,
        left_vib: Optional[str],
        right_vib: Optional[str],
        left_prat: Optional[str],
        right_prat: Optional[str]
    ) -> float:
        """
        Calculate grammar-based score.
        
        Rewards words that have recognized grammatical patterns.
        """
        score = 0.0
        
        # Vibhakti recognition (40% of grammar score)
        if left_vib:
            score += 0.2
        if right_vib:
            score += 0.2
        
        # Pratyaya recognition (40% of grammar score)
        if left_prat:
            score += 0.2
        if right_prat:
            score += 0.2
        
        # Bonus for both words having grammar (20% of grammar score)
        if (left_vib or left_prat) and (right_vib or right_prat):
            score += 0.2
        
        return min(1.0, score)


# Backward compatibility: keep old SandhiEngine class
class SandhiEngine(EnhancedSandhiEngine):
    """Legacy alias for backward compatibility."""
    
    def __init__(self, dictionary, sandhi_rules=None):
        """Initialize with legacy parameters."""
        super().__init__(dictionary)
        # sandhi_rules parameter ignored (we use the comprehensive rule set)
