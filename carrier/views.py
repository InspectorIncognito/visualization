from django.http import HttpResponse
from django.template import loader
from AndroidRequests.models import Report, EventForBus, Service, Event
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime
import json, pytz


def index(request):
    template = loader.get_template('reports.html')
    reports = Report.objects.order_by('-timeStamp')
    context = {
        'reports': reports,
    }
    return HttpResponse(template.render(context, request))


def drivers(request):
    template = loader.get_template('drivers.html')
    carrier = 4 #TODO Select carrier depending on who is logged.
    services = Service.objects.filter(color_id = carrier)
    context = {
        'services': services,
    }
    return HttpResponse(template.render(context,request))


def getDriversReport(request):
    if request.method == 'GET':
        events = Event.objects.filter(category = "conductor")
        events = [event.name for event in events]
        pos = range(0, len(events))
        eventToPos = {name: pos for name,pos in zip(events,pos) }
        def change(dict):
            dict["type"] = eventToPos[dict["type"]]
            return dict
        carrier = 4  # TODO Select carrier depending on who is logged.
        date_init = request.GET.get('date_init')
        date_end = request.GET.get('date_end')
        hour1 = int(request.GET.get('hour1'))
        hour2 = int(request.GET.get('hour2'))
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
        data = {
            "reports": [change(report.getDictionary()) for report in query],
            "types" : events
        }
        return JsonResponse(data, safe=False)

def driversTable(request):
    template = loader.get_template('driversTable.html')
    return HttpResponse(template.render(request = request))

def getDriversTable(request):
    carrier = 4  # TODO Select carrier depending on who is logged.
    query = EventForBus.objects.filter(
        bus__service__in=[service.service for service in Service.objects.filter(color_id=carrier)])
    query = query.filter(event__category="conductor")
    today = datetime.now(pytz.timezone('Chile/Continental'))
    # query = query.filter(timeStamp__year=str(today.year),
    #                     timeStamp__month=str(today.month),
    #                     timeStamp__day=str(today.day))
    data = {
        'data' : [report.getDictionary() for report in query]
    }
    return JsonResponse(data, safe=False)

