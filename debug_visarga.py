
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vedic_tokenizer.sandhi_rules import ALL_SANDHI_RULES

def debug_visarga():
    vis01 = next(r for r in ALL_SANDHI_RULES if r.rule_id == "VIS01")
    vis08 = next(r for r in ALL_SANDHI_RULES if r.rule_id == "VIS08")
    vis05 = next(r for r in ALL_SANDHI_RULES if r.rule_id == "VIS05")
    
    print("--- VIS01 ---")
    print(f"Rule: {vis01}")
    print(f"Left Pattern: '{vis01.left_pattern}' (Len: {len(vis01.left_pattern)})")
    for l, r, e in vis01.examples:
        res = vis01.apply_forward(l, r)
        print(f"Apply('{l}', '{r}') -> '{res}' (Expected '{e}')")
        
    print("\n--- VIS08 ---")
    print(f"Rule: {vis08}")
    print(f"Left Pattern: '{vis08.left_pattern}' (Len: {len(vis08.left_pattern)})")
    for l, r, e in vis08.examples:
        res = vis08.apply_forward(l, r)
        print(f"Apply('{l}', '{r}') -> '{res}' (Expected '{e}')")

    print("\n--- VIS05 ---")
    print(f"Rule: {vis05}")
    for l, r, e in vis05.examples:
        res = vis05.apply_forward(l, r)
        print(f"Apply('{l}', '{r}') -> '{res}' (Expected '{e}')")

if __name__ == "__main__":
    debug_visarga()
