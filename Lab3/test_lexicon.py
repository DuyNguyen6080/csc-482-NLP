import pytest
import numpy as np
import math
import nltk, copy, random
nltk.download('brown')
nltk.download('treebank')
import re
from nltk.corpus import treebank
from Lexicon import lexicalize, colapse, convert_lexicon, substitude, check_if_terminal


S = nltk.grammar.Nonterminal('S')
N, V, P, DT, NBJ, VLDS, NT, NP = nltk.grammar.nonterminals('N, V, P, DT, N-BJ, V^LDS, NT, NP')
lexicon = 'hello'

def test_colapse():
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
    ######################ENDTEST################################################
def test_convert_lexicon():
    

    
    productions = nltk.grammar.Production(N, [lexicon])
    output = convert_lexicon(productions)
    test_product = nltk.grammar.Nonterminal(f"N-{lexicon}")
    assert (output == test_product), f"output: {output} != test_prod: {test_product}"
def test_substitude():
    ###########    def substitude()  #######################   TEST
    example = {nltk.grammar.Production(S, [NP, V]) : 1, nltk.grammar.Production(NP, [NP, V]) : 1}
    target = nltk.grammar.Nonterminal('NP')
    replacment = nltk.grammar.Nonterminal(f'NP-{lexicon}')
    NP_test = nltk.grammar.Nonterminal(f'NP-{lexicon}')

    output = substitude(example,target, replacment)

    test_product = {nltk.grammar.Production(S, [NP_test, V]) : 1, nltk.grammar.Production(NP_test, [NP_test, V]) : 1}



    assert (output == test_product), f"output: {output} != test_prod: {test_product}"
def test_check_if_terminal():
    ###################################
    productions = nltk.grammar.Production(NT, ['hello'])
    assert (check_if_terminal(productions)), f"{productions} not an terminal Expect terminal"
    productions = nltk.grammar.Production(NT, [V, P])
    assert (not check_if_terminal(productions)), f"{productions} an terminal Expect non terminal"
def test_lexicalize():
    t2 = nltk.tree.tree.Tree("NP", [
    nltk.tree.tree.Tree("NP", [
        nltk.tree.tree.Tree("DT", ["the"]),
        nltk.tree.tree.Tree("NN", ["cat"])
    ]),
    nltk.tree.tree.Tree("PP", [
        nltk.tree.tree.Tree("IN", ["on"]),
        nltk.tree.tree.Tree("NP", [
            nltk.tree.tree.Tree("DT", ["the"]),
            nltk.tree.tree.Tree("NN", ["mat"])
        ])
    ])
])  
    expecting = 'cat'
    output = lexicalize(t2)
    assert(output == expecting), f"{output} != {expecting} expecting {output} == {expecting} "

