# -*- coding: UTF-8 -*-
from __future__ import print_function

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "visualization.settings")

# your imports, e.g. Django models
import django
import re
import json
import sys

django.setup()

from AndroidRequests.models import EventForBusv2, EventForBusStop, TimePeriod, \
    Busv2, HalfHourPeriod, Report, ReportInfo, StadisticDataFromRegistrationBus, \
    StadisticDataFromRegistrationBusStop, BusStop, ZonificationTransantiago, \
    PoseInTrajectoryOfToken
from django.contrib.gis.geos import Point
from django.db.models import Q
from datetime import datetime, time, date, timedelta
from pytz import timezone


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def add_time_periods(timestamp, minutes_to_filter):
    counter = 0

    for ev in EventForBusv2.objects.filter(
            Q(transformed=False) | Q(transformed__isnull=True),
            timeStamp__gt=timestamp - timedelta(minutes=minutes_to_filter)):

        # time_to_match = ev.timeCreation
        # print(time_to_match)
        creationTime = ev.timeCreation.time().replace(microsecond=0)
        if ev.timeCreation.strftime("%A") == 'Saturday':
            timePeriod = TimePeriod.objects.get(
                day_type='Sábado',
                initial_time__lte=creationTime,
                end_time__gte=creationTime
            )
        elif ev.timeCreation.strftime("%A") == 'Sunday':
            timePeriod = TimePeriod.objects.get(
                day_type='Domingo',
                initial_time__lte=creationTime,
                end_time__gte=creationTime
            )
        else:
            # Working day
            timePeriod = TimePeriod.objects.get(
                day_type='Laboral',
                initial_time__lte=creationTime,
                end_time__gte=creationTime
            )

        ev.timePeriod = timePeriod
        ev.save()
        counter += 1

    sys.stdout.write("\n EventForBus rows modified: " + str(counter) + "\n")
    sys.stdout.flush()
    counter = 0

    for ev in EventForBusStop.objects.filter(
            Q(transformed=False) | Q(transformed__isnull=True),
            timeStamp__gt=timestamp - timedelta(minutes=minutes_to_filter)):
        # time_to_match = ev.timeCreation
        # print(time_to_match)
        creationTime = ev.timeCreation.time().replace(microsecond=0)
        if ev.timeCreation.strftime("%A") == 'Saturday':
            timePeriod = TimePeriod.objects.get(
                day_type='Sábado',
                initial_time__lte=creationTime,
                end_time__gte=creationTime
            )
        elif ev.timeCreation.strftime("%A") == 'Sunday':
            timePeriod = TimePeriod.objects.get(
                day_type='Domingo',
                initial_time__lte=creationTime,
                end_time__gte=creationTime
            )
        else:
            # Working day
            timePeriod = TimePeriod.objects.get(
                day_type='Laboral',
                initial_time__lte=creationTime,
                end_time__gte=creationTime
            )

        ev.timePeriod = timePeriod
        ev.save()
        counter += 1

    sys.stdout.write("\n EventForBusStop rows modified: "+str(counter) + "\n")
    sys.stdout.flush()


def validate_plates():
    ex = r"\A[a-zA-Z]{4}[0-9]{2}\Z|\A[a-zA-Z]{2}[0-9]{4}\Z"
    regex = re.compile(ex)
    counter = 0
    for bus in Busv2.objects.filter(
            Q(transformed=False) | Q(transformed__isnull=True)):
        if bus.registrationPlate.upper() == 'DUMMYLPT':
            bus.registrationPlate = "No Info."
            counter += 1
            bus.transformed = True
            bus.save()
        elif regex.match(bus.registrationPlate.upper()) is not None:
            aa = bus.registrationPlate[:2].upper()
            bb = bus.registrationPlate[2:4].upper()
            num = bus.registrationPlate[4:]
            bus.registrationPlate = aa + " " + bb + " " + num
            counter += 1
            bus.transformed = True
            bus.save()

    sys.stdout.write("\n Bus rows modified: " + str(counter) + "\n")
    sys.stdout.flush()


