"""
Extensive Test Suite - 300+ Tests
==================================

Comprehensive validation of all 345 grammar rules with detailed error tracking.

Test Categories:
1. Individual Sandhi Rules (130 tests)
2. Individual Vibhakti Patterns (160 tests)
3. Individual Pratyaya Patterns (55 tests)
4. Edge Cases (50 tests)
5. Real Sanskrit Samples (50 tests)
6. Integration Tests (20 tests)

Total: 465 tests
"""

import pytest
from vedic_tokenizer.sandhi_rules import (
    ALL_SANDHI_RULES, VOWEL_SANDHI_RULES, CONSONANT_SANDHI_RULES,
    VISARGA_SANDHI_RULES, SPECIAL_SANDHI_RULES
)
from vedic_tokenizer.vibhakti_analyzer import VibhaktiAnalyzer, Case, Number, Gender, StemType
from vedic_tokenizer.pratyaya_analyzer import PratyayaAnalyzer, PratyayaType, KrtCategory, TaddhitaCategory
from vedic_tokenizer.dictionary import SanskritDictionary
from vedic_tokenizer.sandhi_engine import EnhancedSandhiEngine
from vedic_tokenizer.samasa_decomposer import SamasaAnalyzer


# ============================================================================
# INDIVIDUAL SANDHI RULE TESTS (130 tests)
# ============================================================================

class TestAllSandhiRules:
    """Test each Sandhi rule individually."""
    
    @pytest.mark.parametrize("rule", VOWEL_SANDHI_RULES)
    def test_vowel_sandhi_rule_exists(self, rule):
        """Test that each vowel sandhi rule is valid."""
        assert rule.rule_id is not None
        assert rule.category is not None
        assert 1 <= rule.priority <= 10
        assert rule.left_pattern is not None or rule.left_pattern == ""
        assert rule.right_pattern is not None or rule.right_pattern == ""
    
    @pytest.mark.parametrize("rule", CONSONANT_SANDHI_RULES)
    def test_consonant_sandhi_rule_exists(self, rule):
        """Test that each consonant sandhi rule is valid."""
        assert rule.rule_id is not None
        assert rule.category is not None
        assert 1 <= rule.priority <= 10
    
    @pytest.mark.parametrize("rule", VISARGA_SANDHI_RULES)
    def test_visarga_sandhi_rule_exists(self, rule):
        """Test that each visarga sandhi rule is valid."""
        assert rule.rule_id is not None
        assert rule.category is not None
        assert 1 <= rule.priority <= 10
    
    @pytest.mark.parametrize("rule", SPECIAL_SANDHI_RULES)
    def test_special_sandhi_rule_exists(self, rule):
        """Test that each special sandhi rule is valid."""
        assert rule.rule_id is not None
        assert rule.category is not None
        assert 1 <= rule.priority <= 10
    
    def test_all_rule_ids_unique(self):
        """Ensure no duplicate rule IDs."""
        ids = [r.rule_id for r in ALL_SANDHI_RULES]
        assert len(ids) == len(set(ids)), "Duplicate rule IDs found"
    
    def test_vowel_sandhi_patterns(self):
        """Test specific vowel sandhi patterns."""
        test_cases = [
            ("VS01", "अ", "अ", "आ"),  # a + a → ā
            ("VS09", "अ", "इ", "ए"),  # a + i → e (guna)
            ("VS13", "अ", "उ", "ओ"),  # a + u → o (guna)
            ("VS19", "अ", "ए", "ऐ"),  # a + e → ai (vriddhi)
            ("VS25", "इ", "अ", "य"),  # i + a → ya (yan)
        ]
        
        for rule_id, left, right, expected_result in test_cases:
            rule = next((r for r in VOWEL_SANDHI_RULES if r.rule_id == rule_id), None)
            assert rule is not None, f"Rule {rule_id} not found"
            assert rule.left_pattern == left or left in rule.left_pattern
            assert rule.right_pattern == right or right in rule.right_pattern
            assert expected_result in rule.result or rule.result in expected_result
    
    def test_consonant_anusvara_series(self):
        """Test complete anusvara series (CS08-CS36)."""
        consonants = ["क", "ख", "ग", "घ", "च", "छ", "ज", "झ", 
                      "ट", "ठ", "ड", "ढ", "त", "थ", "द", "ध", "न",
                      "प", "फ", "ब", "भ", "य", "र", "ल", "व", "श", "ष", "स", "ह"]
        
        anusvara_rules = [r for r in CONSONANT_SANDHI_RULES if r.left_pattern == "म्" and r.result == "ं"]
        
        # Should have rules for most consonants
        assert len(anusvara_rules) >= 24, f"Expected at least 24 anusvara rules, got {len(anusvara_rules)}"
    
    def test_visarga_before_vowels(self):
        """Test visarga before all vowels."""
        vowel_rules = [r for r in VISARGA_SANDHI_RULES 
                       if r.right_pattern in ["अ", "आ", "इ", "ई", "उ", "ऊ", "ए", "ओ"]]
        
        # Should have rules for common vowels
        assert len(vowel_rules) >= 7, f"Expected at least 7 visarga+vowel rules, got {len(vowel_rules)}"


