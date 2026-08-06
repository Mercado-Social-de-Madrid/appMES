import logging
from django.views import View
from django.http import JsonResponse
from cities_light.models import SubRegion, City


_logger = logging.getLogger(__name__)

class CityView(View):

    def get(self, request, *args, **kwargs):
        subregion = request.GET.get('city')
        cities = City.objects.filter(subregion=subregion).values_list('id', 'name')
        _logger.debug(f"cities: {cities}")


        return JsonResponse(list(cities), safe=False)
