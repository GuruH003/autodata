from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

import pandas as pd
import json
import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from geopy.distance import great_circle
from shapely.geometry import MultiPoint
from sklearn.metrics.pairwise import euclidean_distances
from rest_framework.permissions import IsAuthenticated

kms_per_radian = 6371.0088
epsilon = 2 / kms_per_radian
k_means_n_clusters = 3


def get_centermost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(
        cluster, key=lambda point: great_circle(point, centroid).m)
    return tuple(centermost_point)


class ClusterView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format='json'):
        clustering_type = request.data['type']
        locations_list = request.data['locations']
        locations_list = [np.array(x) for x in locations_list]
        locations_list = np.array(locations_list)

        try:
            if clustering_type == 'DBSCAN':
                db = DBSCAN(
                    eps=epsilon,
                    min_samples=1,
                    algorithm='ball_tree',
                    metric='haversine'
                ).fit(np.radians(locations_list))
                cluster_labels = db.labels_

                print(cluster_labels)

                num_clusters = len(set(cluster_labels))

                clusters = pd.Series(
                    [locations_list[cluster_labels == n]
                     for n in range(num_clusters)]
                )
                centermost_points = clusters.map(get_centermost_point)
                locations_response = []
                for x in centermost_points:
                    coord = {
                        'lat': x[0],
                        'lng': x[1]
                    }
                    locations_response.append(coord)

                return Response(locations_response, status=status.HTTP_200_OK)

            elif clustering_type == 'K-MEANS':
                kmeans = KMeans(
                    n_clusters=k_means_n_clusters,
                    random_state=0
                ).fit(locations_list)
                cluster_labels = kmeans.labels_

                num_clusters = len(set(cluster_labels))
                dists = euclidean_distances(kmeans.cluster_centers_)
                tri_dists = dists[np.triu_indices(3, 1)]
                mean_dist = tri_dists.mean()

                clusters = pd.Series(
                    [locations_list[cluster_labels == n]
                     for n in range(num_clusters)]
                )
                centermost_points = clusters.map(get_centermost_point)
                locations_response = []
                for x in centermost_points:
                    coord = {
                        'lat': x[0],
                        'lng': x[1]
                    }
                    locations_response.append(coord)

                return Response(
                    locations_response,
                    status=status.HTTP_200_OK
                )

            else:
                return Response({'error': 'Invalid type'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'error': ex}, status=status.HTTP_400_BAD_REQUEST)
