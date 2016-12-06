# -*- coding: utf-8 -*

from django.http import HttpResponse
from django.template import loader
from AndroidRequests.models import *
from accounts.models import *
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, date, timedelta, time
from django.contrib.auth.decorators import login_required
import json, pytz

def filter(request):
    user = request.user.getUser()
    if user.color() == "all":
        return Q()
    else:
        return Q(color_id = user.color())

@login_required
def index(request):
    template = loader.get_template('test.html')
    return HttpResponse(template.render(request=request))

@login_required
def getCount(request):
    events = Event.objects.filter(eventType="bus").distinct("category")
    types = [event.category for event in events]
    datatype = {}
    query = EventForBusv2.objects.filter(
        busassignment__service__in=[service.service for service in Service.objects.filter(filter(request))])
    query = query.exclude(busassignment__uuid__registrationPlate__icontains="No Info.")
    for type in types:
        datatype[type] =  query.filter(event__category = type).count()
    groups = {}
    for type in types:

        events = Event.objects.filter(eventType="bus", category = type)
        names = [event.name for event in events]
        groups[type] = {}
        for name in names:
            groups[type][name] = query.filter(event__category=type, event__name = name).count()

    data = {
        'datatype': datatype,
        'groups': groups,
    }
    return JsonResponse(data, safe=False)

@login_required
def reports(request):
    template = loader.get_template('reports.html')
    return HttpResponse(template.render(request=request))

@login_required
def drivers(request):
    template = loader.get_template('drivers.html')
    services = Service.objects.filter(filter(request))
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
    services = Service.objects.filter(filter(request))
    context = {
        'services': services
    }
    return HttpResponse(template.render(context, request))

@login_required
def getPhysicalHeaders(request):
    events = Event.objects.filter(category="estado físico", eventType="bus")
    events = [event.name for event in events]
    headerInfo = EventForBusv2.objects.filter(event__category='estado físico')
    headerInfo = headerInfo.filter(
        busassignment__service__in=[service.service for service in Service.objects.filter(filter(request))])
    today = date.today()
    year = today.year
    if today.month <= 3:
        last_month = today.month + 12 - 3
        year = year - 1
    else:
        last_month = today.month - 3
    headerInfo = headerInfo.filter(timeCreation__gte=date(year, last_month, today.day)).exclude(
        busassignment__uuid__registrationPlate__icontains="No Info.")
    response = {}
    for ev in events:
        q = headerInfo.filter(event__name=ev)
        q = q.order_by("busassignment__uuid__registrationPlate", "-timeStamp").distinct('busassignment__uuid__registrationPlate')
        q = q.filter(fixed = False)
        response[ev] = q.count()
    return JsonResponse(response, safe=False)

