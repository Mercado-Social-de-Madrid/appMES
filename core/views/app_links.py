import json
import os

from django.conf import settings
from django.http import JsonResponse
from django.views import View


class AppLinksView(View):

    def get(self, request, *args, **kwargs):
        assetlinks_path = settings.ASSETLINKS_FILE

        if not os.path.exists(assetlinks_path):
            return JsonResponse({'error': f"File assetlinks.json is missing. {assetlinks_path}"}, status=404)

        try:
            with open(assetlinks_path, 'r') as file:
                file_content = json.loads(file.read())
        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {e}"}, status=500)

        return JsonResponse(file_content, safe=False)
