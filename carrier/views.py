# -*- coding: utf-8 -*

from django.http import HttpResponse
from django.template import loader
from AndroidRequests.models import Report, EventForBus, Service, Event, Bus
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, date
import json, pytz


def index(request):
    template = loader.get_template('reports.html')
    return HttpResponse(template.render(request=request))


def drivers(request):
    template = loader.get_template('drivers.html')
    carrier = 7  # TODO Select carrier depending on who is logged.
    services = Service.objects.filter(color_id=carrier)
    buses = Bus.objects.filter(service__in=[service.service for service in services])
    buses = buses.exclude(registrationPlate__icontains='dummyLPt')
    plates = [bus.registrationPlate for bus in buses]
    context = {
        'services': services,
        'plates': plates,
    }
    return HttpResponse(template.render(context, request))


def physical(request):
    template = loader.get_template('physical.html')
    carrier = 7  # TODO Select carrier depending on who is logged.
    services = Service.objects.filter(color_id=carrier)
    context = {
        'services': services
    }
    return HttpResponse(template.render(context, request))


def getPhysicalHeaders(request):
    carrier = 7  # TODO Select carrier depending on who is logged.
    events = Event.objects.filter(category="estado físico", eventType="bus")
    events = [event.name for event in events]
    headerInfo = EventForBus.objects.filter(event__category='estado físico')
    headerInfo = headerInfo.filter(
        bus__service__in=[service.service for service in Service.objects.filter(color_id=carrier)])
    today = date.today()
    year = today.year
    if today.month <= 3:
        last_month = today.month + 12 - 3
        year = year - 1
    else:
        last_month = today.month - 3
    headerInfo = headerInfo.filter(timeCreation__gte=date(year, last_month, today.day)).exclude(
        bus__registrationPlate="dummyLPt")
    headerInfo = headerInfo.filter(fixed=False)
    response = {}
    for ev in events:
        q = headerInfo.filter(event__name=ev)
        q = q.distinct('bus__registrationPlate')
        response[ev] = q.count()
    return JsonResponse(response, safe=False)


def getFreeReport(request):  # TODO Change model to support filtering by carrier
    reports = Report.objects.order_by('-timeStamp')
    response = [report.getDictionary() for report in reports]
    return JsonResponse(response, safe=False)


def getDriversReport(request):
    if request.method == 'GET':
        events = Event.objects.filter(category="conductor")
        events = [event.name for event in events]
        pos = range(0, len(events))
        eventToPos = {name: pos for name, pos in zip(events, pos)}

        def change(dict):
            dict["type"] = eventToPos[dict["type"]]
            return dict

        carrier = 7  # TODO Select carrier depending on who is logged.
        date_init = request.GET.get('date_init')
        date_end = request.GET.get('date_end')
        hour1 = int(request.GET.get('hour1'))
        hour2 = int(request.GET.get('hour2'))
        plates = request.GET.get('plate')
        serv = request.GET.get('service')
        hour2 = (hour2 + 24) if hour2 < hour1 else hour2
        hours = [hour % 24 for hour in range(hour1, hour2 + 1)]
        query = EventForBus.objects.filter(
            bus__service__in=[service.service for service in Service.objects.filter(color_id=carrier)])
        query = query.filter(event__category="conductor")
        query = query.filter(timeCreation__range=[date_init, date_end])
        query = query.exclude(bus__registrationPlate__icontains="dummyLPt")
        if plates:
            plates = json.loads(plates)
            plateFilter = reduce(lambda x, y: x | y, [Q(bus__registrationPlate=plate) for plate in plates])
            query = query.filter(plateFilter)
        if serv:
            serv = json.loads(serv)
            serviceFilter = reduce(lambda x, y: x | y, [Q(bus__service=ser) for ser in serv])
            query = query.filter(serviceFilter)
        hourFilter = reduce(lambda x, y: x | y, [Q(timeCreation__hour=h) for h in hours])
        # minuteFilter = reduce(lambda x, y: x | y, [Q(timeCreation__minute=m) for m in minutes])
        query = query.filter(hourFilter)
        # query = query.filter(minuteInterval)
        data = {
            "reports": [change(report.getDictionary()) for report in query],
            "types": events
        }
        return JsonResponse(data, safe=False)


def driversTable(request):
    template = loader.get_template('driversTable.html')
    return HttpResponse(template.render(request=request))


def getDriversTable(request):
    carrier = 7  # TODO Select carrier depending on who is logged.
    query = EventForBus.objects.filter(
        bus__service__in=[service.service for service in Service.objects.filter(color_id=carrier)])
    query = query.filter(event__category="conductor")
    query = query.exclude(bus__registrationPlate__icontains="dummylpt")
    query = query.exclude(event__id='evn00233')
    today = datetime.now(pytz.timezone('Chile/Continental'))
    # query = query.filter(timeCreation__year=str(today.year),
    #                       timeCreation__month=str(today.month),
    #                       timeCreation__day=str(today.day))
    data = {
        'data': [report.getDictionary() for report in query]
    }
    return JsonResponse(data, safe=False)


