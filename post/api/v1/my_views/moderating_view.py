from drf_yasg.utils import swagger_auto_schema

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from post.api.utils.service_outcome import ServiceOutcome
from post.api.v1.services.moderating.change_status import ChangePostStatusService


class ChangePostStatus(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(responses={200: 'ok'})
    def patch(self, request, *args, **kwargs):
        print(request.data.get('status'))
        outcome = ServiceOutcome(ChangePostStatusService, {'post_id': kwargs['pk'], 'status': request.data.get('status')})
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
