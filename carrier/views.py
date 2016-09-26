from django.http import HttpResponse
from django.template import loader
from basedata.models import Report


def index(request):
    template = loader.get_template('reports.html')
    reports = Report.objects.order_by('-timeStamp')
    context = {
        'reports' : reports,
    }
    return HttpResponse(template.render(context, request))
