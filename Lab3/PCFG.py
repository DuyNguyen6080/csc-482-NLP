import numpy as np
import math
import nltk, copy, random
nltk.download('brown')
nltk.download('treebank')
from nltk.corpus import treebank
import pprint

grammar = nltk.CFG.fromstring(""" S -> NP VP 
PP -> P NP 
NP -> 'the' N | N PP | 'the' N PP 
VP -> V NP | V PP | V NP PP 
N -> 'cat' 
N -> 'dog' 
N -> 'rug' 
V -> 'chased' 
V -> 'sat' 
P -> 'in' 
P -> 'on' 
""")
#print(grammar)
def main():
    percentage_file = 10;

    list_file_name = treebank.fileids()
    total_n_file = len(treebank.fileids())
    N_file_range = int(math.ceil((percentage_file*total_n_file)/100))

    print(f"File to read: {N_file_range}, total file: {total_n_file}")
    grammar_rules_count = {}
    total_rules = 0
    # Go through each file and get the grammar rules
    # each
    for i in range(N_file_range):
        treebank_file = list_file_name[i]
        trees = treebank.parsed_sents(treebank_file)
        for each_tree in trees:
            grammar_rules = each_tree.productions()
            #print(grammar_rules)
            for rule in grammar_rules:
                if rule in grammar_rules_count:
                    #print(f"Exists RULE: {rule}")
                    grammar_rules_count[rule] += 1
                
                else:
                    #print(f"non Exists RULE: {rule}")
                    grammar_rules_count[rule] = 1
                total_rules += 1

            #print(sentence_tree.productions())            
        #print(f"reading file: {list_file_name[i]}")
    print(f"total_rules: {total_rules}")
    print(f"lenth grammar: {len(grammar_rules_count)}")
    old = grammar_rules_count.copy
    
    for each_count in grammar_rules_count:
        grammar_rules_count[each_count] = grammar_rules_count[each_count] / total_rules
        #print(each_count, grammar_rules_count[each_count])
    pprint.pprint (grammar_rules_count, indent= 4)
    pprint.pprint(old, indent=4)


if __name__ == "__main__":
    main()