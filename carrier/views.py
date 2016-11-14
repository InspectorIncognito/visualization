# -*- coding: utf-8 -*

from django.http import HttpResponse
from django.template import loader
from AndroidRequests.models import *
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
import json, pytz

@login_required
def index(request):
    template = loader.get_template('test.html')
    return HttpResponse(template.render(request=request))

@login_required
def reports(request):
    template = loader.get_template('reports.html')
    return HttpResponse(template.render(request=request))

@login_required
def drivers(request):
    template = loader.get_template('drivers.html')
    carrier = request.user.carrieruser.carrier.color_id
    services = Service.objects.filter(color_id=carrier)
    ba = Busassignment.objects.filter(service__in=[service.service for service in services])
    ba = ba.values_list('uuid', flat = True)
    buses = Busv2.objects.filter(id__in=ba)
    buses = buses.exclude(registrationPlate__icontains='No Info.').order_by("registrationPlate")
    plates = [bus.registrationPlate for bus in buses]
    context = {
        'services': services,
        'plates': plates,
    }
    return HttpResponse(template.render(context, request))

@login_required
def physical(request):
    template = loader.get_template('physical.html')
    carrier = request.user.carrieruser.carrier.color_id
    services = Service.objects.filter(color_id=carrier)
    context = {
        'services': services
    }
    return HttpResponse(template.render(context, request))

@login_required
def getPhysicalHeaders(request):
    carrier = request.user.carrieruser.carrier.color_id
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

@login_required
def getReports(request):
    if request.method == 'GET':
        carrier = request.user.carrieruser.carrier.color_id
        reports = Report.objects.all() #TODO Filter depending on carrier (after transform)
        data = {
            'data' : [report.getDictionary() for report in reports]
        }
        return JsonResponse(data, safe=False)

@login_required
def getDriversReport(request):
    if request.method == 'GET':
        events = Event.objects.filter(category="conductor")
        events = [event.name for event in events]
        pos = range(0, len(events))
        eventToPos = {name: pos for name, pos in zip(events, pos)}

        def change(dict):
            dict["type"] = eventToPos[dict["type"]]
            return dict

        carrier = request.user.carrieruser.carrier.color_id
        date_init = request.GET.get('date_init')
        date_end = request.GET.get('date_end')
        plates = request.GET.get('plate')
        serv = request.GET.get('service')
        query = EventForBusv2.objects.filter(
            busassignment__service__in=[service.service for service in Service.objects.filter(color_id=carrier)])
        query = query.filter(event__category="conductor")
        query = query.filter(timeCreation__range=[date_init, date_end])
        query = query.exclude(bus__registrationPlate__icontains="No Info.")
        if plates:
            plates = json.loads(plates)
            plateFilter = reduce(lambda x, y: x | y, [Q(bus__registrationPlate=plate) for plate in plates])
            query = query.filter(plateFilter)
        if serv:
            serv = json.loads(serv)
            serviceFilter = reduce(lambda x, y: x | y, [Q(bus__service=ser) for ser in serv])
            query = query.filter(serviceFilter)
        data = {
            "reports": [change(report.getDictionary()) for report in query],
            "types": events
        }
        return JsonResponse(data, safe=False)

@login_required
def driversTable(request):
    template = loader.get_template('driversTable.html')
    return HttpResponse(template.render(request=request))

@login_required
def getDriversTable(request):
    carrier = request.user.carrieruser.carrier.color_id
    query = EventForBusv2.objects.filter(
        busassignment__service__in=[service.service for service in Service.objects.filter(color_id=carrier)])
    query = query.filter(event__category="conductor")
    query = query.exclude(busassignment__uuid__registrationPlate__icontains="No Info.")
    query = query.exclude(event__id='evn00233')
    today = datetime.now(pytz.timezone('Chile/Continental'))
    # query = query.filter(timeCreation__year=str(today.year),
    #                       timeCreation__month=str(today.month),
    #                       timeCreation__day=str(today.day))
    data = {
        'data': [report.getDictionary() for report in query]
    }
    return JsonResponse(data, safe=False)

@login_required
def physicalTable(request):
    template = loader.get_template('physicalTable.html')
    return HttpResponse(template.render(request=request))

@login_required
def getPhysicalTable(request):
    carrier = request.user.carrieruser.carrier.color_id
    query = EventForBus.objects.filter(
        bus__service__in=[service.service for service in Service.objects.filter(color_id=carrier)])
    query = query.filter(event__category="estado físico", fixed = False).exclude(event__id="evn00225")
    query = query.exclude(bus__registrationPlate__icontains="dummyLPt")
    query = query.distinct("event__name", "bus__registrationPlate")
    data = {
        'data': [report.getDictionary() for report in query]
    }
    return JsonResponse(data, safe=False)

@login_required
def getPhysicalReport(request):
    if request.method == 'GET':
        events = Event.objects.filter(category="estado físico", eventType="bus")
        events = [event.name for event in events]
        pos = range(0, len(events))
        eventToPos = {name: pos for name, pos in zip(events, pos)}

        def change(dict):
            dict["type"] = eventToPos[dict["type"]]
            return dict

        carrier = request.user.carrieruser.carrier.color_id
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
        query = query.filter(event__category="estado físico", fixed = False)
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

@login_required
def updatePhysical(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        event = EventForBus.objects.get(id=id)
        event.fixed = True
        event.save()
        ans = "True"
        return JsonResponse(ans, safe=False)

@login_required
def fullTable(request):
    template = loader.get_template('fullTable.html')
    events = Event.objects.filter(eventType="bus").distinct("category")
    types = [event.category for event in events]
    context = {
        'types': types,
    }
    return HttpResponse(template.render(context, request))

@login_required
def getFullTable(request):
    if request.method == 'GET':
        carrier = request.user.carrieruser.carrier.color_id
        #query = EventForBus.objects.filter(
        #    bus__service__in=[service.service for service in Service.objects.filter(color_id=carrier)])
        query = EventForBus.objects.all()
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

@login_required
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
