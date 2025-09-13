from django import template
from markdown import Markdown
from django.utils.safestring import mark_safe


register = template.Library()
html_text_input_types = [
    "text",               # Champ de texte simple pour une ligne de texte
    "password",           # Champ de texte masqué pour les mots de passe
    "email",              # Champ pour entrer une adresse email
    "url",                # Champ pour entrer une URL
    "tel",                # Champ pour entrer un numéro de téléphone
    "textarea"            # Champ de texte multi-lignes pour entrer de grandes quantités de texte
]


### Source : https://www.geeksforgeeks.org/python/python-program-to-convert-integer-to-roman/
@register.filter(name="roman_convert")
def roman_convert(num:int=0):
    if num is None:
        return

    # Storing roman values of digits from 0-9
    # when placed at different places
    m = ["", "M", "MM", "MMM"]
    c = ["", "C", "CC", "CCC", "CD", "D",
         "DC", "DCC", "DCCC", "CM "]
    x = ["", "X", "XX", "XXX", "XL", "L",
         "LX", "LXX", "LXXX", "XC"]
    i = ["", "I", "II", "III", "IV", "V",
         "VI", "VII", "VIII", "IX"]

    # Converting to roman
    thousands = m[num // 1000]
    hundreds = c[(num % 1000) // 100]
    tens = x[(num % 100) // 10]
    ones = i[num % 10]

    ans = (thousands + hundreds +
           tens + ones)

    return ans


@register.filter(name="to_markdown")
def to_markdown(value):
    md = Markdown(extensions=["extra","fenced_code", "codehilite","mdx_math"])
    return mark_safe(md.convert(value))

@register.filter(name="get_ctx_field")
def get_ctx_field(value):
    return value.field.widget.get_context(name=value.name,value=value.value(),attrs=value.field.widget.attrs).get("widget")

@register.filter(name="is_writable")
def is_writable(value):
    if value in html_text_input_types:
        return "input"
    return value

@register.filter(name="placeholder")
def placeholder(value):
    return value.field.widget.attrs.get("placeholder","")