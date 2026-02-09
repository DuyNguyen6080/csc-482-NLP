import numpy as np
import math
import nltk, copy, random
nltk.download('brown')
nltk.download('treebank')
import re
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


def main():
    percentage_file = 10

    list_file_name = treebank.fileids()
    total_n_file = len(treebank.fileids())
    N_file_range = int(math.ceil((percentage_file*total_n_file)/100))

    print(f"File to read: {N_file_range}, total file: {total_n_file}")
    grammar_rules_count = {}
    total_rules = 0
    # Go through each file and get the tree
    # go through each tree to get CFG
    # go through each CFG to get each rule
    # add rule to a hasmap  key -> count++  
    target = nltk.grammar.Nonterminal('NT')
    for i in range(N_file_range):
        treebank_file = list_file_name[i]
        trees = treebank.parsed_sents(treebank_file)
        
        print(f"subtree: {len(trees[0])}")
        for each_tree in trees:
            grammar_rules = each_tree.productions()
            #print(grammar_rules)
            for rule in grammar_rules:
                rule = colapse(rule)
                
                if check_if_terminal(rule):
                    rule_rhs_tuple = rule.rhs()
                    #print(f"rule_rhs_tuple[0]: {rule_rhs_tuple[0]} type: {type(rule_rhs_tuple[0])}" )
                    if not isinstance(rule_rhs_tuple[0], nltk.grammar.Nonterminal):
                        target = rule.lhs()
                        replacement = nltk.grammar.Nonterminal(f'{rule.lhs().symbol()}-{rule.rhs()[0]}')
                        #print(f"replacecing {rule} with {replacement}")
                        #grammar_rules_count = substitude(grammar_rules_count, target, replacement)
                        #print(f"sub grammar rule dict: {substitude(grammar_rules_count, target, replacement)}")
                        continue
                #if check_terminal(rule) 
                if rule in grammar_rules_count:
                    grammar_rules_count[rule] += 1
                else:
                    grammar_rules_count[rule] = 1
                total_rules += 1

            
    print(f"REDUCED_total_rules: {total_rules}")
    print(f"REDUCED_lenth grammar: {len(grammar_rules_count)}")
    print(f"REDUCED_grammar_rules_count: \n{grammar_rules_count}")
    for each_count in grammar_rules_count:
        grammar_rules_count[each_count] = grammar_rules_count[each_count] / total_rules
        
    print (f"REDUCED_PCFG: \n{grammar_rules_count}")


if __name__ == "__main__":
    main()