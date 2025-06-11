from django.template import Library

register = Library()
UNSET = object()

HIGH_SIMILARITY_THRESHOLD = 0.5
LOW_SIMILARITY_THRESHOLD = 0.65

def similarity_level(similarity):
    if similarity < HIGH_SIMILARITY_THRESHOLD:
        return 'high'
    elif similarity > LOW_SIMILARITY_THRESHOLD:
        return 'low'
    else:
        return 'medium'

@register.simple_tag(takes_context=True)
def similarity_check(context, similarity, *args, **kwargs):
    if not similarity:
        return '',''
    if similarity < HIGH_SIMILARITY_THRESHOLD:
        return 'high', 'similarity-high text-black-50'
    elif similarity > LOW_SIMILARITY_THRESHOLD:
        return 'low', 'similarity-low text-black-50'
    else:
        return 'medium', 'similarity-medium text-black-50'