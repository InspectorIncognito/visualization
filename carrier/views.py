from django.http import HttpResponse
from django.template import loader
from AndroidRequests.models import Report, EventForBus, Service
from django.http import JsonResponse
from django.db.models import Q


def index(request):
    template = loader.get_template('reports.html')
    reports = Report.objects.order_by('-timeStamp')
    context = {
        'reports': reports,
    }
    return HttpResponse(template.render(context, request))


def drivers(request, colorId):
    template = loader.get_template('drivers.html')
    return HttpResponse(template.render())


def getDriversReportByInterval(request):
    if request.method == 'GET':
        date_init = request.GET.get('date_init')
        date_end = request.GET.get('date_end')
        hour1 = int(request.GET.get('hour1'))
        hour2 = int(request.GET.get('hour2'))
        carrier = request.GET.get('carrier')
        plate = request.GET.get('plate')
        serv = request.GET.get('service')
        hour2 = (hour2 + 24) if hour2 < hour1 else hour2
        hours = [hour % 24 for hour in range(hour1, hour2 + 1)]
        query = EventForBus.objects.filter(
            bus__service__in=[service.service for service in Service.objects.filter(color_id=carrier)])
        query = query.filter(event__category="conductor")
        query = query.filter(timeCreation__range=[date_init, date_end])
        query = (query.filter(bus__registrationPlate=plate) if plate else query)
        query = (query.filter(bus__service=serv) if serv else query)
        hourInterval = reduce(lambda x, y: x | y, [Q(timeCreation__hour=h) for h in hours])
        # minuteInterval = reduce(lambda x, y: x | y, [Q(timeCreation__minute=m) for m in minutes])
        query = query.filter(hourInterval)
        # query = query.filter(minuteInterval)
        return JsonResponse([report.getDictionary() for report in query], safe=False)
