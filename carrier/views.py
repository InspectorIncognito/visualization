# -*- coding: utf-8 -*

from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import CharField, ExpressionWrapper, F

from datetime import datetime, date, timedelta
from pytz import timezone
import json
import pytz

from AndroidRequests.models import *

def filter(request):
    user = request.user.getUser()
    return user.color()


def is_transapp(user):
    if user.is_authenticated:
        if user.getUser():
            return user.getUser().isTransapp()
    return False


# ----------------------------------------------------------------------------------------------------------------------
# INDEX
# ----------------------------------------------------------------------------------------------------------------------

@login_required
def index(request):
    template = loader.get_template('carrier/test.html')
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
        datatype[type] = query.filter(event__category=type).count()
    groups = {}
    for type in types:

        events = Event.objects.filter(eventType="bus", category=type)
        names = [event.name for event in events]
        groups[type] = {}
        for name in names:
            groups[type][name] = query.filter(event__category=type, event__name=name).count()

    data = {
        'datatype': datatype,
        'groups': groups,
    }
    return JsonResponse(data, safe=False)


# ----------------------------------------------------------------------------------------------------------------------
# DRIVERS
# ----------------------------------------------------------------------------------------------------------------------

@login_required
def drivers(request):
    template = loader.get_template('carrier/drivers.html')
    services = Service.objects.filter(filter(request))
    context = {
        'services': services,
    }
    return HttpResponse(template.render(context, request))


@login_required
def getDriversReport(request):
    if request.method == 'GET':
        events = Event.objects.filter(category="conductor")
        events = [event.name.capitalize() for event in events]
        pos = range(0, len(events))
        event_to_pos = {name: pos for name, pos in zip(events, pos)}

        def change(dict):
            dict["type"] = event_to_pos[dict["type"]]
            return dict

        date_init = request.GET.get('date_init')
        date_end = request.GET.get('date_end')
        plates = request.GET.get('plate')
        serv = request.GET.get('service')
        services = [service.service for service in Service.objects.filter(filter(request))]
        query = EventForBusv2.objects.filter(
            busassignment__service__in=services)
        query = query.filter(event__category="conductor")
        query = query.filter(timeCreation__range=[date_init, date_end])
        query = query.exclude(busassignment__uuid__registrationPlate__icontains="No Info.")
        busassignment = Busassignment.objects.filter(service__in=services).exclude(
            uuid__registrationPlate__icontains="No Info.").select_related('uuid')
        if serv:
            serv = json.loads(serv)
            serviceFilter = reduce(lambda x, y: x | y, [Q(busassignment__service=ser) for ser in serv])
            query = query.filter(serviceFilter)
            busassignment = busassignment.filter(service__in=serv)

        busassignment = busassignment.distinct("uuid__registrationPlate")
        allplates = {ba.uuid.registrationPlate: False for ba in busassignment}
        query2 = query.distinct("busassignment__uuid__registrationPlate").select_related("busassignment__uuid")
        for report in query2:
            plate = report.busassignment.uuid.registrationPlate
            allplates[plate] = True

        # print(allplates)

        if plates:
            plates = json.loads(plates)
            plateFilter = reduce(lambda x, y: x | y,
                                 [Q(busassignment__uuid__registrationPlate=plate) for plate in plates])
            query = query.filter(plateFilter)
        data = {
            "allplates": allplates,
            "reports": [change(report.getDictionary()) for report in query],
            "types": events
        }
        return JsonResponse(data, safe=False)


@login_required
def driversTable(request):
    template = loader.get_template('carrier/driversTable.html')
    return HttpResponse(template.render(request=request))


@login_required
def getDriversTable(request):
    query = EventForBusv2.objects.filter(
        busassignment__service__in=[service.service for service in Service.objects.filter(filter(request))])
    query = query.filter(event__category="conductor")
    query = query.exclude(busassignment__uuid__registrationPlate__icontains="No Info.")
    # query = query.exclude(event__id='evn00233')
    # today = datetime.now().date()
    # tomorrow = today + timedelta(1)
    # today_start = datetime.combine(today, time())
    # today_end = datetime.combine(tomorrow, time())
    # query = query.filter(timeCreation__gte=today_start, timeCreation__lte=today_end)
    data = {
        'data': [item.getDictionary() for item in query]
    }
    return JsonResponse(data, safe=False)


