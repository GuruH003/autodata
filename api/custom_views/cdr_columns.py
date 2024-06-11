from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..models import CallDetailRecord


class CdrColumns(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format='json'):
        cdr_fields = [f.name for f in CallDetailRecord._meta.fields]
        return Response(cdr_fields, status=status.HTTP_200_OK)
