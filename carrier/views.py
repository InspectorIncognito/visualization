# -*- coding: utf-8 -*
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import CharField, ExpressionWrapper, F
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from collections import defaultdict

from datetime import datetime, date, timedelta
from transform import WITHOUT_LICENSE_PLATE

from AndroidRequests.models import Event, Service, EventForBusv2, Busassignment, ReportInfo, TimePeriod, \
    ZonificationTransantiago, StadisticDataFromRegistrationBus, StadisticDataFromRegistrationBusStop, \
    EventForBusStop, NearByBusesLog, DevicePositionInTime, PoseInTrajectoryOfToken, Token, Report

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
    template = loader.get_template('index.html')
    return HttpResponse(template.render(request=request))


@login_required
def getCount(request):
    categories = Event.objects.filter(eventType=Event.BUS).values_list("category", flat=True).distinct()
    routeList = Service.objects.filter(filter(request)).values_list("service", flat=True).distinct()
    query = EventForBusv2.objects.filter(busassignment__service__in=routeList).\
        exclude(busassignment__uuid__registrationPlate=WITHOUT_LICENSE_PLATE)

    queries = {}
    for category in categories:
        queries[category] = query.filter(event__category=category).count()

    groups = defaultdict(dict)
    for category in categories:
        names = Event.objects.filter(eventType=Event.BUS, category=category).values_list("name", flat=True)
        for name in names:
            groups[category][name] = query.filter(event__category=category, event__name=name).count()

    data = {
        'datatype': queries,
        'groups': groups,
    }
    return JsonResponse(data, safe=False)


# ----------------------------------------------------------------------------------------------------------------------
# DRIVERS
# ----------------------------------------------------------------------------------------------------------------------

@login_required
def drivers(request):
    template = "carrier/drivers.html"
    services = Service.objects.filter(filter(request)).values_list("service", flat=True).distinct()
    context = {
        'services': services,
    }
    return render(request, template, context)


@login_required
def getDriversReport(request):
    if request.method == 'GET':
        eventNameList = Event.objects.filter(category="conductor").values_list("name", flat=True)
        eventNameList = map(lambda x: x.capitalize(), eventNameList)
        event_to_pos = {name: index for index, name in enumerate(eventNameList)}

        def change(dict):
            dict["type"] = event_to_pos[dict["type"]]
            return dict

        # params of requests
        date_init = parse_datetime(request.GET.get('date_init'))
        date_end = parse_datetime(request.GET.get('date_end'))
        licensePlates = request.GET.getlist('licensePlates[]')
        routes = request.GET.getlist('routes[]')

        query = EventForBusv2.objects.filter(event__category="conductor", timeCreation__range=[date_init, date_end]).\
            exclude(busassignment__uuid__registrationPlate=WITHOUT_LICENSE_PLATE)

        busassignment = Busassignment.objects.select_related('uuid').\
            exclude(uuid__registrationPlate=WITHOUT_LICENSE_PLATE).distinct("uuid__registrationPlate")

        if routes:
            query = query.filter(busassignment__service__in=routes)
            busassignment = busassignment.filter(service__in=routes)
        else:
            routeList = Service.objects.filter(filter(request)).values_list("service", flat=True).distinct()
            query = query.filter(busassignment__service__in=routeList)
            busassignment = busassignment.filter(service__in=routeList)

        allplates = {ba.uuid.registrationPlate: False for ba in busassignment}
        query2 = query.select_related("busassignment__uuid").distinct("busassignment__uuid__registrationPlate")
        for report in query2:
            plate = report.busassignment.uuid.registrationPlate
            allplates[plate] = True

        # print(allplates)

        if licensePlates:
            query = query.filter(busassignment__uuid__registrationPlate__in=licensePlates)

        data = {
            "allplates": allplates,
            "reports": [change(report.getDictionary()) for report in query],
            "types": eventNameList,
            "authorityPeriods": list(TimePeriod.objects.values_list("name", flat=True).order_by('id'))
        }
        return JsonResponse(data, safe=False)


@login_required
def driversTable(request):
    template = 'carrier/driversTable.html'
    return render(request, template, {})


@login_required
def getDriversTable(request):
    routeList = Service.objects.filter(filter(request)).values_list("service", flat=True).distinct()
    query = EventForBusv2.objects.filter(
        busassignment__service__in=routeList)
    query = query.filter(event__category="conductor")
    query = query.exclude(busassignment__uuid__registrationPlate=WITHOUT_LICENSE_PLATE)
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
    template = 'carrier/busReports.html'
    return render(request, template, {})


