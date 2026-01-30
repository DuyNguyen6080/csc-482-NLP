import random
import nltk
from nltk.corpus import gutenberg
from nltk.probability import FreqDist

nltk.download("gutenberg")
nltk.download("punkt")

# Choose ONE text
text_ids = ["austen-emma.txt", "austen-persuasion.txt", "austen-sense.txt"]

raw = "".join(gutenberg.raw(tid) for tid in text_ids)
sentences = nltk.sent_tokenize(raw)

# Build a single FreqDist over bigrams
fd = FreqDist()
#print(sentences)
for sent in sentences:
    tokens = nltk.word_tokenize(sent.lower())
    tokens = [t for t in tokens if any(c.isalnum() for c in t)]
    if not tokens:
        continue

    tokens = ["<s>"] + tokens + ["</s>"]

    for i in range(len(tokens) - 1):
        fd[(tokens[i], tokens[i + 1])] += 1

#for each in fd.items():
    #print(each)
# Sentence generation (JM-style: filter + sample)
random.seed(42)
num_sentences = 5
max_len = 20
print("Bigram: " )
for _ in range(num_sentences):
    word = "<s>"
    sentence = []

    while word != "</s>" and len(sentence) < max_len:
        # Collect continuation counts
        candidates = []
        counts = []

        for (w1, w2), c in fd.items():
            if w1 == word:
                candidates.append(w2)
                counts.append(c)

        if not candidates:
            break

        word = random.choices(candidates, weights=counts, k=1)[0]

        if word != "</s>":
            sentence.append(word)
    
    print(" ".join(sentence))


def bigram_second_word():
    
    
    candidates = []
    counts = []

    for (w1, w2), c in fd.items():
        if w1 == "<s>":
            candidates.append(w2)
            counts.append(c)

    word = random.choices(candidates, weights=counts, k=1)[0]
    return word

print("\nTrigram: " )
fd1 = FreqDist()
#print(sentences)
for sent in sentences:
    tokens = nltk.word_tokenize(sent.lower())
    tokens = [t for t in tokens if any(c.isalnum() for c in t)]
    if not tokens:
        continue

    tokens = ["<s>"] + tokens + ["</s>"]

    for i in range(len(tokens) - 2):
        fd1[(tokens[i], tokens[i + 1], tokens[i+2])] += 1
for _ in range(num_sentences):
    first_word = "<s>"
    sentence = []
    context = ["<s>", bigram_second_word()]
    sentence = [bigram_second_word()]
    while context[1] != "</s>" and len(sentence) < max_len:
        # Collect continuation counts
        candidates = []
        counts = []

        for (w1, w2, w3), c in fd1.items():
            
            #print("comparing")
            #print((w1, w2, w3), c)
            if w1 == context[0] and w2 == context[1]:
                #print("w1: " , w1, ", w2: " , w2, ", w3: ", w3)
                #print("context[0]: " ,context[0] , ", context[1]: ",  context[1] )
                candidates.append(w3)
                counts.append(c)

        if not candidates:
            break
        #print("candicate word: ", candidates)
        word = random.choices(candidates, weights=counts, k=1)[0]
        #print("word chose: ", word)
        #print("sentence[]: ", sentence)
        if word == "</s>":
            break
        sentence.append(word)
        #print("sentence[]: ", sentence)
        context[0] = sentence[len(sentence)-2] # Second last word
        
        context[1] = sentence[len(sentence)-1] # Last word
        #print("context[0]: " ,context[0] , ", context[1]: ",  context[1] )
    print( " ".join(sentence))
