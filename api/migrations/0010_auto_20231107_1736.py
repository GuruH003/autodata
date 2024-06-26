# Generated by Django 3.2.23 on 2023-11-07 17:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0009_job_linkeddatajobid_job_linkeddatastatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyJobReports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totaljobs', models.BigIntegerField(default=-1, null=True)),
                ('pendingjobs', models.BigIntegerField(default=-1, null=True)),
                ('completedjobs', models.BigIntegerField(default=-1, null=True)),
                ('failedjobs', models.BigIntegerField(default=-1, null=True)),
                ('createdAt', models.DateTimeField(default=None, null=True)),
                ('servernumber', models.IntegerField(default=-1, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='linkeddatarecord',
            name='party1CDRs',
        ),
        migrations.RemoveField(
            model_name='linkeddatarecord',
            name='party2CDRs',
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='calledfirstcellid',
            field=models.FloatField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='calledfirstcgi',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='calledfirstlac',
            field=models.FloatField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='calledfirstlocationaddress',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='calledfirstlocationcity',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='calledfirstlocationlat',
            field=models.FloatField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='calledfirstlocationlga',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='calledfirstlocationlon',
            field=models.FloatField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='calledlastcellid',
            field=models.FloatField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='calledlastcgi',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='calledlastlac',
            field=models.FloatField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='calledlastlocationaddress',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='calledlastlocationcity',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='calledlastlocationlat',
            field=models.FloatField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='calledlastlocationlga',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='calledlastlocationlon',
            field=models.FloatField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callingfirstcellid',
            field=models.FloatField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callingfirstcgi',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callingfirstlac',
            field=models.FloatField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callingfirstlocationaddress',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callingfirstlocationcity',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callingfirstlocationlat',
            field=models.FloatField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callingfirstlocationlga',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callingfirstlocationlon',
            field=models.FloatField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callingimei',
            field=models.BigIntegerField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callingimsi',
            field=models.BigIntegerField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callinglastcellid',
            field=models.FloatField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callinglastcgi',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callinglastlac',
            field=models.FloatField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callinglastlocationaddress',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callinglastlocationcity',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callinglastlocationlat',
            field=models.FloatField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callinglastlocationlga',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callinglastlocationlon',
            field=models.FloatField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callingnumberactual',
            field=models.BigIntegerField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='callingnumberasname',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='cliindicator',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='presentationandscreeningindicator',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='servedimeifull',
            field=models.BigIntegerField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='sscode',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='case',
            name='createdBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='handsethistory',
            name='associatedmsisdn',
            field=models.CharField(db_column='associatedmsisdn', default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='handsethistory',
            name='imsi',
            field=models.CharField(db_column='imsi', default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='createdBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='linkeddatarecord',
            name='job',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='api.job'),
        ),
        migrations.AddField(
            model_name='linkeddatarecord',
            name='linkId',
            field=models.BigIntegerField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='linktree',
            name='interactions',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='account',
            name='designation',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Supervisor', 'Supervisor'), ('Analyst', 'Analyst'), ('Agent', 'Agent'), ('Support', 'Support')], default='Analyst', max_length=32),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='accesspointnameni',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='accountcode',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='address',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='calledimei',
            field=models.BigIntegerField(default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='calledimsi',
            field=models.BigIntegerField(default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='calledportedflag',
            field=models.BigIntegerField(default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='callerportedflag',
            field=models.BigIntegerField(default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='callredirectionflag',
            field=models.BigIntegerField(default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='callreference',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='cellid',
            field=models.FloatField(default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='cgi',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='chargedparty',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='chargelevel',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='city',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='concatsmsrefnumber',
            field=models.BigIntegerField(default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='connectednumber',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='drccallid',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='eventtype',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='firstmccmnc',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='globalcallreference',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='imeistatus',
            field=models.BigIntegerField(default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='intermediatemccmnc',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='lac',
            field=models.FloatField(default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='lastmccmnc',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='lga',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='locationestimate',
            field=models.BigIntegerField(default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='locationnum',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='locationupdatetype',
            field=models.BigIntegerField(default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='maxsmsconcated',
            field=models.BigIntegerField(default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='mscaddress',
            field=models.BigIntegerField(default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='networkcallreference',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='operator',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='partyrelcause',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='rat',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='recordnumber',
            field=models.BigIntegerField(default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='seqnoofcurrentsms',
            field=models.BigIntegerField(default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='sequencenumber',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='servedpdppdnaddress',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='servingnodeipaddress',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='sgwipaddress',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='smstext',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='smsuserdatatype',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='subscribercategory',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='systemtype',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='timebucket',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='timestamp',
            field=models.BigIntegerField(default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='usertype',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='calldetailrecord',
            name='zonecode',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.CreateModel(
            name='LinkedDataCallDetailRecord',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('partyId', models.CharField(choices=[('Party-1', 'Party-1'), ('Party-2', 'Party-2')], max_length=32)),
                ('linkId', models.BigIntegerField(default=-1, null=True)),
                ('geoHash', models.CharField(blank=True, default=None, max_length=16, null=True)),
                ('lac', models.FloatField(default=-1, null=True)),
                ('cellId', models.FloatField(default=-1)),
                ('eventType', models.CharField(default=None, max_length=256, null=True)),
                ('yyyymm', models.BigIntegerField(default=-1, null=True)),
                ('callingIMEI', models.BigIntegerField(default=-1, null=True)),
                ('callingIMSI', models.BigIntegerField(default=-1, null=True)),
                ('callingFirstCgi', models.CharField(default=None, max_length=256, null=True)),
                ('callingLastCgi', models.CharField(default=None, max_length=256, null=True)),
                ('calledFirstCgi', models.CharField(default=None, max_length=256, null=True)),
                ('calledLastCgi', models.CharField(default=None, max_length=256, null=True)),
                ('callingFirstLac', models.FloatField(default=-1, null=True)),
                ('callingFirstCellId', models.FloatField(default=-1, null=True)),
                ('callingLastLac', models.FloatField(default=-1, null=True)),
                ('callingLastCellId', models.FloatField(default=-1, null=True)),
                ('calledFirstLac', models.FloatField(default=-1, null=True)),
                ('calledFirstCellId', models.FloatField(default=-1, null=True)),
                ('calledLastLac', models.FloatField(default=-1, null=True)),
                ('calledLastCellId', models.FloatField(default=-1, null=True)),
                ('callingFirstLocationLat', models.FloatField(default=-1, null=True)),
                ('callingLastLocationLon', models.FloatField(default=-1, null=True)),
                ('callingFirstLocationLon', models.FloatField(default=-1, null=True)),
                ('callingLastLocationLat', models.FloatField(default=-1, null=True)),
                ('calledFirstLocationLat', models.FloatField(default=-1, null=True)),
                ('calledFirstLocationLon', models.FloatField(default=-1, null=True)),
                ('calledLastLocationLat', models.FloatField(default=-1, null=True)),
                ('calledLastLocationLon', models.FloatField(default=-1, null=True)),
                ('callingFirstLocationAddress', models.CharField(default=None, max_length=256, null=True)),
                ('callingFirstLocationCity', models.CharField(default=None, max_length=256, null=True)),
                ('callingFirstLocationLga', models.CharField(default=None, max_length=256, null=True)),
                ('callingLastLocationAddress', models.CharField(default=None, max_length=256, null=True)),
                ('callingLastLocationCity', models.CharField(default=None, max_length=256, null=True)),
                ('callingLastLocationLga', models.CharField(default=None, max_length=256, null=True)),
                ('calledFirstLocationAddress', models.CharField(default=None, max_length=256, null=True)),
                ('calledFirstLocationCity', models.CharField(default=None, max_length=256, null=True)),
                ('calledFirstLocationLga', models.CharField(default=None, max_length=256, null=True)),
                ('calledLastLocationAddress', models.CharField(default=None, max_length=256, null=True)),
                ('calledLastLocationCity', models.CharField(default=None, max_length=256, null=True)),
                ('calledLastLocationLga', models.CharField(default=None, max_length=256, null=True)),
                ('timeStamp', models.BigIntegerField(default=-1, null=True)),
                ('timeBucket', models.CharField(default=None, max_length=256, null=True)),
                ('servedIMSI', models.BigIntegerField(default=-1, null=True)),
                ('servedMSISDN', models.BigIntegerField(default=-1, null=True)),
                ('servedIMEI', models.BigIntegerField(default=-1, null=True)),
                ('servedIMEIFull', models.BigIntegerField(default=-1, null=True)),
                ('callingNumber', models.BigIntegerField(default=-1, null=True)),
                ('calledNumber', models.BigIntegerField(default=-1, null=True)),
                ('recordingEntity', models.BigIntegerField(default=-1, null=True)),
                ('locationLat', models.FloatField(default=-1, null=True)),
                ('locationLon', models.FloatField(default=-1, null=True)),
                ('seizureOrDeliveryTime', models.BigIntegerField(default=-1, null=True)),
                ('answerTime', models.BigIntegerField(default=-1, null=True)),
                ('releaseTime', models.BigIntegerField(default=-1, null=True)),
                ('callDuration', models.BigIntegerField(default=-1, null=True)),
                ('causeForTerm', models.BigIntegerField(default=-1, null=True)),
                ('diagnostics', models.BigIntegerField(default=-1, null=True)),
                ('callReference', models.CharField(default=None, max_length=256, null=True)),
                ('sequenceNumber', models.CharField(default=None, max_length=256, null=True)),
                ('networkCallReference', models.CharField(default=None, max_length=256, null=True)),
                ('mscAddress', models.BigIntegerField(default=-1, null=True)),
                ('systemType', models.CharField(default=None, max_length=256, null=True)),
                ('chargedParty', models.CharField(default=None, max_length=256, null=True)),
                ('calledIMSI', models.BigIntegerField(default=-1, null=True)),
                ('subscriberCategory', models.CharField(default=None, max_length=256, null=True)),
                ('firstMccMnc', models.CharField(default=None, max_length=256, null=True)),
                ('intermediateMccMnc', models.CharField(default=None, max_length=256, null=True)),
                ('lastMccMnc', models.CharField(default=None, max_length=256, null=True)),
                ('userType', models.CharField(default=None, max_length=256, null=True)),
                ('recordNumber', models.BigIntegerField(default=-1, null=True)),
                ('partyRelCause', models.CharField(default=None, max_length=256, null=True)),
                ('chargeLevel', models.CharField(default=None, max_length=256, null=True)),
                ('locationNum', models.CharField(default=None, max_length=256, null=True)),
                ('zoneCode', models.CharField(default=None, max_length=256, null=True)),
                ('accountCode', models.CharField(default=None, max_length=256, null=True)),
                ('calledPortedFlag', models.BigIntegerField(default=-1, null=True)),
                ('calledIMEI', models.BigIntegerField(default=-1, null=True)),
                ('drcCallId', models.CharField(default=None, max_length=256, null=True)),
                ('callRedirectionFlag', models.BigIntegerField(default=-1, null=True)),
                ('globalCallReference', models.CharField(default=None, max_length=256, null=True)),
                ('callerPortedFlag', models.BigIntegerField(default=-1, null=True)),
                ('connectedNumber', models.CharField(default=None, max_length=256, null=True)),
                ('smsUserDataType', models.CharField(default=None, max_length=256, null=True)),
                ('smsText', models.CharField(default=None, max_length=256, null=True)),
                ('maxSMSConcated', models.BigIntegerField(default=-1, null=True)),
                ('concatSMSRefNumber', models.BigIntegerField(default=-1, null=True)),
                ('seqNoOfCurrentSMS', models.BigIntegerField(default=-1, null=True)),
                ('locationEstimate', models.BigIntegerField(default=-1, null=True)),
                ('locationUpdateType', models.BigIntegerField(default=-1, null=True)),
                ('imeiStatus', models.BigIntegerField(default=-1, null=True)),
                ('sgwIPAddress', models.CharField(default=None, max_length=256, null=True)),
                ('servingNodeIPAddress', models.CharField(default=None, max_length=256, null=True)),
                ('accessPointNameNI', models.CharField(default=None, max_length=256, null=True)),
                ('servedPDPPDNAddress', models.CharField(default=None, max_length=256, null=True)),
                ('operator', models.CharField(default=None, max_length=256, null=True)),
                ('rat', models.CharField(default=None, max_length=256, null=True)),
                ('address', models.CharField(default=None, max_length=256, null=True)),
                ('city', models.CharField(default=None, max_length=256, null=True)),
                ('lga', models.CharField(default=None, max_length=256, null=True)),
                ('cgi', models.CharField(default=None, max_length=256, null=True)),
                ('ssCode', models.CharField(default=None, max_length=256, null=True)),
                ('presentationAndScreeningIndicator', models.CharField(default=None, max_length=256, null=True)),
                ('cliIndicator', models.CharField(default=None, max_length=256, null=True)),
                ('callingNumberActual', models.BigIntegerField(default=-1, null=True)),
                ('callingNumberAsName', models.CharField(default=None, max_length=256, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.job')),
            ],
        ),
    ]
