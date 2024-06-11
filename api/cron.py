import uuid
import os
import requests
import paramiko
import json
import pyarrow.parquet as pq
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from django.conf import settings
from django_cron import CronJobBase, Schedule
from .models import Job, CellTowerData
from datetime import datetime, time
from urllib.parse import quote_plus
import time

paramiko.util.log_to_file("./paramiko.log")

hostname = settings.BIG_DATA_HOST
port = settings.BIG_DATA_PORT

sftpHostname = settings.SFTP_DATA_HOST
sftpPassword = settings.SFTP_DATA_PASSWORD

statusEndpoint = "http://{}:{}/ontrack-webservice/status".format(hostname, port)

cellSiteDataEndpoint = "http://{}:{}/ontrack-webservice/cellsites".format(
    hostname, port
)

operatorsList = [
    "MTN",
    "9Mobile",
    "Airtel",
    "Glo",
]

username = settings.BIG_DATA_USERNAME
password = settings.BIG_DATA_HOST_PASSWORD

cronlimit = settings.CRON_LIMIT

dbname = settings.DATABASES["default"]["NAME"]
dbhost = settings.DATABASES["default"]["HOST"]
dbuser = settings.DATABASES["default"]["USER"]
dbpassword = settings.DATABASES["default"]["PASSWORD"]
dbport = settings.DATABASES["default"]["PORT"]


def getFileFromSSH(responseBody):
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
        localFilePath = "response.parquet"
        outputFilePath = responseBody1["outputFile"]
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(sftpHostname, username=username, password=sftpPassword)
        sftp = ssh.open_sftp()
        sftp.get(outputFilePath, localFilePath)
        df = pq.read_table(source="response.parquet").to_pandas()
        df.columns = map(str.lower, df.columns)
        print(df.columns)
        str_df = df.select_dtypes([np.object])
        print(str_df)
        # str_df = str_df.stack().str.decode('utf-8').unstack()
        for col in str_df:
            df[col] = str_df[col]

        print(df)

        engine = create_engine(
            "postgresql://{}:{}@{}:{}/{}".format(
                dbuser, quote_plus(dbpassword), dbhost, dbport, dbname
            )
        )

        df.to_sql("api_celltowerdata", engine, if_exists="append", index=False)

    elif statusResponse.status_code == 202:
        print("Its 202")
    return statusResponse


def ingestParquetFile(localJobId):
    df = pq.read_table(source="temp.parquet").to_pandas()
    print("cdr parquet")
    # print(df.city)
    # print(df.lga)
    # print(df.address)
    # print(df.cgi)
    df["job_id"] = localJobId
    df.columns = df.columns.str.lower()
    str_df = df.select_dtypes([np.object])
    # str_df = str_df.stack().str.decode('utf-8').unstack()

    for col in str_df:
        # if str_df[col] is not None:
        #     print(str_df[col])
        df[col] = str_df[col]
        # print(df[col])
    print("before")
    engine = create_engine(
        "postgresql://{}:{}@{}:{}/{}".format(dbuser, quote_plus(dbpassword), dbhost, dbport, dbname)
    )
    print("Engine:",engine)
    # print("************* Data Frame for " + localJobId + " ********************")
    # print(df)
    # print("***********************************")

    df.to_sql("api_calldetailrecord", engine, if_exists="append", index=False)

    print("Before Exit")
def ingestHandsetHistoryParquetFile(localJobId):
    df = pq.read_table(source="temp.parquet").to_pandas()
    print("hh parquet")
    print(df)
    # df = df[df['type'].notnull()]
    print("0")
    df["job_id"] = localJobId
    print("1")
    df.columns = map(str.lower, df.columns)
    print("2")
    str_df = df.select_dtypes([np.object])
    print("4")
    # str_df = str_df.stack().str.decode('utf-8').unstack()
    print("5")

    for col in str_df:
        print("6")
        df[col] = str_df[col]

    engine = create_engine(
        "postgresql://{}:{}@{}:{}/{}".format(dbuser, quote_plus(dbpassword), dbhost, dbport, dbname)
    )
    df.to_sql("api_handsethistory", engine, if_exists="append", index=False)


