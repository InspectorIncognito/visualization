from django.http import HttpResponse
from django.template import loader
from AndroidRequests.models import Report


def index(request):
    template = loader.get_template('reports.html')
    reports = Report.objects.order_by('-timeStamp')
    context = {
        'reports' : reports,
    }
    return HttpResponse(template.render(context, request))

def drivers(request, colorId):
    template = loader.get_template('drivers.html')
    return HttpResponse(template.render())

def getDriversReportByInterval(request):
    if request.method == 'GET':
        date_init = request.GET.get('date_init')
        date_end = request.GET.get('date_end')
        carrier = request.GET.get('carrier')