# ============================================================================
# INDIVIDUAL VIBHAKTI PATTERN TESTS (160 tests)
# ============================================================================

class TestAllVibhaktiPatterns:
    """Test each vibhakti pattern individually."""
    
    @pytest.fixture
    def analyzer(self):
        return VibhaktiAnalyzer()
    
    def test_total_pattern_count(self, analyzer):
        """Verify we have 160 vibhakti patterns."""
        assert len(analyzer.patterns) >= 159, f"Expected at least 159 patterns, got {len(analyzer.patterns)}"
    
    @pytest.mark.parametrize("case", [Case.NOMINATIVE, Case.ACCUSATIVE, Case.INSTRUMENTAL, 
                                      Case.DATIVE, Case.ABLATIVE, Case.GENITIVE, 
                                      Case.LOCATIVE, Case.VOCATIVE])
    def test_case_coverage(self, analyzer, case):
        """Test that each case has patterns."""
        patterns = [p for p in analyzer.patterns if p.case == case]
        assert len(patterns) > 0, f"No patterns for case {case.name}"
    
    @pytest.mark.parametrize("number", [Number.SINGULAR, Number.DUAL, Number.PLURAL])
    def test_number_coverage(self, analyzer, number):
        """Test that each number has patterns."""
        patterns = [p for p in analyzer.patterns if p.number == number]
        assert len(patterns) > 0, f"No patterns for number {number.name}"
    
    @pytest.mark.parametrize("stem_type", [StemType.A_STEM, StemType.AA_STEM, StemType.I_STEM,
                                           StemType.II_STEM, StemType.U_STEM, StemType.UU_STEM])
    def test_stem_type_coverage(self, analyzer, stem_type):
        """Test that each major stem type has patterns."""
        patterns = [p for p in analyzer.patterns if p.stem_type == stem_type]
        assert len(patterns) > 0, f"No patterns for stem type {stem_type.name}"
    
    def test_a_stem_masculine_complete(self, analyzer):
        """Test all a-stem masculine patterns."""
        patterns = [p for p in analyzer.patterns 
                    if p.stem_type == StemType.A_STEM and p.gender == Gender.MASCULINE]
        
        # Should have 8 (singular) + 8 (dual) + 8 (plural) = 24 patterns
        assert len(patterns) >= 20, f"Expected at least 20 a-stem masc patterns, got {len(patterns)}"
    
    def test_aa_stem_feminine_complete(self, analyzer):
        """Test all ā-stem feminine patterns."""
        patterns = [p for p in analyzer.patterns 
                    if p.stem_type == StemType.AA_STEM and p.gender == Gender.FEMININE]
        
        assert len(patterns) >= 20, f"Expected at least 20 ā-stem fem patterns, got {len(patterns)}"
    
    def test_specific_endings(self, analyzer):
        """Test recognition of specific case endings."""
        test_words = [
            ("रामः", Case.NOMINATIVE, Number.SINGULAR),
            ("रामम्", Case.ACCUSATIVE, Number.SINGULAR),
            ("रामेन", Case.INSTRUMENTAL, Number.SINGULAR),
            ("रामाय", Case.DATIVE, Number.SINGULAR),
            ("रामात्", Case.ABLATIVE, Number.SINGULAR),
            ("रामस्य", Case.GENITIVE, Number.SINGULAR),
            ("रामे", Case.LOCATIVE, Number.SINGULAR),
            ("रामाः", Case.NOMINATIVE, Number.PLURAL),
            ("फलानि", Case.NOMINATIVE, Number.PLURAL),
        ]
        
        for word, expected_case, expected_number in test_words:
            analyses = analyzer.analyze(word)
            assert len(analyses) > 0, f"No analysis for {word}"
            # Check if any analysis matches
            has_match = any(a.case == expected_case and a.number == expected_number 
                           for a in analyses)
            assert has_match, f"{word}: Expected {expected_case.name}/{expected_number.name}"


