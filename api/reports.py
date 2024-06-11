import os
import uuid
import json
import openpyxl
from datetime import datetime, time, timedelta, date
from django.conf import settings
from django_cron import CronJobBase, Schedule
from django.db import connections
from .models import Job, DailyJobReports
import time


class DailyJobReportsCron(CronJobBase):
    RUNS_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUNS_EVERY_MINS)
    code = str(uuid.uuid4())

    def report(self, db_name):
        print(
            "Running cron job to collect data of jobs created and failed in the last 24 hours"
        )
        try:
            print("Collecting data of jobs created and failed in the last 24 hours")

            new_connection = connections[db_name]
            print(new_connection)

            if db_name == "default":
                db_number = 66
            elif db_name == "prod66":
                db_number = 66
            elif db_name == "prod11":
                db_number = 11
            elif db_name == "prod170":
                db_number = 170
            elif db_name == "prod226":
                db_number = 226

            # #today's timestamp
            # midnight = (((int(time.time())*1000) // 86400000)) * 86400000
            # print("Today's timestamp: {}".format(midnight))

            # #yesterday's timestamp
            # yesterday = (((int(time.time())*1000) // 86400000)) * 86400000 - 86400000
            # print("Yesterday's timestamp: {}".format(yesterday))

            today = datetime.now()
            yesterday = today - timedelta(days=1)

            midnight = today.replace(hour=0, minute=0, second=0, microsecond=0)
            print(midnight)

            previous_midnight = yesterday.replace(
                hour=0, minute=0, second=0, microsecond=0
            )
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

            print("---------------Server - {}----------------".format(db_name))
            print("Total Jobs Created : {}".format(total_jobs))
            print("Total Jobs Failed: {}".format(failed_jobs))
            print("Total Jobs Completed: {}".format(completed_jobs))
            print("Total Jobs Pending: {}".format(pending_jobs))

            # insert data into DailyJobReports table

            report = DailyJobReports(
                pendingjobs=pending_jobs,
                completedjobs=completed_jobs,
                failedjobs=failed_jobs,
                totaljobs=total_jobs,
                createdAt=midnight,
                servernumber=db_number,
            )
            report.save(using="default")

        except Exception as ex:
            print(ex)

    def do(self):
        for db_name in settings.DATABASES:
            self.report(db_name)


