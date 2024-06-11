from django.urls import path, include
from rest_framework import routers

from .views import *
from .custom_views.auth import *
from .custom_views.departments import *
from .custom_views.accounts import *
from .custom_views.cdr_columns import *
from .custom_views.clusters import *
from .custom_views.comparision import *
from .custom_views.users import *
from .custom_views.jobreport import *

router = routers.DefaultRouter()
router.register('cases', CaseViewSet)
router.register('zones', ZoneViewSet)
router.register('poi', PoiViewSet)
router.register('jobs', JobViewSet)
router.register('linkeddatarecords', LinkedDataRecordsViewSet)
router.register('linkedcdrrecords', LinkedDataCallDetailRecordViewSet)
router.register('groups', GroupViewSet)
router.register('handset_history', HandsetHistoryViewSet)
router.register('cdr', CallDetailRecordViewSet)
router.register('linktree', LinkTreeViewSet)

urlpatterns = [
    # Auth
    path('api/auth/', CustomAuth.as_view()),
    # Users
    path('api/users/', UsersList.as_view()),
    # Accounts
    path('api/accounts/', AccountsList.as_view()),
    path('api/accounts/<int:pk>/', AccountDetail.as_view()),
    # Departments
    path('api/departments/', DepartmentList.as_view()),
    path('api/departments/<int:pk>/', DepartmentDetail.as_view()),
    # CallDetailRecord columns
    path('api/cdr/columns/', CdrColumns.as_view()),
    # Clustering
    path('api/clusters/', ClusterView.as_view()),
    # CDR comparision
    path('api/cdr_comparision/', ComparisionView.as_view()),
    # General CRUD
    path('api/', include(router.urls)),
    path('resetpassword/', ResetPasswordView.as_view()),
    path('adminreset/', AdminResetPassword.as_view()),
    path('api/linktreexpand/', ProxyView.as_view()),
    path('towers/', CellTowerDataViewSet.as_view()),
    path('api/linked/msisdns/', LinkedMSISDNs.as_view()),
    path('api/linked/cellId/', UsingCellID.as_view()),
    path('api/reports/', WeeklyReportGenerator.as_view()),
    path('api/jobreport/',JobReport.as_view()),
    path('api/jobdetails/',JobDetails.as_view()),
    path('api/jobcancel/',JobUpdate.as_view()),
    path('api/getUser/',GetUserDetails.as_view()),
]
