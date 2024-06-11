from statistics import mode
import requests
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

hostname = settings.BIG_DATA_HOST
port = settings.BIG_DATA_PORT


class Department(models.Model):
    name = models.CharField(max_length=128, default=None, null=True)
    zone = models.CharField(max_length=128, default=None, null=True)
    head = models.CharField(max_length=128, default=None, null=True)
    city = models.CharField(max_length=128, default=None, null=True)
    lga = models.CharField(max_length=128, default=None, null=True)
    state = models.CharField(max_length=128, default=None, null=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=128, default=None, null=True)


class UserAccountPermissions(models.Model):
    view = models.BooleanField()
    add = models.BooleanField()
    edit = models.BooleanField()
    closecase = models.BooleanField(default=None, null=True)
    printcase = models.BooleanField(default=None, null=True)
    addzone = models.BooleanField(default=None, null=True)
    addpoi = models.BooleanField(default=None, null=True)
    export = models.BooleanField(default=None, null=True)
    newnumber = models.BooleanField(default=None, null=True)
    schedule = models.BooleanField(default=None, null=True)

    def __str__(self) -> str:
        return super().__str__()


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=None, null=True)
    phone = models.CharField(max_length=16, default=None, null=True)
    disabled = models.BooleanField(default=False)
    designation = models.CharField(
        max_length=32,
        choices=[
            ("Admin", "Admin"),
            ("Supervisor", "Supervisor"),
            ("Analyst", "Analyst"),
            ("Agent", "Agent"),
            ("Support", "Support"),
        ],
        default="Analyst",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="department",
        default=None,
        null=True,
    )
    modules = ArrayField(
        models.CharField(max_length=128),
        default=list,
    )
    caseot = models.ForeignKey(
        UserAccountPermissions,
        on_delete=models.DO_NOTHING,
        related_name="caseot",
        null=True,
    )
    locateot = models.ForeignKey(
        UserAccountPermissions,
        on_delete=models.DO_NOTHING,
        related_name="locateot",
        null=True,
    )
    checkot = models.ForeignKey(
        UserAccountPermissions,
        on_delete=models.DO_NOTHING,
        related_name="checkot",
        null=True,
    )
    fenceot = models.ForeignKey(
        UserAccountPermissions,
        on_delete=models.DO_NOTHING,
        related_name="fenceot",
        null=True,
    )
    mobileot = models.ForeignKey(
        UserAccountPermissions,
        on_delete=models.DO_NOTHING,
        related_name="mobileot",
        null=True,
    )
    startDate = models.BigIntegerField(default=-1)
    endDate = models.BigIntegerField(default=-1)

    def __str__(self):
        return self.user.username


def delete_user_on_account_removal(sender, instance, **kwargs):
    user_id = instance.user.id
    user = User.objects.get(pk=user_id)
    user.delete()


post_delete.connect(delete_user_on_account_removal, sender=Account)


