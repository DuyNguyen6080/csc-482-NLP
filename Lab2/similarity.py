
import nltk
#nltk.download('wordnet')
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
        return None
    
    current_hypernym = c.hypernyms()
    result = []
    
    if len(current_hypernym) > 0:
        
        result.extend(current_hypernym)
        
        for hyp in current_hypernym:
            next_hyper = get_all_hypernym(hyp)
            for each in next_hyper:
                if each not in result:
                    result.append(each)
    return result

    
def LCS (c1, c2):
    all_hyper1 = get_all_hypernym(c1)
    all_hyper2 = get_all_hypernym(c2)
    
    # Add the concepts themselves
    all_hyper1.insert(0, c1)
    all_hyper2.insert(0, c2)
    
    # Find the first (nearest) common hypernym
    for hyp1 in all_hyper1:
        if hyp1 in all_hyper2:
            return hyp1  # Return the first match (most specific)
    
    return None
def get_top(c):
    hyper = c.hypernyms()
    #print(c, len(hyper))
    if len(hyper) == 0:
        #print("return ",c)
        return c
    if len(hyper) > 0:
        return get_top(hyper[0])

def count_concept(c):
   
    hyponyms = c.hyponyms()
    count = 0
    if len(hyponyms) == 0: #synset is leaf
       count += sum(lemma.count() for lemma in c.lemmas())
    if len(hyponyms) > 0:
       for hypo in hyponyms:
           count += count_concept(hypo)
    return count
def P_concept(c):
    top_concept = get_top(c)
    total_concept = count_concept(top_concept)
    count_c = count_concept(c)
    #print("total count: ", total_concept)
    #print("concept count: ", count_c)
    
    return count_c/total_concept
def pathlen(c1, c2):
    """
    Shortest path length between two synsets (manual BFS).
    """
    visited = set()
    queue = [(c1, 0)]

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
    print("LCS: ", least_common )
    #print("P_Concept: c1", P_concept(least_common))
    print("sim Resnik", -math.log(P_concept(least_common)))
    from nltk.corpus import wordnet_ic
    ic = wordnet_ic.ic('ic-brown.dat') 
    print("\treal sim Resnik: ", c1.res_similarity(c2,ic))
    Lin_numerator = (2 * math.log(P_concept(least_common)))
    Lin_denomerator = math.log(P_concept(c1)) + math.log(P_concept(c2))
    print("sim Lin", Lin_numerator/Lin_denomerator)
    print("real sim Lin: ", c1.lin_similarity(c2, ic))
    #print(f"path similarity: {path_similarity(c1, c2):.3f}")
    #print(f"Resnik: {resnik_similarity(c1, c2):.3f}")
    #print(f"Lin: {lin_similarity(c1, c2):.3f}")
    #print(f"JC: {jc_similarity(c1, c2):.3f}")
    #print(f"extended Lesk: {extended_lesk(c1, c2):.3f}")


if __name__ == "__main__":
    main()