# ----------------------------------------------------------------------------------------------------------------------
# BUS
# ----------------------------------------------------------------------------------------------------------------------


@login_required
def busReports(request):
    template = loader.get_template('carrier/busReports.html')
    return HttpResponse(template.render(request=request))


@login_required
def getBusReports(request):
    if request.method == 'GET':
        services = Service.objects.filter(filter(request))
        date_init = request.GET.get('date_init')
        date_end = request.GET.get('date_end')
        query = ReportInfo.objects.filter(reportType='bus', report__timeStamp__range=[date_init, date_end])
        query = query.filter(service__in=[service.service for service in services])
        data = {
            'data': [q.getDictionary() for q in query]
        }
        return JsonResponse(data, safe=False)



@login_required
def physical(request):
    template = loader.get_template('carrier/physical.html')
    services = Service.objects.filter(filter(request))
    context = {
        'services': services
    }
    return HttpResponse(template.render(context, request))


@login_required
def getPhysicalHeaders(request):
    events = Event.objects.filter(category="estado físico", eventType="bus").exclude(id="evn00225")
    events = [event.name for event in events]
    headerInfo = EventForBusv2.objects.filter(event__category='estado físico').exclude(event__id="evn00225")
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
        q = q.order_by("busassignment__uuid__registrationPlate", "-timeStamp").distinct(
            'busassignment__uuid__registrationPlate')
        q = q.filter(fixed=False)
        response[ev] = q.count()
    return JsonResponse(response, safe=False)


