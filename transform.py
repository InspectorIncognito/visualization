import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "visualization.settings")

# your imports, e.g. Django models
import django
import re
import json
import sys
import pytz
django.setup()
from AndroidRequests.models import EventForBusv2, EventForBusStop, TimePeriod, \
	Busv2, HalfHourPeriod, Report, ReportInfo, StadisticDataFromRegistrationBus, \
	StadisticDataFromRegistrationBusStop, BusStop, zonificationTransantiago
from django.contrib.gis.geos import Point
from django.db.models import Q
from datetime import datetime, time, date, timedelta
from sys import argv
from pytz import timezone


def add_time_periods(timestamp, minutes_to_filter):
	counter = 0

	for ev in EventForBusv2.objects.filter(timeStamp__gt = timestamp - timedelta(minutes=minutes_to_filter), Q(transformed = False)|Q(transformed__isnull = True)):
		# time_to_match = ev.timeCreation
		# print(time_to_match)
		time = ev.timeCreation.time().replace(microsecond=0)
		timeperiod = None
		if ev.timeCreation.strftime("%A") == 'Saturday':
			timeperiod = TimePeriod.objects.get(day_type = 'Sabado',\
				initial_time__lte = time , end_time__gte = time)
		elif ev.timeCreation.strftime("%A") == 'Sunday':
			timeperiod = TimePeriod.objects.get(day_type = 'Domingo',\
				initial_time__lte = time , end_time__gte = time)
		else:
			#Working day
			timeperiod = TimePeriod.objects.get(day_type = 'Laboral',\
				initial_time__lte = time , end_time__gte = time)

		ev.time_period = timeperiod
		ev.save()
		counter = counter + 1

	sys.stdout.write("\n EventForBus rows modified: "+str(counter) + "\n")
	sys.stdout.flush()
	counter = 0

	for ev in EventForBusStop.objects.filter(timeStamp__gt = timestamp - timedelta(minutes=minutes_to_filter), Q(transformed = False)|Q(transformed__isnull = True)):
		# time_to_match = ev.timeCreation
		# print(time_to_match)
		time = ev.timeCreation.time().replace(microsecond=0)
		timeperiod = None
		if ev.timeCreation.strftime("%A") == 'Saturday':
			timeperiod = TimePeriod.objects.get(day_type = 'Sabado',\
				initial_time__lte = time , end_time__gte = time)
		elif ev.timeCreation.strftime("%A") == 'Sunday':
			timeperiod = TimePeriod.objects.get(day_type = 'Domingo',\
				initial_time__lte = time , end_time__gte = time)
		else:
			#Working day
			timeperiod = TimePeriod.objects.get(day_type = 'Laboral',\
				initial_time__lte = time , end_time__gte = time)

		ev.time_period = timeperiod
		ev.save()
		counter = counter + 1

	sys.stdout.write("\n EventForBusStop rows modified: "+str(counter) + "\n")
	sys.stdout.flush()


def validate_plates(timestamp):
	ex = r"\A[a-zA-Z]{4}[0-9]{2}\Z|\A[a-zA-Z]{2}[0-9]{4}\Z"
	regex = re.compile(ex)
	counter = 0
	for bus in Busv2.objects.filter(Q(transformed = False)|Q(transformed__isnull = True)):
		if bus.registrationPlate.upper() == 'DUMMYLPT':
			bus.registrationPlate = "No Info."
			counter = counter + 1
			bus.save()
		elif regex.match(bus.registrationPlate.upper()) != None:
			aa = bus.registrationPlate[:2].upper()
			bb = bus.registrationPlate[2:4].upper()
			num = bus.registrationPlate[4:]
			bus.registrationPlate = aa+" "+bb+" "+num
			counter = counter + 1
			bus.save()
		else:
			pass
	sys.stdout.write("\n Bus rows modified: "+str(counter) + "\n")
	sys.stdout.flush()


