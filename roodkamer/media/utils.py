# -*- coding: utf-8 -*-
'''Helper utilities and decorators, specifically for media.'''
from roodkamer.media.models import Article


def article_viewdb_generate(arts):
    articles = []
    for art in arts:
        article = {}
        article["title"] = art.title
        article["authors"] = ", ".join([t.username for t in art.authors])
        article["authors_ids"] = [t.id for t in art.authors]
        article["category"] = art.category
        article["tags"] = ", ".join([t.name for t in art.subject_tags])
        article["published"] = art.is_visible
        article["timestamp"] = art.created_at.ctime()
        articles.append((article, art.id))
    return articles
