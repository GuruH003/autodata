import time

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from ..models import Account, Department
from ..serializers import AccountSerializer


class CustomAuth(APIView):

    def post(self, request, format='json'):
        operation = request.data['operation']
        if operation == 'logout':
            try:
                request.user.auth_token.delete()
                return Response({'success': True}, status=status.HTTP_200_OK)
            except Exception as ex:
                return Response({'error': ex}, status=status.HTTP_400_BAD_REQUEST)

        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid username/password'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            account = Account.objects.filter(user=user).values().first()
            department = Department.objects.filter(
                id=account['department_id']).values().first()
            account['department'] = department
            account['first_name'] = user.first_name
            account['last_name'] = user.last_name
            account['email'] = user.email
            account['username'] = user.username
            token, created = Token.objects.get_or_create(user=user)
            account['token'] = token.key

            del account['user_id']
            del account['department_id']

            startDate = account['startDate']
            endDate = account['endDate']
            disabled = account['disabled']

            current_unix_timestamp = int(time.time())

            if current_unix_timestamp < endDate and disabled == False:
                return Response(account, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Account either disabled or expired'}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permissions_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        currentToken = request.headers['Authorization']
        tokenValue = currentToken.replace('Token ', '')
        tokenObject = Token.objects.get(key=tokenValue)
        userObject = tokenObject.user
        # username = request.data['username']
        username = userObject.username
        password = request.data['password']
        u = User.objects.get(username__exact=username)
        u.set_password(password)
        u.save()
        return Response({'success': 'Password Changed Successfully'}, status = status.HTTP_200_OK)

class AdminResetPassword(APIView):
    permissions_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        currentToken = request.headers['Authorization']
        tokenValue = currentToken.replace('Token ', '')
        tokenObject = Token.objects.get(key=tokenValue)
        userObject = tokenObject.user
        accountObject = Account.objects.get(user=userObject)
        print(accountObject.designation)
        if(accountObject.designation == 'Admin'):
            username = request.data['username']
            password = request.data['password']
            u = User.objects.get(username__exact=username)
            u.set_password(password)
            u.save()
            return Response({'success': 'Password Changed Successfully'}, status = status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not Authorized to perform this action'}, status = status.HTTP_401_UNAUTHORIZED)

