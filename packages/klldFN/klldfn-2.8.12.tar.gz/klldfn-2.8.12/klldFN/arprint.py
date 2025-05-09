import arabic_reshaper
from bidi.algorithm import get_display

def arprint(arabic_text):
    reshaped_arabic_text = arabic_reshaper.reshape(arabic_text)
    bidi_arabic_text = get_display(reshaped_arabic_text)
    return bidi_arabic_text