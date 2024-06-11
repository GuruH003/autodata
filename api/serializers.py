from django.contrib.postgres import fields
from rest_framework import serializers

from .models import *


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class CaseOTSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccountPermissions
        exclude = ('newnumber', 'schedule', 'id',)


class LocateOTSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccountPermissions
        exclude = ('closecase', 'printcase', 'addzone',
                   'addpoi', 'export', 'id',)


class CheckOTSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccountPermissions
        exclude = ('closecase', 'printcase', 'addzone', 'addpoi', 'id',)


class FenceOTSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccountPermissions
        exclude = ('closecase', 'printcase', 'newnumber', 'schedule', 'id',)


class MobileOTSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccountPermissions
        exclude = ('closecase', 'printcase', 'newnumber',
                   'schedule', 'addzone', 'addpoi', 'export', 'id',)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'


class PoiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poi
        fields = '__all__'


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class HandsetHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HandsetHistory
        fields = '__all__'


class LinkTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkTree
        fields = '__all__'


class CallDetailRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallDetailRecord
        fields = '__all__'


class LinkedDataRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkedDataRecord
        fields = '__all__'


class LinkedDataCellRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkedDataCallDetailRecord
        fields = '__all__'


class CellDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CellTowerData
        fields = ('latitude', 'longitude', 'operator',
                  'lga', 'address', 'city', 'cellsite',)

class DailyJobReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyJobReports
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
     class Meta:
          model = Job
          fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = '__all__'