@login_required
def getBusReports(request):
    if request.method == 'GET':
        services = Service.objects.filter(filter(request)).values_list("service", flat=True).distinct()
        date_init = parse_datetime(request.GET.get('date_init'))
        date_end = parse_datetime(request.GET.get('date_end'))

        query = ReportInfo.objects.filter(reportType=ReportInfo.BUS, report__timeStamp__range=[date_init, date_end])
        query = query.filter(service__in=services)
        data = {
            'data': [q.getDictionary() for q in query]
        }
        return JsonResponse(data, safe=False)


@login_required
def physical(request):
    template = 'carrier/physical.html'
    context = {
        'services': Service.objects.filter(filter(request)).distinct()
    }
    return render(request, template, context)


@login_required
def getPhysicalHeaders(request):
    events = Event.objects.filter(category="estado físico", eventType="bus").exclude(id="evn00225").values_list("name", flat=True)
    routeList = Service.objects.filter(filter(request)).values_list("service", flat=True).distinct()
    headerInfo = EventForBusv2.objects.filter(event__category='estado físico',
                                              busassignment__service__in=routeList).exclude(event__id="evn00225")

    now = timezone.now()
    threeMonthsBefore = now.replace(month=(now.month-3)%12, hour=0, minute=0, second=0, microsecond=0)

    headerInfo = headerInfo.filter(timeCreation__gte=threeMonthsBefore).exclude(
        busassignment__uuid__registrationPlate=WITHOUT_LICENSE_PLATE)
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
    routeList = Service.objects.filter(filter(request)).values_list("service", flat=True).distinct()
    query = EventForBusv2.objects.filter(busassignment__service__in=routeList, event__category="estado físico").\
        exclude(event__id="evn00225")

    now = timezone.now()
    threeMonthsBefore = now.replace(month=(now.month-3)%12, hour=0, minute=0, second=0, microsecond=0)
    #events = Event.objects.filter(eventType="bus", category= "estado físico").exclude(id="evn00225").distinct("name")

    query = query.filter(timeCreation__gte=threeMonthsBefore).exclude(
        busassignment__uuid__registrationPlate=WITHOUT_LICENSE_PLATE)
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
        events = list(Event.objects.filter(category="estado físico", eventType="bus").values_list("name", flat=True))
        eventToPos = {name: pos for pos, name in enumerate(events)}

        def change(dict):
            dict["type"] = eventToPos[dict["type"]]
            return dict

        # request params
        date_init = parse_datetime(request.GET.get('date_init'))
        date_end = parse_datetime(request.GET.get('date_end'))
        plates = request.GET.getlist('license_plates[]')
        #routes = request.GET.getlist('routes')

        reports = EventForBusv2.objects.filter(event__category="estado físico", fixed=False,
                                               timeCreation__range=[date_init, date_end]).\
            exclude(busassignment__uuid__registrationPlate__icontains="No Info")
        routeList = Service.objects.filter(filter(request)).values_list("service", flat=True).distinct()
        #if routes:
        #    routeList = routes
        #reports = reports.filter(busassignment__service__in=routeList)

        if plates:
            reports = reports.filter(busassignment__uuid__registrationPlate__in=plates)

        licensePlateList = Busassignment.objects.filter(service__in=routeList).\
            exclude(uuid__registrationPlate=WITHOUT_LICENSE_PLATE).\
            values_list("uuid__registrationPlate", flat=True).distinct("uuid__registrationPlate")

        allplates = {licensePlate: False for licensePlate in licensePlateList}
        query2 = reports.values_list("busassignment__uuid__registrationPlate", flat=True).\
            distinct("busassignment__uuid__registrationPlate")
        for plate in query2:
            allplates[plate] = True

        data = {
            "reports": [change(report.getDictionary()) for report in reports],
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
    template = 'carrier/busMap.html'
    routeList = Service.objects.filter(filter(request)).values_list("service", flat=True).distinct()
    licensePlates = Busassignment.objects.filter(service__in=routeList).\
        exclude(uuid__registrationPlate=WITHOUT_LICENSE_PLATE).values_list("uuid__registrationPlate", flat=True).\
        distinct()
    communes = ZonificationTransantiago.objects.values_list("comuna", flat=True).distinct().order_by("comuna")
    context = {
        "routes": routeList,
        "licensePlates": licensePlates,
        "communes": communes
    }
    return render(request, template, context)


@login_required
def getBusMapParameters(request):

    routeList = Service.objects.filter(filter(request)).values_list("service", flat=True).distinct()

    events = Event.objects.filter(eventType="bus").exclude(category="estado físico")
    categories = events.distinct("category")
    types = {cat.category.capitalize(): [] for cat in categories}
    for event in events:
        types[event.category.capitalize()].append(event.name.capitalize())
    data = {
        "services": list(routeList),
        'types': types,
    }

    return JsonResponse(data, safe=False)

@login_required
def getBusMap(request):
    date_init = parse_datetime(request.GET.get('date_init'))
    date_end = parse_datetime(request.GET.get('date_end'))
    routes = request.GET.getlist('routes[]')
    licensePlates = request.GET.getlist('licensePlates[]')
    communes = request.GET.getlist('communes[]')

    routeList = Service.objects.filter(filter(request)).values_list("service", flat=True).distinct()
    query = StadisticDataFromRegistrationBus.objects.filter(
        reportOfEvent__timeCreation__range=[date_init, date_end]).exclude(
        reportOfEvent__event__category="estado físico")
    query = query.filter(reportOfEvent__busassignment__service__in=routeList)
    query = query.order_by("reportOfEvent", "-timeStamp").distinct('reportOfEvent')

    if routes:
        query = query.filter(reportOfEvent__busassignment__service__in=routes)

    if licensePlates:
        query = query.filter(reportOfEvent__busassignment__uuid__registrationPlate__in=licensePlates)

    if communes:
        query = query.filter(reportOfEvent__zonification__comuna__in=communes)

    data = {
        'data': [stadistic.getDictionary() for stadistic in query]
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
        query = query.exclude(stopCode__isnull=True)
        data = {
            'data': [report_info.getDictionary() for report_info in query]
        }
        return JsonResponse(data, safe=False)


#@user_passes_test(is_transapp)
@login_required
def getBusStopInfo(request):
    if request.method == 'GET':
        date_init = parse_datetime(request.GET.get('date_init'))
        date_end = parse_datetime(request.GET.get('date_end'))

        response = {}
        # events
        stopsevents = EventForBusStop.objects.filter(timeCreation__range=[date_init, date_end]).\
            values('stopCode').annotate(num_events=Count('id'))
        # confirms
        confirmsstop = StadisticDataFromRegistrationBusStop.objects.filter(timeStamp__range=[date_init, date_end],
                                                                           confirmDecline='confirm').\
            annotate(stopCode=ExpressionWrapper(F('reportOfEvent__stopCode'), output_field=CharField())).\
            values('stopCode').annotate(num_confirms=Count('id'))
        # declines
        declinesstop = StadisticDataFromRegistrationBusStop.objects.filter(timeStamp__range=[date_init, date_end],
                                                                           confirmDecline='decline').\
            annotate(stopCode=ExpressionWrapper(F('reportOfEvent__stopCode'), output_field=CharField())).\
            values('stopCode').annotate(num_declines=Count('id'))
        # touch
        bschecks = NearByBusesLog.objects.filter(timeStamp__range=[date_init, date_end]).\
            values('busStop').annotate(num_checks=Count('timeStamp'))

        for stopevent in stopsevents:
            response[str(stopevent['stopCode'])] = {'eventCount': stopevent['num_events']}

        for confirmstop in confirmsstop:
            if str(confirmstop['stopCode']) in response:
                response[str(confirmstop['stopCode'])].update({'confirmCount': confirmstop['num_confirms']})
            else:
                response[str(confirmstop['stopCode'])] = {'confirmCount': confirmstop['num_confirms']}

        for declinestop in declinesstop:
            if str(declinestop['stopCode']) in response:
                response[str(declinestop['stopCode'])].update({'declineCount': declinestop['num_declines']})
            else:
                response[str(declinestop['stopCode'])] = {'declineCount': declinestop['num_declines']}

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
    template = "carrier/busStopMap.html"
    return render(request, template, {})


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


#@user_passes_test(is_transapp)
@login_required
def getUsersActivities(request):
    if request.method == 'GET':
        date_init = parse_datetime(request.GET.get('date_init'))
        date_end = parse_datetime(request.GET.get('date_end'))

        # Per user id get:
        # devicePositionInTime count
        devices = DevicePositionInTime.objects.filter(timeStamp__range=[date_init, date_end])
        devices = devices.values('phoneId').annotate(num_positions=Count('id'))
        # bus and busstops events -> eventFor*
        busevents = EventForBusv2.objects.filter(timeCreation__range=[date_init, date_end])
        busevents = busevents.values('phoneId').annotate(num_events=Count('id'))
        stopsevents = EventForBusStop.objects.filter(timeCreation__range=[date_init, date_end])
        stopsevents = stopsevents.values('phoneId').annotate(num_events=Count('id'))
        # confirms and declines fro bus and busstops events -> statistic*
        # TODO: if the timeStamp is the first of the event, is the creation of the event and must not be counted
        confirmsbus = StadisticDataFromRegistrationBus.objects.filter(timeStamp__range=[date_init, date_end],
                                                                      confirmDecline='confirm')
        confirmsbus = confirmsbus.values('phoneId').annotate(num_confirms=Count('id'))
        declinesbus = StadisticDataFromRegistrationBus.objects.filter(timeStamp__range=[date_init, date_end],
                                                                      confirmDecline='decline')
        declinesbus = declinesbus.values('phoneId').annotate(num_declines=Count('id'))

        confirmsstop = StadisticDataFromRegistrationBusStop.objects.filter(timeStamp__range=[date_init, date_end],
                                                                           confirmDecline='confirm')
        confirmsstop = confirmsstop.values('phoneId').annotate(num_confirms=Count('id'))
        declinesstop = StadisticDataFromRegistrationBusStop.objects.filter(timeStamp__range=[date_init, date_end],
                                                                           confirmDecline='decline')
        declinesstop = declinesstop.values('phoneId').annotate(num_declines=Count('id'))
        # tokens
        tokens = PoseInTrajectoryOfToken.objects.filter(timeStamp__range=[date_init, date_end]).values('token_id')
        tokens = Token.objects.filter(pk__in=tokens)
        tokens = tokens.values('phoneId').annotate(num_tokens=Count('token'))
        # reports
        reports = Report.objects.filter(timeStamp__range=[date_init, date_end])
        reports = reports.values('phoneId').annotate(num_reports=Count('id'))
        # busstops checkeds -> nearbyBusesLog
        bschecks = NearByBusesLog.objects.filter(timeStamp__range=[date_init, date_end])
        bschecks = bschecks.values('phoneId').annotate(num_checks=Count('timeStamp'))

        tmp_response = {}
        for device in devices:
            tmp_response[str(device['phoneId'])] = {'devicePositionInTimeCount': device['num_positions']}

        for busevent in busevents:
            if str(busevent['phoneId']) in tmp_response:
                tmp_response[str(busevent['phoneId'])].update({'busEventCreationCount': busevent['num_events']})
            else:
                tmp_response[str(busevent['phoneId'])] = {'busEventCreationCount': busevent['num_events']}

        for stopsevent in stopsevents:
            if str(stopsevent['phoneId']) in tmp_response:
                tmp_response[str(stopsevent['phoneId'])].update({'busStopEventCreationCount': stopsevent['num_events']})
            else:
                tmp_response[str(stopsevent['phoneId'])] = {'busStopEventCreationCount': stopsevent['num_events']}

        for confirmbus in confirmsbus:
            if str(confirmbus['phoneId']) in tmp_response:
                tmp_response[str(confirmbus['phoneId'])].update({'confirmBusCount': confirmbus['num_confirms']})
            else:
                tmp_response[str(confirmbus['phoneId'])] = {'confirmBusCount': confirmbus['num_confirms']}

        for declinebus in declinesbus:
            if str(declinebus['phoneId']) in tmp_response:
                tmp_response[str(declinebus['phoneId'])].update({'declineBusCount': declinebus['num_declines']})
            else:
                tmp_response[str(declinebus['phoneId'])] = {'declineBusCount': declinebus['num_declines']}

        for confirmstop in confirmsstop:
            if str(confirmstop['phoneId']) in tmp_response:
                tmp_response[str(confirmstop['phoneId'])].update({'confirmBusStopCount': confirmstop['num_confirms']})
            else:
                tmp_response[str(confirmstop['phoneId'])] = {'confirmBusStopCount': confirmstop['num_confirms']}

        for declinestop in declinesstop:
            if str(declinestop['phoneId']) in tmp_response:
                tmp_response[str(declinestop['phoneId'])].update({'declineBusStopCount': declinestop['num_declines']})
            else:
                tmp_response[str(declinestop['phoneId'])] = {'declineBusStopCount': declinestop['num_declines']}

        for token in tokens:
            if str(token['phoneId']) in tmp_response:
                tmp_response[str(token['phoneId'])].update({'tokenCount': token['num_tokens']})
            else:
                tmp_response[str(token['phoneId'])] = {'tokenCount': token['num_tokens']}

        for report in reports:
            if str(report['phoneId']) in tmp_response:
                tmp_response[str(report['phoneId'])].update({'reportCount': report['num_reports']})
            else:
                tmp_response[str(report['phoneId'])] = {'reportCount': report['num_reports']}

        for bscheck in bschecks:
            if str(bscheck['phoneId']) in tmp_response:
                tmp_response[str(bscheck['phoneId'])].update({'busStopCheckCount': bscheck['num_checks']})
            else:
                tmp_response[str(bscheck['phoneId'])] = {'busStopCheckCount': bscheck['num_checks']}

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


#@user_passes_test(is_transapp)
@login_required
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
                "active_users": len(list(set([position.phoneId for position in period_positions]))),
                "reporting_users": len(list(set(
                    [event.phoneId for event in period_bus_stop_events] + [event.phoneId for event in
                                                                          period_bus_events]))),
                "reports": len(period_bus_stop_events) + len(period_bus_events),
                "active_events": len(bus_active_events) + len(bus_stop_active_events)
            })
        return JsonResponse(data, safe=False)