def add_half_hour_periods(timestamp, minutes_to_filter):
    
    counter = 0
    for ev in EventForBusv2.objects.filter(
            Q(transformed=False) | Q(transformed__isnull=True),
            timeStamp__gt=timestamp - timedelta(minutes=minutes_to_filter)):

        creationTime = ev.timeCreation.time().replace(microsecond=0)
        hhperiod = HalfHourPeriod.objects.get(
            initial_time__lte=creationTime, end_time__gte=creationTime)
        ev.halfHourPeriod = hhperiod
        ev.save()
        counter += 1

    sys.stdout.write("\n EventForBus rows modified: "+str(counter) + "\n")
    sys.stdout.flush()
    counter = 0

    for ev in EventForBusStop.objects.filter(
            Q(transformed=False) | Q(transformed__isnull=True),
            timeStamp__gt=timestamp - timedelta(minutes=minutes_to_filter)):

        creationTime = ev.timeCreation.time().replace(microsecond=0)
        hhperiod = HalfHourPeriod.objects.get(
            initial_time__lte=creationTime, end_time__gte=creationTime)
        ev.halfHourPeriod = hhperiod
        ev.save()
        counter += 1

    sys.stdout.write("\n EventForBusStop rows modified: "+ str(counter) + "\n")
    sys.stdout.flush()


def add_report_info(timestamp, minutes_to_filter):

    counter = 0
    for report1 in Report.objects.filter(
            Q(transformed=False) | Q(transformed__isnull=True),
            timeStamp__gt=timestamp - timedelta(minutes=minutes_to_filter)):

        try:
            report_json = json.loads(report1.reportInfo)
        except ValueError:
            eprint("ERROR: to load  json reportInfo: {}".format(report1.reportInfo))
            continue

        # user location fields
        userLatitude = None
        userLongitude = None
        if 'locationUser' in report_json:
            userLoation = report_json['locationUser']
            if 'latitude' in userLoation:
                strLat = userLoation['latitude']
                try:
                    userLatitude = float(strLat[2:])
                except:
                    eprint("ERROR: problem with latitude format: {}".format(strLat))
                    pass

            if 'longitude' in userLoation:
                strLon = userLoation['longitude']
                try:
                    userLongitude = float(strLon[2:])
                except:
                    eprint("ERROR: problem with longitude format: {}".format(strLon))
                    pass

        # bus and bus stop fields
        if 'bus' in report_json:
            aa = report_json['bus']['licensePlate'][:2].upper()
            bb = report_json['bus']['licensePlate'][2:4].upper()
            num = report_json['bus']['licensePlate'][4:]
            plate = aa + " " + bb + " " + num
            busUUID = None
            try:
                busUUID = report_json['bus']['machineId']
            except:
                if report_json['bus']['licensePlate'].upper() != "DUMMYLPT":
                    busUUID = Busv2.objects.get(registrationPlate=plate).uuid

            if report_json['bus']['licensePlate'].upper() == "DUMMYLPT":
                plate = report_json['bus']['licensePlate'] = 'No Info.'
            if len(report_json['bus']['service']) > 5:
                report_json['bus']['service'] = 'JAVA'

            report_info = ReportInfo.objects.create(
                reportType='bus',
                busUUID=busUUID,
                service=report_json['bus']['service'],
                registrationPlate=plate,
                latitude=report_json['bus']['latitude'],
                longitude=report_json['bus']['longitude'],
                userLatitude=userLatitude,
                userLongitude=userLongitude,
                report=report1,
            )
            counter += 1

        elif 'bus_stop' in report_json:
            report_info = ReportInfo.objects.create(
                reportType='busStop',
                busStop_id=report_json['bus_stop']['id'],
                latitude=report_json['bus_stop']['latitude'],
                longitude=report_json['bus_stop']['longitude'],
                userLatitude=userLatitude,
                userLongitude=userLongitude,
                report=report1,
            )
            counter += 1

        elif 'busStop' in report_json:
            report_info = ReportInfo.objects.create(
                reportType='busStop',
                busStop_id=report_json['busStop']['id'],
                latitude=report_json['busStop']['latitude'],
                longitude=report_json['busStop']['longitude'],
                userLatitude=userLatitude,
                userLongitude=userLongitude,
                report=report1,
            )
            counter += 1
        
        report1.transformed = True
        report1.save()

    sys.stdout.write("\n ReportInfo rows modified: "+str(counter) + "\n")
    sys.stdout.flush()


