from django.shortcuts import render
from api.cron import getFileFromSSH
from rest_framework import viewsets, views, status
from rest_framework.filters import SearchFilter
from rest_framework import generics, permissions, viewsets, generics
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, APIView
from datetime import datetime, time, timedelta, date
from decimal import Decimal
from .models import *
from .serializers import *
from csb_project.pagination import CustomPagination
from django.conf import settings
from django.http import HttpResponse
import time
import paramiko
import pyarrow.parquet as pq
import numpy as np
import json
import openpyxl

class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    permission_classes = (IsAuthenticated,)
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_fields = ['case', ]


class PoiViewSet(viewsets.ModelViewSet):
    queryset = Poi.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = PoiSerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_fields = ['case', ]


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CaseSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        SearchFilter,
    )
    filterset_fields = ["accounts", "category"]
    search_fields = ["name", "description"]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = JobSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = [
        "case",
        "serverJobId",
        "status",
        "category",
        "type",
        "number",
        "num",
        "startTime",
        "endTime",
    ]


class HandsetHistoryViewSet(viewsets.ModelViewSet):
    queryset = HandsetHistory.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = HandsetHistorySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = [
        "job",
    ]


class LinkTreeViewSet(viewsets.ModelViewSet):
    queryset = LinkTree.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = LinkTreeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = [
        "job",
    ]


class CallDetailRecordViewSet(viewsets.ModelViewSet):
    queryset = CallDetailRecord.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CallDetailRecordSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = [
        "job",
    ]
    pagination_class = CustomPagination

    def get_queryset(self):
        return CallDetailRecord.objects.filter().order_by("id")


class LinkedDataRecordsViewSet(viewsets.ModelViewSet):
    queryset = LinkedDataRecord.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = LinkedDataRecordSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = [
        "job",
    ]
    pagination_class = CustomPagination

    def get_queryset(self):
        return LinkedDataRecord.objects.filter().order_by("id")


class LinkedDataCallDetailRecordViewSet(viewsets.ModelViewSet):
    queryset = LinkedDataCallDetailRecord.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = LinkedDataCellRecordSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = [
        "linkId",
        "job",
    ]
    pagination_class = CustomPagination

    def get_queryset(self):
        return LinkedDataCallDetailRecord.objects.filter().order_by("id")


class ProxyView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        hostname = settings.BIG_DATA_HOST
        port = settings.BIG_DATA_PORT
        requestBody = request.data
        paramsMap = {}
        paramsMap["type"] = requestBody["type"]
        paramsMap["number"] = requestBody["number"]
        paramsMap["startTime"] = requestBody["startTime"]
        paramsMap["endTime"] = requestBody["endTime"]
        print(requestBody)
        postURL = "http://{}:{}/ontrack-webservice/links_sync".format(hostname, port)
        # finalURL = postURL + 'type=' + type + '&number=' + str(number) + '&startTime=' + str(startTime) + '&endTime=' + str(endTime)
        response = requests.get(postURL, params=paramsMap)
        print(response)
        print(response.json())
        if response.status_code == 201:
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(
            {"error": "No Response received"}, status=status.HTTP_408_REQUEST_TIMEOUT
        )


class LinkedMSISDNs(APIView):
    permission_classes = (IsAuthenticated,)

    def getFileFromSSH(self, responseBody):
        paramiko.util.log_to_file("./paramiko.log")

        hostname = settings.BIG_DATA_HOST
        port = settings.BIG_DATA_PORT

        sftpHostname = settings.SFTP_DATA_HOST
        sftpPassword = settings.SFTP_DATA_PASSWORD
        username = settings.BIG_DATA_USERNAME
        password = settings.BIG_DATA_HOST_PASSWORD

        statusEndpoint = "http://{}:{}/ontrack-webservice/status".format(hostname, port)
        statusPayload = {"requestID": responseBody["requestID"]}
        getURL = statusEndpoint + "/?requestID=" + responseBody["requestID"]
        print(getURL)
        time.sleep(60)
        statusResponse = requests.get(getURL)
        print(statusResponse.status_code)
        print(statusResponse.json())
        if statusResponse.status_code == 201:
            print("Its 201")
            responseBody1 = statusResponse.json()
            localFilePath = "linkedmsisdn.parquet"
            outputFilePath = responseBody1["outputFile"]
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(sftpHostname, username=username, password=sftpPassword)
            sftp = ssh.open_sftp()
            sftp.get(outputFilePath, localFilePath)
            df = pq.read_table(source="linkedmsisdn.parquet").to_pandas()
            df.columns = map(str.lower, df.columns)
            print(df.columns)
            str_df = df.select_dtypes([np.object])
            print(str_df)
            # str_df = str_df.stack().str.decode('utf-8').unstack()
            for col in str_df:
                df[col] = str_df[col]

            print(df["number"])
            # return_object = {"number": df["number"]}
            return_object = {"df": df}
            return return_object
        else:
            return Response(
                {"error": "No Response received"},
                status=status.HTTP_408_REQUEST_TIMEOUT,
            )

    def post(self, request, *args, **kwargs):
        requestBody = request.data
        paramsMap = {}
        paramsMap["type"] = requestBody["type"]
        paramsMap["numbers"] = requestBody["numbers"]
        paramsMap["startTime"] = requestBody["startTime"]
        paramsMap["endTime"] = requestBody["endTime"]
        print(requestBody)
        postURL = (
            "http://10.0.5.162:8011/ontrack-webservice/linked_msisdns_using_msisdns"
        )
        response = requests.get(postURL, params=paramsMap)
        print(response)
        print(response.json())
        res = response.json()
        print("Getting file from SSH...")
        final_response = self.getFileFromSSH(res)
        if response.status_code == 201:
            return Response(final_response, status=status.HTTP_200_OK)
        return Response(
            {"error": "No Response received"}, status=status.HTTP_408_REQUEST_TIMEOUT
        )


