from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from .permissions import IsStaffOrPostOnly

from .serializers import (
    TelegramUserSerializer,
    ApplicationSerializer,
    CountrySerializer,
    FAQSerializer
)

from telegram.models import TelegramUser, Application, Country, FAQ

class CountryListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)


class FAQListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        # print(not request.user.is_anonymous)
        faqs = FAQ.objects.all()
        serializer = FAQSerializer(faqs, many=True)
        return Response(serializer.data)


class ApplicationView(ListCreateAPIView):
    permission_classes = [IsStaffOrPostOnly]
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    # def get(self, request, format=None):
    #     return Response({})
    #
    # def post(self, request):
    #     serializer = ApplicationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
