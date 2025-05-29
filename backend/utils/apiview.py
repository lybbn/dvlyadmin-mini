from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

class CustomAPIView(APIView):
    serializer_class=None
    throttle_classes = [UserRateThrottle,AnonRateThrottle]