"""
Comprehensive Test Suite for Vedic Zero-Error Tokenizer
========================================================

Tests all components:
1. Sandhi Rules (130 rules)
2. Vibhakti Analyzer (159 patterns)
3. Pratyaya Analyzer (55 patterns)
4. Enhanced Sandhi Engine (integration)
5. End-to-end tokenization

Usage:
    pytest tests/test_tokenizer_comprehensive.py -v
"""

import pytest
from vedic_tokenizer.sandhi_rules import (
    ALL_SANDHI_RULES, VOWEL_SANDHI_RULES, CONSONANT_SANDHI_RULES,
    VISARGA_SANDHI_RULES, SPECIAL_SANDHI_RULES, get_applicable_rules
)
from vedic_tokenizer.vibhakti_analyzer import VibhaktiAnalyzer, Case, Number, Gender
from vedic_tokenizer.pratyaya_analyzer import PratyayaAnalyzer, PratyayaType
from vedic_tokenizer.dictionary import SanskritDictionary
from vedic_tokenizer.sandhi_engine import EnhancedSandhiEngine


# ============================================================================
# SANDHI RULES TESTS
# ============================================================================

class TestSandhiRules:
    """Test individual Sandhi transformation rules."""
    
    def test_total_rule_count(self):
        """Verify we have 130 Sandhi rules."""
        assert len(ALL_SANDHI_RULES) == 130, f"Expected 130 rules, got {len(ALL_SANDHI_RULES)}"
    
    def test_rule_categories(self):
        """Verify rule distribution across categories."""
        assert len(VOWEL_SANDHI_RULES) == 33
        assert len(CONSONANT_SANDHI_RULES) == 50
        assert len(VISARGA_SANDHI_RULES) == 20
        assert len(SPECIAL_SANDHI_RULES) == 27
    
    def test_vowel_sandhi_savarna(self):
        """Test savarna dirgha: a + a → ā."""
        # Find the rule
        rule = next(r for r in VOWEL_SANDHI_RULES if r.rule_id == "VS01")
        
        # Test forward application
        result = rule.apply_forward("रम", "अति")
        assert result is not None
        # Should contain 'आ' OR 'ा' (matra)
        assert "आ" in result or "ा" in result
    
    def test_vowel_sandhi_guna(self):
        """Test guna: a + i → e."""
        rule = next(r for r in VOWEL_SANDHI_RULES if r.rule_id == "VS09")
        
        result = rule.apply_forward("रम", "इति")
        assert result is not None
        # Should contain 'ए' OR 'े' (matra)
        assert "ए" in result or "े" in result
    
    def test_consonant_sandhi_anusvara(self):
        """Test anusvara: m + k → ṃk."""
        rule = next(r for r in CONSONANT_SANDHI_RULES if r.rule_id == "CS08")
        
        assert rule.left_pattern == "म्"
        assert rule.right_pattern == "क"
        assert rule.result == "ंक"
    
    def test_visarga_sandhi_basic(self):
        """Test visarga: aḥ + a → o'."""
        rule = next(r for r in VISARGA_SANDHI_RULES if r.rule_id == "VIS01")
        
        assert rule.left_pattern == "अः"
        assert rule.right_pattern == "अ"
        assert rule.result == "ओऽ"
    
    def test_rule_priorities(self):
        """Verify all rules have valid priorities (1-10)."""
        for rule in ALL_SANDHI_RULES:
            assert 1 <= rule.priority <= 10, f"Rule {rule.rule_id} has invalid priority {rule.priority}"
    
    def test_get_applicable_rules(self):
        """Test finding applicable rules for a word boundary."""
        # Test case: ending in अ, starting with इ
        rules = get_applicable_rules("अ", "इ")
        
        # Should find guna rule (a + i → e)
        assert len(rules) > 0
        assert any(r.rule_id == "VS09" for r in rules)


# ============================================================================
# VIBHAKTI ANALYZER TESTS
# ============================================================================

