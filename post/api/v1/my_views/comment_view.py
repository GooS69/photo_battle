from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView

from post.api.utils.service_outcome import ServiceOutcome
from post.api.v1.my_serializers.comment_serializers import CreateCommentSerializer, CommentSerializer
from post.api.v1.services.comment.create import CommentCreateService


class CreateComment(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    @swagger_auto_schema(request_body=CreateCommentSerializer,
                         responses={201: 'ok'})
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(CommentCreateService, {'user': request.user,
                                                        'text': request.data.get('text'),
                                                        'content_type': request.data.get('content_type'),
                                                        'object_id': request.data.get('object_id')})
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)
