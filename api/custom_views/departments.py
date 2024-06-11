from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..models import Department, Account
from ..serializers import DepartmentSerializer, AccountSerializer


class DepartmentList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format='json'):
        departments = Department.objects.all().values()

        for department in departments:
            accountsInDepartment = Account.objects.filter(
                department=department['id']).values()
            department['accounts'] = accountsInDepartment

        return Response(departments)

    def post(self, request, format='json'):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