class UsingCellID(APIView):
    permission_classes = (IsAuthenticated,)

    def getFileFromSSH(self, responseBody):
        paramiko.util.log_to_file("./paramiko.log")

        hostname = settings.BIG_DATA_HOST
        port = settings.BIG_DATA_PORT

        sftpHostname = settings.SFTP_DATA_HOST
        sftpPassword = settings.SFTP_DATA_PASSWORD
        username = settings.BIG_DATA_USERNAME
        password = settings.BIG_DATA_HOST_PASSWORD

        statusEndpoint = "http://{}:{}/ontrack-webservice/status".format(hostname, port)
        statusPayload = {"requestID": responseBody["requestID"]}
        getURL = statusEndpoint + "/?requestID=" + responseBody["requestID"]
        print(getURL)
        time.sleep(60)
        statusResponse = requests.get(getURL)
        print(statusResponse.status_code)
        print(statusResponse.json())
        if statusResponse.status_code == 201:
            print("Its 201")
            responseBody1 = statusResponse.json()
            localFilePath = "cellids.parquet"
            outputFilePath = responseBody1["outputFile"]
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(sftpHostname, username=username, password=sftpPassword)
            sftp = ssh.open_sftp()
            sftp.get(outputFilePath, localFilePath)
            df = pq.read_table(source="cellids.parquet").to_pandas()
            df.columns = map(str.lower, df.columns)
            print(df.columns)
            str_df = df.select_dtypes([np.object])
            print(str_df)
            # str_df = str_df.stack().str.decode('utf-8').unstack()
            for col in str_df:
                df[col] = str_df[col]

            # print(df["number"])
            # return_object = {"number": df["number"]}
            return_object = {"df": df}
            return return_object
        else:
            return Response(
                {"error": "No Response received"},
                status=status.HTTP_408_REQUEST_TIMEOUT,
            )

    def post(self, request, *args, **kwargs):
        requestBody = request.data
        paramsMap = {}
        # paramsMap['type'] = requestBody['type']
        # paramsMap['numbers'] = requestBody['numbers']
        paramsMap["location1"] = requestBody["location1"]
        paramsMap["location2"] = requestBody["location2"]
        paramsMap["startTime"] = requestBody["startTime"]
        paramsMap["endTime"] = requestBody["endTime"]
        print(requestBody)
        postURL = (
            "http://10.0.5.162:8011/ontrack-webservice/linked_msisdns_using_locations"
        )
        response = requests.get(postURL, params=paramsMap)
        print(response)
        print(response.json())
        res = response.json()
        print("Getting file from SSH...")
        final_response = self.getFileFromSSH(res)
        if response.status_code == 201:
            return Response(final_response, status=status.HTTP_200_OK)
        return Response(
            {"error": "No Response received"}, status=status.HTTP_408_REQUEST_TIMEOUT
        )


