from django.contrib import admin
from .models import *

admin.site.register([UserAccountPermissions, Account, Department, Group, Zone, Poi, Case, Job,
                     HandsetHistory, CallDetailRecord, LinkedDataRecord, LinkedDataCallDetailRecord, LinkTree, CellTowerData, DailyJobReports])
