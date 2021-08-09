from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from post.api.utils.service_outcome import ServiceOutcome
from post.api.v1.my_serializers.comment_serializers import CommentSerializer
from post.api.v1.services.comment_list.post_comments import PostCommentListService


class PostComments(APIView):

    @swagger_auto_schema(responses={200: CommentSerializer})
    def get(self, request, *args, **kwargs):

        outcome = ServiceOutcome(PostCommentListService, {'post_id': kwargs['pk']})
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return Response(CommentSerializer(outcome.result, many=True).data, status=status.HTTP_200_OK)