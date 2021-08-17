from rest_framework import serializers
from .models import Weather, Temperature


class TemperatureSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.temperature


class WeatherSerializer(serializers.ModelSerializer):
    date = serializers.DateField(required=True)
    lat = serializers.DecimalField(required=True, max_digits=7, decimal_places=4)
    lon = serializers.DecimalField(required=True, max_digits=7, decimal_places=4)
    city = serializers.CharField(required=True, max_length=60)
    state = serializers.CharField(required=True, max_length=60)
    temperatures = TemperatureSerializer(many=True, read_only=True)

    def to_internal_value(self, value):
        return value

    class Meta:
        model = Weather
        fields = '__all__'

    def create(self, validated_data):
        temperatures_data = validated_data.pop('temperatures')
        weather = Weather.objects.create(**validated_data)
        for temperature_data in temperatures_data:
            dict = {'temperature': temperature_data}
            Temperature.objects.create(weather=weather, **dict)
        return weather

    def update(self, instance, validated_data):
        instance.date = validated_data.get('date', instance.date)
        instance.lat = validated_data.get('lat', instance.lat)
        instance.lon = validated_data.get('lon', instance.lon)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)

        temperatures_data = validated_data.pop('temperatures')
        temperatures_to_remove = Temperature.objects.filter(weather_id=instance.id)
        temperatures_to_remove.delete()
        for temperature in temperatures_data:
            dict = {'temperature': temperature}
            Temperature.objects.create(weather=instance, **dict)
        instance.save()

        return instance
