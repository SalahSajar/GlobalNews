from django import template
from django.http import QueryDict

register = template.Library()


@register.filter(name='searchForExistence')
def searchForExistence(querySet, args):

    qs = QueryDict(args)

    type = qs.get('type')

    if type == "articleExistence":
        title = qs.get('title')
        source = qs.get('source')

        return any(queryItem.title.lower() == title.lower() and queryItem.source == source for queryItem in querySet)
    else:
        topic = qs.get('topic')

        return any(queryItem.topic.lower() == topic.lower() for queryItem in querySet)
