from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from post.api.v1.my_serializers.like_serializers import CreateLikeSerializer, LikeSerializer
from post.api.utils.service_outcome import ServiceOutcome
from post.api.v1.services.like.create import LikeCreateService
from post.api.v1.services.like.delete import LikeDeleteService


class LikeView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(request_body=CreateLikeSerializer, responses={201: 'ok'})
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(LikeCreateService, {'user': request.user, 'post_id': request.data.get('post_id')})
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=LikeSerializer, responses={200: 'ok'})
    def delete(self, request, *args, **kwargs):
        outcome = ServiceOutcome(LikeDeleteService, {'user': request.user, 'like_id': request.data.get('like_id')})
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
