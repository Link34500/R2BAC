from django import template

register = template.Library()
html_text_input_types = [
    "text",               # Champ de texte simple pour une ligne de texte
    "password",           # Champ de texte masqué pour les mots de passe
    "email",              # Champ pour entrer une adresse email
    "url",                # Champ pour entrer une URL
    "tel",                # Champ pour entrer un numéro de téléphone
    "textarea"            # Champ de texte multi-lignes pour entrer de grandes quantités de texte
]



@register.filter(name="is_writable")
def is_writable(value):
    if value in html_text_input_types:
        return "input"
    return value

@register.filter(name="placeholder")
def placeholder(value):
    return value.field.widget.attrs.get("placeholder","")