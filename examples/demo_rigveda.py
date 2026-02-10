
import json
import os
import sys
import time

# Add project root to path
# We're running from examples/ so go up one level
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from vedic_tokenizer import VedicZeroTokenizer

def run_rigveda_demo():
    print("="*60)
    print("VEDIC ZERO-ERROR TOKENIZER: RIGVEDA DEMO")
    print("="*60)
    
    # Initialize tokenizer
    print("Initializing tokenizer...")
    start_init = time.time()
    tokenizer = VedicZeroTokenizer()
    print(f"Initialization took {time.time() - start_init:.4f}s")
    
    # Load Rigveda data
    data_path = os.path.join(project_root, "data", "rigveda", "rigveda_mandala_1.json")
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}")
        return
        
    print(f"Loading data from {data_path}...")
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return
        
    print(f"Loaded {len(data)} suktas.")
    
    if not data:
        print("No data found.")
        return

    # Process first Sukta (Agni)
    sukta_1 = data[0]
    print("\n" + "="*40)
    print(f"Processing Sukta {sukta_1['sukta']} (Devata: Agni)")
    print("="*40)
    
    raw_text = sukta_1.get('text', '')
    # Split into lines/verses roughly
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    
    total_tokens = 0
    start_process = time.time()
    
    for i, line in enumerate(lines[:10]): # Process first 10 non-empty lines
        if not line: continue
        print(f"\n[Verse {i+1}] Original: {line}")
        
        # Tokenize
        try:
            tokens = tokenizer.tokenize(line)
            print(f"  Tokens: {tokens}")
            total_tokens += len(tokens)
        except Exception as e:
            print(f"  Error tokenizing: {e}")
            import traceback
            traceback.print_exc()

    duration = time.time() - start_process
    print("\n" + "="*60)
    print(f"Processing Complete.")
    print(f"Time: {duration:.4f}s")
    print(f"Total Tokens: {total_tokens}")
    if total_tokens > 0:
        print(f"Avg Time per Token: {duration/total_tokens*1000:.2f}ms")
    print("="*60)

if __name__ == "__main__":
    run_rigveda_demo()
