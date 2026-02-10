"""
Vibhakti (Case Ending) Analyzer for Sanskrit
=============================================

Analyzes Sanskrit case endings (vibhakti) to identify:
- Case: Nominative, Accusative, Instrumental, Dative, Ablative, Genitive, Locative, Vocative
- Number: Singular, Dual, Plural
- Gender: Masculine, Feminine, Neuter
- Stem type: a-stem, ā-stem, i-stem, ī-stem, u-stem, ū-stem, consonant-stem

Total patterns: 72 (8 cases × 3 numbers, with gender variants)
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Set
from enum import Enum


class Case(Enum):
    """Sanskrit cases (vibhakti)."""
    NOMINATIVE = "प्रथमा"      # prathamā (subject)
    ACCUSATIVE = "द्वितीया"     # dvitīyā (object)
    INSTRUMENTAL = "तृतीया"    # tṛtīyā (instrument/means)
    DATIVE = "चतुर्थी"          # caturthī (recipient)
    ABLATIVE = "पञ्चमी"         # pañcamī (source/origin)
    GENITIVE = "षष्ठी"          # ṣaṣṭhī (possession)
    LOCATIVE = "सप्तमी"         # saptamī (location)
    VOCATIVE = "सम्बोधन"        # sambodhana (address)


class Number(Enum):
    """Sanskrit grammatical numbers."""
    SINGULAR = "एकवचन"    # ekavacana
    DUAL = "द्विवचन"      # dvivacana
    PLURAL = "बहुवचन"     # bahuvacana


class Gender(Enum):
    """Sanskrit genders."""
    MASCULINE = "पुंलिङ्ग"    # puṃliṅga
    FEMININE = "स्त्रीलिङ्ग"   # strīliṅga
    NEUTER = "नपुंसकलिङ्ग"     # napuṃsakaliṅga


class StemType(Enum):
    """Types of nominal stems."""
    A_STEM = "अकारान्त"       # akārānta (ends in a)
    AA_STEM = "आकारान्त"      # ākārānta (ends in ā)
    I_STEM = "इकारान्त"       # ikārānta (ends in i)
    II_STEM = "ईकारान्त"      # īkārānta (ends in ī)
    U_STEM = "उकारान्त"       # ukārānta (ends in u)
    UU_STEM = "ऊकारान्त"      # ūkārānta (ends in ū)
    R_STEM = "ऋकारान्त"       # ṛkārānta (ends in ṛ)
    CONSONANT = "हलन्त"        # halanta (consonant-ending)


@dataclass
class VibhaktiPattern:
    """
    Represents a case ending pattern.
    
    Attributes:
        ending: The case ending suffix
        case: Grammatical case
        number: Grammatical number
        gender: Grammatical gender (None means applies to all)
        stem_type: Type of stem this ending applies to
        priority: Matching priority (higher = more specific)
    """
    ending: str
    case: Case
    number: Number
    gender: Optional[Gender]
    stem_type: StemType
    priority: int
    
    def matches(self, word: str) -> bool:
        """Check if word ends with this pattern."""
        return word.endswith(self.ending)
    
    def extract_stem(self, word: str) -> Optional[str]:
        """Extract the stem by removing the ending."""
        if not self.matches(word):
            return None
        
        if not self.ending:  # Zero ending
            return word
        
        stem = word[:-len(self.ending)]
        
        # Add back the stem vowel based on stem type
        if self.stem_type == StemType.A_STEM:
            stem += "अ"
        elif self.stem_type == StemType.AA_STEM:
            stem += "आ"
        elif self.stem_type == StemType.I_STEM:
            stem += "इ"
        elif self.stem_type == StemType.II_STEM:
            stem += "ई"
        elif self.stem_type == StemType.U_STEM:
            stem += "उ"
        elif self.stem_type == StemType.UU_STEM:
            stem += "ऊ"
        elif self.stem_type == StemType.R_STEM:
            stem += "ऋ"
        
        return stem


@dataclass
class VibhaktiAnalysis:
    """Result of vibhakti analysis."""
    stem: str
    ending: str
    case: Case
    number: Number
    gender: Optional[Gender]
    stem_type: StemType
    confidence: float  # 0.0 to 1.0


class VibhaktiAnalyzer:
    """Analyzes Sanskrit case endings."""
    
    def __init__(self):
        self.patterns = self._create_all_patterns()
        # Sort by priority (highest first) for matching
        self.patterns.sort(key=lambda p: p.priority, reverse=True)
    
    def analyze(self, word: str) -> List[VibhaktiAnalysis]:
        """
        Analyze a word for possible case endings.
        
        Returns list of possible analyses, sorted by confidence.
        """
        results = []
        
        for pattern in self.patterns:
            if pattern.matches(word):
                stem = pattern.extract_stem(word)
                if stem:
                    # Calculate confidence based on pattern priority and stem validity
                    confidence = pattern.priority / 10.0
                    
                    analysis = VibhaktiAnalysis(
                        stem=stem,
                        ending=pattern.ending,
                        case=pattern.case,
                        number=pattern.number,
                        gender=pattern.gender,
                        stem_type=pattern.stem_type,
                        confidence=confidence
                    )
                    results.append(analysis)
        
        # Sort by confidence
        results.sort(key=lambda a: a.confidence, reverse=True)
        return results
    
    def _create_all_patterns(self) -> List[VibhaktiPattern]:
        """Create all 72+ vibhakti patterns."""
        patterns = []
        
        # A-stem masculine (like राम rāma)
        patterns.extend(self._create_a_stem_masculine())
        
        # Ā-stem feminine (like रमा ramā)
        patterns.extend(self._create_aa_stem_feminine())
        
        # A-stem neuter (like फल phala)
        patterns.extend(self._create_a_stem_neuter())
        
        # I-stem masculine (like कवि kavi)
        patterns.extend(self._create_i_stem_masculine())
        
        # Ī-stem feminine (like नदी nadī)
        patterns.extend(self._create_ii_stem_feminine())
        
        # U-stem masculine (like गुरु guru)
        patterns.extend(self._create_u_stem_masculine())
        
        # Ū-stem feminine (like वधू vadhū)
        patterns.extend(self._create_uu_stem_feminine())
        
        # R-stem masculine (like पितृ pitṛ)
        patterns.extend(self._create_r_stem_masculine())
        
        # Common consonant stems
        patterns.extend(self._create_consonant_stems())
        
        return patterns
    
    # === A-STEM MASCULINE (अकारान्त पुंलिङ्ग) ===
    def _create_a_stem_masculine(self) -> List[VibhaktiPattern]:
        """A-stem masculine declension (like राम rāma 'Rama')."""
        return [
            # Singular
            VibhaktiPattern("ः", Case.NOMINATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.A_STEM, 10),
            VibhaktiPattern("म्", Case.ACCUSATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.A_STEM, 10),
            VibhaktiPattern("ेन", Case.INSTRUMENTAL, Number.SINGULAR, Gender.MASCULINE, StemType.A_STEM, 10),
            VibhaktiPattern("ाय", Case.DATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.A_STEM, 10),
            VibhaktiPattern("ात्", Case.ABLATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.A_STEM, 10),
            VibhaktiPattern("स्य", Case.GENITIVE, Number.SINGULAR, Gender.MASCULINE, StemType.A_STEM, 10),
            VibhaktiPattern("े", Case.LOCATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.A_STEM, 10),
            VibhaktiPattern("", Case.VOCATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.A_STEM, 9),  # Zero ending
            
            # Dual
            VibhaktiPattern("ौ", Case.NOMINATIVE, Number.DUAL, Gender.MASCULINE, StemType.A_STEM, 9),
            VibhaktiPattern("ौ", Case.ACCUSATIVE, Number.DUAL, Gender.MASCULINE, StemType.A_STEM, 9),
            VibhaktiPattern("ाभ्याम्", Case.INSTRUMENTAL, Number.DUAL, Gender.MASCULINE, StemType.A_STEM, 10),
            VibhaktiPattern("ाभ्याम्", Case.DATIVE, Number.DUAL, Gender.MASCULINE, StemType.A_STEM, 10),
            VibhaktiPattern("ाभ्याम्", Case.ABLATIVE, Number.DUAL, Gender.MASCULINE, StemType.A_STEM, 10),
            VibhaktiPattern("योः", Case.GENITIVE, Number.DUAL, Gender.MASCULINE, StemType.A_STEM, 9),
            VibhaktiPattern("योः", Case.LOCATIVE, Number.DUAL, Gender.MASCULINE, StemType.A_STEM, 9),
            VibhaktiPattern("ौ", Case.VOCATIVE, Number.DUAL, Gender.MASCULINE, StemType.A_STEM, 9),
            
            # Plural
            VibhaktiPattern("ाः", Case.NOMINATIVE, Number.PLURAL, Gender.MASCULINE, StemType.A_STEM, 9),
            VibhaktiPattern("ान्", Case.ACCUSATIVE, Number.PLURAL, Gender.MASCULINE, StemType.A_STEM, 9),
            VibhaktiPattern("ैः", Case.INSTRUMENTAL, Number.PLURAL, Gender.MASCULINE, StemType.A_STEM, 9),
            VibhaktiPattern("ेभ्यः", Case.DATIVE, Number.PLURAL, Gender.MASCULINE, StemType.A_STEM, 10),
            VibhaktiPattern("ेभ्यः", Case.ABLATIVE, Number.PLURAL, Gender.MASCULINE, StemType.A_STEM, 10),
            VibhaktiPattern("ानाम्", Case.GENITIVE, Number.PLURAL, Gender.MASCULINE, StemType.A_STEM, 10),
            VibhaktiPattern("ेषु", Case.LOCATIVE, Number.PLURAL, Gender.MASCULINE, StemType.A_STEM, 9),
            VibhaktiPattern("ाः", Case.VOCATIVE, Number.PLURAL, Gender.MASCULINE, StemType.A_STEM, 9),
        ]
    
    # === Ā-STEM FEMININE (आकारान्त स्त्रीलिङ्ग) ===
    def _create_aa_stem_feminine(self) -> List[VibhaktiPattern]:
        """Ā-stem feminine declension (like रमा ramā 'Ramā')."""
        return [
            # Singular
            VibhaktiPattern("ा", Case.NOMINATIVE, Number.SINGULAR, Gender.FEMININE, StemType.AA_STEM, 10),
            VibhaktiPattern("ाम्", Case.ACCUSATIVE, Number.SINGULAR, Gender.FEMININE, StemType.AA_STEM, 10),
            VibhaktiPattern("या", Case.INSTRUMENTAL, Number.SINGULAR, Gender.FEMININE, StemType.AA_STEM, 10),
            VibhaktiPattern("ायै", Case.DATIVE, Number.SINGULAR, Gender.FEMININE, StemType.AA_STEM, 10),
            VibhaktiPattern("ायाः", Case.ABLATIVE, Number.SINGULAR, Gender.FEMININE, StemType.AA_STEM, 10),
            VibhaktiPattern("ायाः", Case.GENITIVE, Number.SINGULAR, Gender.FEMININE, StemType.AA_STEM, 10),
            VibhaktiPattern("ायाम्", Case.LOCATIVE, Number.SINGULAR, Gender.FEMININE, StemType.AA_STEM, 10),
            VibhaktiPattern("े", Case.VOCATIVE, Number.SINGULAR, Gender.FEMININE, StemType.AA_STEM, 9),
            
            # Dual
            VibhaktiPattern("े", Case.NOMINATIVE, Number.DUAL, Gender.FEMININE, StemType.AA_STEM, 9),
            VibhaktiPattern("े", Case.ACCUSATIVE, Number.DUAL, Gender.FEMININE, StemType.AA_STEM, 9),
            VibhaktiPattern("ाभ्याम्", Case.INSTRUMENTAL, Number.DUAL, Gender.FEMININE, StemType.AA_STEM, 10),
            VibhaktiPattern("ाभ्याम्", Case.DATIVE, Number.DUAL, Gender.FEMININE, StemType.AA_STEM, 10),
            VibhaktiPattern("ाभ्याम्", Case.ABLATIVE, Number.DUAL, Gender.FEMININE, StemType.AA_STEM, 10),
            VibhaktiPattern("योः", Case.GENITIVE, Number.DUAL, Gender.FEMININE, StemType.AA_STEM, 9),
            VibhaktiPattern("योः", Case.LOCATIVE, Number.DUAL, Gender.FEMININE, StemType.AA_STEM, 9),
            VibhaktiPattern("े", Case.VOCATIVE, Number.DUAL, Gender.FEMININE, StemType.AA_STEM, 9),
            
            # Plural
            VibhaktiPattern("ाः", Case.NOMINATIVE, Number.PLURAL, Gender.FEMININE, StemType.AA_STEM, 9),
            VibhaktiPattern("ाः", Case.ACCUSATIVE, Number.PLURAL, Gender.FEMININE, StemType.AA_STEM, 9),
            VibhaktiPattern("ाभिः", Case.INSTRUMENTAL, Number.PLURAL, Gender.FEMININE, StemType.AA_STEM, 10),
            VibhaktiPattern("ाभ्यः", Case.DATIVE, Number.PLURAL, Gender.FEMININE, StemType.AA_STEM, 10),
            VibhaktiPattern("ाभ्यः", Case.ABLATIVE, Number.PLURAL, Gender.FEMININE, StemType.AA_STEM, 10),
            VibhaktiPattern("ानाम्", Case.GENITIVE, Number.PLURAL, Gender.FEMININE, StemType.AA_STEM, 10),
            VibhaktiPattern("ासु", Case.LOCATIVE, Number.PLURAL, Gender.FEMININE, StemType.AA_STEM, 9),
            VibhaktiPattern("ाः", Case.VOCATIVE, Number.PLURAL, Gender.FEMININE, StemType.AA_STEM, 9),
        ]
    
    # === A-STEM NEUTER (अकारान्त नपुंसकलिङ्ग) ===
    def _create_a_stem_neuter(self) -> List[VibhaktiPattern]:
        """A-stem neuter declension (like फल phala 'fruit')."""
        return [
            # Singular
            VibhaktiPattern("म्", Case.NOMINATIVE, Number.SINGULAR, Gender.NEUTER, StemType.A_STEM, 10),
            VibhaktiPattern("म्", Case.ACCUSATIVE, Number.SINGULAR, Gender.NEUTER, StemType.A_STEM, 10),
            VibhaktiPattern("ेन", Case.INSTRUMENTAL, Number.SINGULAR, Gender.NEUTER, StemType.A_STEM, 10),
            VibhaktiPattern("ाय", Case.DATIVE, Number.SINGULAR, Gender.NEUTER, StemType.A_STEM, 10),
            VibhaktiPattern("ात्", Case.ABLATIVE, Number.SINGULAR, Gender.NEUTER, StemType.A_STEM, 10),
            VibhaktiPattern("स्य", Case.GENITIVE, Number.SINGULAR, Gender.NEUTER, StemType.A_STEM, 10),
            VibhaktiPattern("े", Case.LOCATIVE, Number.SINGULAR, Gender.NEUTER, StemType.A_STEM, 10),
            VibhaktiPattern("", Case.VOCATIVE, Number.SINGULAR, Gender.NEUTER, StemType.A_STEM, 9),
            
            # Dual
            VibhaktiPattern("े", Case.NOMINATIVE, Number.DUAL, Gender.NEUTER, StemType.A_STEM, 9),
            VibhaktiPattern("े", Case.ACCUSATIVE, Number.DUAL, Gender.NEUTER, StemType.A_STEM, 9),
            VibhaktiPattern("ाभ्याम्", Case.INSTRUMENTAL, Number.DUAL, Gender.NEUTER, StemType.A_STEM, 10),
            VibhaktiPattern("ाभ्याम्", Case.DATIVE, Number.DUAL, Gender.NEUTER, StemType.A_STEM, 10),
            VibhaktiPattern("ाभ्याम्", Case.ABLATIVE, Number.DUAL, Gender.NEUTER, StemType.A_STEM, 10),
            VibhaktiPattern("योः", Case.GENITIVE, Number.DUAL, Gender.NEUTER, StemType.A_STEM, 9),
            VibhaktiPattern("योः", Case.LOCATIVE, Number.DUAL, Gender.NEUTER, StemType.A_STEM, 9),
            VibhaktiPattern("े", Case.VOCATIVE, Number.DUAL, Gender.NEUTER, StemType.A_STEM, 9),
            
            # Plural  
            VibhaktiPattern("ानि", Case.NOMINATIVE, Number.PLURAL, Gender.NEUTER, StemType.A_STEM, 10),
            VibhaktiPattern("ानि", Case.ACCUSATIVE, Number.PLURAL, Gender.NEUTER, StemType.A_STEM, 10),
            VibhaktiPattern("ैः", Case.INSTRUMENTAL, Number.PLURAL, Gender.NEUTER, StemType.A_STEM, 9),
            VibhaktiPattern("ेभ्यः", Case.DATIVE, Number.PLURAL, Gender.NEUTER, StemType.A_STEM, 10),
            VibhaktiPattern("ेभ्यः", Case.ABLATIVE, Number.PLURAL, Gender.NEUTER, StemType.A_STEM, 10),
            VibhaktiPattern("ानाम्", Case.GENITIVE, Number.PLURAL, Gender.NEUTER, StemType.A_STEM, 10),
            VibhaktiPattern("ेषु", Case.LOCATIVE, Number.PLURAL, Gender.NEUTER, StemType.A_STEM, 9),
            VibhaktiPattern("ानि", Case.VOCATIVE, Number.PLURAL, Gender.NEUTER, StemType.A_STEM, 10),
        ]
    
    # === I-STEM MASCULINE ===
    def _create_i_stem_masculine(self) -> List[VibhaktiPattern]:
        """I-stem masculine declension (like कवि kavi 'poet')."""
        return [
            # Singular
            VibhaktiPattern("िः", Case.NOMINATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.I_STEM, 10),
            VibhaktiPattern("िम्", Case.ACCUSATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.I_STEM, 10),
            VibhaktiPattern("िना", Case.INSTRUMENTAL, Number.SINGULAR, Gender.MASCULINE, StemType.I_STEM, 10),
            VibhaktiPattern("ये", Case.DATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.I_STEM, 9),
            VibhaktiPattern("ेः", Case.ABLATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.I_STEM, 9),
            VibhaktiPattern("ेः", Case.GENITIVE, Number.SINGULAR, Gender.MASCULINE, StemType.I_STEM, 9),
            VibhaktiPattern("ौ", Case.LOCATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.I_STEM, 9),
            VibhaktiPattern("े", Case.VOCATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.I_STEM, 9),
            
            # Plural
            VibhaktiPattern("यः", Case.NOMINATIVE, Number.PLURAL, Gender.MASCULINE, StemType.I_STEM, 9),
            VibhaktiPattern("ीन्", Case.ACCUSATIVE, Number.PLURAL, Gender.MASCULINE, StemType.I_STEM, 9),
            VibhaktiPattern("िभिः", Case.INSTRUMENTAL, Number.PLURAL, Gender.MASCULINE, StemType.I_STEM, 10),
            VibhaktiPattern("िभ्यः", Case.DATIVE, Number.PLURAL, Gender.MASCULINE, StemType.I_STEM, 10),
            VibhaktiPattern("िभ्यः", Case.ABLATIVE, Number.PLURAL, Gender.MASCULINE, StemType.I_STEM, 10),
            VibhaktiPattern("ीनाम्", Case.GENITIVE, Number.PLURAL, Gender.MASCULINE, StemType.I_STEM, 10),
            VibhaktiPattern("िषु", Case.LOCATIVE, Number.PLURAL, Gender.MASCULINE, StemType.I_STEM, 9),
        ]
    
    # === Ī-STEM FEMININE ===
    def _create_ii_stem_feminine(self) -> List[VibhaktiPattern]:
        """Ī-stem feminine declension (like नदी nadī 'river')."""
        return [
            # Singular
            VibhaktiPattern("ी", Case.NOMINATIVE, Number.SINGULAR, Gender.FEMININE, StemType.II_STEM, 10),
            VibhaktiPattern("ीम्", Case.ACCUSATIVE, Number.SINGULAR, Gender.FEMININE, StemType.II_STEM, 10),
            VibhaktiPattern("या", Case.INSTRUMENTAL, Number.SINGULAR, Gender.FEMININE, StemType.II_STEM, 10),
            VibhaktiPattern("यै", Case.DATIVE, Number.SINGULAR, Gender.FEMININE, StemType.II_STEM, 9),
            VibhaktiPattern("याः", Case.ABLATIVE, Number.SINGULAR, Gender.FEMININE, StemType.II_STEM, 9),
            VibhaktiPattern("याः", Case.GENITIVE, Number.SINGULAR, Gender.FEMININE, StemType.II_STEM, 9),
            VibhaktiPattern("याम्", Case.LOCATIVE, Number.SINGULAR, Gender.FEMININE, StemType.II_STEM, 10),
            VibhaktiPattern("ि", Case.VOCATIVE, Number.SINGULAR, Gender.FEMININE, StemType.II_STEM, 9),
            
            # Plural
            VibhaktiPattern("यः", Case.NOMINATIVE, Number.PLURAL, Gender.FEMININE, StemType.II_STEM, 9),
            VibhaktiPattern("ीः", Case.ACCUSATIVE, Number.PLURAL, Gender.FEMININE, StemType.II_STEM, 9),
            VibhaktiPattern("ीभिः", Case.INSTRUMENTAL, Number.PLURAL, Gender.FEMININE, StemType.II_STEM, 10),
            VibhaktiPattern("ीभ्यः", Case.DATIVE, Number.PLURAL, Gender.FEMININE, StemType.II_STEM, 10),
            VibhaktiPattern("ीभ्यः", Case.ABLATIVE, Number.PLURAL, Gender.FEMININE, StemType.II_STEM, 10),
            VibhaktiPattern("ीनाम्", Case.GENITIVE, Number.PLURAL, Gender.FEMININE, StemType.II_STEM, 10),
            VibhaktiPattern("ीषु", Case.LOCATIVE, Number.PLURAL, Gender.FEMININE, StemType.II_STEM, 9),
        ]
    
    # === U-STEM MASCULINE ===
    def _create_u_stem_masculine(self) -> List[VibhaktiPattern]:
        """U-stem masculine declension (like गुरु guru 'teacher')."""
        return [
            # Singular
            VibhaktiPattern("ुः", Case.NOMINATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.U_STEM, 10),
            VibhaktiPattern("ुम्", Case.ACCUSATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.U_STEM, 10),
            VibhaktiPattern("ुना", Case.INSTRUMENTAL, Number.SINGULAR, Gender.MASCULINE, StemType.U_STEM, 10),
            VibhaktiPattern("वे", Case.DATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.U_STEM, 9),
            VibhaktiPattern("ोः", Case.ABLATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.U_STEM, 9),
            VibhaktiPattern("ोः", Case.GENITIVE, Number.SINGULAR, Gender.MASCULINE, StemType.U_STEM, 9),
            VibhaktiPattern("ौ", Case.LOCATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.U_STEM, 9),
            VibhaktiPattern("ो", Case.VOCATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.U_STEM, 9),
            
            # Plural
            VibhaktiPattern("वः", Case.NOMINATIVE, Number.PLURAL, Gender.MASCULINE, StemType.U_STEM, 9),
            VibhaktiPattern("ून्", Case.ACCUSATIVE, Number.PLURAL, Gender.MASCULINE, StemType.U_STEM, 9),
            VibhaktiPattern("ुभिः", Case.INSTRUMENTAL, Number.PLURAL, Gender.MASCULINE, StemType.U_STEM, 10),
            VibhaktiPattern("ुभ्यः", Case.DATIVE, Number.PLURAL, Gender.MASCULINE, StemType.U_STEM, 10),
            VibhaktiPattern("ुभ्यः", Case.ABLATIVE, Number.PLURAL, Gender.MASCULINE, StemType.U_STEM, 10),
            VibhaktiPattern("ूनाम्", Case.GENITIVE, Number.PLURAL, Gender.MASCULINE, StemType.U_STEM, 10),
            VibhaktiPattern("ुषु", Case.LOCATIVE, Number.PLURAL, Gender.MASCULINE, StemType.U_STEM, 9),
        ]
    
    # === Ū-STEM FEMININE ===
    def _create_uu_stem_feminine(self) -> List[VibhaktiPattern]:
        """Ū-stem feminine declension (like वधू vadhū 'bride')."""
        return [
            # Singular
            VibhaktiPattern("ूः", Case.NOMINATIVE, Number.SINGULAR, Gender.FEMININE, StemType.UU_STEM, 10),
            VibhaktiPattern("ूम्", Case.ACCUSATIVE, Number.SINGULAR, Gender.FEMININE, StemType.UU_STEM, 10),
            VibhaktiPattern("वा", Case.INSTRUMENTAL, Number.SINGULAR, Gender.FEMININE, StemType.UU_STEM, 10),
            VibhaktiPattern("वै", Case.DATIVE, Number.SINGULAR, Gender.FEMININE, StemType.UU_STEM, 9),
            VibhaktiPattern("वाः", Case.ABLATIVE, Number.SINGULAR, Gender.FEMININE, StemType.UU_STEM, 9),
            VibhaktiPattern("वाः", Case.GENITIVE, Number.SINGULAR, Gender.FEMININE, StemType.UU_STEM, 9),
            VibhaktiPattern("वाम्", Case.LOCATIVE, Number.SINGULAR, Gender.FEMININE, StemType.UU_STEM, 10),
            VibhaktiPattern("ु", Case.VOCATIVE, Number.SINGULAR, Gender.FEMININE, StemType.UU_STEM, 9),
            
            # Plural
            VibhaktiPattern("वः", Case.NOMINATIVE, Number.PLURAL, Gender.FEMININE, StemType.UU_STEM, 9),
            VibhaktiPattern("ूः", Case.ACCUSATIVE, Number.PLURAL, Gender.FEMININE, StemType.UU_STEM, 9),
            VibhaktiPattern("ूभिः", Case.INSTRUMENTAL, Number.PLURAL, Gender.FEMININE, StemType.UU_STEM, 10),
            VibhaktiPattern("ूभ्यः", Case.DATIVE, Number.PLURAL, Gender.FEMININE, StemType.UU_STEM, 10),
            VibhaktiPattern("ूभ्यः", Case.ABLATIVE, Number.PLURAL, Gender.FEMININE, StemType.UU_STEM, 10),
            VibhaktiPattern("ूनाम्", Case.GENITIVE, Number.PLURAL, Gender.FEMININE, StemType.UU_STEM, 10),
            VibhaktiPattern("ूषु", Case.LOCATIVE, Number.PLURAL, Gender.FEMININE, StemType.UU_STEM, 9),
        ]
    
    # === R-STEM MASCULINE ===
    def _create_r_stem_masculine(self) -> List[VibhaktiPattern]:
        """Ṛ-stem masculine declension (like पितृ pitṛ 'father')."""
        return [
            # Singular
            VibhaktiPattern("ा", Case.NOMINATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.R_STEM, 9),
            VibhaktiPattern("रम्", Case.ACCUSATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.R_STEM, 9),
            VibhaktiPattern("रा", Case.INSTRUMENTAL, Number.SINGULAR, Gender.MASCULINE, StemType.R_STEM, 9),
            VibhaktiPattern("रे", Case.DATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.R_STEM, 9),
            VibhaktiPattern("ुः", Case.ABLATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.R_STEM, 9),
            VibhaktiPattern("ुः", Case.GENITIVE, Number.SINGULAR, Gender.MASCULINE, StemType.R_STEM, 9),
            VibhaktiPattern("रि", Case.LOCATIVE, Number.SINGULAR, Gender.MASCULINE, StemType.R_STEM, 9),
            
            # Plural
            VibhaktiPattern("रः", Case.NOMINATIVE, Number.PLURAL, Gender.MASCULINE, StemType.R_STEM, 9),
            VibhaktiPattern("ॄन्", Case.ACCUSATIVE, Number.PLURAL, Gender.MASCULINE, StemType.R_STEM, 9),
            VibhaktiPattern("ृभिः", Case.INSTRUMENTAL, Number.PLURAL, Gender.MASCULINE, StemType.R_STEM, 10),
            VibhaktiPattern("ृभ्यः", Case.DATIVE, Number.PLURAL, Gender.MASCULINE, StemType.R_STEM, 10),
            VibhaktiPattern("ृभ्यः", Case.ABLATIVE, Number.PLURAL, Gender.MASCULINE, StemType.R_STEM, 10),
            VibhaktiPattern("ॄणाम्", Case.GENITIVE, Number.PLURAL, Gender.MASCULINE, StemType.R_STEM, 10),
            VibhaktiPattern("ृषु", Case.LOCATIVE, Number.PLURAL, Gender.MASCULINE, StemType.R_STEM, 9),
        ]
    
    # === CONSONANT STEMS ===
    def _create_consonant_stems(self) -> List[VibhaktiPattern]:
        """Common consonant-ending stems."""
        return [
            # Singular examples (simplified set)
            VibhaktiPattern("्", Case.NOMINATIVE, Number.SINGULAR, None, StemType.CONSONANT, 7),
            VibhaktiPattern("म्", Case.ACCUSATIVE, Number.SINGULAR, None, StemType.CONSONANT, 8),
            VibhaktiPattern("ा", Case.INSTRUMENTAL, Number.SINGULAR, None, StemType.CONSONANT, 8),
            VibhaktiPattern("े", Case.DATIVE, Number.SINGULAR, None, StemType.CONSONANT, 7),
            VibhaktiPattern("ः", Case.ABLATIVE, Number.SINGULAR, None, StemType.CONSONANT, 7),
            VibhaktiPattern("ः", Case.GENITIVE, Number.SINGULAR, None, StemType.CONSONANT, 7),
            VibhaktiPattern("ि", Case.LOCATIVE, Number.SINGULAR, None, StemType.CONSONANT, 7),
            
            # Plural examples
            VibhaktiPattern("ः", Case.NOMINATIVE, Number.PLURAL, None, StemType.CONSONANT, 7),
            VibhaktiPattern("ः", Case.ACCUSATIVE, Number.PLURAL, None, StemType.CONSONANT, 7),
            VibhaktiPattern("भिः", Case.INSTRUMENTAL, Number.PLURAL, None, StemType.CONSONANT, 9),
            VibhaktiPattern("भ्यः", Case.DATIVE, Number.PLURAL, None, StemType.CONSONANT, 9),
            VibhaktiPattern("भ्यः", Case.ABLATIVE, Number.PLURAL, None, StemType.CONSONANT, 9),
            VibhaktiPattern("ाम्", Case.GENITIVE, Number.PLURAL, None, StemType.CONSONANT, 8),
            VibhaktiPattern("सु", Case.LOCATIVE, Number.PLURAL, None, StemType.CONSONANT, 8),
        ]


# === UTILITY FUNCTIONS ===

def analyze_word(word: str) -> List[VibhaktiAnalysis]:
    """
    Convenience function to analyze a word for vibhakti.
    
    Args:
        word: Sanskrit word in Devanagari
    
    Returns:
        List of possible vibhakti analyses
    """
    analyzer = VibhaktiAnalyzer()
    return analyzer.analyze(word)


def get_stem(word: str) -> Optional[str]:
    """
    Extract the most likely stem from an inflected word.
    
    Args:
        word: Sanskrit word in Devanagari
    
    Returns:
        Most likely stem, or None if no pattern matches
    """
    analyses = analyze_word(word)
    if analyses:
        return analyses[0].stem
    return None
