import sys
import re
import nltk
from nltk.corpus import cmudict
import syllables

# Load CMU Pronouncing Dictionary
CMU_DICT = cmudict.dict()


# -----------------------------
# Text preprocessing functions
# -----------------------------

def tokenize_sentences(text):
    return re.split(r'[.!?]+', text)


def tokenize_words(text):
    return re.findall(r"[a-zA-Z']+", text.lower())


def count_syllables(word):
    """
    Count syllables using CMU dictionary.
    If word is not found, fall back to syllables library.
    """
    if word in CMU_DICT:
        pronunciations = CMU_DICT[word]
        # Count vowel phonemes (digits indicate stress)
        return min(
            sum(1 for phoneme in pron if phoneme[-1].isdigit())
            for pron in pronunciations
        )
    else:
        return syllables.estimate(word)


def count_total_syllables(words):
    return sum(count_syllables(word) for word in words)


def count_complex_words(words):
    """
    Complex words: words with 3 or more syllables
    (excluding proper nouns and common suffix rules ignored per assignment)
    """
    return sum(1 for word in words if count_syllables(word) >= 3)


# -----------------------------
# Readability metrics
# -----------------------------

def flesch_kincaid_grade(words, sentences, syllables_count):
    return (
        0.39 * (len(words) / sentences)
        + 11.8 * (syllables_count / len(words))
        - 15.59
    )


def gunning_fog_index(words, sentences, complex_words):
    return 0.4 * (
        (len(words) / sentences)
        + 100 * (complex_words / len(words))
    )


def load_dale_chall_wordlist(filepath):
    with open(filepath, 'r') as f:
        return set(word.strip().lower() for word in f if word.strip())


def dale_chall_readability(words, sentences, easy_words):
    difficult_words = sum(1 for word in words if word not in easy_words)
    percent_difficult = (difficult_words / len(words)) * 100

    score = (
        0.1579 * percent_difficult
        + 0.0496 * (len(words) / sentences)
    )

    if percent_difficult > 5:
        score += 3.6365

    return score


# -----------------------------
# Main program
# -----------------------------

def main():
    if len(sys.argv) != 2:
        print("Usage: python readability.py <textfile>")
        sys.exit(1)

    textfile = sys.argv[1]

    with open(textfile, 'r', encoding='utf-8') as f:
        text = f.read()

    sentences = tokenize_sentences(text)
    sentences = [s for s in sentences if s.strip()]
    sentence_count = len(sentences)

    words = tokenize_words(text)
    word_count = len(words)

    syllable_count = count_total_syllables(words)
    complex_word_count = count_complex_words(words)

    dale_chall_words = load_dale_chall_wordlist("dalechall.txt")

    fk_grade = flesch_kincaid_grade(words, sentence_count, syllable_count)
    dc_grade = dale_chall_readability(words, sentence_count, dale_chall_words)
    gf_index = gunning_fog_index(words, sentence_count, complex_word_count)

    print(f"Flesch-Kincade Grade Level: {fk_grade:.2f}")
    print(f"Dale-Chall Readability: {dc_grade:.2f}")
    print(f"Gunning-Fog Index: {gf_index:.2f}")


if __name__ == "__main__":
    main()
