
import nltk
nltk.download('wordnet')
import re
#nltk.download('omw-1.4')
import math
import sys
import math
from nltk.corpus import wordnet as wn


def is_concept(arg):
    return arg.count('.') == 2

def get_synset(arg):
    if is_concept(arg):
        return wn.synset(arg)
    synsets = wn.synsets(arg, pos=wn.NOUN)
    if not synsets:
        raise ValueError(f"No noun synsets for {arg}")
    return synsets[0]

def get_all_hypernym(c):
    if not c:
        return set()
    
    result = set()
    for hyp in c.hypernyms():
        result.add(hyp)
        result.update(get_all_hypernym(hyp))
    return result

def LCS(c1, c2):
    all_hyper1 = get_all_hypernym(c1)
    all_hyper2 = get_all_hypernym(c2)
    
    # Add the concepts themselves
    all_hyper1.add(c1)
    all_hyper2.add(c2)
    
    # Find all common hypernyms
    common = all_hyper1 & all_hyper2
    
    if not common:
        return None
    
    # Return the deepest one (most specific)
    return max(common, key=lambda s: s.min_depth())
def get_top(c):
    hyper = c.hypernyms()
    #print(c, len(hyper))
    if len(hyper) == 0:
        #print("return ",c)
        return c
    if len(hyper) > 0:
        return get_top(hyper[0])

def count_concept(c,synset_set):
   
    count = 0
    for lemma in c.lemmas():
        #print(f"{lemma}: {lemma.count()}")
        count += lemma.count() +1  # +1 smoothing
    for hypo in c.hyponyms():
        if hypo not in synset_set:
            #print(f"Not repeat: {c}")
            synset_set.add(hypo)
            count += count_concept(hypo, synset_set)
        #else:
            #print(f"repeated {c}")
    return count
def P_concept(c):
    synset_set = set()
    top_concept = get_top(c)
    
    total_concept = count_concept(top_concept,synset_set)
    #print(f"counting {c}")
    synset_set = set() # reset the set to empty
    count_c = count_concept(c,synset_set)
    #print(f"top concept: {top_concept}, count {top_concept}: {total_concept}")
    #print("total count: ", total_concept)
    #print(f"concept {c} count: ", count_c)
    
    return count_c/total_concept
def pathlen(c1, c2):
    """
    Shortest path length between two synsets (manual BFS).
    """
    visited = set()
    queue = [(c1, 0)]
    if c1 == c2:
        return 1
    while queue:
        current, dist = queue.pop(0)
        if current == c2:
            return dist
        visited.add(current)
        neighbors = current.hypernyms() + current.hyponyms()
        for n in neighbors:
            if n not in visited:
                queue.append((n, dist + 1))

    return None
def n_gram(gloss_tokens, n, match_tokens):
    result = []
    for i in range(len(gloss_tokens) - n + 1):

        result.append(gloss_tokens[i:i+n])
            #print(f"gloss_token count: {gloss_tokens[i:i+n]}")

        
    return result
def overlap_score(gloss1, gloss2):
    # Tokenize and normalize the glosses
    tokens1 = gloss1.lower().split()
    tokens2 = gloss2.lower().split()
    
    # Track which tokens have been matched
    matched1 = set()
    matched2 = set()
    
    total_score = 0
    
    # Start from the maximum possible n-gram size down to 1
    max_n = min(len(tokens1), len(tokens2))
    
    for n in range(max_n, 0, -1):
        # Generate n-grams for both glosses that haven't been fully matched
        ngrams1 = {}
        for i in range(len(tokens1) - n + 1):
            # Check if any token in this n-gram was already matched
            if not any(idx in matched1 for idx in range(i, i + n)):
                ngram = tuple(tokens1[i:i + n])
                if ngram not in ngrams1:
                    ngrams1[ngram] = []
                ngrams1[ngram].append(i)
        
        ngrams2 = {}
        for i in range(len(tokens2) - n + 1):
            # Check if any token in this n-gram was already matched
            if not any(idx in matched2 for idx in range(i, i + n)):
                ngram = tuple(tokens2[i:i + n])
                if ngram not in ngrams2:
                    ngrams2[ngram] = []
                ngrams2[ngram].append(i)
        
        # Find matching n-grams
        #print(f"{n}_gram")
        #print(f"ngram1: {ngrams1}")
        #print(f"ngram2: {ngrams2}\n")
        for ngram in ngrams1:
            if ngram in ngrams2:
                # Match found - use first available position from each
                pos1 = ngrams1[ngram][0]
                pos2 = ngrams2[ngram][0]
                
                # Mark these positions as matched
                for idx in range(pos1, pos1 + n):
                    matched1.add(idx)
                for idx in range(pos2, pos2 + n):
                    matched2.add(idx)
                #print(f"match1: {matched1}")
                #print(f"match1: {matched1}")
                # Add to score (you can weight by n if desired)
                total_score += n ** 2
                
                # Remove this ngram from further consideration
                del ngrams2[ngram]
                #print(f"after del: \nngram1: {ngrams1} \nngram2:{ngrams2}")
    
    return total_score


#
def main():
    if len(sys.argv) != 3:
        print("Usage: python similarity.py <arg1> <arg2>")
        sys.exit(1)

    c1 = get_synset(sys.argv[1])
    c2 = get_synset(sys.argv[2])
    #print(c1)
    #print(c2)
    print("sim path: ", 1/pathlen(c1,c2))
    
    least_common = LCS(c1, c2)
    #print("LCS: ", least_common )
    #print(f"P_Concept: {c1}: ", P_concept(c1))
    #print(c1.definition())
    #print(c2.definition())
    #print(overlap_score("a dog comma can not read the he is not human","A dog dot can not quack then he is not human"))
    #overlap_score(c1.definition(),c2.definition())
    #print(get_hypo_and_hyper_gloss(c1))
    print("sim Resnik", -math.log(P_concept(least_common)))
    
    Lin_numerator = (2 * math.log(P_concept(least_common)))
    Lin_denomerator = math.log(P_concept(c1)) + math.log(P_concept(c2))
    print("sim Lin", Lin_numerator/Lin_denomerator)
    
    JC_denomerator = 2 * (math.log(P_concept(least_common)) - (math.log(P_concept(c1)) + math.log(P_concept(c2))))
    print(f"JC_sim: {1/JC_denomerator}")
    
    c1_hypernyms = c1.hypernyms()
    c2_hypernyms = c2.hypernyms()
    
    c1_hyponyms = c1.hyponyms()
    c2_hyponyms = c2.hyponyms()

    c1_hyper_def = []
    c2_hyper_def = []

    c1_hypo_def = []
    c2_hypo_def = []

    all_c1_def = []
    all_c2_def = []
    for hyper in c1_hypernyms:
        all_c1_def.append(hyper.definition())
    for hyper in c2_hypernyms:
        all_c2_def.append(hyper.definition())
    for hypo in c1_hyponyms:
        all_c1_def.append(hypo.definition())
    for hypo in c2_hyponyms:
        all_c2_def.append(hypo.definition())
    all_c1_def.append(c1.definition())
    all_c2_def.append(c2.definition())
    Lesk_score = 0
    for c1_definition in all_c1_def:
        for c2_definition in all_c2_def:
            Lesk_score += overlap_score(c1_definition, c2_definition)

    print(f"sim eLesk: {Lesk_score}")

if __name__ == "__main__":
    main()