from django.urls.converters import SlugConverter

class EmptyOrSlug(SlugConverter):
    regex = '[-a-zA-Z0-9_]*'
