"""
build_pcfg_reduced.py

Construct a REDUCED PCFG from the Penn Treebank 10% sample.
Labels are normalized to vanilla PTB categories.
"""

import nltk
from nltk.corpus import treebank
from collections import defaultdict
import re


# --------------------------------------------------
# Label normalization
# --------------------------------------------------

def normalize_label(label):
    """
    Convert a PTB label to a reduced 'vanilla' version.
    """
    # Remove functional suffixes: NP-SBJ, VP-TMP, etc.
    label = re.split(r"[-_^]", label)[0]

    # Collapse POS families
    if label.startswith("VB"):
        return "VB"
    if label.startswith("NN"):
        return "NN"
    if label.startswith("JJ"):
        return "JJ"
    if label.startswith("RB"):
        return "RB"

    return label


# --------------------------------------------------
# Load Treebank sample
# --------------------------------------------------

def load_treebank_sample(sample_ratio=0.1):
    trees = treebank.parsed_sents()
    sample_size = int(len(trees) * sample_ratio)
    return trees[:sample_size]


# --------------------------------------------------
# Extract and normalize productions
# --------------------------------------------------

def extract_reduced_productions(trees):
    """
    Extract productions and normalize all symbols.
    """
    reduced_productions = []

    for tree in trees:
        for prod in tree.productions():
            lhs = normalize_label(str(prod.lhs()))
            rhs = tuple(normalize_label(str(sym)) for sym in prod.rhs())
            reduced_productions.append((lhs, rhs))

    return reduced_productions


# --------------------------------------------------
# Count productions
# --------------------------------------------------

def count_productions(productions):
    rule_counts = defaultdict(int)
    lhs_counts = defaultdict(int)

    for lhs, rhs in productions:
        rule_counts[(lhs, rhs)] += 1
        lhs_counts[lhs] += 1

    return rule_counts, lhs_counts


# --------------------------------------------------
# Compute PCFG probabilities
# --------------------------------------------------

def compute_pcfg(rule_counts, lhs_counts):
    pcfg_rules = []
    for (lhs, rhs), count in rule_counts.items():
        prob = count / lhs_counts[lhs]
        pcfg_rules.append((lhs, rhs, prob))
    return pcfg_rules


# --------------------------------------------------
# Print phrase-structure rules only
# --------------------------------------------------

def print_phrase_rules(pcfg_rules):
    """
    Print only NT -> NT* rules (ignore lexicon).
    """
    for lhs, rhs, prob in sorted(pcfg_rules):
        if all(sym.isupper() for sym in rhs):
            rhs_str = " ".join(rhs)
            print(f"{lhs} -> {rhs_str} [{prob:.6f}]")


# --------------------------------------------------
# Write grammar to file
# --------------------------------------------------

def write_pcfg(pcfg_rules, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for lhs, rhs, prob in sorted(pcfg_rules):
            rhs_str = " ".join(rhs)
            f.write(f"{lhs} -> {rhs_str} [{prob:.6f}]\n")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():
    print("Loading Penn Treebank 10% sample...")
    trees = load_treebank_sample()

    print("Extracting and normalizing productions...")
    productions = extract_reduced_productions(trees)

    print("Counting productions...")
    rule_counts, lhs_counts = count_productions(productions)

    print("Computing reduced PCFG...")
    pcfg_rules = compute_pcfg(rule_counts, lhs_counts)

    print("\n===== REDUCED PCFG (PHRASE RULES ONLY) =====\n")
    print_phrase_rules(pcfg_rules)

    print("\nWriting reduced PCFG to file...")
    write_pcfg(pcfg_rules, "pcfg_reduced.txt")

    print("\nDone.")
    print(f"Total reduced rules: {len(pcfg_rules)}")


if __name__ == "__main__":
    nltk.download("treebank")
    main()
