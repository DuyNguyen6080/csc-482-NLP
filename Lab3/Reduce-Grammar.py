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
###########    def Colaps()  #######################   TEST
S = nltk.grammar.Nonterminal('S')
N, V, P, DT, NBJ, VLDS = nltk.grammar.nonterminals('N, V, P, DT, N-BJ, V^LDS')
productions = nltk.grammar.Production(S, [NBJ, VLDS])
new_prod = colapse(productions)
test_product = nltk.grammar.Production(S, [N, V])

assert (new_prod == test_product), f"new_prodc: {new_prod} != test_prod: {test_product}"

productions = nltk.grammar.Production(V, ["do"])
new_prod = colapse(productions)
test_product = nltk.grammar.Production(V, ["do"])

assert (new_prod == test_product), f"new_prodc: {new_prod} != test_prod: {test_product}"

productions = nltk.grammar.Production(NBJ, [V, P])
new_prod = colapse(productions)
test_product = nltk.grammar.Production(N, [V, P])

assert (new_prod == test_product), f"new_prodc: {new_prod} != test_prod: {test_product}"

productions = nltk.grammar.Production(NBJ, [V, VLDS])
new_prod = colapse(productions)
test_product = nltk.grammar.Production(N, [V, V])

assert (new_prod == test_product), f"new_prodc: {new_prod} != test_prod: {test_product}"

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
    for i in range(N_file_range):
        treebank_file = list_file_name[i]
        trees = treebank.parsed_sents(treebank_file)
        for each_tree in trees:
            grammar_rules = each_tree.productions()
            #print(grammar_rules)
            for rule in grammar_rules:
                rule = colapse(rule)
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