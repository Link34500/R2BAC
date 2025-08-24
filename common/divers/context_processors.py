from common.settings import CONTEXTS
from django.template.context_processors import request

def contexts(*args):
    context = {}
    for name,value in CONTEXTS.items():
        context.update({name:value})
    return context