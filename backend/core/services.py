from datetime import datetime
import os
import redis
from dotenv import load_dotenv
from copy import copy
from django.utils import timezone
from django.db import transaction, IntegrityError
from .models import User, Blog, Post, Tag, Subscription, Like, Comment
from .utils import get_tokens, get_blogs_params, get_posts_params
from .serializers import UserSerializer, BlogSerializer, PostSerializer, SubscriptionSerializer
from .schemas import BlogModel, PostModel, BlogUpdate, PostUpdate

load_dotenv()

err_username = {'mes': 'username already exists'}
success = {'mes': 'Successfully!'}
is_not_user = {'mes': 'User is not found'}
bad_password = {'mes': 'Incorrect password'}
bad_token = {'mes': 'Token is not found'}
err_mes = {'mes': 'Some DB error'}
not_owner = {'mes': 'Not owner'}
not_rights = {'mes': 'Not enough rights'}
err_alr_ex = {'mes': 'Already exists'}


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

expiration_time_access = int(os.getenv("EXPIRATION_TIME_ACCESS"))
expiration_time_refresh = int(os.getenv("EXPIRATION_TIME_REFRESH"))

redis_instance = redis.StrictRedis(host=REDIS_HOST, port=int(REDIS_PORT))


def check_token(id, token):
    if f'{id}access' in redis_instance and token == (redis_instance.get(f'{id}access')).decode("utf-8"):
        return True
    return False


def sign_up_service(data):
    try:
        User.objects.create(**data)
    except IntegrityError:
        return err_username, 400
    return success, 200


def sign_in_service(data):
    username = data['username']
    password = data['password']
    if user := User.objects.filter(username=username).first():
        if user.password == password:
            time = int(datetime.utcnow().timestamp())
            user.last_login = time
            user.save()
            id = user.pk
            tokens = get_tokens(id, time)
            tokens['id'] = id
            redis_instance.set(f'{id}access', tokens['access_token'], expiration_time_access)
            redis_instance.set(f'{id}refresh', tokens['refresh_token'], expiration_time_refresh)
            tokens['user'] = UserSerializer(user).data
            return tokens, 200
        return bad_password, 400
    return is_not_user, 400


def refresh_service(data):
    id = data['id']
    refresh_token = data['refresh_token']
    if f'{id}refresh' in redis_instance and refresh_token == (redis_instance.get(f'{id}refresh')).decode("utf-8"):
        user = User.objects.get(pk=id)
        time = int(datetime.utcnow().timestamp())
        user.last_login = time
        user.save()
        tokens = get_tokens(id, time)
        tokens['id'] = id
        redis_instance.set(f'{id}access', tokens['access_token'], expiration_time_access)
        redis_instance.set(f'{id}refresh', tokens['refresh_token'], expiration_time_refresh)
        tokens['user'] = UserSerializer(user).data
        return tokens, 200
    return bad_token, 400


def get_blogs_service(params):
    params = get_blogs_params(params)
    limit = params['limit']
    offset = params['offset']
    sort = params['sort']
    del params['limit']
    del params['offset']
    del params['sort']
    blogs = Blog.objects.filter(**params).order_by(sort)[offset : limit + offset]
    res = BlogSerializer(blogs, many=True).data
    return res, 200


def get_posts_service(params):
    params = get_posts_params(params)
    limit = params['limit']
    offset = params['offset']
    sort = params['sort']
    tags = params['tags']
    del params['tags']
    del params['limit']
    del params['offset']
    del params['sort']
    posts = Post.objects.all()
    for i in tags:
        posts = posts & Post.objects.filter(tags__title__istartswith=i)
    posts = posts & Post.objects.filter(**params)
    posts = posts.order_by(sort)[offset : limit + offset]
    res = PostSerializer(posts, many=True).data
    return res, 200


def create_blog_service(data):
    id = data['id']
    if not check_token(id, data['token']):
        return bad_token, 400
    user = User.objects.get(pk=id)
    blog = BlogModel(**data)
    Blog.objects.create(**(blog.dict()), owner=user)
    return success, 200


def add_author_service(data):
    id = data['id']
    if not check_token(id, data['token']):
        return bad_token, 400
    owner = User.objects.get(pk=id)
    blog = Blog.objects.get(pk=data['id_blog'])
    user = User.objects.get(pk=data['id_user'])
    if blog.owner != owner:
        return not_owner, 400
    blog.authors.add(user)
    return success, 200


