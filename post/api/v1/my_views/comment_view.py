from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from post.api.utils.service_outcome import ServiceOutcome
from post.api.v1.my_serializers.comment_serializers import CreateCommentSerializer, CommentSerializer, \
    PutCommentSerializer, CommentsRequest, CommentListSerializer
from post.api.v1.services.comment.create import CreateCommentService
from post.api.v1.services.comment.delete import DeleteCommentService
from post.api.v1.services.comment.get import GetCommentService
from post.api.v1.services.comment.put import PutCommentService
from post.api.v1.services.comment.list import CommentsService
from post.utils.paginator import paginate


class CommentView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    @swagger_auto_schema(responses={200: CommentSerializer()})
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(GetCommentService, {'comment_id': kwargs['pk']})
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return Response(CommentSerializer(outcome.result).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PutCommentSerializer, responses={200: 'ok'})
    def put(self, request, *args, **kwargs):
        outcome = ServiceOutcome(PutCommentService, {'user': request.user, 'comment_id': kwargs['pk'],
                                                     'text': request.data.get('text')})
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={201: 'ok'})
    def delete(self, request, *args, **kwargs):
        outcome = ServiceOutcome(DeleteCommentService, {'user': request.user, 'comment_id': kwargs['pk']})
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class CommentsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    @swagger_auto_schema(query_serializer=CommentsRequest(), responses={200: CommentListSerializer()})
    def get(self, request, *args, **kwargs):

        outcome = ServiceOutcome(CommentsService, request.query_params.dict())
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return paginate(outcome.result, request, CommentListSerializer)

    @swagger_auto_schema(request_body=CreateCommentSerializer, responses={201: 'ok'})
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(CreateCommentService, {**{'user': request.user}, **request.data})
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)