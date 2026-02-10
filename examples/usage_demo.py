"""
Example: Basic Usage of VedicZeroTokenizer

Demonstrates core functionality with simple examples.
"""

from vedic_tokenizer import VedicZeroTokenizer


def main():
    print("=" * 70)
    print("Vedic Zero-Error Tokenizer - Demo")
    print("=" * 70)
    print()
    
    # Initialize tokenizer
    print("1. Initializing tokenizer...")
    tokenizer = VedicZeroTokenizer()
    print(f"   Dictionary size: {tokenizer.dictionary.size()} words")
    print()
    
    # Example 1: Simple tokenization
    print("2. Simple Tokenization:")
    text1 = "राम सीता लक्ष्मण"
    print(f"   Input:  {text1}")
    tokens1 = tokenizer.tokenize(text1)
    print(f"   Tokens: {tokens1}")
    print()
    
    # Verify reversibility
    restored1 = tokenizer.detokenize(tokens1)
    print(f"   Detokenized: {restored1}")
    print(f"   ✓ Lossless: {restored1 == text1}")
    print()
    
    # Example 2: Longer verse
    print("3. Tokenizing Sanskrit Verse:")
    text2 = "धर्म अर्थ काम मोक्ष"
    print(f"   Input:  {text2}")
    tokens2 = tokenizer.tokenize(text2)
    print(f"   Tokens: {tokens2}")
    is_valid, metrics = tokenizer.verify_integrity(text2, tokens2)
    print(f"   ✓ Verification: {is_valid}")
    print(f"   Accuracy: {metrics['character_accuracy']:.2%}")
    print()
    
    # Example 3: Add custom vocabulary
    print("4. Adding Custom Vocabulary:")
    custom_words = ["कृष्ण", "अर्जुन", "युधिष्ठिर"]
    tokenizer.add_words_to_dictionary(custom_words)
    print(f"   Added: {custom_words}")
    print(f"   New dictionary size: {tokenizer.dictionary.size()}")
    print()
    
    # Example 4: Tokenize with new words
    print("5. Tokenizing with Custom Words:")
    text3 = "कृष्ण अर्जुन युधिष्ठिर"
    tokens3 = tokenizer.tokenize(text3)
    print(f"   Input:  {text3}")
    print(f"   Tokens: {tokens3}")
    print()
    
    # Example 5: Statistics
    print("6. Tokenizer Statistics:")
    stats = tokenizer.get_statistics()
    print(f"   Dictionary size: {stats['dictionary_size']}")
    print(f"   Sandhi enabled: {stats['sandhi_enabled']}")
    print(f"   Samasa enabled: {stats['samasa_enabled']}")
    print(f"   Sandhi rules: {stats['sandhi_rules_count']}")
    print()
    
    # Verification metrics
    vm = stats['verification_metrics']
    print(f"   Verifications performed: {vm['total_verifications']}")
    print(f"   Success rate: {vm['success_rate']:.1%}")
    print()
    
    print("=" * 70)
    print("Demo Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