def create_post_service(data):
    id = data['id']
    if not check_token(id, data['token']):
        return bad_token, 400
    user = User.objects.get(pk=id)
    blog = Blog.objects.get(pk=data['id_blog'])
    if user == blog.owner or user in blog.authors.all():
        post_model = PostModel(**data)
        tags = post_model.tags
        post_model = post_model.dict()
        del post_model['tags']
        post = Post(**post_model, author=user, blog=blog)
        post.save()
        if tags is not None:
            tags = tags.split('-')
            for i in tags:
                post.tags.add(Tag.objects.filter(title=i).first())
        if post.is_published:
            post.created_at = timezone.now()
        post.save()
        return success, 200
    return not_rights, 400


def create_comment_service(data):
    id = data['id']
    if not check_token(id, data['token']):
        return bad_token, 400
    user = User.objects.get(pk=id)
    post = Post.objects.get(pk=data['id_post'])
    Comment.objects.create(body=data['body'], post=post, user=user)
    return success, 200


def create_like_service(data):
    id = data['id']
    if not check_token(id, data['token']):
        return bad_token, 400
    user = User.objects.get(pk=id)
    post = Post.objects.get(pk=data['id_post'])
    try:
        Like.objects.create(post=post, user=user)
    except IntegrityError:
        return err_alr_ex, 400
    return success, 200


def create_subscription_service(data):
    id = data['id']
    if not check_token(id, data['token']):
        return bad_token, 400
    user = User.objects.get(pk=id)
    blog = Blog.objects.get(pk=data['id_blog'])
    try:
        Subscription.objects.create(blog=blog, user=user)
    except IntegrityError:
        return err_alr_ex, 400
    return success, 200


def get_post_service(id):
    post = Post.objects.get(pk=id)
    if not post.is_published:
        return err_mes, 400
    post.views += 1
    post.save()
    res = PostSerializer(post).data
    return res, 200


def get_blog_service(id):
    blog = Blog.objects.get(pk=id)
    res = BlogSerializer(blog).data
    return res, 200


def get_posts_blog_service(id, n):
    blog = Blog.objects.get(pk=id)
    posts = Post.objects.filter(blog=blog, is_published=True).order_by('-created_at')[0:n]
    posts = PostSerializer(posts, many=True).data
    res = BlogSerializer(blog).data
    res['posts'] = posts
    return res, 200


def delete_blog_service(data):
    id = data['id']
    if not check_token(id, data['token']):
        return bad_token, 400
    blog = Blog.objects.get(pk=data['id_blog'])
    user = User.objects.get(pk=id)
    if blog.owner == user:
        blog.delete()
        return success, 200
    return not_rights, 400


def delete_post_service(data):
    id = data['id']
    if not check_token(id, data['token']):
        return bad_token, 400
    post = Post.objects.get(pk=data['id_post'])
    user = User.objects.get(pk=id)
    if post.author == user:
        post.delete()
        return success, 200
    return not_rights, 400


def get_my_subscriptions_service(data):
    id = data['id']
    if not check_token(id, data['token']):
        return bad_token, 400
    user = User.objects.get(pk=id)
    subscriptions = Subscription.objects.filter(user=user)
    res = SubscriptionSerializer(subscriptions, many=True).data
    return res, 200


def get_my_posts_service(data):
    id = data['id']
    if not check_token(id, data['token']):
        return bad_token, 400
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(author=user)
    res = PostSerializer(posts, many=True).data
    return res, 200


def update_blog_service(data):
    id = data['id']
    if not check_token(id, data['token']):
        return bad_token, 400
    user = User.objects.get(pk=id)
    blog = Blog.objects.get(pk=data['id_blog'])
    blog_update = BlogUpdate(**data).dict()
    for key, val in list(blog_update.items()):
        if val is None:
            del blog_update[key]
    if blog.owner == user:
        Blog.objects.filter(pk=data['id_blog']).update(**blog_update)
        blog = Blog.objects.get(pk=data['id_blog'])
        blog.updated_at = timezone.now()
        blog.save()
        return success, 200
    return not_rights, 400


def update_post_service(data):
    id = data['id']
    if not check_token(id, data['token']):
        return bad_token, 400
    user = User.objects.get(pk=id)
    post = Post.objects.get(pk=data['id_post'])
    post_update = PostUpdate(**data).dict()
    if post_update['tags'] is not None:
        tags = post_update['tags'].split('-')
        del post_update['tags']
        post.tags.clear()
        for i in tags:
            post.tags.add(Tag.objects.filter(title=i).first())
        post.save()
    for key, val in list(post_update.items()):
        if val is None:
            del post_update[key]
    if post.author == user:
        Post.objects.filter(pk=data['id_post']).update(**post_update)
        post = Post.objects.get(pk=data['id_post'])
        if post.is_published:
            post.created_at = timezone.now()
            post.save()
        return success, 200
    return not_rights, 400