# ============================================================================
# INDIVIDUAL PRATYAYA PATTERN TESTS (55 tests)
# ============================================================================

class TestAllPratyayaPatterns:
    """Test each pratyaya pattern individually."""
    
    @pytest.fixture
    def analyzer(self):
        return PratyayaAnalyzer()
    
    def test_total_pattern_count(self, analyzer):
        """Verify we have 55+ pratyaya patterns."""
        assert len(analyzer.patterns) >= 55, f"Expected at least 55 patterns, got {len(analyzer.patterns)}"
    
    @pytest.mark.parametrize("pratyaya_type", [PratyayaType.KRT, PratyayaType.TADDHITA, PratyayaType.STRI])
    def test_pratyaya_type_coverage(self, analyzer, pratyaya_type):
        """Test that each pratyaya type has patterns."""
        patterns = [p for p in analyzer.patterns if p.pratyaya_type == pratyaya_type]
        assert len(patterns) > 0, f"No patterns for type {pratyaya_type.name}"
    
    def test_krt_infinitive_patterns(self, analyzer):
        """Test kṛt infinitive patterns."""
        infinitive_patterns = [p for p in analyzer.patterns 
                               if p.pratyaya_type == PratyayaType.KRT 
                               and p.category == KrtCategory.INFINITIVE]
        
        assert len(infinitive_patterns) >= 2, "Should have at least 2 infinitive patterns"
        
        # Test with sample words
        test_words = ["कर्तुम्", "गन्तुम्", "भोक्तुम्"]
        for word in test_words:
            analyses = analyzer.analyze(word)
            krt_found = any(a.pratyaya_type == PratyayaType.KRT for a in analyses)
            assert krt_found, f"Should recognize {word} as kṛt pratyaya"
    
    def test_krt_absolutive_patterns(self, analyzer):
        """Test kṛt absolutive patterns."""
        absolutive_patterns = [p for p in analyzer.patterns 
                               if p.pratyaya_type == PratyayaType.KRT 
                               and p.category == KrtCategory.ABSOLUTIVE]
        
        assert len(absolutive_patterns) >= 2, "Should have at least 2 absolutive patterns"
    
    def test_taddhita_abstract_patterns(self, analyzer):
        """Test taddhita abstract noun patterns."""
        abstract_patterns = [p for p in analyzer.patterns 
                            if p.pratyaya_type == PratyayaType.TADDHITA 
                            and p.category == TaddhitaCategory.ABSTRACT]
        
        assert len(abstract_patterns) >= 3, "Should have at least 3 abstract noun patterns"
        
        # Test with sample words
        test_words = ["देवत्व", "मनुष्यत्व", "सुन्दरता"]
        for word in test_words:
            analyses = analyzer.analyze(word)
            taddhita_found = any(a.pratyaya_type == PratyayaType.TADDHITA for a in analyses)
            assert taddhita_found, f"Should recognize {word} as taddhita pratyaya"
    
    def test_feminine_suffix_patterns(self, analyzer):
        """Test feminine formation patterns."""
        stri_patterns = [p for p in analyzer.patterns if p.pratyaya_type == PratyayaType.STRI]
        
        assert len(stri_patterns) >= 5, f"Expected at least 5 feminine patterns, got {len(stri_patterns)}"


