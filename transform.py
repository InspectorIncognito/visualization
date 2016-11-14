import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "visualization.settings")

# your imports, e.g. Django models
import django
django.setup()
from AndroidRequests.models  import EventForBusv2, EventForBusStop, TimePeriod, \
	Busv2, HalfHourPeriod, Report, ReportInfo, StadisticDataFromRegistrationBus, \
	StadisticDataFromRegistrationBusStop

def add_time_periods():
    
    for ev in EventForBusv2.objects.all():
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

    for ev in EventForBusStop.objects.all():
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

def validate_plates():
	ex = r"\A[a-zA-Z]{4}[0-9]{2}\Z|\A[a-zA-Z]{2}[0-9]{4}\Z"
	regex = re.compile(ex)
	for bus in Busv2.objects.all():
		if bus.registrationPlate.upper() == 'DUMMYLPT':
			bus.registrationPlate = "No Info."
		elif regex.match(bus.registrationPlate.upper()) != None :
			aa = bus.registrationPlate[:2].upper()
			bb = bus.registrationPlate[2:4].upper()
			num = bus.registrationPlate[4:]
			bus.registrationPlate = aa+" "+bb+" "+num
		else:
			pass

		bus.save()

def add_half_hour_periods():
    
    for ev in EventForBusv2.objects.all():
        time = ev.timeCreation.time().replace(microsecond=0)
        hhperiod = HalfHourPeriod.objects.get(initial_time__lte = time , end_time__gte = time)
        ev.half_hour_period = hhperiod
        ev.save()

    for ev in EventForBusStop.objects.all():
        time = ev.timeCreation.time().replace(microsecond=0)
        hhperiod = HalfHourPeriod.objects.get(initial_time__lte = time , end_time__gte = time)
        ev.half_hour_period = hhperiod
        ev.save()

def add_report_info():
	for report1 in Report.objects.all():
		print(report1.pk)
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

			elif 'bus_stop' in reportJson:
				reportinfo = ReportInfo(
					reportType = 'busStop',
					busStopCode = reportJson['bus_stop']['id'],
					latitud = reportJson['bus_stop']['latitude'],
					longitud = reportJson['bus_stop']['longitude'],
					report = report1,
					)
				reportinfo.save()

			elif 'busStop' in reportJson:
				reportinfo = ReportInfo(
					reportType = 'busStop',
					busStopCode = reportJson['busStop']['id'],
					latitud = reportJson['busStop']['latitude'],
					longitud = reportJson['busStop']['longitude'],
					report = report1,
					)
				reportinfo.save()

		except ValueError:
			pass

def add_county():
    for st in StadisticDataFromRegistrationBus.objects.all():
        aux = st.latitud
        st.latitud = st.longitud
        st.longitud = aux
        st.save()

    for ev in EventForBusv2.objects.all():
        statistic_data = StadisticDataFromRegistrationBus.objects.filter(reportOfEvent = ev).order_by('-timeStamp')[0]
        ev_lat = statistic_data.latitud
        ev_long = statistic_data.longitud
        pnt = Point(ev_long, ev_lat)
        county = "Fuera de la zona"
        try:
            county = zonificationTransantiago.objects.filter(geom__intersects = pnt)[0].comuna
        except:
            pass
        ev.county = county
        ev.save()
    
    for ev in EventForBusStop.objects.all():
        statistic_data = StadisticDataFromRegistrationBusStop.objects.filter(reportOfEvent = ev).order_by('-timeStamp')[0]
        ev_lat = statistic_data.latitud
        ev_long = statistic_data.longitud
        pnt = Point(ev_long, ev_lat)
        county = "Fuera de la zona"
        try:
            county = zonificationTransantiago.objects.filter(geom__intersects = pnt)[0].comuna
        except:
            pass
        ev.county = county
        ev.save()

    for ev in ReportInfo.objects.all():

        pnt = Point(ev.longitud, ev.latitud)
        county = "Fuera de la zona"
        try:
            county = zonificationTransantiago.objects.filter(geom__intersects = pnt)[0].comuna
        except:
            pass
        ev.county = county
        ev.save()

def add_nearest_busstops():
    eventsforbusv2 = apps.get_model('AndroidRequests', 'EventForBusv2')
    busstops = apps.get_model('AndroidRequests', 'BusStop')
    statisticsfrombus = apps.get_model('AndroidRequests', 'StadisticDataFromRegistrationBus')
    zonification = apps.get_model('AndroidRequests', 'zonificationTransantiago')
    sys.stdout.write("\nBusStop iteration\nTotal rows: "+str(BusStop.objects.all().count())+"\n")
    sys.stdout.write("\r Rows modified: 0")
    sys.stdout.flush()
    counter = 0
    for busstop in BusStop.objects.all():
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
    for ev in EventForBusv2.objects.all():
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
	add_time_periods()