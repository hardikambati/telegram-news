from rest_framework import (
    views,
    status,
    response,
    permissions,
)


class HealthAPIView(views.APIView):

    permission_classes = [permissions.AllowAny,]

    def get(self, request):
        payload = {
            'details': 'success'
        }
        return response.Response(payload, status=status.HTTP_200_OK)