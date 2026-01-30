import random
import re
import nltk
from nltk.corpus import gutenberg
from nltk.probability import FreqDist

from nltk.tokenize import sent_tokenize

nltk.download("gutenberg")
from nltk.tokenize import RegexpTokenizer
# Choose ONE text
text_id = "bible-kjv.txt"

# -------------------------
# CHANGED: use gutenberg.words() not raw/sent_tokenize
# -------------------------
IGNORE = {"(", ")", "[", "]", "{", "}", '"'}
raw = gutenberg.raw('bible-kjv.txt')
""" token_pattern = r'\d+:\d+|[A-Za-z]+(?:\'[A-Za-z]+)?|\d+(?:\.\d+)?|[^\s]'
tokenizer = RegexpTokenizer(token_pattern)
words = tokenizer.tokenize(raw) """
sent_tok = sent_tokenize(raw)
#print(sent_tok[0])
#print(gutenberg.words(text_id))
# -------------------------
# CHANGED: build trigram FreqDist with <P> and <S> boundary tokens
# We'll treat . ? ! as sentence end markers.
# -------------------------
fd1 = FreqDist()

seq = ["<P>", "<S>"]  # start of corpus paragraph and sentence

def is_sentence_end(tok: str) -> bool:
    return tok in {".", "?", "!"} or tok.endswith((".", "?", "!"))
def is_paragraph_end(tok: str) -> bool:
    return tok.endswith((r'[\n]+'))
def is_chapter_verse(token: str) -> bool:
    """
    Returns True if token is in chapter:verse form (e.g. '3:16'), False otherwise.
    """
    if not isinstance(token, str):
        return False

    return bool(re.fullmatch(r"\d+:\d+", token))
for setence in sent_tok:
    
    
    

    if is_sentence_end(setence):
        # close sentence, start a new one
        seq.append("</S>")
        seq.append("<S>")
    if is_paragraph_end(setence):
        seq.append("</P>")
    else:
        seq.append(setence)

# add a final end marker so model can stop
seq.append("</S>")

# count trigrams
for i in range(len(seq) - 2):
    fd1[(seq[i], seq[i + 1], seq[i + 2])] += 1

#for each in fd.items():
    #print(each)
# Sentence generation (JM-style: filter + sample)
random.seed(1001)
num_paragraphs = 3
max_len_sentence = 30  # per-sentence cap to prevent runaway

for _p in range(num_paragraphs):
    n_sents = random.randint(2, 5)   # 2–5 sentences per paragraph
    paragraph_sentences = []

    for _s in range(n_sents):
        # start each sentence with hidden <S>
        # first sentence uses context (<P>, <S>), later sentences use (</S>, <S>)
        if not paragraph_sentences:
            context0, context1 = "<P>", "<S>"
        else:
            context0, context1 = "</S>", "<S>"

        sentence = []

        while len(sentence) < max_len_sentence:
            candidates = []
            counts = []

            for (w1, w2, w3), c in fd1.items():
                if w1 == context0 and w2 == context1:
                    candidates.append(w3)
                    counts.append(c)

            if not candidates:
                break

            word = random.choices(candidates, weights=counts, k=1)[0]

            # stop sentence at end token
            if word == "</P>" or word == "</S>":
                break
            
            sentence.append(word)

            # CHANGED: correct trigram context slide
            context0, context1 = context1, word
        sentence = [w for w in sentence if w not in {"<S>", "</S>"}] # remove the {"<S>", "</S>"}
        paragraph_sentences.append(" ".join(sentence))

    # print paragraph as 2–5 sentences
    
    print("\n".join(paragraph_sentences) )