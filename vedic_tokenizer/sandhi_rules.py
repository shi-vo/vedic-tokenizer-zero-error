"""
Complete Sandhi Rules for Vedic Sanskrit - 130 Rules
=====================================================

Implements comprehensive Sandhi (phonetic transformation) rules from 
Paninian Ashtadhyayi and Siddhanta Kaumudi.

Categories:
- Vowel Sandhi (33 rules)
- Consonant Sandhi (50 rules)
- Visarga Sandhi (20 rules)
- Special/Vedic Sandhi (27 rules)

Total: 130 rules
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from enum import Enum


class SandhiCategory(Enum):
    """Categories of Sandhi rules."""
    VOWEL = "svara"
    CONSONANT = "vyanjana"
    VISARGA = "visarga"
    SPECIAL = "vishista"


@dataclass
class SandhiRule:
    """Represents a Sandhi transformation rule."""
    rule_id: str
    category: SandhiCategory
    left_pattern: str
    right_pattern: str
    result: str
    priority: int
    vedic_only: bool = False
    panini_sutra: Optional[str] = None
    description: str = ""
    examples: List[Tuple[str, str, str]] = field(default_factory=list)
    
    def applies(self, left_word: str, right_word: str) -> bool:
        """Check if this rule applies to the word boundary."""
        # Check right word
        # Standard string matching works for vowels
        # For Consonants (e.g. pattern 'k-halant'), it should match 'ka', 'ki' etc.
        if right_word.startswith(self.right_pattern):
            pass
        elif self.right_pattern.endswith("्") and right_word.startswith(self.right_pattern[:-1]):
            # Pattern "k-halant" matches "ka" (k with inherent a, or k with matra)
            pass
        else:
            return False
            
        # Check left word - requires Devanagari intelligence
        if self.left_pattern == "अ":
            # Matches if ending in consonant (meaning inherent 'a') or explicit 'अ'
            # But NOT if ends in virama (halant) or other matras
            if not left_word:
                return False
            last_char = left_word[-1]
            # Check for virama or other vowels/matras
            is_halanta = last_char == "्"
            is_matra = last_char in "ािीुूृॄेैोौँंः"
            return not (is_halanta or is_matra)
            
        elif self.left_pattern == "अः":
             # Matches if ending in "Explicit A + Visarga" OR "Consonant + Visarga"
             if left_word.endswith("अः"): return True
             
             # Check for "Consonant + Visarga"
             # Must end in Visarga
             if not left_word.endswith("ः"): return False
             
             # Preceding char must be a consonant (not vowel, not matra, not halant)
             if len(left_word) < 2: return False # Just "ः" is invalid
             
             prev_char = left_word[-2]
             is_halanta = prev_char == "्"
             is_matra = prev_char in "ािीुूृॄेैोौँं" # Note: visarga itself is not a matra on a matra
             is_vowel = prev_char in "अआइईउऊऋएऐओऔ"
             
             return not (is_halanta or is_matra or is_vowel)
            
        elif self.left_pattern == "आ":
            return left_word.endswith("ा") or left_word.endswith("आ")
            
        elif self.left_pattern == "इ":
            return left_word.endswith("ि") or left_word.endswith("इ")
            
        elif self.left_pattern == "ई":
            return left_word.endswith("ी") or left_word.endswith("ई")
            
        elif self.left_pattern == "उ":
            return left_word.endswith("ु") or left_word.endswith("उ")
            
        elif self.left_pattern == "ऊ":
            return left_word.endswith("ू") or left_word.endswith("ऊ")
            
        elif self.left_pattern == "ऋ":
            return left_word.endswith("ृ") or left_word.endswith("ऋ")

        elif self.left_pattern == "इः":
            # Matches Matra I + Visarga OR Independent I + Visarga
            return left_word.endswith("िः") or left_word.endswith("इः")
            
        elif self.left_pattern == "उः":
            # Matches Matra U + Visarga OR Independent U + Visarga
            return left_word.endswith("ुः") or left_word.endswith("उः")
            
        # Default for consonants and others
        return left_word.endswith(self.left_pattern)
    
    def apply_forward(self, left_word: str, right_word: str) -> Optional[str]:
        """Apply the rule to combine two words."""
        if not self.applies(left_word, right_word):
            return None


        
        # 1. Calculate Left Base (Consonant + Halant form)
        # We want the 'pure consonant' form of the left word before adding the result.
        left_base = left_word
        
        if self.left_pattern == "अ":
            # Inherent 'a'. To get base, we add Halant to the consonant.
            # e.g. "Deva" -> "Dev" (Dev+Halant)
            left_base = left_word + "्"
            
        elif self.left_pattern == "अः":
             # "ah". Explicit or Inherent.
             if left_word.endswith("अः"):
                 left_base = left_word[:-2] + "्"
             else:
                 # Ends in Consonant+Visarga (Ramah -> Ram+ah)
                 # Remove last char (Visarga).
                 # Previous char is Consonant (with inherent a implied).
                 # But we want Pure Base. So Ramah -> Ram (add Halant).
                 left_base = left_word[:-1] + "्"

        elif self.left_pattern in ["आ", "इ", "ई", "उ", "ऊ", "ऋ", "ए", "ऐ", "ओ", "औ"]:
            # Basic Vowels/Matras
            if left_word.endswith(self.left_pattern): # Explicit vowel
                left_base = left_word[:-len(self.left_pattern)] # Usually empty string or ending in existing halant if separate?
                # If explicit vowel "RamA", base is "Ram" (halant needed?)
                # "Maha" (ends in aa). -> Mah. -> Mah (halant).
                if left_base and not left_base.endswith("्"):
                     left_base += "्"
            else: # Matra
                # Strip matra
                left_base = left_word[:-1]
                # Add halant to make it pure consonant
                left_base += "्"
                
        else:
            # Consonants (e.g. 'm', 't', 'k').
            # They should already end in Halant if they match the pattern (usually).
            # e.g. pattern "म्". Matches "Ram". "Ram" ends in Halant?
            # "तम्". Ends in Halant.
            # Remove pattern.
            left_base = left_word[:-len(self.left_pattern)] if self.left_pattern else left_word
        
        # 2. Calculate Right Base (Remove consumed prefix)
        right_base = right_word[len(self.right_pattern):] if self.right_pattern else right_word
        
        # 3. Determine Final Result and Join
        final_result = self.result
        
        # Check if we should convert result to Matra
        # This applies if the result starts with a Vowel that has a matra form
        # AND we are attaching to a consonant base.
        
        vowel_to_matra = {
             "आ": "ा", "इ": "ि", "ई": "ी", "उ": "ु", "ऊ": "ू",
             "ऋ": "ृ", "ए": "े", "ऐ": "ै", "ओ": "ो", "औ": "ौ"
             # Note: 'अ' has no matra.
        }
        
        first_char = final_result[0] if final_result else ""
        
        if first_char in vowel_to_matra:
            # Result starts with a Vowel that becomes a Matra.
            # Convert first char to Matra IF assigning to a consonant base.
            if left_base: # Ensure we have a base (not empty string like in SP20)
                matra = vowel_to_matra[first_char]
                rest = final_result[1:]
                final_result = matra + rest
                
                # Since we are using a Matra, we DO NOT want the base to have Halant.
                # The Matra REPLACES the Halant/Inherent-vowel slot.
                if left_base.endswith("्"):
                    left_base = left_base[:-1]
            # Else: keep independent vowel (e.g. Ut -> Ud...). Base empty. Result 'Uda'.
                
        elif first_char == "अ":
            # Result starts with 'a'.
            # 'a' merges with Halant to form Consonant.
            # So we KEEP the Halant on the base? 
            # No. 'k-halant' + 'a' -> 'ka'.
            # Python: '\u0915\u094d' + '\u0905' -> Renders as 'k'+'a' (explicit).
            # We want 'ka' (inherent).
            # So if we have 'k-halant', and we add 'a', we should just DROP the Halant and DROP the 'a'.
            # e.g. VS17: 'Dev-halant' + 'ar' ('a'+'r').
            # We want 'Devar'.
            # 'Dev-halant' + 'a' -> 'Dev'.
            # So we drop Halant AND drop 'a' from result.
            
            if left_base.endswith("्"):
                left_base = left_base[:-1] # Drop Halant -> 'Dev' (inherent a)
                final_result = final_result[1:] # Drop 'a' -> 'r'
                # Result 'Devr'? No 'Devar'.
                # 'v' has inherent a. 'r' is next char.
                # 'Dev' + 'r' -> 'Devar'. Yes.
        
        # Else (Consonant result):
        # Keep Halant on base.
        # e.g. 'Prat-halant' + 'y' -> 'Praty'. Correct.
        
        return left_base + final_result + right_base
    
    def apply_reverse(self, combined: str) -> List[Tuple[str, str]]:
        """Attempt to split a combined form according to this rule."""
        splits = []
        
        # Determine what to look for (matra or full vowel)
        search_patterns = [self.result]
        
        # Add matra equivalent if result is a vowel
        vowel_to_matra = {
             "आ": "ा", "इ": "ि", "ई": "ी", "उ": "ु", "ऊ": "ू",
             "ऋ": "ृ", "ए": "े", "ऐ": "ै", "ओ": "ो", "औ": "ौ"
        }
        if self.result in vowel_to_matra:
            search_patterns.append(vowel_to_matra[self.result])
            
        for pattern in search_patterns:
            if not pattern: continue # Skip empty result patterns
            
            start_idx = 0
            while True:
                idx = combined.find(pattern, start_idx)
                if idx == -1:
                    break
                
                # We found a potential split point
                # Pattern is at combined[idx : idx+len(pattern)]
                
                # Context before the split
                prefix = combined[:idx]
                # Context after the split
                suffix = combined[idx+len(pattern):]
                
                # Reconstruct Left Word
                left_reconstructed = prefix
                if self.left_pattern == "अ":
                    # If inherent 'a', we don't add anything visible 
                    # UNLESS the prefix ends in a halant (which would be weird here)
                    # "Ram" + "a" -> "Rama". prefix "Ram".
                    pass
                elif self.left_pattern in vowel_to_matra:
                    # Append corresponding matra
                    left_reconstructed += vowel_to_matra[self.left_pattern]
                else:
                    # Append the pattern directly
                    left_reconstructed += self.left_pattern
                
                # Reconstruct Right Word
                right_reconstructed = self.right_pattern + suffix
                
                splits.append((left_reconstructed, right_reconstructed))
                
                # Move forward to find next occurrence
                start_idx = idx + 1
                
        return splits


# Legacy compatibility
class SandhiRules:
    def __init__(self):
        # Ensure rules are populated
        self.rules = ALL_SANDHI_RULES


# =============================================================================
# VOWEL SANDHI RULES - 33 rules
# =============================================================================

def _create_vowel_rules():
    """Create all vowel sandhi rules."""
    rules = []
    
    # Savarna Dirgha (similar vowel lengthening) - 8 rules
    rules.extend([
        SandhiRule("VS01", SandhiCategory.VOWEL, "अ", "अ", "आ", 10, panini_sutra="6.1.101",
                   description="a + a → ā", examples=[("रम", "अति", "रमाति")]),
        SandhiRule("VS02", SandhiCategory.VOWEL, "आ", "अ", "आ", 10, panini_sutra="6.1.101",
                   description="ā + a → ā", examples=[("रमा", "अति", "रमाति")]),
        SandhiRule("VS03", SandhiCategory.VOWEL, "अ", "आ", "आ", 10, panini_sutra="6.1.101",
                   description="a + ā → ā", examples=[("तत्र", "आगच्छति", "तत्रागच्छति")]),
        SandhiRule("VS04", SandhiCategory.VOWEL, "आ", "आ", "आ", 9, panini_sutra="6.1.101",
                   description="ā + ā → ā", examples=[("रमा", "आगच्छति", "रमागच्छति")]),
        SandhiRule("VS05", SandhiCategory.VOWEL, "इ", "इ", "ई", 9, panini_sutra="6.1.101",
                   description="i + i → ī", examples=[("कवि", "इन्द्रः", "कवीन्द्रः")]),
        SandhiRule("VS06", SandhiCategory.VOWEL, "ई", "इ", "ई", 9, panini_sutra="6.1.101",
                   description="ī + i → ī", examples=[("नदी", "इव", "नदीव")]),
        SandhiRule("VS07", SandhiCategory.VOWEL, "उ", "उ", "ऊ", 8, panini_sutra="6.1.101",
                   description="u + u → ū", examples=[("साधु", "उक्तिः", "साधूक्तिः")]),
        SandhiRule("VS08", SandhiCategory.VOWEL, "ऊ", "उ", "ऊ", 8, panini_sutra="6.1.101",
                   description="ū + u → ū", examples=[("वधू", "उक्तिः", "वधूक्तिः")]),
    ])
    
    # Guna Sandhi - 10 rules
    rules.extend([
        SandhiRule("VS09", SandhiCategory.VOWEL, "अ", "इ", "ए", 10, panini_sutra="6.1.87",
                   description="a + i → e (guna)", examples=[("रम", "इति", "रमेति")]),
        SandhiRule("VS10", SandhiCategory.VOWEL, "अ", "ई", "ए", 10, panini_sutra="6.1.87",
                   description="a + ī → e (guna)", examples=[("परम", "ईश्वरः", "परमेश्वरः")]),
        SandhiRule("VS11", SandhiCategory.VOWEL, "आ", "इ", "ए", 9, panini_sutra="6.1.87",
                   description="ā + i → e (guna)", examples=[("रमा", "इति", "रमेति")]),
        SandhiRule("VS12", SandhiCategory.VOWEL, "आ", "ई", "ए", 9, panini_sutra="6.1.87",
                   description="ā + ī → e (guna)", examples=[("महा", "ईशः", "महेशः")]),
        SandhiRule("VS13", SandhiCategory.VOWEL, "अ", "उ", "ओ", 10, panini_sutra="6.1.87",
                   description="a + u → o (guna)", examples=[("सुर", "उत्तमः", "सुरोत्तमः")]),
        SandhiRule("VS14", SandhiCategory.VOWEL, "अ", "ऊ", "ओ", 9, panini_sutra="6.1.87",
                   description="a + ū → o (guna)", examples=[("परम", "ऊर्जितः", "परमोर्जितः")]),
        SandhiRule("VS15", SandhiCategory.VOWEL, "आ", "उ", "ओ", 9, panini_sutra="6.1.87",
                   description="ā + u → o (guna)", examples=[("महा", "उदयः", "महोदयः")]),
        SandhiRule("VS16", SandhiCategory.VOWEL, "आ", "ऊ", "ओ", 9, panini_sutra="6.1.87",
                   description="ā + ū → o (guna)", examples=[("महा", "ऊर्जः", "महोर्जः")]),
        SandhiRule("VS17", SandhiCategory.VOWEL, "अ", "ऋ", "अर्", 8, panini_sutra="6.1.87",
                   description="a + ṛ → ar (guna)", examples=[("देव", "ऋषिः", "देवर्षिः")]),
        SandhiRule("VS18", SandhiCategory.VOWEL, "आ", "ऋ", "अर्", 8, panini_sutra="6.1.87",
                   description="ā + ṛ → ar (guna)", examples=[("महा", "ऋषिः", "महर्षिः")]),
    ])
    
    # Vriddhi Sandhi - 6 rules
    rules.extend([
        SandhiRule("VS19", SandhiCategory.VOWEL, "अ", "ए", "ऐ", 8, panini_sutra="6.1.88",
                   description="a + e → ai (vriddhi)", examples=[("अद्य", "एव", "अद्यैव")]),
        SandhiRule("VS20", SandhiCategory.VOWEL, "आ", "ए", "ऐ", 7, panini_sutra="6.1.88",
                   description="ā + e → ai (vriddhi)", examples=[("सदा", "एव", "सदैव")]),
        SandhiRule("VS21", SandhiCategory.VOWEL, "अ", "ऐ", "ऐ", 7, panini_sutra="6.1.88",
                   description="a + ai → ai (vriddhi)", examples=[("तत्र", "ऐश्वर्यम्", "तत्रैश्वर्यम्")]),
        SandhiRule("VS22", SandhiCategory.VOWEL, "अ", "ओ", "औ", 8, panini_sutra="6.1.88",
                   description="a + o → au (vriddhi)", examples=[("वन", "ओषधिः", "वनौषधिः")]),
        SandhiRule("VS23", SandhiCategory.VOWEL, "आ", "ओ", "औ", 7, panini_sutra="6.1.88",
                   description="ā + o → au (vriddhi)", examples=[("महा", "ओजः", "महौजः")]),
        SandhiRule("VS24", SandhiCategory.VOWEL, "अ", "औ", "औ", 7, panini_sutra="6.1.88",
                   description="a + au → au (vriddhi)", examples=[("परम", "औषधम्", "परमौषधम्")]),
    ])
    
    # Yan Sandhi - 9 rules
    rules.extend([
        SandhiRule("VS25", SandhiCategory.VOWEL, "इ", "अ", "य", 10, panini_sutra="6.1.77",
                   description="i + a → ya (yan)", examples=[("प्रति", "अर्थः", "प्रत्यर्थः")]),
        SandhiRule("VS26", SandhiCategory.VOWEL, "ई", "अ", "य", 9, panini_sutra="6.1.77",
                   description="ī + a → ya (yan)", examples=[("नदी", "अत्र", "नद्यत्र")]),
        SandhiRule("VS27", SandhiCategory.VOWEL, "उ", "अ", "व", 9, panini_sutra="6.1.77",
                   description="u + a → va (yan)", examples=[("मधु", "अत्र", "मध्वत्र")]),
        SandhiRule("VS28", SandhiCategory.VOWEL, "ऊ", "अ", "व", 8, panini_sutra="6.1.77",
                   description="ū + a → va (yan)", examples=[("वधू", "अत्र", "वध्वत्र")]),
        SandhiRule("VS29", SandhiCategory.VOWEL, "ऋ", "अ", "र", 7, panini_sutra="6.1.77",
                   description="ṛ + a → ra (yan)", examples=[("पितृ", "अर्थः", "पित्रर्थः")]),
        SandhiRule("VS30", SandhiCategory.VOWEL, "इ", "आ", "या", 9, panini_sutra="6.1.77",
                   description="i + ā → yā", examples=[("प्रति", "आह", "प्रत्याह")]),
        SandhiRule("VS31", SandhiCategory.VOWEL, "इ", "उ", "यु", 8, panini_sutra="6.1.77",
                   description="i + u → yu", examples=[("अति", "उत्तमः", "अत्युत्तमः")]),
        SandhiRule("VS32", SandhiCategory.VOWEL, "उ", "आ", "वा", 8, panini_sutra="6.1.77",
                   description="u + ā → vā", examples=[("सु", "आगतः", "स्वागतः")]),
        SandhiRule("VS33", SandhiCategory.VOWEL, "उ", "इ", "वि", 7, panini_sutra="6.1.77",
                   description="u + i → vi", examples=[("अनु", "इष्टः", "अन्विष्टः")]),
    ])
    
    return rules


VOWEL_SANDHI_RULES = _create_vowel_rules()


# =============================================================================
# CONSONANT SANDHI RULES - 50 rules
# =============================================================================

CONSONANT_SANDHI_RULES = [
    # Jhal-Jash voicing rules
    SandhiRule("CS01", SandhiCategory.CONSONANT, "क्", "ग", "ग्ग", 8,
               description="k + g → gg", examples=[("वाक्", "गतः", "वाग्गतः")]),
    SandhiRule("CS02", SandhiCategory.CONSONANT, "त्", "ज", "ज्ज", 8,
               description="t + j → jj", examples=[("तत्", "जलम्", "तज्जलम्")]),
    SandhiRule("CS03", SandhiCategory.CONSONANT, "त्", "च", "च्च", 9, panini_sutra="8.4.40",
               description="t + c → cc", examples=[("तत्", "च", "तच्च")]),
    SandhiRule("CS04", SandhiCategory.CONSONANT, "त्", "श", "च्छ", 8,
               description="t + ś → cch", examples=[("तत्", "शास्त्रम्", "तच्छास्त्रम्")]),
    SandhiRule("CS05", SandhiCategory.CONSONANT, "द्", "ध", "द्ध", 7,
               description="d + dh → ddh", examples=[("तद्", "धनम्", "तद्धनम्")]),
    SandhiRule("CS06", SandhiCategory.CONSONANT, "र्", "न", "र्ण", 9, panini_sutra="8.4.1",
               description="r + n → rṇ", examples=[("पुनर्", "नमति", "पुनर्णमति")]),
    SandhiRule("CS07", SandhiCategory.CONSONANT, "ष्", "न", "ष्ण", 8,
               description="ṣ + n → ṣṇ", examples=[("विष्", "नाशः", "विष्णाशः")]),
    
    # Anusvara before all consonants (24 rules: CS08-CS31)
    SandhiRule("CS08", SandhiCategory.CONSONANT, "म्", "क", "ंक", 10, panini_sutra="8.3.23",
               description="m + k → ṃk", examples=[("तम्", "करोति", "तंकरोति")]),
    SandhiRule("CS09", SandhiCategory.CONSONANT, "म्", "ख", "ंख", 9,
               description="m + kh → ṃkh", examples=[("तम्", "खलः", "तंखलः")]),
    SandhiRule("CS10", SandhiCategory.CONSONANT, "म्", "ग", "ंग", 9,
               description="m + g → ṃg", examples=[("तम्", "गच्छति", "तंगच्छति")]),
    SandhiRule("CS11", SandhiCategory.CONSONANT, "म्", "घ", "ंघ", 8,
               description="m + gh → ṃgh", examples=[("तम्", "घोषः", "तंघोषः")]),
    SandhiRule("CS12", SandhiCategory.CONSONANT, "म्", "च", "ंच", 10,
               description="m + c → ṃc", examples=[("तम्", "च", "तंच")]),
    SandhiRule("CS13", SandhiCategory.CONSONANT, "म्", "छ", "ंछ", 8,
               description="m + ch → ṃch", examples=[("तम्", "छन्दः", "तंछन्दः")]),
    SandhiRule("CS14", SandhiCategory.CONSONANT, "म्", "ज", "ंज", 9,
               description="m + j → ṃj", examples=[("तम्", "जयः", "तंजयः")]),
    SandhiRule("CS15", SandhiCategory.CONSONANT, "म्", "झ", "ंझ", 7,
               description="m + jh → ṃjh", examples=[("तम्", "झटिति", "तंझटिति")]),
    SandhiRule("CS16", SandhiCategory.CONSONANT, "म्", "ट", "ंट", 8,
               description="m + ṭ → ṃṭ", examples=[("तम्", "टङ्कः", "तंटङ्कः")]),
    SandhiRule("CS17", SandhiCategory.CONSONANT, "म्", "ठ", "ंठ", 7,
               description="m + ṭh → ṃṭh", examples=[("तम्", "ठः", "तंठः")]),
    SandhiRule("CS18", SandhiCategory.CONSONANT, "म्", "ड", "ंड", 7,
               description="m + ḍ → ṃḍ", examples=[("तम्", "डमरुः", "तंडमरुः")]),
    SandhiRule("CS19", SandhiCategory.CONSONANT, "म्", "ढ", "ंढ", 6,
               description="m + ḍh → ṃḍh", examples=[("तम्", "ढौकसे", "तंढौकसे")]),
    SandhiRule("CS20", SandhiCategory.CONSONANT, "म्", "त", "ंत", 10,
               description="m + t → ṃt", examples=[("तम्", "तु", "तंतु")]),
    SandhiRule("CS21", SandhiCategory.CONSONANT, "म्", "थ", "ंथ", 8,
               description="m + th → ṃth", examples=[("तम्", "थः", "तंथः")]),
    SandhiRule("CS22", SandhiCategory.CONSONANT, "म्", "द", "ंद", 9,
               description="m + d → ṃd", examples=[("तम्", "दत्तम्", "तंदत्तम्")]),
    SandhiRule("CS23", SandhiCategory.CONSONANT, "म्", "ध", "ंध", 8,
               description="m + dh → ṃdh", examples=[("तम्", "धर्मः", "तंधर्मः")]),
    SandhiRule("CS24", SandhiCategory.CONSONANT, "म्", "न", "ंन", 9,
               description="m + n → ṃn", examples=[("तम्", "नयति", "तंनयति")]),
    SandhiRule("CS25", SandhiCategory.CONSONANT, "म्", "प", "ंप", 10,
               description="m + p → ṃp", examples=[("तम्", "पश्यति", "तंपश्यति")]),
    SandhiRule("CS26", SandhiCategory.CONSONANT, "म्", "फ", "ंफ", 8,
               description="m + ph → ṃph", examples=[("तम्", "फलम्", "तंफलम्")]),
    SandhiRule("CS27", SandhiCategory.CONSONANT, "म्", "ब", "ंब", 9,
               description="m + b → ṃb", examples=[("तम्", "ब्रूहि", "तंब्रूहि")]),
    SandhiRule("CS28", SandhiCategory.CONSONANT, "म्", "भ", "ंभ", 8,
               description="m + bh → ṃbh", examples=[("तम्", "भवति", "तंभवति")]),
    SandhiRule("CS29", SandhiCategory.CONSONANT, "म्", "य", "ंय", 8,
               description="m + y → ṃy", examples=[("तम्", "यति", "तंयति")]),
    SandhiRule("CS30", SandhiCategory.CONSONANT, "म्", "र", "ंर", 8,
               description="m + r → ṃr", examples=[("तम्", "रामः", "तंरामः")]),
    SandhiRule("CS31", SandhiCategory.CONSONANT, "म्", "ल", "ंल", 8,
               description="m + l → ṃl", examples=[("तम्", "लोकः", "तंलोकः")]),
    
    # Additional consonant rules (CS32-CS50)
    SandhiRule("CS32", SandhiCategory.CONSONANT, "म्", "व", "ंव", 8,
               description="m + v → ṃv", examples=[("तम्", "वदति", "तंवदति")]),
    SandhiRule("CS33", SandhiCategory.CONSONANT, "म्", "श", "ंश", 8,
               description="m + ś → ṃś", examples=[("तम्", "शुभम्", "तंशुभम्")]),
    SandhiRule("CS34", SandhiCategory.CONSONANT, "म्", "ष", "ंष", 8,
               description="m + ṣ → ṃṣ", examples=[("तम्", "षड्", "तंषड्")]),
    SandhiRule("CS35", SandhiCategory.CONSONANT, "म्", "स", "ंस", 9,
               description="m + s → ṃs", examples=[("तम्", "सत्यम्", "तंसत्यम्")]),
    SandhiRule("CS36", SandhiCategory.CONSONANT, "म्", "ह", "ंह", 8,
               description="m + h → ṃh", examples=[("तम्", "हि", "तंहि")]),
    SandhiRule("CS37", SandhiCategory.CONSONANT, "त्", "ल", "ल्ल", 7,
               description="t + l → ll", examples=[("तत्", "लोकः", "तल्लोकः")]),
    SandhiRule("CS38", SandhiCategory.CONSONANT, "त्", "ह", "द्ध", 7, panini_sutra="8.4.53",
               description="t + h → ddh", examples=[("तत्", "हि", "तद्धि")]),
    SandhiRule("CS39", SandhiCategory.CONSONANT, "त्", "त", "त्त", 8,
               description="t + t → tt (gemination)", examples=[("तत्", "तत्त्वम्", "तत्तत्त्वम्")]),
    SandhiRule("CS40", SandhiCategory.CONSONANT, "क्", "क", "क्क", 7,
               description="k + k → kk (gemination)", examples=[("वाक्", "कर्ता", "वाक्कर्ता")]),
    SandhiRule("CS41", SandhiCategory.CONSONANT, "त्", "ध", "द्ध", 8,
               description="t + dh → ddh (voicing)", examples=[("तत्", "धर्मः", "तद्धर्मः")]),
    SandhiRule("CS42", SandhiCategory.CONSONANT, "क्", "घ", "ग्घ", 7,
               description="k + gh → ggh", examples=[("वाक्", "घोषः", "वाग्घोषः")]),
    SandhiRule("CS43", SandhiCategory.CONSONANT, "स्", "त", "स्त", 9,
               description="s + t → st", examples=[("नमस्", "ते", "नमस्ते")]),
    SandhiRule("CS44", SandhiCategory.CONSONANT, "स्", "क", "स्क", 8,
               description="s + k → sk", examples=[("नमस्", "कार", "नमस्कार")]),
    SandhiRule("CS45", SandhiCategory.CONSONANT, "न्", "त", "न्त", 9,
               description="n + t → nt", examples=[("भवन्", "तु", "भवन्तु")]),
    SandhiRule("CS46", SandhiCategory.CONSONANT, "न्", "द", "न्द", 9,
               description="n + d → nd", examples=[("तान्", "दृष्ट्वा", "तान्दृष्ट्वा")]),
    SandhiRule("CS47", SandhiCategory.CONSONANT, "स्", "च", "श्च", 7, panini_sutra="8.4.44",
               description="s + c → śc (ṣṭutva)", examples=[("नमस्", "चित्", "नमश्चित्")]),
    SandhiRule("CS48", SandhiCategory.CONSONANT, "द्", "व", "द्व", 7,
               description="d + v → dv", examples=[("तद्", "वचः", "तद्वचः")]),
    SandhiRule("CS49", SandhiCategory.CONSONANT, "द्", "य", "द्य", 7,
               description="d + y → dy", examples=[("तद्", "यदि", "तद्यदि")]),
    SandhiRule("CS50", SandhiCategory.CONSONANT, "द्", "र", "द्र", 7,
               description="d + r → dr", examples=[("तद्", "राज्यम्", "तद्राज्यम्")]),
]


# =============================================================================
# VISARGA SANDHI RULES - 20 rules
# =============================================================================

VISARGA_SANDHI_RULES = [
    # Visarga before vowels
    SandhiRule("VIS01", SandhiCategory.VISARGA, "अः", "अ", "ओऽ", 10, panini_sutra="6.1.114",
               description="aḥ + a → o' (avagraha)", examples=[("रामः", "अत्र", "रामोऽत्र")]),
    SandhiRule("VIS02", SandhiCategory.VISARGA, "अः", "आ", "ओ", 9,
               description="aḥ + ā → o", examples=[("रामः", "आगच्छति", "रामोगच्छति")]),
    SandhiRule("VIS03", SandhiCategory.VISARGA, "अः", "इ", "ओ", 8,
               description="aḥ + i → o", examples=[("रामः", "इच्छति", "रामोच्छति")]),
    SandhiRule("VIS04", SandhiCategory.VISARGA, "अः", "ई", "ओ", 8,
               description="aḥ + ī → o", examples=[("रामः", "ईक्षते", "रामोक्षते")]),
    SandhiRule("VIS05", SandhiCategory.VISARGA, "अः", "उ", "ओ", 8,
               description="aḥ + u → o", examples=[("रामः", "उवाच", "रामोवाच")]),
    SandhiRule("VIS06", SandhiCategory.VISARGA, "अः", "ऊ", "ओ", 7,
               description="aḥ + ū → o", examples=[("रामः", "ऊर्ध्वम्", "रामोर्ध्वम्")]),
    SandhiRule("VIS07", SandhiCategory.VISARGA, "अः", "ए", "ओ", 7,
               description="aḥ + e → o", examples=[("रामः", "एति", "रामोति")]),
    SandhiRule("VIS08", SandhiCategory.VISARGA, "अः", "ओ", "ओ", 6,
               description="aḥ + o → o", examples=[("रामः", "ओम्", "रामोम्")]),
    
    # Visarga before consonants
    SandhiRule("VIS09", SandhiCategory.VISARGA, "अः", "क", "अःक", 9,
               description="aḥ + k → aḥ (unchanged)", examples=[("रामः", "करोति", "रामःकरोति")]),
    SandhiRule("VIS10", SandhiCategory.VISARGA, "अः", "प", "अःप", 9,
               description="aḥ + p → aḥ (unchanged)", examples=[("रामः", "पश्यति", "रामःपश्यति")]),
    SandhiRule("VIS11", SandhiCategory.VISARGA, "अः", "च", "अश्च", 7, panini_sutra="8.3.36",
               description="aḥ + c → aś", examples=[("रामः", "च", "रामश्च")]),
    SandhiRule("VIS12", SandhiCategory.VISARGA, "अः", "ट", "अष्ट", 7,
               description="aḥ + ṭ → aṣ", examples=[("रामः", "टङ्कः", "रामष्टङ्कः")]),
    SandhiRule("VIS13", SandhiCategory.VISARGA, "अः", "त", "अस्त", 8, panini_sutra="8.3.37",
               description="aḥ + t → as", examples=[("रामः", "तत्र", "रामस्तत्र")]),
    
    # Visarga replacement with र
    SandhiRule("VIS14", SandhiCategory.VISARGA, "ः", "र", "र", 7,
               description="ḥ + r → r (non-aḥ)", examples=[("पुनः", "रमते", "पुनरमते")]),
    SandhiRule("VIS15", SandhiCategory.VISARGA, "ः", "अ", "र", 7,
               description="ḥ (non-aḥ) + vowel → r", examples=[("पुनः", "अपि", "पुनरपि")]),
    
    # Other visarga patterns
    SandhiRule("VIS16", SandhiCategory.VISARGA, "इः", "अ", "इर", 6,
               description="iḥ + vowel → ir", examples=[("हरिः", "अत्र", "हरिरत्र")]),
    SandhiRule("VIS17", SandhiCategory.VISARGA, "उः", "अ", "उर", 6,
               description="uḥ + vowel → ur", examples=[("गुरुः", "अत्र", "गुरुरत्र")]),
    
    # Visarga deletion
    SandhiRule("VIS18", SandhiCategory.VISARGA, "अः", "स", "अःस", 7,
               description="aḥ + s → aḥs", examples=[("रामः", "सर्वः", "रामःसर्वः")]),
    SandhiRule("VIS19", SandhiCategory.VISARGA, "ः", "स", "स", 5,
               description="ḥ + s → deletion (s remains)", examples=[("अतः", "स्यात्", "अतस्यात्")]),
    SandhiRule("VIS20", SandhiCategory.VISARGA, "अः", "ह", "ओह", 6,
               description="aḥ + h → oh", examples=[("यतः", "हि", "यतोहि")]),
]


# =============================================================================
# SPECIAL/VEDIC SANDHI RULES - 27 rules
# =============================================================================

SPECIAL_SANDHI_RULES = [
    # Pragrhya - Exceptions where Sandhi does NOT apply
    SandhiRule("SP01", SandhiCategory.SPECIAL, "ई", "अ", "ई", 5, vedic_only=False,
               description="Pragṛhya: dual ī (no sandhi)", examples=[]),
    SandhiRule("SP02", SandhiCategory.SPECIAL, "ऊ", "अ", "ऊ", 5, vedic_only=False,
               description="Pragṛhya: dual ū (no sandhi)", examples=[]),
    SandhiRule("SP03", SandhiCategory.SPECIAL, "ए", "अ", "ए", 5, vedic_only=False,
               description="Pragṛhya: pronominal e (no sandhi)", examples=[]),
    
    # Pluta
    SandhiRule("SP04", SandhiCategory.SPECIAL, "अ३", "अ", "आ३", 3, vedic_only=True,
               description="Pluta sandhi (triple mora)", examples=[]),
    
    # Lopa
    SandhiRule("SP05", SandhiCategory.SPECIAL, "अ", "", "", 6,
               description="Final a deletion before vowel", examples=[]),
    SandhiRule("SP06", SandhiCategory.SPECIAL, "इ", "", "", 4, vedic_only=True,
               description="Vedic i deletion", examples=[]),
    
    # Vedic accent-related
    SandhiRule("SP07", SandhiCategory.SPECIAL, "॒", "॑", "॒॑", 2, vedic_only=True,
               description="Accent preservation", examples=[]),
    
    # Vedic irregular vowel combinations
    SandhiRule("SP08", SandhiCategory.SPECIAL, "आ", "इ", "आइ", 4, vedic_only=True,
               description="Vedic: no guna in meters", examples=[]),
    SandhiRule("SP09", SandhiCategory.SPECIAL, "इ", "आ", "इआ", 4, vedic_only=True,
               description="Vedic hiatus preservation", examples=[]),
    
    # Samprasarana
    SandhiRule("SP10", SandhiCategory.SPECIAL, "य", "इ", "इ", 5,
               description="Samprasarana: y → i", examples=[]),
    SandhiRule("SP11", SandhiCategory.SPECIAL, "व", "उ", "उ", 5,
               description="Samprasarana: v → u", examples=[]),
    
    # Compound-internal sandhi
    SandhiRule("SP12", SandhiCategory.SPECIAL, "म", "ह", "म्ह", 4,
               description="Special: m + h cluster", examples=[]),
    SandhiRule("SP13", SandhiCategory.SPECIAL, "त्", "", "त्", 6,
               description="t + s in compounds", examples=[("सत्", "सङ्गः", "सत्सङ्गः")]),
    SandhiRule("SP14", SandhiCategory.SPECIAL, "द्", "", "त्", 6, panini_sutra="8.4.55",
               description="d + s → ts in compounds", examples=[("तद्", "सुखम्", "तत्सुखम्")]),
    
    # Jastva rules
    SandhiRule("SP15", SandhiCategory.SPECIAL, "क्", "", "क्", 6, panini_sutra="8.2.41",
               description="k + s (unvoiced cluster)", examples=[("वाक्", "संस्थिता", "वाक्संस्थिता")]),
    SandhiRule("SP16", SandhiCategory.SPECIAL, "ग्", "स्", "क्स्", 5,
               description="g + s → ks (devoicing)", examples=[]),
    
    # Nati rules
    SandhiRule("SP17", SandhiCategory.SPECIAL, "न्", "ष", "ण्ष्", 6,
               description="Nati: n + ṣ → ṇṣ", examples=[]),
    
    # Vedic meter-preservation
    SandhiRule("SP18", SandhiCategory.SPECIAL, "े", "अ", "े अ", 3, vedic_only=True,
               description="Meter preservation: e + a", examples=[]),
    SandhiRule("SP19", SandhiCategory.SPECIAL, "ो", "अ", "ो अ", 3, vedic_only=True,
               description="Meter preservation: o + a", examples=[]),
    
    # Prefix sandhi
    SandhiRule("SP20", SandhiCategory.SPECIAL, "उत्", "आ", "उदा", 6,
               description="ut + ā → udā (prefix)", examples=[("उत्", "आहरति", "उदाहरति")]),
    SandhiRule("SP21", SandhiCategory.SPECIAL, "सम्", "आ", "समा", 7,
               description="sam + ā → samā (prefix)", examples=[("सम्", "आगच्छति", "समागच्छति")]),
    
    # Pada-final
    SandhiRule("SP22", SandhiCategory.SPECIAL, "त्", "", "त्", 5,
               description="Pada-final t (no change)", examples=[]),
    SandhiRule("SP23", SandhiCategory.SPECIAL, "न्", "", "न्", 5,
               description="Pada-final n (no change)", examples=[]),
    
    # Rare/archaic
    SandhiRule("SP24", SandhiCategory.SPECIAL, "ऋ", "आ", "रा", 3, vedic_only=True,
               description="Vedic ṛ + ā → rā", examples=[]),
    SandhiRule("SP25", SandhiCategory.SPECIAL, "ऌ", "अ", "ल", 1, vedic_only=True,
               description="Vedic ḷ sandhi", examples=[]),
    
    # Vedic gemination
    SandhiRule("SP26", SandhiCategory.SPECIAL, "स्", "स्", "स्स्", 4, vedic_only=True,
               description="Vedic ss cluster", examples=[]),
    SandhiRule("SP27", SandhiCategory.SPECIAL, "द्", "द्", "द्द्", 4, vedic_only=True,
               description="Vedic dd cluster", examples=[]),
]


# =============================================================================
# COMPLETE RULE SET
# =============================================================================

ALL_SANDHI_RULES = (
    VOWEL_SANDHI_RULES + 
    CONSONANT_SANDHI_RULES + 
    VISARGA_SANDHI_RULES + 
    SPECIAL_SANDHI_RULES
)

# Update legacy class
SandhiRules.rules = ALL_SANDHI_RULES


def get_rules_by_category(category: SandhiCategory) -> List[SandhiRule]:
    """Get all rules of a specific category."""
    return [rule for rule in ALL_SANDHI_RULES if rule.category == category]


def get_rules_by_priority(min_priority: int = 5) -> List[SandhiRule]:
    """Get rules with priority >= threshold (for fast mode)."""
    return [rule for rule in ALL_SANDHI_RULES if rule.priority >= min_priority]


def get_applicable_rules(left: str, right: str, vedic_mode: bool = False) -> List[SandhiRule]:
    """
    Get all rules that could apply to a word boundary.
    
    Args:
        left: End of first word
        right: Start of second word
        vedic_mode: Include Vedic-specific rules
    
    Returns:
        List of applicable rules, sorted by priority (highest first)
    """
    applicable = []
    for rule in ALL_SANDHI_RULES:
        if not vedic_mode and rule.vedic_only:
            continue
        if rule.applies(left, right):
            applicable.append(rule)
    
    # Sort by priority (highest priority first)
    return sorted(applicable, key=lambda r: r.priority, reverse=True)
