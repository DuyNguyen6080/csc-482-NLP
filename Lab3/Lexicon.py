import time
import matplotlib.pyplot as plt
import numpy as np
import math
import nltk, copy, random
nltk.download('brown')
nltk.download('treebank')
from collections import defaultdict
import re
import pprint
from nltk.corpus import treebank
#from nltk import Production
def colapse(rule: nltk.grammar.Production) -> nltk.grammar.Production:
    lhs = rule.lhs()
    rhs = rule.rhs()
    lhs_new_POS = nltk.grammar.Nonterminal([w for w in re.split(r'[-_^]+', lhs.symbol()) if w][0])
    rhs_new_POS = ()
    
    for each_POS in rhs:
        if isinstance( each_POS, nltk.grammar.Nonterminal):
            new_POS = (nltk.grammar.Nonterminal(re.split(r"[-_^]+",each_POS.symbol())[0]))
            
            rhs_new_POS += (new_POS,)
        else:
            rhs_new_POS += (each_POS,)
    

    if isinstance(lhs_new_POS, nltk.grammar.Nonterminal) and \
        isinstance(rhs_new_POS, tuple):
        new_production = nltk.grammar.Production(lhs_new_POS, rhs_new_POS)
    return nltk.grammar.Production(lhs_new_POS, rhs_new_POS)

def convert_lexicon(rule: nltk.grammar.Production) -> nltk.grammar.Nonterminal:
    lhs = rule.lhs()
    rhs = rule.rhs()

    if rule.is_lexical() and len(rhs) == 1 :
        s_new_nonterminal = lhs.symbol() + "-" + rhs[0]
        return nltk.grammar.Nonterminal(s_new_nonterminal)
    else:
        return None
def substitude(grammar_rules_count: dict, sub_target: nltk.grammar.Nonterminal, replacement: nltk.grammar.Nonterminal):
    new_counts = {}
    for key, value in grammar_rules_count.items():
        lhs = key.lhs()
        rhs = key.rhs()
        new_lhs = replacement if lhs == sub_target else lhs
        new_rhs = ()
        for each_rhs in rhs:
            if each_rhs == sub_target:
                new_rhs += (replacement,)
            else:
                new_rhs += (each_rhs,)
        new_rules = nltk.grammar.Production(new_lhs, new_rhs)
        new_counts[new_rules] = value
    return new_counts



def check_if_terminal(rule: nltk.grammar.Production)-> bool:
    rhs = rule.rhs()
    #print(len(rhs))
    if len(rhs) == 1 and not isinstance(rhs, nltk.grammar.Nonterminal):
        return True
    return False

