from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from post.api.v1.my_serializers.like_serializers import LikeSerializer
from post.my_models.like import Like


class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    @swagger_auto_schema(request_body=LikeSerializer, responses={201: 'ok'})
    def post(self, request, *args, **kwargs):
        like = Like.objects.create(post_id=request.data['post'], user=request.user)
        return Response()

    @swagger_auto_schema(request_body=LikeSerializer, responses={200: 'ok'})
    def delete(self, request, *args, **kwargs):
        like = Like.objects.get(post_id=request.data['post'], user=request.user)
        like.delete()
        return Response()