class CellTowerDataViewSet(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        dataMap = request.data
        print(dataMap)
        if Decimal(dataMap["lat1"]) > Decimal(dataMap["lat2"]):
            if Decimal(dataMap["lon1"]) > Decimal(dataMap["lon2"]):
                towerDetails = CellTowerData.objects.filter(
                    latitude__lt=Decimal(dataMap["lat1"]),
                    latitude__gt=Decimal(dataMap["lat2"]),
                    longitude__lt=Decimal(dataMap["lon1"]),
                    longitude__gt=Decimal(dataMap["lon2"]),
                )
            else:
                towerDetails = CellTowerData.objects.filter(
                    latitude__lt=Decimal(dataMap["lat1"]),
                    latitude__gt=Decimal(dataMap["lat2"]),
                    longitude__lt=Decimal(dataMap["lon2"]),
                    longitude__gt=Decimal(dataMap["lon1"]),
                )
        else:
            if Decimal(dataMap["lon1"]) > Decimal(dataMap["lon2"]):
                towerDetails = CellTowerData.objects.filter(
                    latitude__lt=Decimal(dataMap["lat2"]),
                    latitude__gt=Decimal(dataMap["lat1"]),
                    longitude__lt=Decimal(dataMap["lon1"]),
                    longitude__gt=Decimal(dataMap["lon2"]),
                )
            else:
                towerDetails = CellTowerData.objects.filter(
                    latitude__lt=Decimal(dataMap["lat2"]),
                    latitude__gt=Decimal(dataMap["lat1"]),
                    longitude__lt=Decimal(dataMap["lon2"]),
                    longitude__gt=Decimal(dataMap["lon1"]),
                )
        serializedData = CellDataSerializer(towerDetails, many=True)
        return Response(serializedData.data)


# class CustomJobView(views.APIView):
#     permission_classes = (IsAuthenticated,)
#     def post(self, request, *args, **kwargs):
#         dataMap = request.data
#         new_job_object = Job(
#             case = dataMap['case'],
#             name = dataMap['name'],
#             query = dataMap['query'],
#             serverJobId = dataMap['serverJobId']
#         )


class WeeklyReportGenerator(APIView):
    permission_classes = (IsAuthenticated,)

    def report(self, db_name, startDate, days):

        dataForWorkBook = [["Date", "Total Jobs Created", "Total Jobs Completed"]]

        for day in range(0, days):
            try:
                present = startDate - timedelta(days=day)
                previous = present - timedelta(days=1)


                midnight = present.replace(hour=0, minute=0, second=0, microsecond=0)

                previous_midnight = previous.replace(
                    hour=0, minute=0, second=0, microsecond=0
                )

                print(midnight)
                print(previous_midnight)


                total_jobs = (
                    Job.objects.using(db_name)
                    .filter(createdAt__lt=midnight, createdAt__gte=previous_midnight)
                    .count()
                )
                failed_jobs = (
                    Job.objects.using(db_name)
                    .filter(
                        createdAt__lt=midnight,
                        createdAt__gte=previous_midnight,
                        status="FAILED",
                    )
                    .count()
                )
                completed_jobs = (
                    Job.objects.using(db_name)
                    .filter(
                        createdAt__lt=midnight,
                        createdAt__gte=previous_midnight,
                        status="FINISHED",
                    )
                    .count()
                )
                pending_jobs = (
                    Job.objects.using(db_name)
                    .filter(
                        createdAt__lt=midnight,
                        createdAt__gte=previous_midnight,
                        status="PENDING",
                    )
                    .count()
                )

                print(
                    "---------------Report for - {}----------------".format(
                        previous_midnight
                    )
                )
                print("---------------Server - {}----------------".format(db_name))
                print("Total Jobs Created : {}".format(total_jobs))
                print("Total Jobs Failed: {}".format(failed_jobs))
                print("Total Jobs Completed: {}".format(completed_jobs))
                print("Total Jobs Pending: {}".format(pending_jobs))

                dataForWorkBook.append([previous_midnight, total_jobs, completed_jobs])

            except Exception as ex:
                print(ex)

        return dataForWorkBook

    def post(self, request, *args, **kwargs):
        
        requestBody = request.data
        print(requestBody)

        startDate = requestBody["startDate"]
        endDate = requestBody["endDate"]

        startDatetimeObject = datetime.fromtimestamp(startDate)
        endDatetimeObject = datetime.fromtimestamp(endDate)

        print("Start Date: {}, End Date: {}".format(startDatetimeObject, endDatetimeObject))

        counter = endDatetimeObject - startDatetimeObject
        counter = counter.days

        print("Counter: {}".format(counter))

        dbname = "default"

        # Pass end date and counter to compute reports
        dataForWorkBook = self.report(dbname, endDatetimeObject, counter)
        
        try:
            workbook = openpyxl.Workbook()
            worksheet = workbook.active

            for row in dataForWorkBook:
                worksheet.append(row)

            # Create an HTTP response with the Excel file
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="report.xlsx"'
            workbook.save(response)

            return response
        

        except Exception as ex:
            print(ex)


class JobUpdate(generics.GenericAPIView):
    def get(self,request):
        job = request.GET.get('id')
        qs = Job.objects.filter(id=job)
        if(len(qs) == 0):
           return Response('Job Id Not available',500)
        else:
           qs[0].status="FAILED"
           qs[0].save()
           qs = Job.objects.filter(id=job)
           serializer = JobSerializer(qs,many=True)
           return Response(serializer.data)

class JobDetails(generics.GenericAPIView):
    def get(self,request):
        job = request.GET.get('id')
        qs = Job.objects.filter(id=job)
        if(len(qs) == 0):
           return Response('Job Id Not available',500)
        else:
           serializer = JobSerializer(qs,many=True)
           return Response(serializer.data)
              

class GetUserDetails(generics.GenericAPIView):
    def get(self,request):
        user_id = request.GET.get('id')
        user = User.objects.get(pk=user_id) 
        serializer = UserSerializer(user)
        return Response(serializer.data)
