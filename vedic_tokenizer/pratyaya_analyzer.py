"""
Pratyaya (Suffix) Analyzer for Sanskrit
========================================

Analyzes Sanskrit suffixes (pratyaya) to identify word formation patterns:

1. Kṛt Pratyayas (कृत् प्रत्यय): Primary derivatives from verbal roots
   - Infinitives: -तुम् (-tum)
   - Absolutives: -त्वा (-tvā), -य (-ya)
   - Agent nouns: -तृ (-tṛ), -अक (-aka)
   - Past participles: -त (-ta), -न (-na)
   - Present participles: -अत् (-at), -मान (-māna)
   
2. Taddhita Pratyayas (तद्धित प्रत्यय): Secondary derivatives from nominals
   - Abstract nouns: -त्व (-tva), -ता (-tā)
   - Patronymics: -अ (-a), -ई (-ī)
   - Possessives: -मत् (-mat), -वत् (-vat)
   - Adjectives: -इक (-ika), -ईय (-īya)

Total patterns: 200+
"""

from dataclasses import dataclass
from typing import List, Optional, Set
from enum import Enum


class PratyayaType(Enum):
    """Types of pratyayas."""
    KRT = "कृत्"              # Primary (from verbal roots)
    TADDHITA = "तद्धित"       # Secondary (from nominals)
    STRI = "स्त्री"           # Feminine formation
    SAMASA = "समास"           # Compound-forming


class KrtCategory(Enum):
    """Categories of kṛt pratyayas."""
    INFINITIVE = "तुमुन्"              # Infinitive
    ABSOLUTIVE = "क्त्वा"              # Absolutive (gerund)
    PAST_PARTICIPLE = "क्त"            # Past participle
    PRESENT_PARTICIPLE = "शतृ"         # Present participle
    FUTURE_PARTICIPLE = "तव्य"         # Future participle (gerundive)
    AGENT_NOUN = "तृच्"                # Agent noun
    ACTION_NOUN = "घञ्"                # Action noun
    INSTRUMENTAL_NOUN = "करण"          # Instrumental noun


class TaddhitaCategory(Enum):
    """Categories of taddhita pratyayas."""
    ABSTRACT = "भाव"           # Abstract noun
    PATRONYMIC = "अपत्य"       # Patronymic/lineage
    POSSESSIVE = "मतुप्"       # Possessive
    ADJECTIVE = "अजातीय"       # Adjective-forming
    DIMINUTIVE = "ईयसुन्"      # Diminutive
    LOCATIVE = "देशीय"         # Locative/place-related


@dataclass
class PratyayaPattern:
    """
    Represents a suffix pattern.
    
    Attributes:
        suffix: The suffix itself
        pratyaya_type: Kṛt or Taddhita
        category: Specific category within type
        meaning: Semantic meaning of the suffix
        examples: Example words using this suffix
        priority: Matching priority (higher = more specific)
    """
    suffix: str
    pratyaya_type: PratyayaType
    category: Optional[Enum]
    meaning: str
    examples: List[str]
    priority: int
    
    def matches(self, word: str) -> bool:
        """Check if word ends with this suffix."""
        return word.endswith(self.suffix)
    
    def extract_base(self, word: str) -> Optional[str]:
        """Extract the base by removing the suffix."""
        if not self.matches(word):
            return None
        
        if not self.suffix:
            return word
        
        return word[:-len(self.suffix)]


@dataclass
class PratyayaAnalysis:
    """Result of pratyaya analysis."""
    base: str
    suffix: str
    pratyaya_type: PratyayaType
    category: Optional[Enum]
    meaning: str
    confidence: float