class Case(models.Model):
    name = models.CharField(max_length=128, default=None, null=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    accounts = models.ManyToManyField(Account, blank=True, related_name="accounts")
    targets = ArrayField(
        models.CharField(max_length=128),
        default=list,
    )
    description = models.CharField(max_length=512)
    teamLead = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    category = models.CharField(
        max_length=32,
        choices=[
            ("Robbery", "Robbery"),
            ("Theft", "Theft"),
            ("Bomb Blast", "Bomb Blast"),
            ("Other", "Other"),
        ],
        default="Other",
    )
    status = models.CharField(
        max_length=32,
        choices=[("Open", "Open"), ("Close", "Close"), ("Delayed", "Delayed")],
        default="Open",
    )
    startDate = models.BigIntegerField(default=-1)
    endDate = models.BigIntegerField(default=-1)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Zone(models.Model):
    name = models.CharField(max_length=128, default=None, null=True)
    description = models.CharField(max_length=512, default=None, null=True)
    cases = models.ManyToManyField(Case, blank=True, related_name="zone_cases")
    lat1 = models.CharField(max_length=100, default=None, null=True)
    lng1 = models.CharField(max_length=100, default=None, null=True)
    lat2 = models.CharField(max_length=100, default=None, null=True)
    lng2 = models.CharField(max_length=100, default=None, null=True)
    area = models.FloatField(default=-1)


class Poi(models.Model):
    name = models.CharField(max_length=128, default=None, null=True)
    description = models.CharField(max_length=512, default=None, null=True)
    cases = models.ManyToManyField(Case, blank=True, related_name="poi_cases")
    address = models.CharField(max_length=256, default=None, null=True)
    city = models.CharField(max_length=512, default=None, null=True)
    zipcode = models.BigIntegerField(default=-1)
    lat = models.FloatField(default=-1)
    lng = models.FloatField(default=-1)


class Job(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, default=None, null=True)
    query = models.CharField(max_length=128, default=None, null=True)
    query1 = models.CharField(max_length=128, default=None, null=True)
    query2 = models.CharField(max_length=128, default=None, null=True)
    serverJobId = models.CharField(max_length=128, default=None, null=True)
    handsetHistoryJobId = models.CharField(max_length=128, default=None, null=True)
    linkTreeJobId = models.CharField(max_length=128, default=None, null=True)
    linkedDataJobId = models.CharField(max_length=128, default=None, null=True)
    status = models.CharField(
        max_length=32,
        choices=[
            ("PENDING", "PENDING"),
            ("FINISHED", "FINISHED"),
            ("FAILED", "FAILED"),
        ],
        default="PENDING",
    )
    handsetHistoryStatus = models.CharField(
        max_length=32,
        choices=[
            ("PENDING", "PENDING"),
            ("FINISHED", "FINISHED"),
            ("FAILED", "FAILED"),
        ],
        default="PENDING",
    )
    linkedDataStatus = models.CharField(
        max_length=32,
        choices=[
            ("PENDING", "PENDING"),
            ("FINISHED", "FINISHED"),
            ("FAILED", "FAILED"),
        ],
        default="PENDING",
    )
    linkTreeStatus = models.CharField(
        max_length=32,
        choices=[
            ("PENDING", "PENDING"),
            ("FINISHED", "FINISHED"),
            ("FAILED", "FAILED"),
        ],
        default="PENDING",
    )
    category = models.CharField(
        max_length=32,
        choices=[
            ("IMSI", "IMSI"),
            ("IMEI", "IMEI"),
            ("MSISDN", "MSISDN"),
            ("Location", "Location"),
            ("LAC/Cell-ID", "LAC/Cell-ID"),
        ],
        default="IMSI",
    )
    type = models.CharField(
        max_length=32,
        choices=[
            ("Single Target", "Single Target"),
            ("MSISDN Linked", "MSISDN Linked"),
            ("CellID Linked", "CellID Linked"),
        ],
        default="Single Target",
    )
    radius = models.CharField(
        max_length=32,
        choices=[
            ("0", "0"),
            ("250", "250"),
            ("500", "500"),
            ("1000", "1000"),
        ],
        default="0",
    )
    number = models.CharField(
        max_length=32,
        choices=[
            ("0", "0"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("7", "7"),
            ("8", "8"),
            ("9", "9"),
            ("10", "10"),
            ("11", "11"),
            ("12", "12"),
            ("13", "13"),
            ("14", "14"),
            ("15", "15"),
            ("16", "16"),
            ("17", "17"),
            ("18", "18"),
            ("19", "19"),
            ("20", "20"),
            ("21", "21"),
            ("22", "22"),
            ("23", "23"),
            ("24", "24"),
            ("25", "25"),
            ("26", "26"),
            ("27", "27"),
            ("28", "28"),
            ("29", "29"),
            ("30", "30"),
            ("31", "31"),
        ],
        default="0",
    )
    num = models.CharField(
        max_length=32,
        choices=[
            ("0", "0"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("7", "7"),
            ("8", "8"),
            ("9", "9"),
            ("10", "10"),
            ("11", "11"),
            ("12", "12"),
            ("13", "13"),
            ("14", "14"),
            ("15", "15"),
            ("16", "16"),
            ("17", "17"),
            ("18", "18"),
            ("19", "19"),
            ("20", "20"),
            ("21", "21"),
            ("22", "22"),
            ("23", "23"),
            ("24", "24"),
        ],
        default="0",
    )
    startTime = models.BigIntegerField(default=-1)
    endTime = models.BigIntegerField(default=-1)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.serverJobId)


def create_server_job(sender, instance, **kwargs):
    jobId = instance.id
    query = instance.query
    query1 = instance.query1
    query2 = instance.query2
    radius = instance.radius
    category = instance.category
    type = instance.type
    number = instance.number
    num = instance.num
    startTime = instance.startTime
    endTime = instance.endTime

    # Call Detail Record API
    payload = {
        "startTime": startTime,
        "endTime": endTime,
    }

    if type == "Single Target":
        if category == "IMSI":
            endpoint = "http://{}:{}/ontrack-webservice/imsilocations".format(
                hostname, port
            )
            payload["imsi"] = query
        elif category == "IMEI":
            endpoint = "http://{}:{}/ontrack-webservice/imeilocations".format(
                hostname, port
            )
            payload["imei"] = query
        elif category == "MSISDN":
            endpoint = "http://{}:{}/ontrack-webservice/msisdnlocations".format(
                hostname, port
            )
            payload["msisdn"] = query
        elif category == "Location":
            queryArr = query.split(",")
            payload["lat"] = queryArr[0]
            payload["lon"] = queryArr[1]
            payload["distance"] = queryArr[2]
            endpoint = "http://{}:{}/ontrack-webservice/locations".format(
                hostname, port
            )

        # elif type == 'CellID Linked':
        #     payload['type'] = type
        #     payload["location1"] = query1
        #     payload["location2"] = query2
        #     endpoint = 'http://10.0.5.162:8011/ontrack-webservice/linked_msisdns_using_locations'

        print("cdr server job request payload =" + str(payload))
        print(endpoint)
        print(payload)
        response = requests.get(endpoint, params=payload)
        response = response.json()
        print(response)
        serverJobId = response["requestID"]
        Job.objects.filter(pk=jobId).update(serverJobId=serverJobId)

    # Handset history API
    # MSISDN
    if category == "MSISDN" and type == "Single Target":
        payload = {
            "startTime": startTime,
            "endTime": endTime,
            # 'type': str(category).lower(),
            # 'number': query,
            str(category).lower(): query,
        }
        endpoint = (
            "http://{}:{}/ontrack-webservice/handsethistorywithassociates".format(
                hostname, port
            )
        )
        print("Endpoint :- " + str(endpoint))
        print("hh server job request paylod = " + str(payload))
        response = requests.get(endpoint, params=payload)
        print("HH Response :- ")
        print(response)
        print(response.text)
        print(response.raw)
        print(response.headers)
        print(response.status_code)
        print(response.content)
        print(response.json())
        response = response.json()
        handsetHistoryJobId = response["requestID"]
        Job.objects.filter(pk=jobId).update(handsetHistoryJobId=handsetHistoryJobId)
        # Job.objects.filter(pk=jobId).update(serverJobId=handsetHistoryJobId)

    #IMEI
    if category == "IMEI" and type == "Single Target":
        payload = {
            "startTime": startTime,
            "endTime": endTime,
            str(category).lower(): query,
        }
        endpoint = (
            "http://{}:{}/ontrack-webservice/handsethistoryforimei".format(
                hostname, port
            )
        )
        print("Endpoint :- " + str(endpoint))
        print("hh server job request paylod = " + str(payload))
        response = requests.get(endpoint, params=payload)
        print("HH Response :- ")
        print(response)
        print(response.json())
        response = response.json()
        handsetHistoryJobId = response["requestID"]
        Job.objects.filter(pk=jobId).update(handsetHistoryJobId=handsetHistoryJobId)
    
    #IMSI
    if category == "IMSI" and type == "Single Target":
        payload = {
            "startTime": startTime,
            "endTime": endTime,
            str(category).lower(): query,
        }
        endpoint = (
            "http://{}:{}/ontrack-webservice/handsethistoryforimsi".format(
                hostname, port
            )
        )
        print("Endpoint :- " + str(endpoint))
        print("hh server job request paylod = " + str(payload))
        response = requests.get(endpoint, params=payload)
        print("HH Response :- ")
        print(response)
        print(response.json())
        response = response.json()
        handsetHistoryJobId = response["requestID"]
        Job.objects.filter(pk=jobId).update(handsetHistoryJobId=handsetHistoryJobId)

    # LinkTree API
    if (
        category == "IMSI" or category == "IMEI" or category == "MSISDN"
    ) and type == "Single Target":
        endpoint = "http://{}:{}/ontrack-webservice/links".format(hostname, port)
        payload = {
            "type": str(category).lower(),
            "number": query,
            "startTime": startTime,
            "endTime": endTime,
        }
        print("lt server job request paylod = " + str(payload))
        response = requests.get(endpoint, params=payload)
        response = response.json()
        linkTreeJobId = response["requestID"]
        Job.objects.filter(pk=jobId).update(linkTreeJobId=linkTreeJobId)
        # Job.objects.filter(pk=jobId).update(serverJobId=linkTreeJobId)

    # Linked Data
    if type == "MSISDN Linked" or type == "CellID Linked":
        if category == "MSISDN":
            newendpoint = (
                "http://{}:{}/ontrack-webservice/linked_msisdns_using_msisdns".format(
                    hostname, port
                )
            )
            payload = {
                "type": str(category).lower(),
                "numbers": query + "," + query1,
                "startTime": startTime,
                "endTime": endTime,
            }
            print("LinkedData server job request paylod = " + str(payload))
            response = requests.get(newendpoint, params=payload)
            response = response.json()
            linkedDataJobId = response["requestID"]
            Job.objects.filter(pk=jobId).update(linkedDataJobId=linkedDataJobId)

        elif category == "LAC/Cell-ID":
            newendpoint = (
                "http://{}:{}/ontrack-webservice/linked_msisdns_using_locations".format(
                    hostname, port
                )
            )
            payload = {
                "type": str(category).lower(),
                "location1": query1,
                "location2": query2,
                "startTime": startTime,
                "endTime": endTime,
            }
            print("LinkedData server job request paylod = " + str(payload))
            response = requests.get(newendpoint, params=payload)
            response = response.json()
            linkedDataJobId = response["requestID"]
            print(linkedDataJobId)
            Job.objects.filter(pk=jobId).update(linkedDataJobId=linkedDataJobId)
        Job.objects.filter(pk=jobId).update(serverJobId=linkedDataJobId)


post_save.connect(create_server_job, sender=Job)


class HandsetHistory(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, default=-1)
    associatedmsisdn = models.CharField(
        max_length=100, null=True, default=None, db_column="associatedmsisdn"
    )
    # type = models.CharField(max_length=50, null=True, default=None)
    imei = models.CharField(max_length=50, null=True, default=None, db_column="imei")
    imsi = models.CharField(max_length=100, null=True, default=None, db_column="imsi")

    msisdn = models.CharField(
        max_length=100, null=True, default=None, db_column="msisdn"
    )
    startTime = models.BigIntegerField(default=-1, db_column="starttime")
    endTime = models.BigIntegerField(default=-1, db_column="endtime")


class LinkTree(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, default=-1)
    msisdn = models.CharField(max_length=32, default=None, null=True)
    interactions = models.BigIntegerField(default=0)


class CallDetailRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    geohash = models.CharField(max_length=16, default=None, null=True, blank=True)
    lac = models.FloatField(default=-1, null=True)
    cellid = models.FloatField(default=-1, null=True)
    eventtype = models.CharField(max_length=256, default=None, null=True)
    yyyymm = models.BigIntegerField(default=-1, null=True)
    callingimei = models.BigIntegerField(default=-1, null=True)
    callingimsi = models.BigIntegerField(default=-1, null=True)
    callingfirstcgi = models.CharField(max_length=256, default=None, null=True)
    callinglastcgi = models.CharField(max_length=256, default=None, null=True)
    calledfirstcgi = models.CharField(max_length=256, default=None, null=True)
    calledlastcgi = models.CharField(max_length=256, default=None, null=True)
    callingfirstlac = models.FloatField(default=-1, null=True)
    callingfirstcellid = models.FloatField(default=-1, null=True)
    callinglastlac = models.FloatField(default=-1, null=True)
    callinglastcellid = models.FloatField(default=-1, null=True)
    calledfirstlac = models.FloatField(default=-1, null=True)
    calledfirstcellid = models.FloatField(default=-1, null=True)
    calledlastlac = models.FloatField(default=-1, null=True)
    calledlastcellid = models.FloatField(default=-1, null=True)
    callingfirstlocationlat = models.FloatField(default=-1, null=True)
    callinglastlocationlon = models.FloatField(default=-1, null=True)
    callingfirstlocationlon = models.FloatField(default=-1, null=True)
    callinglastlocationlat = models.FloatField(default=-1, null=True)
    calledfirstlocationlat = models.FloatField(default=-1, null=True)
    calledfirstlocationlon = models.FloatField(default=-1, null=True)
    calledlastlocationlat = models.FloatField(default=-1, null=True)
    calledlastlocationlon = models.FloatField(default=-1, null=True)
    callingfirstlocationaddress = models.CharField(
        max_length=256, default=None, null=True
    )
    callingfirstlocationcity = models.CharField(max_length=256, default=None, null=True)
    callingfirstlocationlga = models.CharField(max_length=256, default=None, null=True)
    callinglastlocationaddress = models.CharField(
        max_length=256, default=None, null=True
    )
    callinglastlocationcity = models.CharField(max_length=256, default=None, null=True)
    callinglastlocationlga = models.CharField(max_length=256, default=None, null=True)
    calledfirstlocationaddress = models.CharField(
        max_length=256, default=None, null=True
    )
    calledfirstlocationcity = models.CharField(max_length=256, default=None, null=True)
    calledfirstlocationlga = models.CharField(max_length=256, default=None, null=True)
    calledlastlocationaddress = models.CharField(
        max_length=256, default=None, null=True
    )
    calledlastlocationcity = models.CharField(max_length=256, default=None, null=True)
    calledlastlocationlga = models.CharField(max_length=256, default=None, null=True)
    subscribercategory = models.CharField(max_length=256, default=None, null=True)
    timestamp = models.BigIntegerField(default=-1, null=True)
    timebucket = models.CharField(max_length=256, default=None, null=True)
    servedimsi = models.BigIntegerField(default=-1, null=True)
    servedimei = models.BigIntegerField(default=-1, null=True)
    servedimeifull = models.BigIntegerField(default=-1, null=True)
    servedmsisdn = models.BigIntegerField(default=-1, null=True)
    callingnumber = models.BigIntegerField(default=-1, null=True)
    callednumber = models.BigIntegerField(default=-1, null=True)
    recordingentity = models.BigIntegerField(default=-1, null=True)
    locationlat = models.FloatField(default=-1, null=True)
    locationlon = models.FloatField(default=-1, null=True)
    seizureordeliverytime = models.BigIntegerField(default=-1, null=True)
    answertime = models.BigIntegerField(default=-1, null=True)
    releasetime = models.BigIntegerField(default=-1, null=True)
    callduration = models.BigIntegerField(default=-1, null=True)
    causeforterm = models.BigIntegerField(default=-1, null=True)
    diagnostics = models.BigIntegerField(default=-1, null=True)
    callreference = models.CharField(max_length=256, default=None, null=True)
    sequencenumber = models.CharField(max_length=256, default=None, null=True)
    networkcallreference = models.CharField(max_length=256, default=None, null=True)
    mscaddress = models.BigIntegerField(default=-1, null=True)
    systemtype = models.CharField(max_length=256, default=None, null=True)
    chargedparty = models.CharField(max_length=256, default=None, null=True)
    calledimsi = models.BigIntegerField(default=-1, null=True)
    subscribercategory = models.CharField(max_length=256, default=None, null=True)
    firstmccmnc = models.CharField(max_length=256, default=None, null=True)
    intermediatemccmnc = models.CharField(max_length=256, default=None, null=True)
    lastmccmnc = models.CharField(max_length=256, default=None, null=True)
    usertype = models.CharField(max_length=256, default=None, null=True)
    recordnumber = models.BigIntegerField(default=-1, null=True)
    partyrelcause = models.CharField(max_length=256, default=None, null=True)
    chargelevel = models.CharField(max_length=256, default=None, null=True)
    locationnum = models.CharField(max_length=256, default=None, null=True)
    zonecode = models.CharField(max_length=256, default=None, null=True)
    accountcode = models.CharField(max_length=256, default=None, null=True)
    calledportedflag = models.BigIntegerField(default=-1, null=True)
    calledimei = models.BigIntegerField(default=-1, null=True)
    drccallid = models.CharField(max_length=256, default=None, null=True)
    callredirectionflag = models.BigIntegerField(default=-1, null=True)
    globalcallreference = models.CharField(max_length=256, default=None, null=True)
    callerportedflag = models.BigIntegerField(default=-1, null=True)
    connectednumber = models.CharField(max_length=256, default=None, null=True)
    smsuserdatatype = models.CharField(max_length=256, default=None, null=True)
    smstext = models.CharField(max_length=256, default=None, null=True)
    maxsmsconcated = models.BigIntegerField(default=-1, null=True)
    concatsmsrefnumber = models.BigIntegerField(default=-1, null=True)
    seqnoofcurrentsms = models.BigIntegerField(default=-1, null=True)
    locationestimate = models.BigIntegerField(default=-1, null=True)
    locationupdatetype = models.BigIntegerField(default=-1, null=True)
    imeistatus = models.BigIntegerField(default=-1, null=True)
    sgwipaddress = models.CharField(max_length=256, default=None, null=True)
    servingnodeipaddress = models.CharField(max_length=256, default=None, null=True)
    accesspointnameni = models.CharField(max_length=256, default=None, null=True)
    servedpdppdnaddress = models.CharField(max_length=256, default=None, null=True)
    operator = models.CharField(max_length=256, default=None, null=True)
    rat = models.CharField(max_length=256, default=None, null=True)
    address = models.CharField(max_length=256, default=None, null=True)
    city = models.CharField(max_length=256, default=None, null=True)
    lga = models.CharField(max_length=256, default=None, null=True)
    cgi = models.CharField(max_length=256, default=None, null=True)
    sscode = models.CharField(max_length=256, default=None, null=True)
    presentationandscreeningindicator = models.CharField(
        max_length=256, default=None, null=True
    )
    cliindicator = models.CharField(max_length=256, default=None, null=True)
    callingnumberactual = models.BigIntegerField(default=-1, null=True)
    callingnumberasname = models.CharField(max_length=256, default=None, null=True)

    def __str__(self):
        return str(self.job)


class LinkedDataRecord(models.Model):
    type = models.CharField(max_length=32, default=None, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, default=-1)
    number = models.BigIntegerField(default=-1, null=True)
    linkingReason = models.CharField(max_length=256, default=None, null=True)
    linkId = models.BigIntegerField(default=-1, null=True)
    # party1CDRs = ArrayField(CallDetailRecord)
    # party2CDRs = ArrayField(CallDetailRecord)
    # party1CDRs = ArrayField(models.JSONField(null=True))
    # party2CDRs = ArrayField(models.JSONField(null=True))
    # party1CDRs = models.TextField(null=True)
    # party2CDRs = models.TextField(null=True)


class LinkedDataCallDetailRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    partyId = models.CharField(
        max_length=32, choices=[("Party-1", "Party-1"), ("Party-2", "Party-2")]
    )
    linkId = models.BigIntegerField(default=-1, null=True)
    geoHash = models.CharField(max_length=16, default=None, null=True, blank=True)
    lac = models.FloatField(default=-1, null=True)
    cellId = models.FloatField(default=-1)
    eventType = models.CharField(max_length=256, default=None, null=True)
    yyyymm = models.BigIntegerField(default=-1, null=True)
    callingIMEI = models.BigIntegerField(default=-1, null=True)
    callingIMSI = models.BigIntegerField(default=-1, null=True)
    callingFirstCgi = models.CharField(max_length=256, default=None, null=True)
    callingLastCgi = models.CharField(max_length=256, default=None, null=True)
    calledFirstCgi = models.CharField(max_length=256, default=None, null=True)
    calledLastCgi = models.CharField(max_length=256, default=None, null=True)
    callingFirstLac = models.FloatField(default=-1, null=True)
    callingFirstCellId = models.FloatField(default=-1, null=True)
    callingLastLac = models.FloatField(default=-1, null=True)
    callingLastCellId = models.FloatField(default=-1, null=True)
    calledFirstLac = models.FloatField(default=-1, null=True)
    calledFirstCellId = models.FloatField(default=-1, null=True)
    calledLastLac = models.FloatField(default=-1, null=True)
    calledLastCellId = models.FloatField(default=-1, null=True)
    callingFirstLocationLat = models.FloatField(default=-1, null=True)
    callingLastLocationLon = models.FloatField(default=-1, null=True)
    callingFirstLocationLon = models.FloatField(default=-1, null=True)
    callingLastLocationLat = models.FloatField(default=-1, null=True)
    calledFirstLocationLat = models.FloatField(default=-1, null=True)
    calledFirstLocationLon = models.FloatField(default=-1, null=True)
    calledLastLocationLat = models.FloatField(default=-1, null=True)
    calledLastLocationLon = models.FloatField(default=-1, null=True)
    callingFirstLocationAddress = models.CharField(
        max_length=256, default=None, null=True
    )
    callingFirstLocationCity = models.CharField(max_length=256, default=None, null=True)
    callingFirstLocationLga = models.CharField(max_length=256, default=None, null=True)
    callingLastLocationAddress = models.CharField(
        max_length=256, default=None, null=True
    )
    callingLastLocationCity = models.CharField(max_length=256, default=None, null=True)
    callingLastLocationLga = models.CharField(max_length=256, default=None, null=True)
    calledFirstLocationAddress = models.CharField(
        max_length=256, default=None, null=True
    )
    calledFirstLocationCity = models.CharField(max_length=256, default=None, null=True)
    calledFirstLocationLga = models.CharField(max_length=256, default=None, null=True)
    calledLastLocationAddress = models.CharField(
        max_length=256, default=None, null=True
    )
    calledLastLocationCity = models.CharField(max_length=256, default=None, null=True)
    calledLastLocationLga = models.CharField(max_length=256, default=None, null=True)
    subscriberCategory = models.CharField(max_length=256, default=None, null=True)
    timeStamp = models.BigIntegerField(default=-1, null=True)
    timeBucket = models.CharField(max_length=256, default=None, null=True)
    servedIMSI = models.BigIntegerField(default=-1, null=True)
    servedMSISDN = models.BigIntegerField(default=-1, null=True)
    servedIMEI = models.BigIntegerField(default=-1, null=True)
    servedIMEIFull = models.BigIntegerField(default=-1, null=True)
    callingNumber = models.BigIntegerField(default=-1, null=True)
    calledNumber = models.BigIntegerField(default=-1, null=True)
    recordingEntity = models.BigIntegerField(default=-1, null=True)
    locationLat = models.FloatField(default=-1, null=True)
    locationLon = models.FloatField(default=-1, null=True)
    seizureOrDeliveryTime = models.BigIntegerField(default=-1, null=True)
    answerTime = models.BigIntegerField(default=-1, null=True)
    releaseTime = models.BigIntegerField(default=-1, null=True)
    callDuration = models.BigIntegerField(default=-1, null=True)
    causeForTerm = models.BigIntegerField(default=-1, null=True)
    diagnostics = models.BigIntegerField(default=-1, null=True)
    callReference = models.CharField(max_length=256, default=None, null=True)
    sequenceNumber = models.CharField(max_length=256, default=None, null=True)
    networkCallReference = models.CharField(max_length=256, default=None, null=True)
    mscAddress = models.BigIntegerField(default=-1, null=True)
    systemType = models.CharField(max_length=256, default=None, null=True)
    chargedParty = models.CharField(max_length=256, default=None, null=True)
    calledIMSI = models.BigIntegerField(default=-1, null=True)
    subscriberCategory = models.CharField(max_length=256, default=None, null=True)
    firstMccMnc = models.CharField(max_length=256, default=None, null=True)
    intermediateMccMnc = models.CharField(max_length=256, default=None, null=True)
    lastMccMnc = models.CharField(max_length=256, default=None, null=True)
    userType = models.CharField(max_length=256, default=None, null=True)
    recordNumber = models.BigIntegerField(default=-1, null=True)
    partyRelCause = models.CharField(max_length=256, default=None, null=True)
    chargeLevel = models.CharField(max_length=256, default=None, null=True)
    locationNum = models.CharField(max_length=256, default=None, null=True)
    zoneCode = models.CharField(max_length=256, default=None, null=True)
    accountCode = models.CharField(max_length=256, default=None, null=True)
    calledPortedFlag = models.BigIntegerField(default=-1, null=True)
    calledIMEI = models.BigIntegerField(default=-1, null=True)
    drcCallId = models.CharField(max_length=256, default=None, null=True)
    callRedirectionFlag = models.BigIntegerField(default=-1, null=True)
    globalCallReference = models.CharField(max_length=256, default=None, null=True)
    callerPortedFlag = models.BigIntegerField(default=-1, null=True)
    connectedNumber = models.CharField(max_length=256, default=None, null=True)
    smsUserDataType = models.CharField(max_length=256, default=None, null=True)
    smsText = models.CharField(max_length=256, default=None, null=True)
    maxSMSConcated = models.BigIntegerField(default=-1, null=True)
    concatSMSRefNumber = models.BigIntegerField(default=-1, null=True)
    seqNoOfCurrentSMS = models.BigIntegerField(default=-1, null=True)
    locationEstimate = models.BigIntegerField(default=-1, null=True)
    locationUpdateType = models.BigIntegerField(default=-1, null=True)
    imeiStatus = models.BigIntegerField(default=-1, null=True)
    sgwIPAddress = models.CharField(max_length=256, default=None, null=True)
    servingNodeIPAddress = models.CharField(max_length=256, default=None, null=True)
    accessPointNameNI = models.CharField(max_length=256, default=None, null=True)
    servedPDPPDNAddress = models.CharField(max_length=256, default=None, null=True)
    operator = models.CharField(max_length=256, default=None, null=True)
    rat = models.CharField(max_length=256, default=None, null=True)
    address = models.CharField(max_length=256, default=None, null=True)
    city = models.CharField(max_length=256, default=None, null=True)
    lga = models.CharField(max_length=256, default=None, null=True)
    cgi = models.CharField(max_length=256, default=None, null=True)
    ssCode = models.CharField(max_length=256, default=None, null=True)
    presentationAndScreeningIndicator = models.CharField(
        max_length=256, default=None, null=True
    )
    cliIndicator = models.CharField(max_length=256, default=None, null=True)
    callingNumberActual = models.BigIntegerField(default=-1, null=True)
    callingNumberAsName = models.CharField(max_length=256, default=None, null=True)


class CellTowerData(models.Model):
    mcc = models.IntegerField(null=True, default=None)
    mnc = models.IntegerField(null=True, default=None)
    lac = models.IntegerField(null=True, default=None)
    cellsite = models.IntegerField(null=True, default=None)
    operator = models.CharField(
        max_length=128,
        null=True,
    )
    latitude = models.DecimalField(
        max_digits=22, decimal_places=16, null=True, default=None
    )
    longitude = models.DecimalField(
        max_digits=22, decimal_places=16, null=True, default=None
    )
    geohash = models.CharField(
        max_length=128,
        null=True,
    )
    address = models.TextField(null=True)
    city = models.CharField(max_length=256, null=True)
    lga = models.CharField(max_length=256, null=True)

    def __str__(self) -> str:
        return str(self.operator)


class DailyJobReports(models.Model):
    totaljobs = models.BigIntegerField(null=True, default=-1)
    pendingjobs = models.BigIntegerField(null=True, default=-1)
    completedjobs = models.BigIntegerField(null=True, default=-1)
    failedjobs = models.BigIntegerField(null=True, default=-1)
    createdAt = models.DateTimeField(null=True, default=None)
    servernumber = models.IntegerField(null=True, default=-1)