def lexicalize(head: nltk.tree.tree.Tree) -> str:
    #base case if the Tree in the form of Tree(lHS RHS)
    # LHS is a string
    # RHS is a list
    tree = head
    if tree.label() == '-NONE-':
        return 'NONE'
    if len(tree) == 1 and isinstance(tree[0], str) and tree[0] != '-NONE-':
        return tree[0]
    
    for i in range(len(tree)):
        
        # Colapse node_POS into vanila
        head_value = [w for w in re.split(r'[-_^]+', tree.label()) if w][0]
       

        label = head_value
        children = [c for c in tree if isinstance(c, nltk.tree.tree.Tree)]
        head_child = None
        # Rules to be lexicalized
        #print(children)
        # =========================
        # 1. NP
        # =========================
        if label == "NP":
            # If leftmost NP
            for c in children:
                if c.label() == "NP":
                    return lexicalize(c)

            # Else if rightmost N*
            if head_child is None:
                for c in reversed(children):
                    if re.match(r"NN|NNS|NNP|NNPS", c.label()):
                        return lexicalize(c)

            # Else if rightmost JJ*
            if head_child is None:
                for c in reversed(children):
                    if re.match(r"JJ|JJR|JJS", c.label()):
                        return lexicalize(c)

            # Else rightmost child
            if isinstance(children[-1], nltk.tree.tree.Tree):
                return lexicalize(children[0])

        # =========================
        # 2. VP
        # =========================
            for c in children:
                if c.label() == "VP":
                    return lexicalize(c)

            # Prefer leftmost main verb
            if head_child is None:
                for c in children:
                    if re.match(r"VB|VBD|VBG|VBN|VBP|VBZ", c.label()):
                        return lexicalize(c)

            # Prefer modal auxiliary if no main verb
            if head_child is None:
                for c in children:
                    if c.label() == "MD":
                        return lexicalize(c)


            # Else leftmost child
            if head_child is None and children:
                return lexicalize( children[0])

        # =========================
        # 3. PP
        # =========================
        elif label == "PP":
            # Else if leftmost PP
            
            for c in children:
                if c.label() == "PP":
                    return lexicalize(c)
                    
            # If leftmost IN or TO
            if head_child is None:
                for c in children:
                    if c.label() in {"IN", "TO", "RP"}:
                        return lexicalize(c)

            

            # Else leftmost child
            if head_child is None and children:
                return lexicalize( children[0])

        # =========================
        # 4. ADJP
        # =========================
        elif label == "ADJP":
            # Prefer recursive ADJP
            for c in children:
                if c.label() == "ADJP":
                    return lexicalize(c)

            # Prefer right most adjective
            if head_child is None:
                for c in reversed(children):
                    if re.match(r"JJ|JJR|JJS", c.label()):
                        return lexicalize(c)

            # Allow adjectival participles
            if head_child is None:
                for c in reversed(children):
                    if c.label() in ("VBN", "VBG"):
                        return lexicalize(c)

            # Adverbs modify adjectives
            if head_child is None:
                for c in reversed(children):
                    if re.match(r"RB|RBR|RBS", c.label()):
                        return lexicalize(c)

                # Fallback: rightmost constituent
            if isinstance(children[-1], nltk.tree.tree.Tree):
                return lexicalize(children[-1])

        # =========================
        # 5. ADVP
        # =========================
        elif label == "ADVP":
            # Prefer recursive ADVP
            for c in children:
                if c.label() == "ADVP":
                    return lexicalize(c)

            # Prefer rightmost adverb or wh-adverb
            if head_child is None:
                for c in reversed(children):
                    if re.match(r"RB|RBR|RBS|WRB", c.label()):
                        return lexicalize(c)

            # Fallback: rightmost constituent
            if isinstance(children[-1], nltk.tree.tree.Tree):
                return lexicalize(children[-1])
        # =========================
        # 6. S
        # =========================
        elif label == "S":
            # If leftmost VP
            for c in children:
                if c.label() == "VP":
                    return lexicalize(c)

            # Else if leftmost S
            if head_child is None:
                for c in children:
                    if c.label() in ("S", "SBAR"):
                        return lexicalize(c)

            # Else leftmost child
            if head_child is None and children:
                return lexicalize(children[0])

        # =========================
        # 7. SBAR
        # =========================
        elif label == "SBAR":
           # Prefer recursive SBAR
            for c in children:
                if c.label() == "SBAR":
                    return lexicalize(c)

            # Prefer wh-phrase
            if head_child is None:
                for c in children:
                    if c.label() in ("WHNP", "WHADVP", "WHPP"):
                        return lexicalize(c)

            # Prefer complementizer
            if head_child is None:
                for c in children:
                    if c.label() == "IN":
                        return lexicalize(c)

            # Prefer embedded clause
            if head_child is None:
                for c in children:
                    if c.label() == "S":
                        return lexicalize(c)

            # Fallback: leftmost constituent
            if isinstance(children[0], nltk.tree.tree.Tree):
                return lexicalize(children[0])
        
        # =========================
        # 8. WHNP (Wh-Noun Phrase)
        # =========================
        # Headedness: RIGHT-headed
        # Rationale: wh-determiner modifies a nominal head
        if label == "WHNP":
            # Prefer recursive WHNP
            for c in children:
                if c.label() == "WHNP":
                    return lexicalize(c)

            # Prefer rightmost wh-word
            if head_child is None:
                for c in reversed(children):
                    if c.label() in ("WDT", "WP", "WP$"):
                        return lexicalize(c)

            # Prefer noun
            if head_child is None:
                for c in reversed(children):
                    if re.match(r"NN|NNS|NNP|NNPS", c.label()):
                        return lexicalize(c)

            # Fallback: rightmost constituent
            if isinstance(children[-1], nltk.tree.tree.Tree):
                return lexicalize(children[-1])
        # =========================
        # Default rule
        # =========================
        if head_child is None and children:
            return lexicalize(children[0])
        else: # if head_child and children is empty raise an error
            raise Exception(f"Can not lexicalize {head}")