def add_half_hour_periods(timestamp, minutes_to_filter):
	
	counter = 0

	for ev in EventForBusv2.objects.filter(timeStamp__gt = timestamp - timedelta(minutes=minutes_to_filter), Q(transformed = False)|Q(transformed__isnull = True)):
		time = ev.timeCreation.time().replace(microsecond=0)
		hhperiod = HalfHourPeriod.objects.get(initial_time__lte = time , end_time__gte = time)
		ev.half_hour_period = hhperiod
		ev.save()
		counter = counter + 1

	sys.stdout.write("\n EventForBus rows modified: "+str(counter) + "\n")
	sys.stdout.flush()
	counter = 0

	for ev in EventForBusStop.objects.filter(timeStamp__gt = timestamp - timedelta(minutes=minutes_to_filter), Q(transformed = False)|Q(transformed__isnull = True)):
		time = ev.timeCreation.time().replace(microsecond=0)
		hhperiod = HalfHourPeriod.objects.get(initial_time__lte = time , end_time__gte = time)
		ev.half_hour_period = hhperiod
		ev.save()
		counter = counter + 1

	sys.stdout.write("\n EventForBusStop rows modified: "+str(counter) + "\n")
	sys.stdout.flush()


def add_report_info(timestamp, minutes_to_filter):

	counter = 0

	for report1 in Report.objects.filter(timeStamp__gt = timestamp - timedelta(minutes=minutes_to_filter), Q(transformed = False)|Q(transformed__isnull = True)):
		try:
			reportJson = json.loads(report1.reportInfo)
			if 'bus' in reportJson:
				aa = reportJson['bus']['licensePlate'][:2].upper()
				bb = reportJson['bus']['licensePlate'][2:4].upper()
				num = reportJson['bus']['licensePlate'][4:]
				plate = aa + " " + bb + " " + num
				busUUIDn = None
				try:
					busUUIDn = reportJson['bus']['machineId']
				except:
					if reportJson['bus']['licensePlate'].upper() != "DUMMYLPT":
						busUUIDn = Busv2.objects.get(registrationPlate = plate).uuid
				if reportJson['bus']['licensePlate'].upper() == "DUMMYLPT":
					plate = reportJson['bus']['licensePlate'].upper()
				reportinfo = ReportInfo(
					reportType = 'bus',
					busUUID = busUUIDn,
					service = reportJson['bus']['service'],
					registrationPlate = plate,
					latitud = reportJson['bus']['latitude'],
					longitud = reportJson['bus']['longitude'],
					report = report1,
					)
				reportinfo.save()
				counter = counter + 1
			elif 'bus_stop' in reportJson:
				reportinfo = ReportInfo(
					reportType = 'busStop',
					busStopCode = reportJson['bus_stop']['id'],
					latitud = reportJson['bus_stop']['latitude'],
					longitud = reportJson['bus_stop']['longitude'],
					report = report1,
					)
				reportinfo.save()
				counter = counter + 1
			elif 'busStop' in reportJson:
				reportinfo = ReportInfo(
					reportType = 'busStop',
					busStopCode = reportJson['busStop']['id'],
					latitud = reportJson['busStop']['latitude'],
					longitud = reportJson['busStop']['longitude'],
					report = report1,
					)
				reportinfo.save()
				counter = counter + 1
		except ValueError:
			pass

	sys.stdout.write("\n ReportInfo rows modified: "+str(counter) + "\n")
	sys.stdout.flush()


def add_county(timestamp, minutes_to_filter):

	counter = 0

	for ev in EventForBusv2.objects.filter(timeStamp__gt = timestamp- timedelta(minutes=minutes_to_filter), Q(transformed = False)|Q(transformed__isnull = True)):
		zon = None
		try:
			statistic_data = StadisticDataFromRegistrationBus.objects.filter(reportOfEvent = ev).order_by('-timeStamp')[0]
			ev_lat = statistic_data.latitud
			ev_long = statistic_data.longitud
			pnt = Point(ev_long, ev_lat)
			zon = zonificationTransantiago.objects.filter(geom__intersects = pnt)[0]
			ev.zonification = zon
			ev.save()
			counter = counter + 1
		except:
			pass

	sys.stdout.write("\n EventForBus rows modified: "+str(counter) + "\n")
	sys.stdout.flush()
	counter = 0
	
	for ev in EventForBusStop.objects.filter(timeStamp__gt = timestamp - timedelta(minutes=minutes_to_filter), Q(transformed = False)|Q(transformed__isnull = True)):
		zon = None
		try:
			statistic_data = StadisticDataFromRegistrationBusStop.objects.filter(reportOfEvent = ev).order_by('-timeStamp')[0]
			ev_lat = statistic_data.latitud
			ev_long = statistic_data.longitud
			pnt = Point(ev_long, ev_lat)
			zon = zonificationTransantiago.objects.filter(geom__intersects = pnt)[0]
			ev.zonification = zon
			ev.save()
			counter = counter + 1
		except:
			pass

	sys.stdout.write("\n EventForBusStop rows modified: "+str(counter) + "\n")
	sys.stdout.flush()
	counter = 0

	for ev in ReportInfo.objects.filter(Q(transformed = False)|Q(transformed__isnull = True)):
		pnt = Point(ev.longitud, ev.latitud)
		zon = None
		try:
			zon = zonificationTransantiago.objects.filter(geom__intersects = pnt)[0]
			counter = counter + 1
		except:
			pass
		ev.zonification = zon
		ev.save()

	sys.stdout.write("\n ReportInfo rows modified: "+str(counter) + "\n")
	sys.stdout.flush()