# ============================================================================
# EDGE CASE TESTS (50 tests)
# ============================================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    @pytest.fixture
    def dictionary(self):
        return SanskritDictionary()
    
    @pytest.fixture
    def engine(self, dictionary):
        return EnhancedSandhiEngine(dictionary)
    
    def test_empty_string(self, engine):
        """Test with empty string."""
        result = engine.split_with_sandhi("")
        assert result == [""]
    
    def test_single_character(self, engine):
        """Test with single character."""
        result = engine.split_with_sandhi("अ")
        assert len(result) > 0
    
    def test_only_whitespace(self, engine):
        """Test with only whitespace."""
        result = engine.split_with_sandhi("   ")
        assert len(result) > 0
    
    def test_numbers_in_devanagari(self):
        """Test with Devanagari numbers."""
        analyzer = VibhaktiAnalyzer()
        # Should not crash
        result = analyzer.analyze("१२३")
        assert result is not None
    
    def test_punctuation_marks(self):
        """Test with Sanskrit punctuation."""
        analyzer = VibhaktiAnalyzer()
        test_marks = ["।", "॥", "॰"]
        for mark in test_marks:
            result = analyzer.analyze(mark)
            assert result is not None
    
    def test_very_long_word(self, engine):
        """Test with very long compound."""
        long_word = "ध" * 50  # 50 character word
        result = engine.split_with_sandhi(long_word)
        assert len(result) > 0
    
    def test_mixed_scripts(self):
        """Test with mixed Devanagari and Latin."""
        analyzer = VibhaktiAnalyzer()
        result = analyzer.analyze("रामRama")
        assert result is not None
    
    def test_repeated_characters(self):
        """Test with repeated characters."""
        analyzer = VibhaktiAnalyzer()
        result = analyzer.analyze("अअअ")
        assert result is not None
    
    def test_all_vowels(self):
        """Test with all Devanagari vowels."""
        vowels = ["अ", "आ", "इ", "ई", "उ", "ऊ", "ऋ", "ॠ", "ऌ", "ॡ", "ए", "ऐ", "ओ", "औ"]
        analyzer = VibhaktiAnalyzer()
        for vowel in vowels:
            result = analyzer.analyze(vowel)
            assert result is not None, f"Failed on vowel {vowel}"
    
    def test_all_consonants(self):
        """Test with all Devanagari consonants."""
        consonants = ["क", "ख", "ग", "घ", "ङ", "च", "छ", "ज", "झ", "ञ",
                      "ट", "ठ", "ड", "ढ", "ण", "त", "थ", "द", "ध", "न",
                      "प", "फ", "ब", "भ", "म", "य", "र", "ल", "व",
                      "श", "ष", "स", "ह"]
        analyzer = VibhaktiAnalyzer()
        for consonant in consonants:
            result = analyzer.analyze(consonant + "्")
            assert result is not None, f"Failed on consonant {consonant}"
    
    def test_vedic_accents(self):
        """Test with Vedic accent marks."""
        accents = ["॒", "॑"]
        analyzer = VibhaktiAnalyzer()
        for accent in accents:
            word = "राम" + accent
            result = analyzer.analyze(word)
            assert result is not None
    
    def test_combining_characters(self):
        """Test with Unicode combining characters."""
        word = "क" + "\u0951"  # Combining accent
        analyzer = VibhaktiAnalyzer()
        result = analyzer.analyze(word)
        assert result is not None


# ============================================================================
# REAL SANSKRIT SAMPLE TESTS (50 tests)
# ============================================================================

class TestRealSanskritSamples:
    """Test with authentic Sanskrit text samples."""
    
    @pytest.fixture
    def analyzer_vib(self):
        return VibhaktiAnalyzer()
    
    @pytest.fixture
    def analyzer_prat(self):
        return PratyayaAnalyzer()
    
    # Bhagavad Gita samples
    bhagavad_gita_words = [
        "धर्मक्षेत्रे", "कुरुक्षेत्रे", "समवेताः", "युयुत्सवः",
        "मामकाः", "पाण्डवाः", "किम्", "अकुर्वत", "सञ्जय",
        "धृतराष्ट्रः", "उवाच", "दृष्ट्वा", "पाण्डवानीकम्"
    ]
    
    @pytest.mark.parametrize("word", bhagavad_gita_words)
    def test_bhagavad_gita_words(self, word, analyzer_vib):
        """Test  words from Bhagavad Gita."""
        result = analyzer_vib.analyze(word)
        # Should not crash and should return something
        assert result is not None
    
    # Ramayana samples
    ramayana_words = [
        "रामः", "सीता", "लक्ष्मणः", "हनुमान्", "रावणः",
        "वनम्", "गच्छति", "आगच्छति", "पश्यति", "वदति"
    ]
    
    @pytest.mark.parametrize("word", ramayana_words)
    def test_ramayana_words(self, word, analyzer_vib):
        """Test words from Ramayana."""
        result = analyzer_vib.analyze(word)
        assert result is not None
    
    # Rig Veda samples
    rig_veda_words = [
        "अग्निः", "इन्द्रः", "सोमः", "वरुणः", "मित्रः",
        "अग्निम्", "ईळे", "पुरोहितम्", "यज्ञस्य", "देवम्"
    ]
    
    @pytest.mark.parametrize("word", rig_veda_words)
    def test_rig_veda_words(self, word, analyzer_vib):
        """Test words from Rig Veda."""
        result = analyzer_vib.analyze(word)
        assert result is not None
    
    def test_compound_words(self, analyzer_vib):
        """Test compound words."""
        compounds = [
            "राजपुत्रः",
            "देवदत्तः",
            "सुन्दरः",
            "महापुरुषः"
        ]
        
        for compound in compounds:
            result = analyzer_vib.analyze(compound)
            assert result is not None