class WeeklyReportsCron(CronJobBase):
    RUNS_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUNS_EVERY_MINS)
    code = str(uuid.uuid4())

    def report(self, db_name, days):
        print("Running cron job to create a weekly report")

        dataForWorkBook = [["Date", "Total Jobs Created", "Total Jobs Completed"]]

        for day in range(0, days):
            try:
                new_connection = connections[db_name]
                print(new_connection)

                if db_name == "default":
                    db_number = 66
                elif db_name == "prod66":
                    db_number = 66
                elif db_name == "prod11":
                    db_number = 11
                elif db_name == "prod170":
                    db_number = 170
                elif db_name == "prod226":
                    db_number = 226

                now = datetime.now()

                today = now - timedelta(days=day)
                yesterday = today - timedelta(days=1)


                midnight = today.replace(hour=0, minute=0, second=0, microsecond=0)

                previous_midnight = yesterday.replace(
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

                # insert data into DailyJobReports table

                report = DailyJobReports(
                    pendingjobs=pending_jobs,
                    completedjobs=completed_jobs,
                    failedjobs=failed_jobs,
                    totaljobs=total_jobs,
                    createdAt=midnight,
                    servernumber=db_number,
                )
                report.save(using="default")

                dataForWorkBook.append([previous_midnight, total_jobs, completed_jobs])

            except Exception as ex:
                print(ex)

        return dataForWorkBook

    def writeToExcel(self, data):
        try:
            workbook = openpyxl.Workbook()
            sheet = workbook.active

            for row in data:
                sheet.append(row)

            # check if dir exists
            if not os.path.exists(settings.REPORTS_PATH):
                os.makedirs(settings.REPORTS_PATH)

            # name file
            current_date = datetime.now().strftime("%d%m%Y")
            filename = f"{settings.REPORTS_PATH}data_{current_date}.xlsx"

            workbook.save(filename)

            return "Succesfully saved"

        except Exception as ex:
            print(ex)

    def do(self):
        counter = int(
            input(
                "Prompt : Enter the number of days for which you want the report. Ex : 7 will generate a report for the last days, excluding today\n"
            )
        )

        for db_name in settings.DATABASES:
            print(db_name)
            dataForWorkBook = self.report(db_name, counter)
            self.writeToExcel(dataForWorkBook)


class AccountBasedReportsCron(CronJobBase):
    RUNS_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUNS_EVERY_MINS)
    code = str(uuid.uuid4())

    def report(self, db_name, day, account):
        print(
            "Running cron job to collect data of jobs created and failed in the last 24 hours"
        )
        try:
            print("Collecting data of jobs created and failed in the last 24 hours")

            new_connection = connections[db_name]
            print(new_connection)

            if db_name == "default":
                db_number = 180
            elif db_name == "prod66":
                db_number = 66
            elif db_name == "prod11":
                db_number = 11
            elif db_name == "prod170":
                db_number = 170
            elif db_name == "prod226":
                db_number = 226

            today = datetime.now()
            yesterday = today - timedelta(days=day)

            midnight = today.replace(hour=0, minute=0, second=0, microsecond=0)

            previous_midnight = yesterday.replace(
                hour=0, minute=0, second=0, microsecond=0
            )

            total_jobs = (
                Job.objects.using(db_name)
                .filter(
                    createdAt__lt=midnight,
                    createdAt__gte=previous_midnight,
                    createdBy=account,
                )
                .count()
            )
            failed_jobs = (
                Job.objects.using(db_name)
                .filter(
                    createdAt__lt=midnight,
                    createdAt__gte=previous_midnight,
                    status="FAILED",
                    createdBy=account,
                )
                .count()
            )
            completed_jobs = (
                Job.objects.using(db_name)
                .filter(
                    createdAt__lt=midnight,
                    createdAt__gte=previous_midnight,
                    status="FINISHED",
                    createdBy=account,
                )
                .count()
            )
            pending_jobs = (
                Job.objects.using(db_name)
                .filter(
                    createdAt__lt=midnight,
                    createdAt__gte=previous_midnight,
                    status="PENDING",
                    createdBy=account,
                )
                .count()
            )

            print(
                "---------------Report for Account Acct- {}----------------".format(
                    5 - account
                )
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

            # insert data into DailyJobReports table

            report = DailyJobReports(
                pendingjobs=pending_jobs,
                completedjobs=completed_jobs,
                failedjobs=failed_jobs,
                totaljobs=total_jobs,
                createdAt=midnight,
                servernumber=db_number,
            )
            report.save(using="default")

        except Exception as ex:
            print(ex)

    def do(self):
        counter = 7
        accounts = [5, 6, 7, 8, 9]

        for day in range(1, counter + 1):
            for account in accounts:
                self.report("default", day, account)
                time.sleep(2)


class AllAccountBasedReportsCron(CronJobBase):
    RUNS_EVERY_MINS = 60  # Adjust as necessary
    schedule = Schedule(run_every_mins=RUNS_EVERY_MINS)
    code = str(uuid.uuid4())

    def report(self, db_name, start_date, end_date, account):
        print(f"Running report for account: {account} from {start_date} to {end_date}")

        try:
            new_connection = connections[db_name]
            print(f"Connected to database: {db_name}")

            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)  # include the end day fully

            total_jobs = Job.objects.using(db_name).filter(
                createdAt__range=(start_date, end_date),
                createdBy=account
            ).count()

            failed_jobs = Job.objects.using(db_name).filter(
                createdAt__range=(start_date, end_date),
                status="FAILED",
                createdBy=account
            ).count()

            completed_jobs = Job.objects.using(db_name).filter(
                createdAt__range=(start_date, end_date),
                status="FINISHED",
                createdBy=account
            ).count()

            pending_jobs = Job.objects.using(db_name).filter(
                createdAt__range=(start_date, end_date),
                status="PENDING",
                createdBy=account
            ).count()

            print(f"Account: {account}, Total Jobs Created: {total_jobs}")
            print(f"Account: {account}, Total Jobs Failed: {failed_jobs}")
            print(f"Account: {account}, Total Jobs Completed: {completed_jobs}")
            print(f"Account: {account}, Total Jobs Pending: {pending_jobs}")

            report = DailyJobReports(
                pendingjobs=pending_jobs,
                completedjobs=completed_jobs,
                failedjobs=failed_jobs,
                totaljobs=total_jobs,
                createdAt=datetime.now(),
                servernumber=db_name
            )
            report.save(using=db_name)

        except Exception as ex:
            print(f"Error while running report for account {account}: {ex}")

    def do(self):
        start_date = '2024-04-27'
        end_date = '2024-05-05'
        accounts = range(1, 56) 

        for account in accounts:
            self.report("default", start_date, end_date, account)
            time.sleep(2)

