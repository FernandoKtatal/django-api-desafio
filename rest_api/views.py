from django.http import QueryDict
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Weather, Temperature
from .serializers import WeatherSerializer


@api_view(['GET', 'POST'])
def weather_list(request):
    if request.method == 'GET':
        weater = Weather.objects.all().order_by('id')
        date = request.query_params.get('date', None)
        lat = request.query_params.get('lat', None)
        lon = request.query_params.get('lon', None)
        city = request.query_params.get('city', None)
        state = request.query_params.get('state', None)
        sort = request.query_params.get('sort', None)

        if date:
            weater = weater.filter(date=date)
        if lat:
            weater = weater.filter(lat__in=lat)
        if lon:
            weater = weater.filter(lon__in=lon)
        if city:
            city = city.split(',')
            weater = weater.filter(city__iregex=r'(' + '|'.join(city) + ')')
        if state:
            state = state.split(',')
            weater = weater.filter(state__iregex=r'(' + '|'.join(state) + ')')

        if sort:
            weater = weater.order_by(sort, 'id')

        serializer = WeatherSerializer(weater, many=True)

        if len(weater) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data)

    elif request.method == 'POST':
        body = request.data
        try:
            if isinstance(request.data, QueryDict):
                body = dict(request.data.lists())
                body['date'] = body['date'][0]
                body['lat'] = body['lat'][0]
                body['lon'] = body['lon'][0]
                body['city'] = body['city'][0]
                body['state'] = body['state'][0]
                body['temperatures'] = [float(value) for value in body.get('temperatures')]

            serializer = WeatherSerializer(data=body)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def weather_detail(request, pk):
    try:
        weather = Weather.objects.get(pk=pk)
    except Weather.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WeatherSerializer(weather)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = WeatherSerializer(weather, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        weather.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
