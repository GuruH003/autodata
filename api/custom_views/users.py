from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class UsersList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format='json'):
        users = User.objects.all().values()
        return Response(users)
