
from datetime import datetime
from django.http import HttpResponse
import openpyxl
from rest_framework.views import APIView
from api.models import Account, Job

class JobReport(APIView):
    def post(self, request):
        
        requestBody = request.data
        print(requestBody)

        startDate = requestBody["startDate"]
        endDate = requestBody["endDate"]
        
        start_date = datetime.fromtimestamp(startDate)
        end_date = datetime.fromtimestamp(endDate)

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Job Report"

        headers = ['First Name', 'Last Name', 'Designation', 'Department', 'Requested', 'Completed']
        sheet.append(headers)

        accounts = Account.objects.filter(user__is_active=True)
        for account in accounts:
            user = account.user

            jobs = Job.objects.filter(
                createdBy=user,
                createdAt__range=(start_date, end_date)
            )

            total_requested = jobs.count()
            total_completed = jobs.filter(endTime__gt=0).count() 

            row = [
                user.first_name,
                user.last_name,
                account.designation,
                account.department.name if account.department else '',
                total_requested,
                total_completed
            ]
            
            print(row)
            sheet.append(row)

        # Create an HTTP response with the Excel file
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="job_report.xlsx"'
        workbook.save(response)
        return response
