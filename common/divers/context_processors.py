from common.settings import CONTEXTS

def contexts(*args):
    context = {}
    for name,value in CONTEXTS.items():
        context.update({name:value})
    return context