def ingestLinkTreeParquetFile(localJobId):
    df = pq.read_table(source="temp.parquet").to_pandas()
    print("lt parquet")
    print(df)
    df["job_id"] = localJobId

    engine = create_engine(
        "postgresql://{}:{}@{}:{}/{}".format(dbuser, quote_plus(dbpassword), dbhost, dbport, dbname)
    )
    df.to_sql("api_linktree", engine, if_exists="append", index=False)


def ingestLinkedDataParquetFile(localJobId):
    df = pq.read_table(source="linkedmsisdns.parquet").to_pandas()
    print("lt parquet")
    df["job_id"] = localJobId

    engine = create_engine(
        "postgresql://{}:{}@{}:{}/{}".format(dbuser, quote_plus(dbpassword), dbhost, dbport, dbname)
    )
    df.to_sql("api_linkeddatarecord", engine, if_exists="append", index=False)

    time.sleep(30)

    # second file
    df = pq.read_table(source="linkedmsisdncdrs.parquet").to_pandas()
    print("linked cdr parquet")
    print(df)
    df["job_id"] = localJobId

    try:
        engine = create_engine(
            "postgresql://{}:{}@{}:{}/{}".format(
                dbuser, quote_plus(dbpassword), dbhost, dbport, dbname
            )
        )
        df.to_sql(
            "api_linkeddatacalldetailrecord", engine, if_exists="append", index=False
        )
    except Exception as ex:
        print("Error:", ex)


class FetchRecordsFromBigData(CronJobBase):
    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    def do(self):
        # ================== Fetching Call Detail Records =====================
        pendingJobs = Job.objects.filter(status="PENDING")