#@user_passes_test(is_transapp)
@login_required
def getUsersPositions(request):
    if request.method == 'GET':
        date_init = parse_datetime(request.GET.get('date_init'))
        date_end = parse_datetime(request.GET.get('date_end'))

        devices = DevicePositionInTime.objects.filter(timeStamp__range=[date_init, date_end]).\
            order_by('phoneId', 'timeStamp').values()

        response = {}
        for device in devices:
            device_id = str(device['phoneId'])

            # already exists: save the last one
            if device_id in response:
                response[device_id]['last'] = {
                    'lat': device['latitude'],
                    'lon': device['longitude'],
                    'timeStamp': device['timeStamp']
                }
            else:
                # new device
                response[device_id] = {
                    'first': {
                        'lat': device['latitude'],
                        'lon': device['longitude'],
                        'timeStamp': device['timeStamp']
                    }
                }

        return JsonResponse(response, safe=False)


#@user_passes_test(is_transapp)
@login_required
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
            values('latitude', 'longitude', 'timeStamp', 'token_id', 'service')
        
        for tokenpose in tokenposes:
            if str(tokenpose['token_id']) not in response:
                response[str(tokenpose['token_id'])] = {'service': tokenpose['service'],
                                                        'origin': {'latitude': tokenpose['latitude'],
                                                                   'longitude': tokenpose['longitude'],
                                                                   'timeStamp': tokenpose['timeStamp']}}
        
        tokenposes = PoseInTrajectoryOfToken.objects.filter(token_id__in=response).order_by('token_id',
                                                                                            '-timeStamp')

        for resp in response:
            response[resp].update({'destination': {'latitude': tokenposes.filter(token_id=resp).first().latitude,
                                                   'longitude': tokenposes.filter(token_id=resp).first().longitude,
                                                   'timeStamp': tokenposes.filter(
                                                       token_id=resp).first().timeStamp}})
        
        return JsonResponse(response, safe=False)


