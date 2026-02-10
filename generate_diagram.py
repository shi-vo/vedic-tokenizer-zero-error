import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 14)
    ax.axis('off')

    # Styles
    box_props = dict(boxstyle='round,pad=0.5', facecolor='#e6f3ff', edgecolor='#0066cc', linewidth=1.5)
    layer_props = dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', edgecolor='#cccccc', linewidth=1, alpha=0.5)
    arrow_props = dict(arrowstyle='->', lw=1.5, color='#444444')
    
    # Layer Backgrounds
    # Layer 1: Input
    ax.add_patch(patches.FancyBboxPatch((0.5, 11.5), 11, 2, boxstyle="round,pad=0.2", fc="#f0f0f0", ec="#aaaaaa", lw=1))
    ax.text(1, 13.2, "Layer 1: Input Processing", fontsize=10, fontweight='bold', color='#555555')
    
    # Layer 2: Core
    ax.add_patch(patches.FancyBboxPatch((0.5, 5.5), 11, 5.5, boxstyle="round,pad=0.2", fc="#f0f0f0", ec="#aaaaaa", lw=1))
    ax.text(1, 10.7, "Layer 2: Multi-Candidate Generation & Morphology", fontsize=10, fontweight='bold', color='#555555')
    
    # Layer 3: Output
    ax.add_patch(patches.FancyBboxPatch((0.5, 0.5), 11, 4.5, boxstyle="round,pad=0.2", fc="#f0f0f0", ec="#aaaaaa", lw=1))
    ax.text(1, 4.7, "Layer 3: Scoring & Verification", fontsize=10, fontweight='bold', color='#555555')

    # Nodes
    
    # Layer 1
    ax.text(6, 12.5, "Input Text", ha='center', va='center', bbox=box_props, fontsize=11)
    ax.text(6, 11.8, "Normalization\n(Unicode + Accents)", ha='center', va='center', bbox=box_props, fontsize=10)
    
    # Layer 2
    ax.text(6, 10.0, "Sandhi Splitter Engine", ha='center', va='center', bbox=dict(boxstyle='round,pad=0.5', facecolor='#fff0e6', edgecolor='#cc6600'), fontsize=11)
    
    # Strategies
    strategies = ["Left-to-Right\nGreedy", "Right-to-Left\nGreedy", "Balanced\nSplitting", "No-Split\nCheck"]
    for i, strat in enumerate(strategies):
        x = 2.5 + i * 2.3
        ax.text(x, 8.5, strat, ha='center', va='center', bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor='#666666'), fontsize=9)
        # Arrow from Splitter to Strategies
        ax.annotate("", xy=(x, 8.9), xytext=(6, 9.6), arrowprops=arrow_props)
    
    # Morphology
    ax.text(4, 6.5, "Vibhakti Analyzer\n(160 Patterns)", ha='center', va='center', bbox=dict(boxstyle='round,pad=0.5', facecolor='#e6ffe6', edgecolor='#009900'), fontsize=10)
    ax.text(8, 6.5, "Pratyaya Analyzer\n(55 Patterns)", ha='center', va='center', bbox=dict(boxstyle='round,pad=0.5', facecolor='#e6ffe6', edgecolor='#009900'), fontsize=10)
    
    # Layer 3
    ax.text(6, 4.0, "Tri-Component Scorer\n(40% Rules, 30% Freq, 30% Gram)", ha='center', va='center', bbox=dict(boxstyle='round,pad=0.5', facecolor='#fff9e6', edgecolor='#e6b800'), fontsize=11)
    ax.text(6, 2.5, "Candidate Ranking", ha='center', va='center', bbox=box_props, fontsize=10)
    ax.text(6, 1.5, "Zero-Error Verifier\n(Reversibility Check)", ha='center', va='center', bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffe6e6', edgecolor='#cc0000'), fontsize=11)
    ax.text(6, 0.5, "Final Tokens", ha='center', va='center', bbox=box_props, fontsize=11)

    # Dictionary DB Side Node
    ax.add_patch(patches.FancyBboxPatch((0.5, 6), 1.5, 4, boxstyle="round,pad=0.2", fc="#eeeeee", ec="#333333", lw=1))
    ax.text(1.25, 8, "Vedic\nDB\n\n(345\nRules,\n348K\nWords)", ha='center', va='center', fontsize=9, fontweight='bold', color='#333333')

    # Connections
    # L1
    ax.annotate("", xy=(6, 12.1), xytext=(6, 12.3), arrowprops=arrow_props)
    ax.annotate("", xy=(6, 10.4), xytext=(6, 11.5), arrowprops=arrow_props)
    
    # L2
    # Strategies to Morphology
    ax.annotate("", xy=(4, 7.0), xytext=(2.5, 8.1), arrowprops=arrow_props)
    ax.annotate("", xy=(4, 7.0), xytext=(4.8, 8.1), arrowprops=arrow_props)
    ax.annotate("", xy=(8, 7.0), xytext=(7.1, 8.1), arrowprops=arrow_props)
    ax.annotate("", xy=(8, 7.0), xytext=(9.4, 8.1), arrowprops=arrow_props)
    
    # Morphology to Scorer
    ax.annotate("", xy=(6, 4.4), xytext=(4, 6.1), arrowprops=arrow_props)
    ax.annotate("", xy=(6, 4.4), xytext=(8, 6.1), arrowprops=arrow_props)
    
    # L3
    ax.annotate("", xy=(6, 2.8), xytext=(6, 3.6), arrowprops=arrow_props)
    ax.annotate("", xy=(6, 1.9), xytext=(6, 2.2), arrowprops=arrow_props)
    ax.annotate("", xy=(6, 0.8), xytext=(6, 1.2), arrowprops=arrow_props)

    plt.title("Vedic Sanskrit Tokenization System Architecture", fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('architecture_diagram.png', dpi=300, bbox_inches='tight')
    print("Diagram generated successfully as architecture_diagram.png")

if __name__ == "__main__":
    create_architecture_diagram()
