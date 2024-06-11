from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import pandas as pd
from rest_framework.permissions import IsAuthenticated

from api.models import CallDetailRecord


class ComparisionView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format='json'):
        try:
            job1_id = int(request.data['job1_id'])
            job2_id = int(request.data['job2_id'])

            response_map = {}

            cdr1 = CallDetailRecord.objects.filter(
                job=job1_id
            )
            cdr2 = CallDetailRecord.objects.filter(
                job=job2_id
            )

            cdr1 = cdr1.values_list(
                'servedmsisdn', 'locationlat', 'locationlon'
            )
            cdr2 = cdr2.values_list(
                'servedmsisdn', 'locationlat', 'locationlon'
            )
            df1 = pd.DataFrame(list(cdr1))
            df2 = pd.DataFrame(list(cdr2))

            merged_df = pd.merge(df1, df2, how='inner', on=[0])
            print(merged_df)

            for index, row in merged_df.iterrows():
                servedmsisdn = int(row[0])
                lat1 = row['1_x']
                lng1 = row['2_x']
                lat2 = row['1_y']
                lng2 = row['2_y']
                if servedmsisdn not in response_map:
                    response_map[servedmsisdn] = []

                response_map[servedmsisdn].append({
                    'lat': lat1,
                    'lng': lng1
                })

                response_map[servedmsisdn].append({
                    'lat': lat2,
                    'lng': lng2
                })

            return Response(response_map, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response({'error': ex}, status=status.HTTP_400_BAD_REQUEST)
