from googletrans import Translator


def detect_language(txt):
    t = Translator()
    detected = t.detect(txt)
    src_lang = detected.lang
    return src_lang


