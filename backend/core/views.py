from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services import *


@api_view(['POST', 'GET'])
def index(request):
    data = request.data
    print(data)
    return Response(data, 200)


@api_view(['POST'])
def sign_up(request):
    mes, code = sign_up_service(request.data)
    return Response(mes, code)


@api_view(['POST'])
def sign_in(request):
    mes, code = sign_in_service(request.data)
    return Response(mes, code)


@api_view(['POST'])
def refresh(request):
    mes, code = refresh_service(request.data)
    return Response(mes, code)


@api_view(['GET'])
def get_blogs(request):
    mes, code = get_blogs_service((request.query_params).dict())
    return Response(mes, code)


@api_view(['GET'])
def get_posts(request):
    mes, code = get_posts_service((request.query_params).dict())
    return Response(mes, code)


@api_view(['POST'])
def create_blog(request):
    mes, code = create_blog_service(request.data)
    return Response(mes, code)


@api_view(['PUT'])
def add_author(request):
    mes, code = add_author_service(request.data)
    return Response(mes, code)


@api_view(['POST'])
def create_post(request):
    mes, code = create_post_service(request.data)
    return Response(mes, code)


@api_view(['POST'])
def create_comment(request):
    mes, code = create_comment_service(request.data)
    return Response(mes, code)


@api_view(['POST'])
def create_like(request):
    mes, code = create_like_service(request.data)
    return Response(mes, code)


@api_view(['POST'])
def create_subscription(request):
    mes, code = create_subscription_service(request.data)
    return Response(mes, code)


@api_view(['GET'])
def get_post(request, id):
    mes, code = get_post_service(id)
    return Response(mes, code)


@api_view(['GET'])
def get_blog(request, id):
    mes, code = get_blog_service(id)
    return Response(mes, code)


@api_view(['GET'])
def get_posts_blog(request, id, n):
    mes, code = get_posts_blog_service(id, n)
    return Response(mes, code)


@api_view(['DELETE'])
def delete_blog(request):
    mes, code = delete_blog_service(request.data)
    return Response(mes, code)


@api_view(['DELETE'])
def delete_post(request):
    mes, code = delete_post_service(request.data)
    return Response(mes, code)


@api_view(['POST'])
def get_my_posts(request):
    mes, code = get_my_posts_service(request.data)
    return Response(mes, code)


@api_view(['POST'])
def get_my_subscriptions(request):
    mes, code = get_my_subscriptions_service(request.data)
    return Response(mes, code)


@api_view(['PUT'])
def update_post(request):
    mes, code = update_post_service(request.data)
    return Response(mes, code)


@api_view(['PUT'])
def update_blog(request):
    mes, code = update_blog_service(request.data)
    return Response(mes, code)