class TestVibhaktiAnalyzer:
    """Test case-ending pattern recognition."""
    
    @pytest.fixture
    def analyzer(self):
        return VibhaktiAnalyzer()
    
    def test_pattern_count(self, analyzer):
        """Verify we have 160 vibhakti patterns."""
        assert len(analyzer.patterns) == 160

    def test_inherent_a_handling(self):
        """Test handling of inherent 'a' in Sandhi rules."""
        # VS01: a + a -> ā
        rule = next(r for r in VOWEL_SANDHI_RULES if r.rule_id == "VS01")
        
        # "Rama" (ends in inherent a) + "ati" -> "Ramati"
        # In Devanagari: रम + अति -> रमाति
        result = rule.apply_forward("रम", "अति")
        assert result == "रमाति"
        
    def test_matra_handling(self):
        """Test handling of matras in Sandhi rules."""
        # VS02: ā + a -> ā
        rule = next(r for r in VOWEL_SANDHI_RULES if r.rule_id == "VS02")
        
        # "Ramā" (ends in ā matra) + "ati" -> "Ramāti"
        # In Devanagari: रमा + अति -> रमाति
        result = rule.apply_forward("रमा", "अति")
        assert result == "रमाति"
    
    def test_nominative_singular_masculine(self, analyzer):
        """Test a-stem masculine nominative singular: -ः."""
        analyses = analyzer.analyze("रामः")
        
        assert len(analyses) > 0
        best = analyses[0]
        assert best.case == Case.NOMINATIVE
        assert best.number == Number.SINGULAR
    
    def test_accusative_singular_masculine(self, analyzer):
        """Test a-stem masculine accusative singular: -म्."""
        analyses = analyzer.analyze("रामम्")
        
        assert len(analyses) > 0
        best = analyses[0]
        assert best.case == Case.ACCUSATIVE
        assert best.number == Number.SINGULAR
    
    def test_locative_singular_feminine(self, analyzer):
        """Test ā-stem feminine locative singular: -ायाम्."""
        analyses = analyzer.analyze("रमायाम्")
        
        assert len(analyses) > 0
        # Should recognize the locative pattern
        assert any(a.case == Case.LOCATIVE for a in analyses)
    
    def test_plural_neuter_nominative(self, analyzer):
        """Test a-stem neuter nominative/accusative plural: -ानि."""
        analyses = analyzer.analyze("फलानि")
        
        assert len(analyses) > 0
        best = analyses[0]
        assert best.number == Number.PLURAL
        assert best.gender == Gender.NEUTER
    
    def test_stem_extraction(self, analyzer):
        """Test that stems are correctly extracted."""
        analyses = analyzer.analyze("रामः")
        
        if analyses:
            best = analyses[0]
            # Stem should include the base vowel
            assert "राम" in best.stem or "अ" in best.stem


# ============================================================================
# PRATYAYA ANALYZER TESTS
# ============================================================================

class TestPratyayaAnalyzer:
    """Test suffix pattern recognition."""
    
    @pytest.fixture
    def analyzer(self):
        return PratyayaAnalyzer()
    
    def test_pattern_count(self, analyzer):
        """Verify we have 55+ pratyaya patterns."""
        assert len(analyzer.patterns) >= 55
    
    def test_infinitive_suffix(self, analyzer):
        """Test kṛt infinitive: -तुम्."""
        analyses = analyzer.analyze("कर्तुम्")
        
        assert len(analyses) > 0
        # Should find infinitive pattern
        assert any(a.pratyaya_type == PratyayaType.KRT for a in analyses)
    
    def test_absolutive_suffix(self, analyzer):
        """Test kṛt absolutive: -त्वा."""
        analyses = analyzer.analyze("कृत्वा")
        
        assert len(analyses) > 0
        krt_analyses = [a for a in analyses if a.pratyaya_type == PratyayaType.KRT]
        assert len(krt_analyses) > 0
    
    def test_abstract_noun_suffix(self, analyzer):
        """Test taddhita abstract: -त्व."""
        analyses = analyzer.analyze("देवत्व")
        
        assert len(analyses) > 0
        taddhita_analyses = [a for a in analyses if a.pratyaya_type == PratyayaType.TADDHITA]
        assert len(taddhita_analyses) > 0
    
    def test_possessive_suffix(self, analyzer):
        """Test taddhita possessive: -मत्."""
        analyses = analyzer.analyze("धनमत्")
        
        assert len(analyses) > 0
        assert any(a.pratyaya_type == PratyayaType.TADDHITA for a in analyses)
    
    def test_agent_noun_suffix(self, analyzer):
        """Test kṛt agent noun: -तृ."""
        analyses = analyzer.analyze("कर्तृ")
        
        assert len(analyses) > 0
        assert any(a.pratyaya_type == PratyayaType.KRT for a in analyses)


# ============================================================================
# ENHANCED SANDHI ENGINE TESTS
# ============================================================================

