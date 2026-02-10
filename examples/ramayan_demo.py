"""
Example: Loading and Tokenizing Ramayan Data

Demonstrates integration with your authentic Vedic JSON datasets.
"""

from pathlib import Path
from vedic_tokenizer import VedicZeroTokenizer


def main():
    print("=" * 70)
    print("Ramayan Tokenization Demo")
    print("=" * 70)
    print()
    
    # Initialize tokenizer
    tokenizer = VedicZeroTokenizer()
    
    # Path to your Ramayan data
    # This path goes up one level from vedic-tokenizer directory
    ramayan_file = Path("d:/projects/automated-content-creator/data/1_बाल_काण्ड_data.json")
    
    print(f"1. Loading Ramayan dictionary from:")
    print(f"   {ramayan_file}")
    print()
    
    if ramayan_file.exists():
        # Load dictionary from JSON
        tokenizer.load_dictionary_from_json(
            str(ramayan_file),
            text_field="content",
            extract_words=True
        )
        
        print(f"✓ Dictionary loaded successfully!")
        print(f"   Dictionary size: {tokenizer.dictionary.size()} words")
        print()
        
        # Example verses to tokenize (from Ramayan)
        verses = [
            "वर्णानामर्थसंघानां रसानां छन्दसामपि",
            "मङ्गलानां च कर्त्तारौ वन्दे वाणीविनायकौ",
            "भवानीशङ्करौ वन्दे श्रद्धाविश्वासरूपिणौ"
        ]
        
        print("2. Tokenizing Ramayan verses:")
        print()
        
        for i, verse in enumerate(verses, 1):
            print(f"   Verse {i}:")
            print(f"   Input:  {verse}")
            
            # Tokenize
            tokens = tokenizer.tokenize(verse)
            print(f"   Tokens: {tokens}")
            
            # Verify
            is_valid, metrics = tokenizer.verify_integrity(verse, tokens)
            print(f"   ✓ Lossless: {is_valid}")
            print(f"   Accuracy: {metrics['character_accuracy']:.2%}")
            print()
        
        # Show statistics
        print("3. Final Statistics:")
        stats = tokenizer.get_statistics()
        vm = stats['verification_metrics']
        print(f"   Total verifications: {vm['total_verifications']}")
        print(f"   Success rate: {vm['success_rate']:.1%}")
        print()
        
    else:
        print(f"⚠ Ramayan file not found at:")
        print(f"   {ramayan_file}")
        print()
        print("Please adjust the path to match your data location.")
        print()
        print("Using mock dictionary instead...")
        print()
        
        # Demo with mock data
        verse = "राम सीता लक्ष्मण हनुमान्"
        print(f"Input:  {verse}")
        tokens = tokenizer.tokenize(verse)
        print(f"Tokens: {tokens}")
        print()
    
    print("=" * 70)


if __name__ == "__main__":
    main()
