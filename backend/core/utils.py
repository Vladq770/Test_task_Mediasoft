import os
from dotenv import load_dotenv
from jwt import encode

from .schemas import BlogParams, PostParams

load_dotenv()

JWT_SECRET_KEY1 = os.getenv("JWT_SECRET_KEY1")
JWT_SECRET_KEY2 = os.getenv("JWT_SECRET_KEY2")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

get_blogs_dict = {
    'start': 'updated_at__date__gte',
    'end': 'updated_at__date__lte',
    'title': 'title__istartswith',
    'owner': 'owner__username__istartswith'
}

get_posts_dict = {
    'start': 'created_at__date__gte',
    'end': 'created_at__date__lte',
    'title': 'title__istartswith',
    'author': 'author__username__istartswith'
}

def get_tokens(id, last_login):
    token = {
        'access_token': encode({"id": id}, f"{JWT_SECRET_KEY1}{last_login}", algorithm=JWT_ALGORITHM),
        'refresh_token': encode({"id": id}, f"{JWT_SECRET_KEY2}{last_login}", algorithm=JWT_ALGORITHM)
    }
    return token


def get_blogs_params(params):
    params = BlogParams(**params).dict()
    for key, val in list(params.items()):
        if val is None:
            del params[key]
            continue
        if key in ('start', 'end', 'title', 'owner'):
            params[get_blogs_dict[key]] = val
            del params[key]
    return params


def get_posts_params(params):
    params = PostParams(**params).dict()
    if params['tags']:
        tags = params['tags'].split('-')
        params['tags'] = tags
    else:
        params['tags'] = []
    for key, val in list(params.items()):
        if val is None:
            del params[key]
            continue
        if key in ('start', 'end', 'title', 'author'):
            params[get_posts_dict[key]] = val
            del params[key]
    params['is_published'] = True
    return params