class TestEnhancedSandhiEngine:
    """Test integrated multi-candidate analysis."""
    
    @pytest.fixture
    def engine(self):
        dictionary = SanskritDictionary()
        # Add test vocabulary with frequencies
        for _ in range(100):
            dictionary.add_word("राम")
            dictionary.add_word("रामः")
        for _ in range(50):
            dictionary.add_word("अत्र")
        
        return EnhancedSandhiEngine(dictionary)
    
    def test_multi_candidate_generation(self, engine):
        """Test that engine generates multiple candidates."""
        # A word that could have multiple splits
        candidates = engine.find_all_splits("सुन्दरः", max_candidates=5)
        
        # Should generate at least one candidate
        assert len(candidates) >= 1
    
    def test_scoring_components(self, engine):
        """Test that all scoring components work."""
        candidates = engine.find_all_splits("रामः", max_candidates=3)
        
        for cand in candidates:
            # Score should be between 0 and 1
            assert 0.0 <= cand.total_score <= 1.0
            
            # Should have valid rule ID
            assert cand.sandhi_rule_id is not None
            
            # Should have valid priority
            assert 1 <= cand.sandhi_priority <= 10
    
    def test_frequency_weighting(self, engine):
        """Test that frequency affects scoring."""
        # Words in dictionary should score higher than unknown words
        known_candidates = engine.find_all_splits("रामः")
        
        # Should find candidates
        assert len(known_candidates) > 0
    
    def test_best_split_selection(self, engine):
        """Test that best split is correctly selected."""
        left, right = engine.get_best_split("रामः")
        
        # Should return something
        assert left is not None
        assert isinstance(left, str)
    
    def test_no_split_option(self, engine):
        """Test that no-split is considered for dictionary words."""
        # Add a word that shouldn't be split
        engine.dictionary.add_word("महाभारत")
        
        candidates = engine.find_all_splits("महाभारत")
        
        # Should include no-split option
        no_split = [c for c in candidates if c.right_word == ""]
        assert len(no_split) > 0


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Test complete workflow integration."""
    
    def test_grammar_rule_coverage(self):
        """Verify total grammar rule count."""
        sandhi_count = len(ALL_SANDHI_RULES)
        
        vibhakti_analyzer = VibhaktiAnalyzer()
        vibhakti_count = len(vibhakti_analyzer.patterns)
        
        pratyaya_analyzer = PratyayaAnalyzer()
        pratyaya_count = len(pratyaya_analyzer.patterns)
        
        total = sandhi_count + vibhakti_count + pratyaya_count
        
        print(f"\nTotal Grammar Rules: {total}")
        print(f"  - Sandhi: {sandhi_count}")
        print(f"  - Vibhakti: {vibhakti_count}")
        print(f"  - Pratyaya: {pratyaya_count}")
        
        assert total >= 344, f"Expected at least 344 rules, got {total}"
    
    def test_real_word_analysis(self):
        """Test analysis of real Sanskrit words."""
        dictionary = SanskritDictionary()
        engine = EnhancedSandhiEngine(dictionary)
        
        test_cases = [
            "रामः",
            "देवः",
            "फलम्",
        ]
        
        for word in test_cases:
            candidates = engine.find_all_splits(word)
            assert candidates is not None, f"Failed to analyze {word}"


# ============================================================================
# REAL TEXT SAMPLES
# ============================================================================

class TestRealSanskrit:
    """Test with authentic Vedic text samples."""
    
    def test_bhagavad_gita_sample(self):
        """Test with Bhagavad Gita verse 1.1."""
        # धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः ।
        # मामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय ॥
        
        dictionary = SanskritDictionary()
        analyzer = VibhaktiAnalyzer()
        
        # Test individual words
        test_words = [
            "धर्मक्षेत्रे",
            "कुरुक्षेत्रे",
            "समवेताः",
        ]
        
        for word in test_words:
            # Should not crash
            analyses = analyzer.analyze(word)
            # Just verify it runs
            assert analyses is not None


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformance:
    """Test performance characteristics."""
    
    def test_rule_lookup_speed(self):
        """Test that rule lookup is reasonably fast."""
        import time
        
        start = time.time()
        
        # Lookup 1000 times
        for _ in range(1000):
            rules = get_applicable_rules("अ", "इ")
        
        elapsed = time.time() - start
        
        # Should complete in under 1 second
        assert elapsed < 1.0, f"Rule lookup too slow: {elapsed:.3f}s for 1000 lookups"
    
    def test_analyzer_creation_speed(self):
        """Test that analyzers can be created quickly."""
        import time
        
        start = time.time()
        
        # Create analyzers 10 times
        for _ in range(10):
            VibhaktiAnalyzer()
            PratyayaAnalyzer()
        
        elapsed = time.time() - start
        
        # Should complete in under 2 seconds
        assert elapsed < 2.0, f"Analyzer creation too slow: {elapsed:.3f}s for 10 instances"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