@login_required
def physicalTable(request):
    template = loader.get_template('carrier/physicalTable.html')
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

    events = Event.objects.filter(eventType="bus", category= "estado físico").exclude(id="evn00225")
    events = events.distinct("name")

    query = query.filter(timeCreation__gte=date(year, last_month, today.day)).exclude(
        busassignment__uuid__registrationPlate__icontains="No Info.")
    query = query.order_by("event__name", "busassignment__uuid__registrationPlate", "-timeStamp").distinct(
        "event__name", "busassignment__uuid__registrationPlate")
    query = query.filter(fixed=False).select_related("event")

    name = request.GET.get('name')
    if not name == "all":
        query = query.filter(event__name__icontains = name)

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
        # hour1 = int(request.GET.get('hour1'))
        # hour2 = int(request.GET.get('hour2'))
        plates = request.GET.get('plate')
        serv = request.GET.get('service')
        # hour2 = (hour2 + 24) if hour2 < hour1 else hour2
        # hours = [hour % 24 for hour in range(hour1, hour2 + 1)]
        services = [service.service for service in Service.objects.filter(filter(request))]
        query = EventForBusv2.objects.filter(
            busassignment__service__in=services)
        query = query.filter(event__category="estado físico", fixed=False)
        query = query.filter(timeCreation__range=[date_init, date_end])
        query = query.exclude(busassignment__uuid__registrationPlate__icontains="No Info")

        busassignment = Busassignment.objects.filter(service__in=services).exclude(
            uuid__registrationPlate__icontains="No Info.").select_related('uuid').distinct("uuid__registrationPlate")
        allplates = {ba.uuid.registrationPlate: False for ba in busassignment}
        query2 = query.distinct("busassignment__uuid__registrationPlate").select_related("busassignment__uuid")
        for report in query2:
            plate = report.busassignment.uuid.registrationPlate
            allplates[plate] = True

        if plates:
            plates = json.loads(plates)
            plateFilter = reduce(lambda x, y: x | y,
                                 [Q(busassignment__uuid__registrationPlate__icontains=plate) for plate in plates])
            query = query.filter(plateFilter)
        if serv:
            serv = json.loads(serv)
            serviceFilter = reduce(lambda x, y: x | y, [Q(busassignment__service=ser) for ser in serv])
            query = query.filter(serviceFilter)
        # hourFilter = reduce(lambda x, y: x | y, [Q(timeCreation__hour=h) for h in hours])
        # query = query.filter(hourFilter)
        data = {
            "reports": [change(report.getDictionary()) for report in query],
            "types": events,
            "allplates": allplates
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
def busMap(request):
    template = loader.get_template('carrier/busMap.html')
    return HttpResponse(template.render(request=request))


@login_required
def getBusMap(request):
    date_init = request.GET.get('date_init')
    date_end = request.GET.get('date_end')
    serv = request.GET.get('service')
    plate = request.GET.get('plate')
    comunas = request.GET.get('comuna')

    services = Service.objects.filter(filter(request))
    query = StadisticDataFromRegistrationBus.objects.filter(
        reportOfEvent__timeCreation__range=[date_init, date_end]).exclude(
        reportOfEvent__event__category="estado físico")
    query = query.filter(reportOfEvent__busassignment__service__in=[service.service for service in services])
    query = query.order_by("reportOfEvent", "-timeStamp").distinct('reportOfEvent')

    if serv:
        serv = json.loads(serv)
        serviceFilter = reduce(lambda x, y: x | y, [Q(reportOfEvent__busassignment__service=ser) for ser in serv])
        query = query.filter(serviceFilter)

    if plate:
        plates = json.loads(plate)
        plateFilter = reduce(lambda x, y: x | y,
                             [Q(reportOfEvent__busassignment__uuid__registrationPlate=plate) for plate in plates])
        query = query.filter(plateFilter)

    if comunas:
        comunas = json.loads(comunas)
        comunaFilter = reduce(lambda x, y: x | y,
                              [Q(reportOfEvent__zonification__comuna=comuna) for comuna in comunas])
        query = query.filter(comunaFilter)

    data = {
        'data': [stadistic.getDictionary() for stadistic in query]
    }
    return JsonResponse(data, safe=False)


@login_required
def getBusMapParameters(request):
    services = [service.service for service in Service.objects.filter(filter(request))]
    busassignment = Busassignment.objects.filter(service__in=services).exclude(
        uuid__registrationPlate__icontains="No Info.").select_related('uuid').distinct('uuid__registrationPlate')
    plates = [ba.uuid.registrationPlate for ba in busassignment]
    zones = zonificationTransantiago.objects.distinct("comuna")
    comunas = [zone.comuna for zone in zones]
    events = Event.objects.filter(eventType="bus").exclude(category="estado físico")
    categories = events.distinct("category")
    types = {cat.category.capitalize(): [] for cat in categories}
    for event in events:
        types[event.category.capitalize()].append(event.name.capitalize())
    data = {
        'services': services,
        'plates': plates,
        'comunas': comunas,
        'types': types,
    }

    return JsonResponse(data, safe=False)


# ----------------------------------------------------------------------------------------------------------------------
# BUS STOP
# ----------------------------------------------------------------------------------------------------------------------


@login_required
def busStopReports(request):
    template = loader.get_template('carrier/busStopReports.html')
    return HttpResponse(template.render(request=request))


@login_required
def getBusStopReports(request):
    if request.method == 'GET':
        date_init = request.GET.get('date_init')
        date_end = request.GET.get('date_end')
        query = ReportInfo.objects.filter(reportType='busStop', report__timeStamp__range=[date_init, date_end])
        query = query.exclude(busStop__isnull=True)
        data = {
            'data': [report_info.getDictionary() for report_info in query]
        }
        return JsonResponse(data, safe=False)


@user_passes_test(is_transapp)
def getBusStopInfo(request):
    if request.method == 'GET':
        date_init = datetime.strptime(request.GET.get('date_init'), "%Y-%m-%dT%H:%M:%S")
        date_end = datetime.strptime(request.GET.get('date_end'), "%Y-%m-%dT%H:%M:%S")

        pytz.timezone('America/Santiago').localize(date_init)
        pytz.timezone('America/Santiago').localize(date_end)

        response = {}
        # events
        stopsevents = EventForBusStop.objects.filter(timeCreation__range=[date_init, date_end])
        stopsevents = stopsevents.values('busStop_id').annotate(num_events=Count('id'))
        # confirms
        confirmsstop = StadisticDataFromRegistrationBusStop.objects.filter(timeStamp__range=[date_init, date_end],
                                                                           confirmDecline='confirm') \
            .annotate(busStop=ExpressionWrapper(F('reportOfEvent__busStop'), output_field=CharField()))
        confirmsstop = confirmsstop.values('busStop').annotate(num_confirms=Count('id'))
        # declines
        declinesstop = StadisticDataFromRegistrationBusStop.objects.filter(timeStamp__range=[date_init, date_end],
                                                                           confirmDecline='decline') \
            .annotate(busStop=ExpressionWrapper(F('reportOfEvent__busStop'), output_field=CharField()))
        declinesstop = declinesstop.values('busStop').annotate(num_declines=Count('id'))
        # touch
        bschecks = NearByBusesLog.objects.filter(timeStamp__range=[date_init, date_end])
        bschecks = bschecks.values('busStop').annotate(num_checks=Count('timeStamp'))

        for stopevent in stopsevents:
            response[str(stopevent['busStop_id'])] = {'eventCount': stopevent['num_events']}

        for confirmstop in confirmsstop:
            if str(confirmstop['busStop']) in response:
                response[str(confirmstop['busStop'])].update({'confirmCount': confirmstop['num_confirms']})
            else:
                response[str(confirmstop['busStop'])] = {'confirmCount': confirmstop['num_confirms']}

        for declinestop in declinesstop:
            if str(declinestop['busStop']) in response:
                response[str(declinestop['busStop'])].update({'declineCount': declinestop['num_declines']})
            else:
                response[str(declinestop['busStop'])] = {'declineCount': declinestop['num_declines']}

        for bscheck in bschecks:
            if str(bscheck['busStop']) in response:
                response[str(bscheck['busStop'])].update({'busStopCheckCount': bscheck['num_checks']})
            else:
                response[str(bscheck['busStop'])] = {'busStopCheckCount': bscheck['num_checks']}

        for resp in response:

            if 'eventCount' not in response[resp]:
                response[resp].update({'eventCount': 0})

            if 'confirmCount' not in response[resp]:
                response[resp].update({'confirmCount': 0})

            if 'declineCount' not in response[resp]:
                response[resp].update({'declineCount': 0})

            if 'busStopCheckCount' not in response[resp]:
                response[resp].update({'busStopCheckCount': 0})

            response[resp]['confirmCount'] = response[resp]['confirmCount'] - response[resp]['eventCount']

        return JsonResponse(response, safe=False)


@login_required
def busStopMap(request):
    template = loader.get_template('carrier/busStopMap.html')
    return HttpResponse(template.render(request=request))


# ----------------------------------------------------------------------------------------------------------------------
# USERS
# ----------------------------------------------------------------------------------------------------------------------

@login_required
def userActivities(request):
    template = loader.get_template('carrier/userActivities.html')
    return HttpResponse(template.render(request=request))


@login_required
def activeUsers(request):
    template = loader.get_template('carrier/activeUsers.html')
    return HttpResponse(template.render(request=request))


@login_required
def busStopViewsMap(request):
    template = loader.get_template('carrier/busStopViewsMap.html')
    return HttpResponse(template.render(request=request))


@login_required
def usersTravelMap(request):
    template = loader.get_template('carrier/usersTravelMap.html')
    return HttpResponse(template.render(request=request))


@user_passes_test(is_transapp)
def getUsersActivities(request):
    if request.method == 'GET':
        date_init = datetime.strptime(request.GET.get('date_init'), "%Y-%m-%dT%H:%M:%S")
        date_end = datetime.strptime(request.GET.get('date_end'), "%Y-%m-%dT%H:%M:%S")

        pytz.timezone('America/Santiago').localize(date_init)
        pytz.timezone('America/Santiago').localize(date_end)
        # ADD TIMEZONE

        # Per user id get:
        # devicePositionInTime count
        devices = DevicePositionInTime.objects.filter(timeStamp__range=[date_init, date_end])
        devices = devices.values('userId').annotate(num_positions=Count('id'))
        # bus and busstops events -> eventFor*
        busevents = EventForBusv2.objects.filter(timeCreation__range=[date_init, date_end])
        busevents = busevents.values('userId').annotate(num_events=Count('id'))
        stopsevents = EventForBusStop.objects.filter(timeCreation__range=[date_init, date_end])
        stopsevents = stopsevents.values('userId').annotate(num_events=Count('id'))
        # confirms and declines fro bus and busstops events -> statistic*
        # TODO: if the timeStamp is the first of the event, is the creation of the event and must not be counted
        confirmsbus = StadisticDataFromRegistrationBus.objects.filter(timeStamp__range=[date_init, date_end],
                                                                      confirmDecline='confirm')
        confirmsbus = confirmsbus.values('userId').annotate(num_confirms=Count('id'))
        declinesbus = StadisticDataFromRegistrationBus.objects.filter(timeStamp__range=[date_init, date_end],
                                                                      confirmDecline='decline')
        declinesbus = declinesbus.values('userId').annotate(num_declines=Count('id'))

        confirmsstop = StadisticDataFromRegistrationBusStop.objects.filter(timeStamp__range=[date_init, date_end],
                                                                           confirmDecline='confirm')
        confirmsstop = confirmsstop.values('userId').annotate(num_confirms=Count('id'))
        declinesstop = StadisticDataFromRegistrationBusStop.objects.filter(timeStamp__range=[date_init, date_end],
                                                                           confirmDecline='decline')
        declinesstop = declinesstop.values('userId').annotate(num_declines=Count('id'))
        # tokens
        tokens = PoseInTrajectoryOfToken.objects.filter(timeStamp__range=[date_init, date_end]).values('token_id')
        tokens = Token.objects.filter(token__in=tokens)
        tokens = tokens.values('userId').annotate(num_tokens=Count('token'))
        # reports
        reports = Report.objects.filter(timeStamp__range=[date_init, date_end])
        reports = reports.values('userId').annotate(num_reports=Count('id'))
        # busstops checkeds -> nearbyBusesLog
        bschecks = NearByBusesLog.objects.filter(timeStamp__range=[date_init, date_end])
        bschecks = bschecks.values('userId').annotate(num_checks=Count('timeStamp'))

        tmp_response = {}
        for device in devices:
            tmp_response[str(device['userId'])] = {'devicePositionInTimeCount': device['num_positions']}

        for busevent in busevents:
            if str(busevent['userId']) in tmp_response:
                tmp_response[str(busevent['userId'])].update({'busEventCreationCount': busevent['num_events']})
            else:
                tmp_response[str(busevent['userId'])] = {'busEventCreationCount': busevent['num_events']}

        for stopsevent in stopsevents:
            if str(stopsevent['userId']) in tmp_response:
                tmp_response[str(stopsevent['userId'])].update({'busStopEventCreationCount': stopsevent['num_events']})
            else:
                tmp_response[str(stopsevent['userId'])] = {'busStopEventCreationCount': stopsevent['num_events']}

        for confirmbus in confirmsbus:
            if str(confirmbus['userId']) in tmp_response:
                tmp_response[str(confirmbus['userId'])].update({'confirmBusCount': confirmbus['num_confirms']})
            else:
                tmp_response[str(confirmbus['userId'])] = {'confirmBusCount': confirmbus['num_confirms']}

        for declinebus in declinesbus:
            if str(declinebus['userId']) in tmp_response:
                tmp_response[str(declinebus['userId'])].update({'declineBusCount': declinebus['num_declines']})
            else:
                tmp_response[str(declinebus['userId'])] = {'declineBusCount': declinebus['num_declines']}

        for confirmstop in confirmsstop:
            if str(confirmstop['userId']) in tmp_response:
                tmp_response[str(confirmstop['userId'])].update({'confirmBusStopCount': confirmstop['num_confirms']})
            else:
                tmp_response[str(confirmstop['userId'])] = {'confirmBusStopCount': confirmstop['num_confirms']}

        for declinestop in declinesstop:
            if str(declinestop['userId']) in tmp_response:
                tmp_response[str(declinestop['userId'])].update({'declineBusStopCount': declinestop['num_declines']})
            else:
                tmp_response[str(declinestop['userId'])] = {'declineBusStopCount': declinestop['num_declines']}

        for token in tokens:
            if str(token['userId']) in tmp_response:
                tmp_response[str(token['userId'])].update({'tokenCount': token['num_tokens']})
            else:
                tmp_response[str(token['userId'])] = {'tokenCount': token['num_tokens']}

        for report in reports:
            if str(report['userId']) in tmp_response:
                tmp_response[str(report['userId'])].update({'reportCount': report['num_reports']})
            else:
                tmp_response[str(report['userId'])] = {'reportCount': report['num_reports']}

        for bscheck in bschecks:
            if str(bscheck['userId']) in tmp_response:
                tmp_response[str(bscheck['userId'])].update({'busStopCheckCount': bscheck['num_checks']})
            else:
                tmp_response[str(bscheck['userId'])] = {'busStopCheckCount': bscheck['num_checks']}

        for device_id in tmp_response:
            if 'devicePositionInTimeCount' not in tmp_response[device_id]:
                tmp_response[device_id].update({'devicePositionInTimeCount': 0})

            if 'busEventCreationCount' not in tmp_response[device_id]:
                tmp_response[device_id].update({'busEventCreationCount': 0})

            if 'busStopEventCreationCount' not in tmp_response[device_id]:
                tmp_response[device_id].update({'busStopEventCreationCount': 0})

            if 'confirmBusCount' not in tmp_response[device_id]:
                tmp_response[device_id].update({'confirmBusCount': 0})

            if 'declineBusCount' not in tmp_response[device_id]:
                tmp_response[device_id].update({'declineBusCount': 0})

            if 'tokenCount' not in tmp_response[device_id]:
                tmp_response[device_id].update({'tokenCount': 0})

            if 'reportCount' not in tmp_response[device_id]:
                tmp_response[device_id].update({'reportCount': 0})

            if 'busStopCheckCount' not in tmp_response[device_id]:
                tmp_response[device_id].update({'busStopCheckCount': 0})

            if 'confirmBusStopCount' not in tmp_response[device_id]:
                tmp_response[device_id].update({'confirmBusStopCount': 0})

            if 'declineBusStopCount' not in tmp_response[device_id]:
                tmp_response[device_id].update({'declineBusStopCount': 0})

            tmp_response[device_id]['confirmBusCount'] = tmp_response[device_id]['confirmBusCount'] - tmp_response[device_id][
                'busEventCreationCount']
            tmp_response[device_id]['confirmBusStopCount'] = tmp_response[device_id]['confirmBusStopCount'] - tmp_response[device_id][
                'busStopEventCreationCount']

        # as array
        response = []
        for device_id in tmp_response:
            info = tmp_response[device_id]
            info["device_id"] = device_id
            response.append(info)

        return JsonResponse({"data": response}, safe=False)


@user_passes_test(is_transapp)
def getActiveUsers(request):
    if request.method == 'GET':
        tz = timezone('Chile/Continental')
        date = request.GET.get('date')
        date_start = datetime.strptime(date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        date_start = tz.localize(date_start)
        date_finish = datetime.strptime(date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        date_finish = tz.localize(date_finish)
        positions = DevicePositionInTime.objects.filter(timeStamp__range=[date_start, date_finish])
        highest_lifespan = Event.objects.all().order_by("-lifespam")[0].lifespam
        busevents = EventForBusv2.objects.filter(timeCreation__gte=(date_start - timedelta(highest_lifespan)))
        busstopevents = EventForBusStop.objects.filter(timeCreation__gte=(date_start - timedelta(highest_lifespan)))

        data = {
            "half_hours": []
        }

        for x in xrange(1, 49):
            period_positions = positions.filter(
                timeStamp__range=[date_start + timedelta(minutes=30 * (x - 1)), date_start + timedelta(minutes=30 * x)])
            period_bus_stop_events = busstopevents.filter(
                timeCreation__range=[date_start + timedelta(minutes=30 * (x - 1)),
                                     date_start + timedelta(minutes=30 * x)])
            period_bus_events = busevents.filter(timeCreation__range=[date_start + timedelta(minutes=30 * (x - 1)),
                                                                      date_start + timedelta(minutes=30 * x)])

            bus_active_events = []
            bus_stop_active_events = []

            for be in busevents:
                if be.timeStamp > (date_start + timedelta(minutes=30 * x) - timedelta(minutes=be.event.lifespam)):
                    bus_active_events.append(be)
            for bse in busstopevents:
                if bse.timeStamp > (date_start + timedelta(minutes=30 * x) - timedelta(minutes=bse.event.lifespam)):
                    bus_stop_active_events.append(bse)

            data["half_hours"].append({
                "half_hour": str(date_start + timedelta(minutes=30 * (x - 1))) + " " + str(
                    date_finish + timedelta(minutes=30 * (x))),
                "active_users": len(list(set([position.userId for position in period_positions]))),
                "reporting_users": len(list(set(
                    [event.userId for event in period_bus_stop_events] + [event.userId for event in
                                                                          period_bus_events]))),
                "reports": len(period_bus_stop_events) + len(period_bus_events),
                "active_events": len(bus_active_events) + len(bus_stop_active_events)
            })
        return JsonResponse(data, safe=False)


@user_passes_test(is_transapp)
def getUsersPositions(request):
    if request.method == 'GET':
        date_init = datetime.strptime(request.GET.get('date_init'), "%Y-%m-%dT%H:%M:%S")
        date_end = datetime.strptime(request.GET.get('date_end'), "%Y-%m-%dT%H:%M:%S")

        pytz.timezone('America/Santiago').localize(date_init)
        pytz.timezone('America/Santiago').localize(date_end)

        devices = DevicePositionInTime.objects.filter(
            timeStamp__range=[date_init, date_end]
        ).order_by('userId', 'timeStamp').values()

        response = {}
        for device in devices:
            device_id = str(device['userId'])

            # already exists: save the last one
            if device_id in response:
                response[device_id]['last'] = {
                    'lat': device['latitud'],
                    'lon': device['longitud'],
                    'timeStamp': device['timeStamp']
                }
            else:
                # new device
                response[device_id] = {
                    'first': {
                        'lat': device['latitud'],
                        'lon': device['longitud'],
                        'timeStamp': device['timeStamp']
                    }
                }

        return JsonResponse(response, safe=False)


@user_passes_test(is_transapp)
def getUsersTravelMap(request):
    if request.method == 'GET':
        date_init = datetime.strptime(request.GET.get('date_init'), "%Y-%m-%dT%H:%M:%S")
        date_end = datetime.strptime(request.GET.get('date_end'), "%Y-%m-%dT%H:%M:%S")

        pytz.timezone('America/Santiago').localize(date_init)
        pytz.timezone('America/Santiago').localize(date_end)

        response = {}

        tokenposes = PoseInTrajectoryOfToken.objects.filter(timeStamp__range=[date_init, date_end]).order_by(
            'token_id',
            'timeStamp'). \
            annotate(service=ExpressionWrapper(F('token__busassignment__service'), output_field=CharField())). \
            values('latitud', 'longitud', 'timeStamp', 'token_id', 'service')

        for tokenpose in tokenposes:
            if str(tokenpose['token_id']) not in response:
                response[str(tokenpose['token_id'])] = {'service': tokenpose['service'],
                                                        'origin': {'latitude': tokenpose['latitud'],
                                                                   'longitude': tokenpose['longitud'],
                                                                   'timeStamp': tokenpose['timeStamp']}}

        tokenposes = PoseInTrajectoryOfToken.objects.filter(token_id__in=response).order_by('token_id',
                                                                                            '-timeStamp')

        for resp in response:
            response[resp].update({'destination': {'latitude': tokenposes.filter(token_id=resp).first().latitud,
                                                   'longitude': tokenposes.filter(token_id=resp).first().longitud,
                                                   'timeStamp': tokenposes.filter(
                                                       token_id=resp).first().timeStamp}})

        return JsonResponse(response, safe=False)


# ----------------------------------------------------------------------------------------------------------------------
# TOOLS
# ----------------------------------------------------------------------------------------------------------------------


@login_required
def fullTable(request):
    template = loader.get_template('carrier/fullTable.html')
    events = Event.objects.filter(eventType="bus").distinct("category")
    types = [event.category.capitalize() for event in events]
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
            typeFilter = reduce(lambda x, y: x | y, [Q(event__category__icontains=type) for type in types])
            query = query.filter(typeFilter)

        data = {
            'data': [report.getDictionary() for report in query]
        }
        return JsonResponse(data, safe=False)