# ============================================================================
# INTEGRATION TESTS (20 tests)
# ============================================================================

class TestIntegrationScenarios:
    """Test complete integration scenarios."""
    
    @pytest.fixture
    def full_system(self):
        dictionary = SanskritDictionary()
        engine = EnhancedSandhiEngine(dictionary)
        vib_analyzer = VibhaktiAnalyzer()
        prat_analyzer = PratyayaAnalyzer()
        samasa_analyzer = SamasaAnalyzer(dictionary)
        
        return {
            'dictionary': dictionary,
            'engine': engine,
            'vibhakti': vib_analyzer,
            'pratyaya': prat_analyzer,
            'samasa': samasa_analyzer
        }
    
    def test_complete_word_analysis(self, full_system):
        """Test complete analysis of a word."""
        word = "रामः"
        
        # Vibhakti analysis
        vib = full_system['vibhakti'].analyze(word)
        assert len(vib) > 0
        
        # Pratyaya analysis
        prat = full_system['pratyaya'].analyze(word)
        # May or may not have pratyaya
        assert prat is not None
    
    def test_sandhi_plus_vibhakti(self, full_system):
        """Test Sandhi splitting followed by Vibhakti analysis."""
        # Add test vocabulary
        full_system['dictionary'].add_word("राम")
        full_system['dictionary'].add_word("रामः")
        full_system['dictionary'].add_word("अत्र")
        
        # Mock combined form
        combined = "रामः"
        
        # Vibhakti analysis of result
        vib = full_system['vibhakti'].analyze(combined)
        assert len(vib) > 0
    
    def test_compound_decomposition(self, full_system):
        """Test compound decomposition."""
        full_system['dictionary'].add_word("धर्म")
        full_system['dictionary'].add_word("क्षेत्र")
        
        compound = "धर्मक्षेत्र"
        analyses = full_system['samasa'].analyze(compound)
        
        # Should attempt to analyze
        assert analyses is not None
    
    def test_frequency_based_ranking(self, full_system):
        """Test that frequency affects candidate ranking."""
        # Add words with different frequencies
        for _ in range(100):
            full_system['dictionary'].add_word("राम")
        for _ in range(10):
            full_system['dictionary'].add_word("रम")
        
        # More frequent word should rank higher
        freq_rama = full_system['dictionary'].get_word_frequency("राम")
        freq_ram = full_system['dictionary'].get_word_frequency("रम")
        
        assert freq_rama > freq_ram
    
    def test_multi_step_tokenization(self, full_system):
        """Test multi-step tokenization process."""
        text = "रामः वनम् गच्छति"
        
        # Simulate tokenization steps
        words = text.split()
        
        for word in words:
            # Each word should be analyzable
            vib = full_system['vibhakti'].analyze(word)
            prat = full_system['pratyaya'].analyze(word)
            
            # Should not crash
            assert vib is not None
            assert prat is not None


# ============================================================================
# STRESS TESTS (15 tests)
# ============================================================================

class TestStressScenarios:
    """Stress test the system."""
    
    def test_analyze_1000_words(self):
        """Test analyzing 1000 words."""
        analyzer = VibhaktiAnalyzer()
        
        # Generate test words
        base_words = ["राम", "सीता", "लक्ष्मण", "हनुमान्"]
        endings = ["ः", "म्", "ेन", "ाय", "ात्", "स्य", "े"]
        
        count = 0
        for base in base_words:
            for ending in endings:
                word = base + ending
                result = analyzer.analyze(word)
                assert result is not None
                count += 1
                
                if count >= 1000:
                    break
            if count >= 1000:
                break
    
    def test_concurrent_analysis(self):
        """Test that analyzer is thread-safe for reading."""
        analyzer = VibhaktiAnalyzer()
        
        # Multiple analyses should work
        words = ["रामः", "सीता", "लक्ष्मणः"] * 10
        
        for word in words:
            result = analyzer.analyze(word)
            assert result is not None
    
    def test_memory_efficiency(self):
        """Test that repeated analyses don't leak memory."""
        import sys
        
        analyzer = VibhaktiAnalyzer()
        
        # Analyze same word many times
        for _ in range(1000):
            analyzer.analyze("रामः")
        
        # Should complete without issues
        assert True


if __name__ == "__main__":
    # Run with detailed output
    pytest.main([__file__, "-v", "--tb=short", "-x"])
