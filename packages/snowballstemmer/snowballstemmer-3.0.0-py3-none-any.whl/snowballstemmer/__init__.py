__all__ = ('language', 'stemmer')



_languages = {

}

try:
    import Stemmer
    cext_available = True
except ImportError:
    cext_available = False

def algorithms():
    if cext_available:
        return Stemmer.language()
    else:
        return list(_languages.keys())

def stemmer(lang):
    if cext_available:
        return Stemmer.Stemmer(lang)
    if lang.lower() in _languages:
        return _languages[lang.lower()]()
    else:
        raise KeyError("Stemming algorithm '%s' not found" % lang)
