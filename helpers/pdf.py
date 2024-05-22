import mimetypes

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS, default_url_fetcher
from weasyprint.fonts import FontConfiguration

def weasyprint_local_fetcher(url):
    if url.startswith('local://'):
        filepath = settings.MEDIA_ROOT + url[13:]
        with open(filepath, 'rb') as f:
            file_data = f.read()
        return {
            'string': file_data,
            'mime_type': mimetypes.guess_type(filepath)[0],
        }
    return default_url_fetcher(url)

def render_pdf_response(request, pdf_template, context_params, filename='temp'):
    html_string = render_to_string(pdf_template, context_params)
    #return HttpResponse(html_string)

    font_config = FontConfiguration()
    html = HTML(string=html_string,
                url_fetcher=weasyprint_local_fetcher,
                base_url=request.build_absolute_uri())

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="{filename}.pdf"'.format(filename=filename)

    html.write_pdf(response, font_config=font_config)

    return response
