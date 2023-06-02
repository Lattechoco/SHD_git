import spacy
import nltk
from nltk.corpus import wordnet

nlp = spacy.load("en_core_web_sm")

def extract_command(text):
    doc = nlp(text)
    verbs = []
    objects = []
    adjectives = []
    
    # root verb 추출
    for token in doc:
        if token.head == token and token.pos_ == "VERB":
            verbs.append(token.text)
            # 유사한 동사 찾기
            # synsets = wordnet.synsets(token.text, pos=wordnet.VERB)
            # for synset in synsets:
            #     for lemma in synset.lemmas():
            #         if lemma.name() != token.text:
            #             verbs.append(lemma.name())
    
    # 목적어 추출
    for token in doc:
        if token.pos_ == "NOUN":
            objects.append(token.text)

    # 형용사 추출
    for token in doc:
        if token.pos_ == "ADJ":
            adjectives.append(token.text)

    return verbs, objects, adjectives

text = input("Command: ")
verbs, objects, adjectives = extract_command(text)

print("Verbs:", verbs)
print("Objects:", objects)
print("Adjectives:", adjectives)
