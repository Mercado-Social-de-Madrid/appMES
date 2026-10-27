from django.views import View
from django.http import JsonResponse
from cities_light.models import City


class CityView(View):

    def get(self, request, *args, **kwargs):
        region = request.GET.get('region')
        cities = City.objects.filter(subregion=region).order_by('name').values_list('id', 'name') if region else []
        return JsonResponse(list(cities), safe=False)