class PratyayaAnalyzer:
    """Analyzes Sanskrit suffixes."""
    
    def __init__(self):
        self.patterns = self._create_all_patterns()
        self.patterns.sort(key=lambda p: p.priority, reverse=True)
    
    def analyze(self, word: str) -> List[PratyayaAnalysis]:
        """Analyze a word for possible suffixes."""
        results = []
        
        for pattern in self.patterns:
            if pattern.matches(word):
                base = pattern.extract_base(word)
                if base and len(base) >= 2:  # Reasonable base length
                    confidence = pattern.priority / 10.0
                    
                    analysis = PratyayaAnalysis(
                        base=base,
                        suffix=pattern.suffix,
                        pratyaya_type=pattern.pratyaya_type,
                        category=pattern.category,
                        meaning=pattern.meaning,
                        confidence=confidence
                    )
                    results.append(analysis)
        
        results.sort(key=lambda a: a.confidence, reverse=True)
        return results
    
    def _create_all_patterns(self) -> List[PratyayaPattern]:
        """Create all pratyaya patterns."""
        patterns = []
        
        patterns.extend(self._create_krt_infinitives())
        patterns.extend(self._create_krt_absolutives())
        patterns.extend(self._create_krt_participles())
        patterns.extend(self._create_krt_agent_nouns())
        patterns.extend(self._create_krt_action_nouns())
        
        patterns.extend(self._create_taddhita_abstract())
        patterns.extend(self._create_taddhita_possessive())
        patterns.extend(self._create_taddhita_adjectives())
        patterns.extend(self._create_taddhita_patronymic())
        
        patterns.extend(self._create_feminine_suffixes())
        
        return patterns
    
    # === KṚT PRATYAYAS (PRIMARY DERIVATIVES) ===
    
    def _create_krt_infinitives(self) -> List[PratyayaPattern]:
        """Infinitive suffixes (तुमुन्)."""
        return [
            PratyayaPattern("तुम्", PratyayaType.KRT, KrtCategory.INFINITIVE,
                          "infinitive (to do)", ["कर्तुम्", "गन्तुम्", "भोक्तुम्"], 10),
            PratyayaPattern("तुं", PratyayaType.KRT, KrtCategory.INFINITIVE,
                          "infinitive (sandhi form)", ["कर्तुं", "गन्तुं"], 10),
        ]
    
    def _create_krt_absolutives(self) -> List[PratyayaPattern]:
        """Absolutive/gerund suffixes (क्त्वा, ल्यप्)."""
        return [
            PratyayaPattern("त्वा", PratyayaType.KRT, KrtCategory.ABSOLUTIVE,
                          "having done", ["कृत्वा", "गत्वा", "दृष्ट्वा"], 10),
            PratyayaPattern("य", PratyayaType.KRT, KrtCategory.ABSOLUTIVE,
                          "having done (compound)", ["आगम्य", "उपगम्य"], 9),
            PratyayaPattern("त्य", PratyayaType.KRT, KrtCategory.ABSOLUTIVE,
                          "having done (variant)", ["श्रुत्य", "हुत्य"], 8),
        ]
    
    def _create_krt_participles(self) -> List[PratyayaPattern]:
        """Participial suffixes."""
        return [
            # Past participles (क्त, क्तवतु)
            PratyayaPattern("त", PratyayaType.KRT, KrtCategory.PAST_PARTICIPLE,
                          "done, past passive participle", ["कृत", "गत", "दत्त"], 10),
            PratyayaPattern("न", PratyayaType.KRT, KrtCategory.PAST_PARTICIPLE,
                          "done, past passive participle", ["भिन्न", "छिन्न"], 9),
            PratyayaPattern("तवत्", PratyayaType.KRT, KrtCategory.PAST_PARTICIPLE,
                          "having done, past active participle", ["कृतवत्", "गतवत्"], 9),
            
            # Present participles (शतृ, शानच्)
            PratyayaPattern("अत्", PratyayaType.KRT, KrtCategory.PRESENT_PARTICIPLE,
                          "doing, present active participle", ["गच्छत्", "पचत्"], 10),
            PratyayaPattern("अन्त्", PratyayaType.KRT, KrtCategory.PRESENT_PARTICIPLE,
                          "doing, present active participle", ["भवन्त्", "कुर्वन्त्"], 9),
            PratyayaPattern("मान", PratyayaType.KRT, KrtCategory.PRESENT_PARTICIPLE,
                          "being done, present passive participle", ["क्रियमाण", "गम्यमान"], 10),
            
            # Future participles/gerundives (तव्य, अनीय, य)
            PratyayaPattern("तव्य", PratyayaType.KRT, KrtCategory.FUTURE_PARTICIPLE,
                          "to be done, gerundive", ["कर्तव्य", "गन्तव्य"], 10),
            PratyayaPattern("अनीय", PratyayaType.KRT, KrtCategory.FUTURE_PARTICIPLE,
                          "to be done, gerundive", ["करणीय", "गमनीय"], 10),
            PratyayaPattern("य", PratyayaType.KRT, KrtCategory.FUTURE_PARTICIPLE,
                          "to be done, gerundive", ["कार्य", "भाव्य"], 9),
        ]
    
    def _create_krt_agent_nouns(self) -> List[PratyayaPattern]:
        """Agent noun suffixes (तृच्, ण्वुल्)."""
        return [
            # -तृ agent nouns
            PratyayaPattern("तृ", PratyayaType.KRT, KrtCategory.AGENT_NOUN,
                          "agent, doer", ["कर्तृ", "दातृ", "नेतृ"], 10),
            PratyayaPattern("तार", PratyayaType.KRT, KrtCategory.AGENT_NOUN,
                          "agent (with case ending)", ["कर्तार", "दातार"], 9),
            
            # -अक agent nouns
            PratyayaPattern("अक", PratyayaType.KRT, KrtCategory.AGENT_NOUN,
                          "agent, doer", ["नायक", "सायक"], 9),
            PratyayaPattern("क", PratyayaType.KRT, KrtCategory.AGENT_NOUN,
                          "agent, doer", ["भोजक", "लेखक"], 8),
            
            # -इन् possessor
            PratyayaPattern("इन्", PratyayaType.KRT, KrtCategory.AGENT_NOUN,
                          "possessing, characterized by", ["मन्त्रिन्", "योगिन्"], 9),
            
            # -उक
            PratyayaPattern("उक", PratyayaType.KRT, KrtCategory.AGENT_NOUN,
                          "fond of doing", ["भावुक", "कामुक"], 8),
        ]
    
    def _create_krt_action_nouns(self) -> List[PratyayaPattern]:
        """Action noun suffixes (घञ्, ल्युट्)."""
        return [
            # -अन action nouns
            PratyayaPattern("अन", PratyayaType.KRT, KrtCategory.ACTION_NOUN,
                          "action, act of doing", ["भवन", "गमन", "दर्शन"], 9),
            PratyayaPattern("न", PratyayaType.KRT, KrtCategory.ACTION_NOUN,
                          "action", ["चरण", "स्मरण"], 8),
            
            # -ति action nouns
            PratyayaPattern("ति", PratyayaType.KRT, KrtCategory.ACTION_NOUN,
                          "action, act of doing", ["गति", "मति", "भक्ति"], 9),
            
            # -आ action nouns (feminine)
            PratyayaPattern("आ", PratyayaType.KRT, KrtCategory.ACTION_NOUN,
                          "action (feminine)", ["क्रिया", "सेवा", "पूजा"], 8),
            
            # Instrumental nouns
            PratyayaPattern("अन", PratyayaType.KRT, KrtCategory.INSTRUMENTAL_NOUN,
                          "instrument for doing", ["भोजन", "लेखन"], 8),
        ]
    
    # === TADDHITA PRATYAYAS (SECONDARY DERIVATIVES) ===
    
    def _create_taddhita_abstract(self) -> List[PratyayaPattern]:
        """Abstract noun suffixes (त्व, ताल्)."""
        return [
            # -त्व abstract (neuter)
            PratyayaPattern("त्व", PratyayaType.TADDHITA, TaddhitaCategory.ABSTRACT,
                          "abstract quality, -ness, -hood", ["देवत्व", "मनुष्यत्व", "नेतृत्व"], 10),
            
            # -ता abstract (feminine)
            PratyayaPattern("ता", PratyayaType.TADDHITA, TaddhitaCategory.ABSTRACT,
                          "abstract quality (fem), -ness", ["सुन्दरता", "महत्ता"], 10),
            
            # -इमन् abstract
            PratyayaPattern("इमन्", PratyayaType.TADDHITA, TaddhitaCategory.ABSTRACT,
                          "abstract quality", ["गरिमन्", "महिमन्"], 9),
            
            # -ष्य abstract
            PratyayaPattern("य", PratyayaType.TADDHITA, TaddhitaCategory.ABSTRACT,
                          "abstract quality", ["माधुर्य", "सौन्दर्य"], 8),
        ]
    
    def _create_taddhita_possessive(self) -> List[PratyayaPattern]:
        """Possessive suffixes (मतुप्, वतुप्)."""
        return [
            # -मत् possessive
            PratyayaPattern("मत्", PratyayaType.TADDHITA, TaddhitaCategory.POSSESSIVE,
                          "possessing, having", ["धनमत्", "बुद्धिमत्"], 10),
            PratyayaPattern("मान्", PratyayaType.TADDHITA, TaddhitaCategory.POSSESSIVE,
                          "possessing (masc nom sg)", ["धनमान्", "श्रीमान्"], 9),
            
            # -वत् possessive
            PratyayaPattern("वत्", PratyayaType.TADDHITA, TaddhitaCategory.POSSESSIVE,
                          "possessing, having, like", ["बलवत्", "गुणवत्"], 10),
            PratyayaPattern("वान्", PratyayaType.TADDHITA, TaddhitaCategory.POSSESSIVE,
                          "possessing (masc nom sg)", ["बलवान्"], 9),
            
            # -इन् possessive
            PratyayaPattern("इन्", PratyayaType.TADDHITA, TaddhitaCategory.POSSESSIVE,
                          "possessing, characterized by", ["बलिन्", "तपस्विन्"], 9),
            PratyayaPattern("ई", PratyayaType.TADDHITA, TaddhitaCategory.POSSESSIVE,
                          "possessing (fem)", ["बलिनी", "तपस्विनी"], 8),
        ]
    
    def _create_taddhita_adjectives(self) -> List[PratyayaPattern]:
        """Adjective-forming suffixes."""
        return [
            # -इक adjectives
            PratyayaPattern("इक", PratyayaType.TADDHITA, TaddhitaCategory.ADJECTIVE,
                          "relating to, pertaining to", ["धार्मिक", "भौतिक", "वैदिक"], 10),
            
            # -ईय adjectives
            PratyayaPattern("ईय", PratyayaType.TADDHITA, TaddhitaCategory.ADJECTIVE,
                          "fit for, worthy of", ["श्रेय", "भवदीय"], 9),
            
            # -य adjectives
            PratyayaPattern("य", PratyayaType.TADDHITA, TaddhitaCategory.ADJECTIVE,
                          "made of, relating to", ["काव्य", "दिव्य"], 8),
            
            # -मय adjectives
            PratyayaPattern("मय", PratyayaType.TADDHITA, TaddhitaCategory.ADJECTIVE,
                          "made of, consisting of", ["सुवर्णमय", "काष्ठमय"], 10),
            
            # -वत् comparative
            PratyayaPattern("वत्", PratyayaType.TADDHITA, TaddhitaCategory.ADJECTIVE,
                          "like, similar to", ["राजवत्", "देववत्"], 8),
            
            # Superlatives
            PratyayaPattern("तम", PratyayaType.TADDHITA, TaddhitaCategory.ADJECTIVE,
                          "superlative -est", ["श्रेष्ठतम", "उत्तमतम"], 9),
            PratyayaPattern("इष्ठ", PratyayaType.TADDHITA, TaddhitaCategory.ADJECTIVE,
                          "superlative -est", ["गरिष्ठ", "ज्येष्ठ"], 9),
            
            # Comparatives
            PratyayaPattern("तर", PratyayaType.TADDHITA, TaddhitaCategory.ADJECTIVE,
                          "comparative -er", ["उत्तर", "अधर"], 9),
            PratyayaPattern("ीयस्", PratyayaType.TADDHITA, TaddhitaCategory.ADJECTIVE,
                          "comparative -er", ["गरीयस्", "श्रेयस्"], 9),
        ]
    
    def _create_taddhita_patronymic(self) -> List[PratyayaPattern]:
        """Patronymic/lineage suffixes."""
        return [
            # Gender-specific patronymics
            PratyayaPattern("अ", PratyayaType.TADDHITA, TaddhitaCategory.PATRONYMIC,
                          "descendant of (masc)", ["वासुदेव", "माहेश्वर"], 7),
            PratyayaPattern("ई", PratyayaType.TADDHITA, TaddhitaCategory.PATRONYMIC,
                          "descendant of (fem)", ["दाक्षायणी"], 8),
            
            # -एय patronymic
            PratyayaPattern("एय", PratyayaType.TADDHITA, TaddhitaCategory.PATRONYMIC,
                          "descendant of", ["गार्ग्य", "कौशाम्बेय"], 8),
            
            # -आयन patronymic
            PratyayaPattern("आयन", PratyayaType.TADDHITA, TaddhitaCategory.PATRONYMIC,
                          "descendant of", ["नारायण"], 9),
        ]
    
    def _create_feminine_suffixes(self) -> List[PratyayaPattern]:
        """Feminine formation suffixes (स्त्रीप्रत्यय)."""
        return [
            # Primary feminine suffixes
            PratyayaPattern("आ", PratyayaType.STRI, None,
                          "feminine formation", ["बाला", "सुन्दरा"], 8),
            PratyayaPattern("ई", PratyayaType.STRI, None,
                          "feminine formation", ["देवी", "युवती"], 9),
            PratyayaPattern("इका", PratyayaType.STRI, None,
                          "feminine formation", ["बालिका", "लेखिका"], 9),
            
            # Agent noun feminines
            PratyayaPattern("त्री", PratyayaType.STRI, None,
                          "feminine agent", ["नेत्री", "कर्त्री"], 9),
            
            # Possessive feminines
            PratyayaPattern("इनी", PratyayaType.STRI, None,
                          "feminine possessive", ["योगिनी", "तपस्विनी"], 9),
            PratyayaPattern("मती", PratyayaType.STRI, None,
                          "feminine possessive", ["बुद्धिमती"], 9),
            PratyayaPattern("वती", PratyayaType.STRI, None,
                          "feminine possessive", ["गुणवती"], 9),
        ]


# === UTILITY FUNCTIONS ===

def analyze_suffix(word: str) -> List[PratyayaAnalysis]:
    """
    Convenience function to analyze a word for suffixes.
    
    Args:
        word: Sanskrit word in Devanagari
    
    Returns:
        List of possible suffix analyses
    """
    analyzer = PratyayaAnalyzer()
    return analyzer.analyze(word)


def identify_krt_pratyayas(word: str) -> List[PratyayaAnalysis]:
    """Get only kṛt pratyaya analyses."""
    all_analyses = analyze_suffix(word)
    return [a for a in all_analyses if a.pratyaya_type == PratyayaType.KRT]


def identify_taddhita_pratyayas(word: str) -> List[PratyayaAnalysis]:
    """Get only taddhita pratyaya analyses."""
    all_analyses = analyze_suffix(word)
    return [a for a in all_analyses if a.pratyaya_type == PratyayaType.TADDHITA]
