
import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vedic_tokenizer.sandhi_rules import ALL_SANDHI_RULES, SandhiRule

class TestPaniniCompliance:
    """
    Test suite to verify compliance with Panini's Ashtadhyayi rules.
    Iterates through all defined Sandhi rules and checks if:
    1. They have a Panini Sutra citation (optional but tracked).
    2. They function correctly against their provided examples.
    """

    def test_all_panini_rules(self):
        """
        Dynamic test that checks every rule with a defined Panini Sutra.
        """
        panini_rules = [r for r in ALL_SANDHI_RULES if r.panini_sutra]
        
        print(f"\nFound {len(panini_rules)} rules with Panini Sutra citations.")
        
        passed_count = 0
        failed_rules = []
        
        for rule in panini_rules:
            if not rule.examples:
                print(f"Warning: Rule {rule.rule_id} ({rule.panini_sutra}) has no examples.")
                continue
                
            rule_passed = True
            for left, right, expected in rule.examples:
                # Test forward application
                result = rule.apply_forward(left, right)
                
                # Check for direct match OR matra equivalence (for Devanagari)
                # Since apply_forward might return None if it doesn't apply (which shouldn't happen for the example)
                if result is None:
                     print(f"FAILURE: Rule {rule.rule_id} ({rule.panini_sutra}) failed to apply to {left} + {right}")
                     rule_passed = False
                     break
                
                # For string matching, we accept exact match
                if result != expected:
                    # Debug print
                    print(f"FAILURE: Rule {rule.rule_id} ({rule.panini_sutra}): {left} + {right} -> {result} (Expected: {expected})")
                    rule_passed = False
                    break
            
            if rule_passed:
                passed_count += 1
            else:
                failed_rules.append(rule)

        # Report
        print(f"\nPanini Compliance Report:")
        print(f"Total Panini-cited Rules: {len(panini_rules)}")
        print(f"Verified Passed: {passed_count}")
        print(f"Failed: {len(failed_rules)}")
        
        if failed_rules:
            pytest.fail(f"{len(failed_rules)} Panini rules failed verification: {[r.rule_id for r in failed_rules]}")

    def test_general_rule_correctness(self):
        """
        Verify that ALL rules (even without citations) pass their examples.
        This ensures general integrity of the rule logic.
        """
        failed_rules = []
        total_examples = 0
        
        for rule in ALL_SANDHI_RULES:
            if not rule.examples:
                continue
                
            for left, right, expected in rule.examples:
                total_examples += 1
                result = rule.apply_forward(left, right)
                
                if result != expected:
                    # Allow for minor matra variations if strictly equivalent, but for now expect exact
                    print(f"General Failure: Rule {rule.rule_id}: {left} + {right} -> {result} (Expected: {expected})")
                    failed_rules.append(rule.rule_id)
                    break 
        
        assert len(failed_rules) == 0, f"{len(failed_rules)} rules failed their example tests: {failed_rules[:5]}..."