# ----------------------------------------------------------------------------------------------------------------------
# TOOLS
# ----------------------------------------------------------------------------------------------------------------------


@login_required
def fullTableBus(request):
    template = "carrier/fullTableBus.html"
    categoryList = Event.objects.filter(eventType="bus").values_list("category", flat=True).distinct()
    types = map(lambda c: c.capitalize(), categoryList)
    context = {
        'types': types,
    }
    return render(request, template, context)


@login_required
def getFullTableBus(request):
    if request.method == 'GET':

        date_init = parse_datetime(request.GET.get('date_init'))
        date_end = parse_datetime(request.GET.get('date_end'))
        types = request.GET.getlist('types[]')

        routeList = Service.objects.filter(filter(request)).values_list("service", flat=True).distinct()
        query = EventForBusv2.objects.filter(busassignment__service__in=routeList,
                                             timeCreation__range=[date_init, date_end]).\
            exclude(busassignment__uuid__registrationPlate=WITHOUT_LICENSE_PLATE)

        if types:
            types = map(lambda c: c.lower(), types)
            query = query.filter(event__category__in=types)

        data = {
            'data': [report.getDictionary() for report in query]
        }

        return JsonResponse(data, safe=False)

@login_required
def fullTableStop(request):
    template = "carrier/fullTableStop.html"
    categoryList = Event.objects.filter(eventType="busStop").values_list("category", flat=True).distinct()
    types = map(lambda c: c.capitalize(), categoryList)
    context = {
        'types': types,
    }
    return render(request, template, context)


@login_required
def getFullTableStop(request):
    if request.method == 'GET':
        date_init = parse_datetime(request.GET.get('date_init'))
        date_end = parse_datetime(request.GET.get('date_end'))
        types = request.GET.getlist('types[]')

        query = EventForBusStop.objects.filter(timeCreation__range=[date_init, date_end])
        if types:
            types = map(lambda c: c.lower(), types)
            query = query.filter(event__category__in=types)

        data = {
            'data': [report.getDictionary() for report in query]
        }
        
        return JsonResponse(data, safe=False)