def add_county(timestamp, minutes_to_filter):

    counter = 0
    for ev in EventForBusv2.objects.filter(
            Q(transformed=False) | Q(transformed__isnull=True),
            timeStamp__gt=timestamp-timedelta(minutes=minutes_to_filter)):

        try:
            statistic_data = StadisticDataFromRegistrationBus.objects.filter(reportOfEvent=ev).order_by('-timeStamp')[0]
            evLat = statistic_data.latitude
            evLong = statistic_data.longitude
            pnt = Point(evLong, evLat)
            zon = ZonificationTransantiago.objects.filter(geom__intersects=pnt)[0]
            ev.zonification = zon
            ev.save()
            counter += 1
        except:
            pass

    sys.stdout.write("\n EventForBus rows modified: " + str(counter) + "\n")
    sys.stdout.flush()
    counter = 0
    
    for ev in EventForBusStop.objects.filter(
            Q(transformed=False) | Q(transformed__isnull=True),
            timeStamp__gt=timestamp - timedelta(minutes=minutes_to_filter)):

        try:
            statistic_data = StadisticDataFromRegistrationBusStop.objects.filter(
                reportOfEvent=ev
            ).order_by('-timeStamp')[0]

            evLat = statistic_data.latitude
            evLong = statistic_data.longitude
            pnt = Point(evLong, evLat)
            zon = ZonificationTransantiago.objects.filter(geom__intersects=pnt)[0]
            ev.zonification = zon
            ev.save()
            counter += 1
        except:
            pass
        ev.transformed = True
        ev.save()

    sys.stdout.write("\n EventForBusStop rows modified: " + str(counter) + "\n")
    sys.stdout.flush()
    counter = 0

    for ev in ReportInfo.objects.filter(
            Q(transformed=False) | Q(transformed__isnull=True)):
        pnt = Point(ev.longitude, ev.latitude)
        zon = None
        try:
            zon = ZonificationTransantiago.objects.filter(geom__intersects=pnt)[0]
            counter += 1
        except:
            pass

        ev.zonification = zon
        ev.transformed = True
        ev.save()

    sys.stdout.write("\n ReportInfo rows modified: " + str(counter) + "\n")
    sys.stdout.flush()


def add_direction_eventforbus_reportinfo(timestamp, minutes_to_filter):
    counter = 0
    for ev in EventForBusv2.objects.filter(
            Q(transformed=False) | Q(transformed__isnull=True),
            timeStamp__gt=timestamp - timedelta(minutes=minutes_to_filter)):

        direction = None
        pose = PoseInTrajectoryOfToken.objects.filter(
            timeStamp__lte=ev.timeStamp,
            token__phoneId=ev.phoneId).order_by('-timeStamp').first()
        try:
            direction = pose.token.direction
            counter += 1
        except:
            pass
        ev.direction = direction
        ev.save()
    sys.stdout.write("\n EventForBus rows modified: "+str(counter) + "\n")
    sys.stdout.flush()

    counter = 0
    for report in ReportInfo.objects.filter(
            Q(transformed=False) | Q(transformed__isnull=True),
            reportType='bus'):

        direction = None
        pose = PoseInTrajectoryOfToken.objects.filter(
            timeStamp__lte=report.report.timeStamp,
            token__phoneId=report.report.phoneId).order_by('-timeStamp').first()
        try:
            direction = pose.token.direction
            counter += 1
        except:
            pass

        report.direction = direction
        report.save()

    sys.stdout.write("\n ReportInfo rows modified: " + str(counter) + "\n")
    sys.stdout.flush()


