# -*- coding: UTF-8 -*-
from AndroidRequests.models import EventForBusv2, EventForBusStop, TimePeriod, \
    Busv2, HalfHourPeriod, Report, ReportInfo, StadisticDataFromRegistrationBus, \
    StadisticDataFromRegistrationBusStop, BusStop, ZonificationTransantiago, PoseInTrajectoryOfToken
from django.contrib.gis.geos import Point
from django.db.models import Q
from datetime import datetime, time, date, timedelta
from django.utils import timezone

# your imports, e.g. Django models
import django
import re
import json
import sys
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "visualization.settings")

django.setup()

WITHOUT_LICENSE_PLATE= "No Info."

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
    for bus in Busv2.objects.filter(Q(transformed=False) | Q(transformed__isnull=True)):
        if bus.registrationPlate.upper() == 'DUMMYLPT':
            bus.registrationPlate = WITHOUT_LICENSE_PLATE
        elif regex.match(bus.registrationPlate.upper()) is not None:
            bus.registrationPlate = license_plate_formatter(bus.registrationPlate)
        else:
            pass

        counter += 1
        bus.transformed = True
        bus.save()

    sys.stdout.write("\n Bus rows modified: " + str(counter) + "\n")
    sys.stdout.flush()


def add_half_hour_periods(timestamp, minutes_to_filter):
    
    counter = 0
    for event in EventForBusv2.objects.filter(Q(transformed=False) | Q(transformed__isnull=True),
            timeStamp__gt=timestamp - timedelta(minutes=minutes_to_filter)):

        creationTime = timezone.localtime(event.timeCreation).time().replace(microsecond=0)
        hhperiod = HalfHourPeriod.objects.get(initial_time__lte=creationTime,
                                              end_time__gte=creationTime)
        event.halfHourPeriod = hhperiod
        event.save()
        counter += 1

    sys.stdout.write("\n EventForBus rows modified: "+str(counter) + "\n")
    sys.stdout.flush()
    counter = 0

    for event in EventForBusStop.objects.filter(
            Q(transformed=False) | Q(transformed__isnull=True),
            timeStamp__gt=timestamp - timedelta(minutes=minutes_to_filter)):

        creationTime = timezone.localtime(event.timeCreation).time().replace(microsecond=0)
        hhperiod = HalfHourPeriod.objects.get(initial_time__lte=creationTime,
                                              end_time__gte=creationTime)
        event.halfHourPeriod = hhperiod
        event.save()
        counter += 1

    sys.stdout.write("\n EventForBusStop rows modified: "+ str(counter) + "\n")
    sys.stdout.flush()


def license_plate_formatter(license_plate):
    """ give format 'XX XX XX' to license plate"""
    aa = license_plate[:2].upper()
    bb = license_plate[2:4].upper()
    num = license_plate[4:]
    license_plate = "{} {} {}".format(aa, bb, num)

    return license_plate


def add_report_info(timestamp, minutes_to_filter):
    """

    """
    counter = 0
    for report1 in Report.objects.filter(Q(transformed=False) | Q(transformed__isnull=True),
            timeStamp__gt=timestamp - timedelta(minutes=minutes_to_filter)):

        if report1.reportInfo is None or report1.reportInfo == "":
            continue

        reportJson = json.loads(report1.reportInfo)

        # user location fields
        userLatitude = None
        userLongitude = None
        if 'locationUser' in reportJson:
            userLocation = reportJson['locationUser']
            if 'latitude' in userLocation:
                strLat = userLocation['latitude']
                try:
                    userLatitude = float(strLat[2:])
                except:
                    pass

            if 'longitude' in userLocation:
                strLon = userLocation['longitude']
                try:
                    userLongitude = float(strLon[2:])
                except:
                    pass

        if "bus" in reportJson:
            licensePlate = reportJson['bus']['licensePlate'].upper()
            if reportJson['bus']['licensePlate'].upper() == "DUMMYLPT":
                plate = WITHOUT_LICENSE_PLATE
            elif licensePlate[2] == " " and licensePlate[5] == " ":
                plate = licensePlate.upper()
            else:
                plate = license_plate_formatter(licensePlate)

            if "machineId" in reportJson["bus"] and reportJson['bus']['machineId'] != "":
                busUUIDn = reportJson['bus']['machineId']
            elif Busv2.objects.filter(registrationPlate = plate).count() == 1:
                busUUIDn = Busv2.objects.filter(registrationPlate=plate).values_list("uuid", flat=True)[0]
            else:
                busUUIDn = None

            if busUUIDn is not None:
                plate = Busv2.objects.filter(uuid=busUUIDn).values_list("registrationPlate", flat=True)[0]

            if len(reportJson['bus']['service']) > 5:
                reportJson['bus']['service'] = '-'

            ReportInfo.objects.create(
                reportType = 'bus',
                busUUID = busUUIDn,
                service = reportJson['bus']['service'],
                registrationPlate = plate,
                latitude = reportJson['bus']['latitude'],
                longitude = reportJson['bus']['longitude'],
                userLongitude=userLongitude,
                userLatitude=userLatitude,
                report = report1)
            counter += 1

        elif 'bus_stop' in reportJson:
            ReportInfo.objects.create(
                reportType = 'busStop',
                stopCode = reportJson['bus_stop']['id'],
                latitude = reportJson['bus_stop']['latitude'],
                longitude = reportJson['bus_stop']['longitude'],
                userLongitude=userLongitude,
                userLatitude=userLatitude,
                report = report1)
            counter += 1

        elif 'busStop' in reportJson:
            ReportInfo.objects.create(
                reportType = 'busStop',
                stopCode = reportJson['busStop']['id'],
                latitude = reportJson['busStop']['latitude'],
                longitude = reportJson['busStop']['longitude'],
                userLongitude=userLongitude,
                userLatitude=userLatitude,
                report = report1)
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
        pnt = Point(ev.userLongitude, ev.userLatitude)
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

    dttz = timezone.localtime(dt)
    print(dttz)
    
    add_time_periods(dttz, arg_minutes_to_filter)
    validate_plates()
    add_half_hour_periods(dttz, arg_minutes_to_filter)
    # alwas add_report_info has to be done after validate_plates method
    add_report_info(dttz, arg_minutes_to_filter)
    add_county(dttz, arg_minutes_to_filter)
    add_direction_eventforbus_reportinfo(dttz, arg_minutes_to_filter)
    add_nearest_busstops(dttz, arg_minutes_to_filter)