@login_required
def getReports(request):
    if request.method == 'GET':
        services = Service.objects.filter(filter(request))
        date_init = request.GET.get('date_init')
        date_end = request.GET.get('date_end')
        query = ReportInfo.objects.filter(reportType='bus', report__timeStamp__range=[date_init,date_end])
        query = query.filter(service__in=[service.service for service in services])
        data = {
            'data': [q.report.getDictionary() for q in query]
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

        date_init = request.GET.get('date_init')
        date_end = request.GET.get('date_end')
        plates = request.GET.get('plate')
        serv = request.GET.get('service')
        query = EventForBusv2.objects.filter(
            busassignment__service__in=[service.service for service in Service.objects.filter(filter(request))])
        query = query.filter(event__category="conductor")
        query = query.filter(timeCreation__range=[date_init, date_end])
        query = query.exclude(busassignment__uuid__registrationPlate__icontains="No Info.")
        if plates:
            plates = json.loads(plates)
            plateFilter = reduce(lambda x, y: x | y, [Q(busassignment__uuid__registrationPlate=plate) for plate in plates])
            query = query.filter(plateFilter)
        if serv:
            serv = json.loads(serv)
            serviceFilter = reduce(lambda x, y: x | y, [Q(busassignment__service=ser) for ser in serv])
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
    query = EventForBusv2.objects.filter(
        busassignment__service__in=[service.service for service in Service.objects.filter(filter(request))])
    query = query.filter(event__category="conductor")
    query = query.exclude(busassignment__uuid__registrationPlate__icontains="No Info.")
    #query = query.exclude(event__id='evn00233')
    #today = datetime.now().date()
    #tomorrow = today + timedelta(1)
    #today_start = datetime.combine(today, time())
    #today_end = datetime.combine(tomorrow, time())
    #query = query.filter(timeCreation__gte=today_start, timeCreation__lte=today_end)
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
    query = EventForBusv2.objects.filter(
        busassignment__service__in=[service.service for service in Service.objects.filter(filter(request))])
    query = query.filter(event__category="estado físico").exclude(event__id="evn00225")
    today = date.today()
    year = today.year
    if today.month <= 3:
        last_month = today.month + 12 - 3
        year = year - 1
    else:
        last_month = today.month - 3
    query = query.filter(timeCreation__gte=date(year, last_month, today.day)).exclude(
        busassignment__uuid__registrationPlate__icontains="No Info.")
    query = query.order_by("event__name", "busassignment__uuid__registrationPlate", "-timeStamp").distinct("event__name", "busassignment__uuid__registrationPlate")
    query = query.filter(fixed = False)
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

        date_init = request.GET.get('date_init')
        date_end = request.GET.get('date_end')
        #hour1 = int(request.GET.get('hour1'))
        #hour2 = int(request.GET.get('hour2'))
        plates = request.GET.get('plate')
        serv = request.GET.get('service')
        #hour2 = (hour2 + 24) if hour2 < hour1 else hour2
        #hours = [hour % 24 for hour in range(hour1, hour2 + 1)]
        query = EventForBusv2.objects.filter(
            busassignment__service__in=[service.service for service in Service.objects.filter(filter(request))])
        query = query.filter(event__category="estado físico", fixed = False)
        query = query.filter(timeCreation__range=[date_init, date_end])
        query = query.exclude(busassignment__uuid__registrationPlate__icontains="No Info")
        if plates:
            plates = json.loads(plates)
            plateFilter = reduce(lambda x, y: x | y, [Q(busassignment__uuid__registrationPlate=plate) for plate in plates])
            query = query.filter(plateFilter)
        if serv:
            serv = json.loads(serv)
            serviceFilter = reduce(lambda x, y: x | y, [Q(busassignment__service=ser) for ser in serv])
            query = query.filter(serviceFilter)
        #hourFilter = reduce(lambda x, y: x | y, [Q(timeCreation__hour=h) for h in hours])
        #query = query.filter(hourFilter)
        data = {
            "reports": [change(report.getDictionary()) for report in query],
            "types": events
        }
        return JsonResponse(data, safe=False)

@login_required
def updatePhysical(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        event = EventForBusv2.objects.get(id=id)
        event.fixed = True
        try:
            event.save()
            ans = "True"
        except:
            ans = "False"
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
        query = EventForBusv2.objects.filter(
            busassignment__service__in=[service.service for service in Service.objects.filter(filter(request))])
        query = query.exclude(busassignment__uuid__registrationPlate__icontains="No Info.")
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
    template = loader.get_template('maptest3.html')
    return HttpResponse(template.render(request=request))

@login_required
def getMap(request):
    services = Service.objects.filter(filter(request))
    query = StadisticDataFromRegistrationBus.objects.exclude(reportOfEvent__event__category="estado físico")
    query = query.order_by("reportOfEvent", "-timeStamp").distinct('reportOfEvent')
    dict = {}
    for service in services:
        dict[service.service] = [stadistic.getDictionary() for stadistic in query.filter(reportOfEvent__busassignment__service = service.service)]
    data = {
        'data': dict
    }
    return JsonResponse(data, safe=False)