class FetchRecordsFromBigData(CronJobBase):
    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = str(uuid.uuid4())

    def do(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(sftpHostname, username=username, password=sftpPassword)
            sftp = ssh.open_sftp()
        except Exception as ex:
            print(ex)
        # ssh2 = paramiko.SSHClient()
        # ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh2.connect(sftpHostname,usrname=username,password=sftpPassword)
        # sftp = ssh2.open_sftp()w
        localFilePath = "temp.parquet"
        print("\ncdr")

        pendingJobs = Job.objects.filter(status="PENDING", type="Single Target").order_by('id')

        counter = 0

        for job in pendingJobs:
            localJobId = job.id
            if job.serverJobId == None:
                continue
            if counter == cronlimit:
                break
            print("localjobid=" + str(job.id))
            payload = {"requestID": job.serverJobId}
            print("cdr payload = " + str(payload))
            try:
                response = requests.get(statusEndpoint, params=payload)
                response = response.json()
                print("cdr status resp: " + str(response))
                if response["status"] == "FINISHED":
                    remoteFilePath = response["outputFile"]
                    print("Remote File Path is :" + remoteFilePath)
                    # remoteFilePath = '/home/centos/autodata/Output/f6069e87-a0e0-4842-9081-b49e451a7e5f/response.parquet'
                    sftp.get(remoteFilePath, localFilePath)
                    print("SRikanth Here before Ingestion")
                    ingestParquetFile(localJobId)
                    print("Srikanth here post Ingestion")
                    Job.objects.filter(pk=localJobId).update(status="FINISHED")
                elif response["status"] == "FAILED":
                    Job.objects.filter(pk=localJobId).update(status="FAILED")
                counter += 1
            except Exception as ex:
                # Job.objects.filter(pk=localJobId).update(status='FAILED')
                print("Error for cdr job id: {}".format(job.id))
                print(ex)
            print()

        # Link Tree
        print("lt")
        pendingJobs = Job.objects.filter(linkTreeStatus="PENDING").order_by('id')

        counter = 0
        for job in pendingJobs:
            localJobId = job.id
            if counter == cronlimit:
                break
            if (
                job.category == "IMSI"
                or job.category == "IMEI"
                or job.category == "MSISDN"
            ) and job.linkTreeJobId != None:
                print("localjobid=" + str(job.id))
                payload = {"requestID": job.linkTreeJobId}
                print("lt payload = " + str(payload))
                try:
                    response = requests.get(statusEndpoint, params=payload)
                    response = response.json()
                    print("lt status resp: " + str(response))
                    if response["status"] == "FINISHED":
                        remoteFilePath = response["outputFile"]
                        # remoteFilePath = '/home/centos/autodata/Output/f6069e87-a0e0-4842-9081-b49e451a7e5f/response.parquet'
                        sftp.get(remoteFilePath, localFilePath)
                        ingestLinkTreeParquetFile(localJobId)
                        Job.objects.filter(pk=localJobId).update(
                            linkTreeStatus="FINISHED"
                        )
                    elif response["status"] == "FAILED":
                        Job.objects.filter(pk=localJobId).update(
                            linkTreeStatus="FAILED"
                        )
                    counter += 1
                except Exception as ex:
                    # Job.objects.filter(pk=localJobId).update(linkTreeStatus='FAILED')
                    print("Error for lt job id: {}".format(job.id))
                    print(ex)
                print()

        # Handset History
        print("hh")
        pendingJobs = Job.objects.filter(handsetHistoryStatus="PENDING").order_by("id")

        counter = 0
        for job in pendingJobs:
            if counter == cronlimit:
                break
            localJobId = job.id
            if (
                job.category == "IMSI"
                or job.category == "IMEI"
                or job.category == "MSISDN"
            ) and job.handsetHistoryJobId != None:
                print("localjobid=" + str(job.id))
                payload = {"requestID": job.handsetHistoryJobId}
                print("hh payload = " + str(payload))

                try:
                    response = requests.get(statusEndpoint, params=payload)
                    response = response.json()
                    print("hh status resp: " + str(response))
                    if response["status"] == "FINISHED":
                        remoteFilePath = response["outputFile"]
                        # remoteFilePath = '/home/centos/autodata/Output/f6069e87-a0e0-4842-9081-b49e451a7e5f/response.parquet'
                        sftp.get(remoteFilePath, localFilePath)
                        ingestHandsetHistoryParquetFile(localJobId)
                        Job.objects.filter(pk=localJobId).update(
                            handsetHistoryStatus="FINISHED"
                        )
                    elif response["status"] == "FAILED":
                        Job.objects.filter(pk=localJobId).update(
                            handsetHistoryStatus="FAILED"
                        )
                    counter += 1
                except Exception as ex:
                    # Job.objects.filter(pk=localJobId).update(handsetHistoryStatus='FAILED')
                    print("Error for hh job id: {}".format(job.id))
                    print(ex)
                print()

        # Linked Data
        print("Linked")
        pendingJobs = Job.objects.filter(
            status="PENDING",
            linkedDataStatus="PENDING",
            category="LAC/Cell-ID",
            type="CellID Linked",
        ).order_by('id') | Job.objects.filter(
            status="PENDING",
            linkedDataStatus="PENDING",
            category="MSISDN",
            type="MSISDN Linked",
        ).order_by('id')

        counter = 0

        for job in pendingJobs:
            if counter == cronlimit:
                break
            localJobId = job.id
            if job.linkedDataJobId != None:
                print("localjobid=" + str(job.id))
                payload = {"requestID": job.linkedDataJobId}
                print("linkeddata payload = " + str(payload))

                try:
                    response = requests.get(statusEndpoint, params=payload)
                    response = response.json()
                    print("linkeddata status resp: " + str(response))
                    print("response: " + response["status"])
                    if response["status"] == "FINISHED":
                        remoteFilePath = response["outputFile"]
                        remoteFiles = remoteFilePath.split(",")
                        print(remoteFiles)
                        # remoteFilePath = '/home/centos/autodata/Output/f6069e87-a0e0-4842-9081-b49e451a7e5f/response.parquet'
                        localFilePath = "linkedmsisdns.parquet"
                        localFilePath1 = "linkedmsisdncdrs.parquet"
                        # sftp = ssh.open_sftp()
                        sftp.get(remoteFiles[0], localFilePath)
                        sftp.get(remoteFiles[1], localFilePath1)
                        ingestLinkedDataParquetFile(localJobId)
                        Job.objects.filter(pk=localJobId).update(
                            linkedDataStatus="FINISHED", status="FINISHED"
                        )
                    elif response["status"] == "FAILED":
                        Job.objects.filter(pk=localJobId).update(
                            linkedDataStatus="FAILED", status="FAILED"
                        )
                    counter += 1
                except Exception as ex:
                    # Job.objects.filter(pk=localJobId).update(handsetHistoryStatus='FAILED')
                    print("Error for linkedData job id: {}".format(job.id))
                    print(ex)
                print()

        sftp.close()
        ssh.close()


class FetchCellSiteData(CronJobBase):
    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = str(uuid.uuid4())

    def do(self):
        CellTowerData.objects.all().delete()
        for operator in operatorsList:
            print("Cell")
            operatorParam = {"operator": operator}
            response = requests.get(cellSiteDataEndpoint, params=operatorParam)
            responseBody = response.json()
            print(responseBody)
            if responseBody["status"] == "ACCEPTED":
                statusResponse = getFileFromSSH(responseBody=responseBody)
                if statusResponse.status_code != "202":
                    print(statusResponse.status_code)
                elif statusResponse.status_code == "202":
                    print("Sleeping for 40 secs")
                    time.sleep(40)
                    print("Starting again")
                    statusResponse2 = getFileFromSSH(responseBody=responseBody)
                    print(statusResponse2.status_code)
            else:
                print(
                    "Failed to create request "
                    + cellSiteDataEndpoint
                    + " "
                    + operatorParam
                )

class FetchAndDeleteFailedJobs(CronJobBase):
    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = str(uuid.uuid4())

    def do(self):
        # print("Delete Failed Jobs")
        # filter jobs based on status as Pending and delete them
        print("=====DELETING FAILED JOBS=====")
        try:
            failedJobs = Job.objects.filter(status="FAILED")
            print(failedJobs)
            failedJobs.delete()
        except Exception as ex:
           print(ex)

class FetchFailedJobs(CronJobBase):
    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = str(uuid.uuid4())

    def do(self):
        print("=====FAILED JOBS=====")
        try:
            today = datetime.now()
            midnight = today.replace(hour=0, minute=0, second=0, microsecond=0)

            failedJobs = Job.objects.filter(status="FAILED", createdAt__gte=midnight)
            #print all jobs
            for job in failedJobs:
                print(job)
        except Exception as ex:
            print(ex)

class FetchPendingJobs(CronJobBase):
    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = str(uuid.uuid4())

    def do(self):
        print("=====Pending JOBS=====")
        try:
            today = datetime.now()
            midnight = today.replace(hour=0, minute=0, second=0, microsecond=0)

            pendingJobs = Job.objects.filter(status="PENDING", createdAt__gte=midnight)
            #print all jobs
            for job in pendingJobs:
                print(job)
        except Exception as ex:
            print(ex)


class HandleJobs(CronJobBase):
    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = str(uuid.uuid4())

    def do(self):
        print("=====FAILING JOBS=====")
        try:
            pendingJobs = Job.objects.filter(status="PENDING")

            for job in pendingJobs:
                print(job.id)
                localJobId = job.id
                Job.objects.filter(pk=localJobId).update(status='FAILED')

        except Exception as ex:
           print(ex)
