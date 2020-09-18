from fastai2.text.all import *

# get our corpus of texts

txt = "The law prohibits all forms of forced or compulsory labor. The law prescribes penalties, including a “maximum term” of imprisonment for forced labor (between eight and 15 years)"

spacy = WordTokenizer()
toks = first(spacy([txt]))
print(coll_repr(toks, 30))