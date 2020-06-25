from rest_framework import serializers

from telegram.models import TelegramUser, Application, Country, FAQ

class TelegramUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TelegramUser
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    # client = serializers.ReadOnlyField(source='client.full_name')

    class Meta:
        model = Application
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQ
        fields = '__all__'