def add_nearest_busstops(timestamp, minutes_to_filter):
	sys.stdout.write("\nBusStop iteration\nTotal rows: "+str(BusStop.objects.all().count())+"\n")
	sys.stdout.write("\r Rows modified: 0")
	sys.stdout.flush()
	counter = 0
	last_bus_stop_events = EventForBusStop.objects.filter(timeStamp__gt = timestamp - timedelta(minutes=minutes_to_filter)).values_list('busStop_id', flat=True)

	for busstop in BusStop.objects.filter(code__in = last_bus_stop_events, Q(transformed = False)|Q(transformed__isnull = True)):
		busstop.point = Point(busstop.longitud, busstop.latitud)
		#print("creando point")
		busstop.save()
		counter = counter + 1
		if counter%100==0:
			sys.stdout.write("\r Rows modified: "+str(counter))
			sys.stdout.flush()
	sys.stdout.write("\n Total rows modified: "+str(counter) + "\n")
	#print("points creados")
	busstopsdict = BusStop.objects.values()
	sys.stdout.write("\nEvents for Bus iteration\nTotal rows: "+str(EventForBusv2.objects.all().count())+"\n")
	sys.stdout.write("\r Rows modified: 0")
	sys.stdout.flush()
	counter = 0
	for ev in EventForBusv2.objects.filter(timeStamp__gt = timestamp - timedelta(minutes=minutes_to_filter), Q(transformed = False)|Q(transformed__isnull = True)):
		nearest = []
		statistic_data = StadisticDataFromRegistrationBus.objects.filter(reportOfEvent = ev).order_by('-timeStamp')[0]
		ev_lat = statistic_data.latitud
		ev_long = statistic_data.longitud
		evpoint = Point(ev_long, ev_lat)
		for busstop in busstopsdict:
			busstop["distance"] = busstop['point'].distance(evpoint)
		nearest = sorted(busstopsdict, key = lambda busstop: busstop['distance'])
		ev.busStop1 = BusStop.objects.get(code = nearest[0]['code'])
		ev.busStop2 = BusStop.objects.get(code = nearest[1]['code'])
		ev.save()
		counter = counter +1
		if counter%100==0:
			sys.stdout.write("\r Rows modified: "+str(counter))
			sys.stdout.flush()
	sys.stdout.write("\n Total rows modified: "+str(counter) + "\n")


if __name__ == '__main__':

	ts1 = argv[1].split('.')[0]
	ts2 = ts1.split('__')[0]
	ts_time = ts1.split('__')[1]
	ts_date = ts2.split('_')[1]
	year = ts_date.split('-')[0]
	month = ts_date.split('-')[1]
	day = ts_date.split('-')[2]
	hour = ts_time.split('_')[0]
	minute = ts_time.split('_')[1]
	second = ts_time.split('_')[2]

	minutes_to_filter = int(argv[2])

	ddate = date(int(year),int(month),int(day))
	# print(ddate)
	dtime = time(int(hour), int(minute),int(second))
	# print(dtime)
	dt = datetime.combine(ddate, dtime)
	# print(dt)

	tz = timezone('Chile/Continental')

	dttz = tz.localize(dt)
	print(dttz)
	
	add_time_periods(dttz, minutes_to_filter)
	validate_plates(dttz)
	add_half_hour_periods(dttz, minutes_to_filter)
	add_report_info(dttz, minutes_to_filter)
	add_county(dttz, minutes_to_filter)
	add_nearest_busstops(dttz, minutes_to_filter)
