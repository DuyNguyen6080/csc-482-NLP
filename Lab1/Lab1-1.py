import nltk
import sys
nltk.corpus.udhr.fileids

SUPPORTED = [
    "Afrikaans",
    "Danish",
    "Dutch",
    "English",
    "French",
    "German",
    "Indonesian",
    "Italian",
    "Spanish",
    "Swedish",
]


# Character “hints” (small bonuses). These are intentionally simple.
CHAR_BONUS = {
    "Danish": {
        "chars": ["æ", "ø", "å"],
        "common_words": ["og", "i", "det"]
    },
    "Swedish": {
        "chars": ["å", "ä", "ö"],
        "common_words": ["och", "att", "det"]
    },
    "German": {
        "chars": ["ß", "ä", "ö", "ü"],
        "common_words": ["der", "und", "ist"]
    },
    "Spanish": {
        "chars": ["ñ", "¿", "¡"],
        "common_words": ["de", "la", "que"]
    },
    "French": {
        "chars": ["ç", "é", "è", "ê", "ë", "à", "â", "î", "ï", "ô", "ù", "û", "ü", "œ"],
        "common_words": ["de", "le", "et"]
    },
    "Dutch": {
        "chars": ["ij"],
        "common_words": ["de", "en", "het"]
    },
    "Italian": {
        "chars": ["à", "è", "é", "ì", "ò", "ù"],
        "common_words": ["di", "e", "il"]
    },
    "Afrikaans": {
        "chars": ["ê", "ë", "ï", "ô", "û"],
        "common_words": ["die", "en", "is"]
    },
    "Indonesian": {
        "chars": [],
        "common_words": ["dan", "yang", "di"]
    },
    "English": {
        "chars": [],
        "common_words": ["the", "and", "of"]
    }
}
def find_language_by_char(char):
    for language, features in CHAR_BONUS.items():
        if char in features["chars"]:
            #print(char)
            return language
    return None
def find_language_by_word(word):
    for language, features in CHAR_BONUS.items():
        if word in features["common_words"]:
            #print(word)
            return language
    return None
def count_score(file_freq):
    scores = {lang: 0 for lang in SUPPORTED}
    for char, freq in file_freq.items():
        language = find_language_by_char(char)
        if language != None:
            
            scores[language] += freq
    return scores
def count_score_words(file_freq):
    scores = {lang: 0 for lang in SUPPORTED}
    for word, freq in file_freq.items():
        language = find_language_by_word(word)
        if language != None:
            
            scores[language] += freq
    return scores

def evaluate(content):
    char_freq = nltk.FreqDist(content)
    
    word_tokens = nltk.word_tokenize(content)
    clean_words_tokens = [word.lower() for word in word_tokens if word.isalpha()]
    token_freq = nltk.FreqDist(clean_words_tokens)
    char_freq = nltk.FreqDist(content)
    word_score = count_score_words(token_freq)
    char_score = count_score(char_freq)
    combined_scores = {
    key: word_score.get(key, 0) + char_score.get(key, 0)
    for key in word_score
}
    #print(combined_scores)
    language = max(combined_scores, key = combined_scores.get)
    return language
    
def main():
    if len(sys.argv) != 2:
        print("Program take 1 argument")
    else:
        filename = sys.argv[1]
        try:
            with open(filename, 'r',encoding="utf-8") as file:
                content = file.read()
                #print(content)
                language = evaluate(content)
                print(language)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except IOError:
            print(f"Error: Cannot read file '{filename}'.")
if __name__ == "__main__":
    main()