def physicalTable(request):
    template = loader.get_template('physicalTable.html')
    return HttpResponse(template.render(request=request))


def getPhysicalTable(request):
    carrier = 7  # TODO Select carrier depending on who is logged.
    query = EventForBus.objects.filter(
        bus__service__in=[service.service for service in Service.objects.filter(color_id=carrier)])
    query = query.filter(event__category="estado físico").exclude(event__id="evn00225")
    query = query.exclude(bus__registrationPlate__icontains="dummyLPt")
    query = query.distinct("event__name", "bus__registrationPlate")
    query = query.exclude(fixed=True)
    data = {
        'data': [report.getDictionary() for report in query]
    }
    return JsonResponse(data, safe=False)


def getPhysicalReport(request):
    if request.method == 'GET':
        events = Event.objects.filter(category="estado físico", eventType="bus")
        events = [event.name for event in events]
        pos = range(0, len(events))
        eventToPos = {name: pos for name, pos in zip(events, pos)}

        def change(dict):
            dict["type"] = eventToPos[dict["type"]]
            return dict

        carrier = 7  # TODO Select carrier depending on who is logged.
        date_init = request.GET.get('date_init')
        date_end = request.GET.get('date_end')
        hour1 = int(request.GET.get('hour1'))
        hour2 = int(request.GET.get('hour2'))
        plates = request.GET.get('plate')
        serv = request.GET.get('service')
        hour2 = (hour2 + 24) if hour2 < hour1 else hour2
        hours = [hour % 24 for hour in range(hour1, hour2 + 1)]
        query = EventForBus.objects.filter(
            bus__service__in=[service.service for service in Service.objects.filter(color_id=carrier)])
        query = query.filter(event__category="estado físico")
        query = query.filter(timeCreation__range=[date_init, date_end])
        query = query.exclude(bus__registrationPlate__icontains="dummyLPt")
        query = query.exclude(fixed=True)
        if plates:
            plates = json.loads(plates)
            plateFilter = reduce(lambda x, y: x | y, [Q(bus__registrationPlate=plate) for plate in plates])
            query = query.filter(plateFilter)
        if serv:
            serv = json.loads(serv)
            serviceFilter = reduce(lambda x, y: x | y, [Q(bus__service=ser) for ser in serv])
            query = query.filter(serviceFilter)
        hourFilter = reduce(lambda x, y: x | y, [Q(timeCreation__hour=h) for h in hours])
        # minuteFilter = reduce(lambda x, y: x | y, [Q(timeCreation__minute=m) for m in minutes])
        query = query.filter(hourFilter)
        # query = query.filter(minuteInterval)
        data = {
            "reports": [change(report.getDictionary()) for report in query],
            "types": events
        }
        return JsonResponse(data, safe=False)


def updatePhysical(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        event = EventForBus.objects.get(id=id)
        event.fixed = True
        event.save()
        ans = "True"
        return JsonResponse(ans, safe=False)


def fullTable(request):
    template = loader.get_template('fullTable.html')
    events = Event.objects.filter(eventType="bus").distinct("category")
    types = [event.category for event in events]
    context = {
        'types': types,
    }
    return HttpResponse(template.render(context, request))


def getFullTable(request):
    if request.method == 'GET':
        carrier = 7  # TODO Select carrier depending on who is logged.
        query = EventForBus.objects.filter(
            bus__service__in=[service.service for service in Service.objects.filter(color_id=carrier)])
        query = query.exclude(bus__registrationPlate__icontains="dummyLPt")
        date_init = request.GET.get('date_init')
        date_end = request.GET.get('date_end')
        types = request.GET.get('types')
        query = query.filter(timeCreation__range=[date_init, date_end])
        if types:
            types = json.loads(types)
            typeFilter = reduce(lambda x, y: x | y, [Q(event__category = type) for type in types])
            query = query.filter(typeFilter)

        data = {
            'data': [report.getDictionary() for report in query]
        }
        return JsonResponse(data, safe=False)

def maptest(request):
    template = loader.get_template('maptest.html')
    return HttpResponse(template.render(request=request))

# from AndroidRequests.models import EventForBus, Service
# from datetime import datetime, date, timedelta
# from random import randint
# import pytz
#
# query = EventForBus.objects.filter(bus__service__in=[service.service for service in Service.objects.filter(color_id=7)])
# events = query.filter(event__category='conductor')[:12]
# for event in events:
#     time = datetime.now(pytz.timezone('Chile/Continental'))
#     delta = timedelta(seconds=randint(0, 3600 * 5))
#     time = time - delta
#     event.timeCreation = time
#     event.save()