def add_nearest_busstops(timestamp, minutes_to_filter):
    sys.stdout.write("\nBusStop iteration")
    sys.stdout.write("\nTotal rows: " + str(BusStop.objects.all().count()) + "\n")
    sys.stdout.write("\r Rows modified: 0")
    sys.stdout.flush()
    counter = 0
    last_bus_stop_events = EventForBusStop.objects.filter(
        timeStamp__gt=timestamp - timedelta(minutes=minutes_to_filter)
    ).values_list('busStop_id', flat=True)

    for stop in BusStop.objects.filter(
            Q(transformed=False) | Q(transformed__isnull=True),
            code__in=last_bus_stop_events):

        stop.point = Point(stop.longitude, stop.latitude)
        stop.transformed = True
        stop.save()
        counter += 1
        if counter % 100 == 0:
            sys.stdout.write("\r Rows modified: " + str(counter))
            sys.stdout.flush()

    sys.stdout.write("\n Total rows modified: " + str(counter) + "\n")
    busstopsdict = BusStop.objects.values()
    sys.stdout.write("\nEvents for Bus iteration")
    sys.stdout.write("\nTotal rows: " + str(EventForBusv2.objects.all().count()) + "\n")
    sys.stdout.write("\r Rows modified: 0")
    sys.stdout.flush()
    counter = 0
    for ev in EventForBusv2.objects.filter(
            Q(transformed=False) | Q(transformed__isnull=True),
            timeStamp__gt=timestamp - timedelta(minutes=minutes_to_filter)):

        statistic_data = StadisticDataFromRegistrationBus.objects.filter(reportOfEvent=ev).order_by('-timeStamp')[0]
        evLat = statistic_data.latitude
        evLong = statistic_data.longitude
        evpoint = Point(evLong, evLat)
        for stop in busstopsdict:
            stop["distance"] = stop['point'].distance(evpoint)

        nearest = sorted(busstopsdict, key=lambda a_bus_stop: a_bus_stop['distance'])
        ev.busStop1 = BusStop.objects.get(code=nearest[0]['code'])
        ev.busStop2 = BusStop.objects.get(code=nearest[1]['code'])
        ev.transformed = True
        ev.save()
        counter += 1

        if counter % 100 == 0:
            sys.stdout.write("\r Rows modified: " + str(counter))
            sys.stdout.flush()

    sys.stdout.write("\n Total rows modified: " + str(counter) + "\n")


if __name__ == '__main__':

    ts1 = sys.argv[1].split('.')[0]
    ts2 = ts1.split('__')[0]
    ts_time = ts1.split('__')[1]
    ts_date = ts2.split('_')[1]
    year = ts_date.split('-')[0]
    month = ts_date.split('-')[1]
    day = ts_date.split('-')[2]
    hour = ts_time.split('_')[0]
    minute = ts_time.split('_')[1]
    second = ts_time.split('_')[2]

    arg_minutes_to_filter = int(sys.argv[2])

    ddate = date(int(year), int(month), int(day))
    # print(ddate)
    dtime = time(int(hour), int(minute), int(second))
    # print(dtime)
    dt = datetime.combine(ddate, dtime)
    # print(dt)

    tz = timezone('Chile/Continental')

    dttz = tz.localize(dt)
    print(dttz)
    
    add_time_periods(dttz, arg_minutes_to_filter)
    validate_plates()
    add_half_hour_periods(dttz, arg_minutes_to_filter)
    add_report_info(dttz, arg_minutes_to_filter)
    add_county(dttz, arg_minutes_to_filter)
    add_direction_eventforbus_reportinfo(dttz, arg_minutes_to_filter)
    add_nearest_busstops(dttz, arg_minutes_to_filter)
