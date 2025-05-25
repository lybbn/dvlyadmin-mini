from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

class CustomAPIView(APIView):
    throttle_classes = [UserRateThrottle,AnonRateThrottle]