def force_lexicalize_and_colapse(tree: nltk.tree.tree.Tree) -> nltk.tree.tree.Tree: #take a raw tree and return a tree with colapsed <label-headword>
    if len(tree) == 1 and isinstance(tree[0], str):
        return nltk.tree.tree.Tree(f"{tree.label()}-{tree[0]}", [tree[0]]) # if it is preterminal then return a tree with <label>-<terminal> not to children Tree
    # for each children of original tree force_lexicalize the children to get another tree with nameheadword(by calling lexicalize(head)) and return it as as new tree(s) with label contain the headwords
    # then create a new tree on previous return tree with label contain head word
    
    # Colapse node_POS into vanila
    colaps_head_value = [w for w in re.split(r'[-_^]+', tree.label()) if w][0]# colapse to vanila form
    
    head_word = lexicalize(tree)
    children_list = []
    for children in tree:
        children_list.append(force_lexicalize_and_colapse(children))

    new_POS = colaps_head_value + "-" + head_word
    new_tree = nltk.tree.tree.Tree(new_POS, children_list)

    return new_tree
def load_treebank_sample(sample_ratio=0.1):
    """
    Load a fixed 10% sample of the Penn Treebank.
    """
    trees = treebank.parsed_sents()
    sample_size = int(len(trees) * sample_ratio)
    return trees[:sample_size]

# --------------------------------------------------
# Step 4: Compute PCFG probabilities (MLE)
# --------------------------------------------------

def compute_pcfg(rule_counts, lhs_counts):
    """
    Convert rule counts to PCFG rules with probabilities.
    """
    pcfg_rules = []

    for (lhs, rhs), count in rule_counts.items():
        prob = count / lhs_counts[lhs]
        pcfg_rules.append((lhs, rhs, prob))

    return pcfg_rules
# --------------------------------------------------
# Step 2: Extract productions
# --------------------------------------------------

def extract_productions(trees):
    """
    Extract all CFG productions from a list of parse trees.
    Returns a list of nltk.Production objects.
    """
    productions = []
    for tree in trees:
        productions.extend(tree.productions())
    return productions
def count_productions(productions):
    """
    Count rule frequencies and LHS frequencies.
    """
    rule_counts = defaultdict(int)
    lhs_counts = defaultdict(int)

    for prod in productions:
        lhs = str(prod.lhs())
        rhs = tuple(str(sym) for sym in prod.rhs())

        rule_counts[(lhs, rhs)] += 1
        lhs_counts[lhs] += 1

    return rule_counts, lhs_counts
# --------------------------------------------------
# Step 5: Write PCFG to file
# --------------------------------------------------

def write_pcfg(pcfg_rules, output_path):
    """
    Write PCFG rules to a text file in standard format.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for lhs, rhs, prob in sorted(pcfg_rules):
            rhs_str = " ".join(rhs)
            f.write(f"{lhs} -> {rhs_str} [{prob:.6f}]\n")
def print_pcfg(pcfg_rules):
    """
    Print PCFG rules to stdout in standard format.
    """
    for lhs, rhs, prob in sorted(pcfg_rules):
        rhs_str = " ".join(rhs)
        print(f"{lhs} -> {rhs_str} [{prob:.6f}]")


def main():
    percentage_file = 10

    
    grammar_rules_count = {}
    total_rules = 0
    # Go through each file and get the tree
    # go through each tree to get CFG
    # go through each CFG to get each rule
    # add rule to a hasmap  key -> count++  
    trees = load_treebank_sample()
    new_lex_tree = []
    for each_tree in trees:
        #return a new tree without modify the original tree
        new_tree = force_lexicalize_and_colapse(each_tree)
        #new_tree.draw()
        new_lex_tree.append(new_tree)
    
    print("Extracting productions...")
    productions = extract_productions(new_lex_tree)
    print(new_lex_tree[0])
    temp_production = extract_productions(new_lex_tree[0])
    temp_rule_counts, temp_lhs_counts=count_productions(temp_production)
    temp_pcfg_rules = compute_pcfg(temp_rule_counts, temp_lhs_counts)
    print_pcfg(temp_pcfg_rules)
    print("Counting productions...")
    rule_counts, lhs_counts = count_productions(productions)

    print("Computing PCFG probabilities...")
    pcfg_rules = compute_pcfg(rule_counts, lhs_counts)

    #print_pcfg(pcfg_rules)
    print("Writing PCFG to file...")
    write_pcfg(pcfg_rules, "lexicalize_pcfg.txt")

   
if __name__ == "__main__":
    main()