import json
from django.core import serializers
from django.http import Http404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..models import Account, Department, Case, Group, UserAccountPermissions
from ..serializers import AccountSerializer, CaseOTSerializer, LocateOTSerializer, CheckOTSerializer, FenceOTSerializer, MobileOTSerializer


class AccountsList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format='json'):
        accounts = Account.objects.all().values()
        for account in accounts:
            user = User.objects.filter(id=account['user_id']).values().first()
            department = Department.objects.filter(
                id=account['department_id']).values().first()
            cases = Case.objects.filter(accounts__in=[account['id']]).exclude(
                name='DEFAULT_CASE_CHECK_OT').values()
            account['cases'] = cases
            account['department'] = department
            account['first_name'] = user['first_name']
            account['last_name'] = user['last_name']
            account['email'] = user['email']
            account['username'] = user['username']
            del account['user_id']
            del account['department_id']
            tempMap = {}
            caseOTObject = UserAccountPermissions.objects.get(pk = account['caseot_id'])
            serializedData = CaseOTSerializer(caseOTObject)
            del account['caseot_id']
            tempMap['caseot'] = serializedData.data
            locateOTObject = UserAccountPermissions.objects.get(pk = account['locateot_id'])
            serializedData = LocateOTSerializer(locateOTObject)
            del account['locateot_id']
            tempMap['locateot'] = serializedData.data
            checkOTObject = UserAccountPermissions.objects.get(pk = account['checkot_id'])
            serializedData = CheckOTSerializer(checkOTObject)
            del account['checkot_id']
            tempMap['checkot'] = serializedData.data
            fenceOTObject = UserAccountPermissions.objects.get(pk = account['fenceot_id'])
            serializedData = FenceOTSerializer(fenceOTObject)
            del account['fenceot_id']
            tempMap['fenceot'] = serializedData.data
            mobileOTObject = UserAccountPermissions.objects.get(pk = account['mobileot_id'])
            serializedData = MobileOTSerializer(mobileOTObject)
            del account['mobileot_id']
            tempMap['mobileot'] = serializedData.data
            del account['modules']
            account['modules'] = tempMap

        return Response(accounts)

    def post(self, request, format='json'):
        username = request.data['username']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        email = request.data['email']
        phone = request.data['phone']
        group_id = request.data['group']
        password = request.data['password']
        disabled = request.data['disabled']
        designation = request.data['designation']
        department_id = request.data['department']
        startDate = request.data['start_date']
        endDate = request.data['end_date']
        modules = request.data['modules']

        tempMap = modules['caseot']
        caseOTObject = UserAccountPermissions.objects.create(
            view = tempMap['view'],
            add = tempMap['add'],
            edit = tempMap['edit'],
            closecase = tempMap['closecase'],
            printcase = tempMap['printcase'],
            addzone = tempMap['addzone'],
            addpoi = tempMap['addpoi'],
            export = tempMap['export'],
            newnumber = None,
            schedule = None,
        )
        tempMap = modules['locateot']
        locateOTObject = UserAccountPermissions.objects.create(
            view = tempMap['view'],
            add = tempMap['add'],
            edit = tempMap['edit'],
            closecase = None,
            printcase = None,
            addzone = None,
            addpoi = None,
            export = None,
            newnumber = tempMap['newnumber'],
            schedule = tempMap['schedule'],
        )
        tempMap = modules['checkot']
        checkOTObject = UserAccountPermissions.objects.create(
            view = tempMap['view'],
            add = tempMap['add'],
            edit = tempMap['edit'],
            closecase = None,
            printcase = None,
            addzone = None,
            addpoi = None,
            export = tempMap['export'],
            newnumber = tempMap['newnumber'],
            schedule = tempMap['schedule'],
        )
        tempMap = modules['fenceot']
        fenceOTObject = UserAccountPermissions.objects.create(
            view = tempMap['view'],
            add = tempMap['add'],
            edit = tempMap['edit'],
            closecase = None,
            printcase = None,
            addzone = tempMap['addzone'],
            addpoi = tempMap['addpoi'],
            export = tempMap['export'],
            newnumber = None,
            schedule = None,
        )
        tempMap = modules['mobileot']
        mobileOTObject = UserAccountPermissions.objects.create(
            view = tempMap['view'],
            add = tempMap['add'],
            edit = tempMap['edit'],
            closecase = None,
            printcase = None,
            addzone = None,
            addpoi = None,
            export = None,
            newnumber = None,
            schedule = None,
        )

        group = Group.objects.get(pk=group_id)

        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.set_password(password)
        user.save()

        account = Account.objects.create(
            user=user,
            phone=phone,
            group=group,
            disabled=disabled,
            designation=designation,
            department=Department.objects.get(pk=department_id),
            caseot = caseOTObject,
            locateot = locateOTObject,
            checkot = checkOTObject,
            fenceot = fenceOTObject,
            mobileot = mobileOTObject,
            startDate=startDate,
            endDate=endDate
        )

        customResponse = {
            'id': account.id,
            'first_name': account.user.first_name,
            'last_name': account.user.last_name,
            'email': account.user.email,
            'group': Group.objects.filter(id=group_id).values().first(),
            'username': account.user.username,
            'start_date': account.startDate,
            'end_date': account.endDate,
            'disabled': account.disabled,
            'department': Department.objects.filter(id=account.department.id).values().first(),
            'designation': account.designation,
            'modules': {
                'caseot': CaseOTSerializer(caseOTObject).data,
                'locateot': LocateOTSerializer(locateOTObject).data,
                'checkot': CheckOTSerializer(checkOTObject).data,
                'fenceot': FenceOTSerializer(fenceOTObject).data,
                'mobileot': MobileOTSerializer(mobileOTObject).data,
            },
        }

        return Response(customResponse, status=status.HTTP_201_CREATED)


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer

    def get(self, request, pk, format='json'):
        account = Account.objects.get(pk=pk)
        serializedObject = AccountSerializer(account)
        tempMap = serializedObject.data
        caseOTObject = UserAccountPermissions.objects.get(pk = tempMap['caseot'])
        locateOTObject = UserAccountPermissions.objects.get(pk = tempMap['locateot'])
        checkOTObject = UserAccountPermissions.objects.get(pk = tempMap['checkot'])
        fenceOTObject = UserAccountPermissions.objects.get(pk = tempMap['fenceot'])
        mobileOTObject = UserAccountPermissions.objects.get(pk = tempMap['mobileot'])
        del tempMap['caseot']
        del tempMap['locateot']
        del tempMap['checkot']
        del tempMap['fenceot']
        del tempMap['mobileot']
        tempMap['modules'] = {
            'caseot' : CaseOTSerializer(caseOTObject).data,
            'locateot': LocateOTSerializer(locateOTObject).data,
            'checkot': CheckOTSerializer(checkOTObject).data,
            'fenceot': FenceOTSerializer(fenceOTObject).data,
            'mobileot': MobileOTSerializer(mobileOTObject).data,
        }
        print(tempMap)
        return Response(tempMap, status = status.HTTP_200_OK)

    def put(self, request, pk):
        account = Account.objects.get(pk=pk)
        username = request.data['username']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        email = request.data['email']
        phone = request.data['phone']
        group_id = request.data['group']
        disabled = request.data['disabled']
        designation = request.data['designation']
        department_id = request.data['department']
        startDate = request.data['start_date']
        endDate = request.data['end_date']
        modules = request.data['modules']

        tempMap = modules['caseot']
        caseOTObject = UserAccountPermissions.objects.filter(id = account.caseot.id).update(
            view = tempMap['view'],
            add = tempMap['add'],
            edit = tempMap['edit'],
            closecase = tempMap['closecase'],
            printcase = tempMap['printcase'],
            addzone = tempMap['addzone'],
            addpoi = tempMap['addpoi'],
            export = tempMap['export'],
            newnumber = None,
            schedule = None,
        )
        tempMap = modules['locateot']
        locateOTObject = UserAccountPermissions.objects.filter(id = account.locateot.id).update(
            view = tempMap['view'],
            add = tempMap['add'],
            edit = tempMap['edit'],
            closecase = None,
            printcase = None,
            addzone = None,
            addpoi = None,
            export = None,
            newnumber = tempMap['newnumber'],
            schedule = tempMap['schedule'],
        )
        tempMap = modules['checkot']
        checkOTObject = UserAccountPermissions.objects.filter(id = account.checkot.id).update(
            view = tempMap['view'],
            add = tempMap['add'],
            edit = tempMap['edit'],
            closecase = None,
            printcase = None,
            addzone = None,
            addpoi = None,
            export = tempMap['export'],
            newnumber = tempMap['newnumber'],
            schedule = tempMap['schedule'],
        )
        tempMap = modules['fenceot']
        fenceOTObject = UserAccountPermissions.objects.filter(id = account.fenceot.id).update(
            view = tempMap['view'],
            add = tempMap['add'],
            edit = tempMap['edit'],
            closecase = None,
            printcase = None,
            addzone = tempMap['addzone'],
            addpoi = tempMap['addpoi'],
            export = tempMap['export'],
            newnumber = None,
            schedule = None,
        )
        tempMap = modules['mobileot']
        mobileOTObject = UserAccountPermissions.objects.filter(id = account.mobileot.id).update(
            view = tempMap['view'],
            add = tempMap['add'],
            edit = tempMap['edit'],
            closecase = None,
            printcase = None,
            addzone = None,
            addpoi = None,
            export = None,
            newnumber = None,
            schedule = None,
        )

        user = User.objects.get(pk=account.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()

        account.user = user
        account.phone = phone
        account.group = Group.objects.get(pk=group_id)
        account.disabled = disabled
        account.startDate = startDate
        account.endDate = endDate
        account.designation = designation
        account.department = Department.objects.get(pk=department_id)
        account.save()



        customResponse = {
            'id': account.id,
            'first_name': account.user.first_name,
            'last_name': account.user.last_name,
            'email': account.user.email,
            'group': Group.objects.filter(id=group_id).values().first(),
            'username': account.user.username,
            'start_date': account.startDate,
            'end_date': account.endDate,
            'disabled': account.disabled,
            'department': Department.objects.filter(id=account.department.id).values().first(),
            'designation': account.designation
        }

        return Response(customResponse, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        account = Account.objects.get(pk=pk)
        account.user.delete()
        account.caseot.delete()
        account.locateot.delete()
        account.checkot.delete()
        account.fenceot.delete()
        account.mobileot.delete()
        
        return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
