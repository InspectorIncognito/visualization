import uuid
from django.utils import timezone
from django.contrib.gis.db import models
import pytz

import logging

WHITOUT_DATA_LABEL = "No Info."

class ReportInfo(models.Model):
    """ Table for the report info data in Report """
    BUS = "bus"
    STOP = "busStop"
    REPORT_TYPE = (
        (BUS, 'An event for the bus.'),
        (STOP, 'An event for the busStop.'))
    reportType = models.CharField('Event Type', max_length=7, choices=REPORT_TYPE)
    """ Represents the element to which the report refers """
    busUUID = models.UUIDField(null=True)
    """ Bus uuid """
    service = models.CharField('Service', max_length=11, null=True)
    """ Bus service """
    registrationPlate = models.CharField(max_length=8)
    """ Bus registrationplate """
    stopCode = models.CharField('StopCode', max_length=6, null=True)
    """ Bus stop code"""
    longitude = models.FloatField('Longitude', null=False, blank=False)
    """ longitude from the geolocation """
    latitude = models.FloatField('Latitude', null=False, blank=False)
    """ latitude from the geolocation """
    report = models.ForeignKey('Report', verbose_name='The Report')
    """ Link to the report """
    zonification = models.ForeignKey('zonificationTransantiago', verbose_name='zonification', null=True)
    """Indicates the zonification for the event"""
    transformed = models.NullBooleanField(default=False, verbose_name=b'Transformed')
    """Indicates if the current row was transformed """
    direction = models.CharField(max_length=1, null=True)
    """ route direction that the bus was doing. It can be 'R' or 'I' """
    userLatitude = models.FloatField(null=True)
    """ the latitude of user who reported this """
    userLongitude = models.FloatField(null=True)
    """ the longitude of user who reported this """

    def getDictionary(self):
        res = dict()
        res["registrationPlate"] = self.registrationPlate if self.registrationPlate else WHITOUT_DATA_LABEL
        res["service"] = self.service if self.service else WHITOUT_DATA_LABEL

        res["busStopCode"] = WHITOUT_DATA_LABEL
        res["busStopName"] = WHITOUT_DATA_LABEL
        if self.stopCode is not None:
            busStopName = BusStop.objects.filter(code=self.stopCode).order_by('-gtfs__timeCreation').first().name
            res["busStopCode"] = self.stopCode
            res["busStopName"] = busStopName.replace(self.stopCode + "-", "", 1)

        report = self.report.getDictionary()
        res["imageName"] = report["imageName"]
        res["timeStamp"] = report["timeStamp"]
        res["message"] = report["message"]
        res["reportType"] = self.reportType
        res["latitude"] = self.userLatitude
        res["longitude"] = self.userLongitude
        res["userLatitude"] = self.userLatitude
        res["userLongitude"] = self.userLongitude
        res["commune"] = self.zonification.comuna if self.zonification else WHITOUT_DATA_LABEL
        res["direction"] = self.direction if self.direction else WHITOUT_DATA_LABEL
        return res


class TimePeriod(models.Model):
    """ Time period with standar names """
    day_type = models.CharField(max_length=8)
    """ Type of day: Working day, Saturday, Sunday """
    name = models.CharField(max_length=30)
    """ Standar name """
    initial_time = models.TimeField(auto_now=False, auto_now_add=False)
    """ Initial time for the period """
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    """ End time for the period """


class HalfHourPeriod(models.Model):
    """ Time period with standar names """
    name = models.CharField(max_length=30)
    """ Name of the period """
    initial_time = models.TimeField(auto_now=False, auto_now_add=False)
    """ Initial time for the period """
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    """ End time for the period """


class Location(models.Model):
    """ Some of our models require to set a geolocation (coodinates)"""
    longitude = models.FloatField('Longitude', null=False, blank=False)
    """ longitude from the geolocation """
    latitude = models.FloatField('Latitude', null=False, blank=False)
    """ longitude from the geolocation """

    class Meta:
        """This makes that the fields here define are added to the tables that
        extends this, and no ForeignKey is made."""
        abstract = True


class DevicePositionInTime(Location):
    """Helps storing the position of active users"""
    timeStamp = models.DateTimeField("Time Stamp", null=False, blank=False)
    """ Specific date time when the server received the device's position """
    phoneId = models.UUIDField()
    """ To identify the AndroidRequests owner """


class Event(models.Model):
    BUS = "bus"
    STOP = "Stop"
    """Here are all the events, it's configuration and information."""
    id = models.CharField('Identifier', max_length=8, primary_key=True)
    """ string code that identifies the event """
    name = models.CharField('Name', max_length=30, null=False, blank=False)
    """ It's a short name for the event """
    description = models.CharField('Description', max_length=140, null=True)
    """ Explain the event with a better detail level """
    lifespam = models.IntegerField('Lifespan', default=30)  # this value is in minutes
    """ It represents the time (in minutes) during which the event is valid since the last report """
    category = models.CharField('Category', max_length=20)
    """ group of events with a similar context """

    REPORT_ORIGIN = (
        ('i', 'the event was taken inside the bus'),  # this is an I for inside
        ('o', 'the event was taken from a bustop'),)  # this is an O for outside
    REPORT_TYPE = (
        (BUS, 'An event for the bus.'),
        (STOP, 'An event for the busStop.'))
    origin = models.CharField('Origin', max_length=1, choices=REPORT_ORIGIN, default='o')
    """ Represents the place from where the event was reported """
    eventType = models.CharField('Event Type', max_length=7, choices=REPORT_TYPE)
    """ Represents the element to which the event refers """

    def getDictionary(self):
        """ Return a dictionary with the event information """
        dictionary = dict()
        dictionary['name'] = self.name
        dictionary['description'] = self.description
        dictionary['eventcode'] = self.id
        return dictionary

    def __str__(self):
        return "category %s and description %s" % (self.category, self.description)


##
#
# These are the models to handle the event registration for a bus or a bus stop
#
##
class StadisticDataFromRegistration(Location):
    timeStamp = models.DateTimeField('Time Stamp', null=False, blank=False)
    """ Specific date time when the server received the event registration """
    confirmDecline = models.CharField('Confirm - Decline', max_length=10)
    """ Represents if the event was confirmed or declined """
    phoneId = models.UUIDField()
    """ To identify the AndroidRequests owner """

    class Meta:
        abstract = True


class StadisticDataFromRegistrationBus(StadisticDataFromRegistration):
    """ Save the report done for a user to confirm or decline a bus event """
    reportOfEvent = models.ForeignKey('EventForBusv2', verbose_name='Bus Event')
    gpsLongitude = models.FloatField('GPS Longitude', null=True, blank=False)
    """ longitude of the bus GPS """
    gpsLatitude = models.FloatField('GPS Latitude', null=True, blank=False)
    """ latitude of the bus GPS """
    gpsTimeStamp = models.DateTimeField('GPS Time Stamp', null=True, blank=False)
    """ date time of the bus GPS position data """
    distance = models.FloatField('Distance', null=True, blank=False)
    """ distance from the report to the bus GPS """

    def getDictionary(self):
        dictionary = dict()
        dictionary["lat"] = self.latitude
        dictionary["lon"] = self.longitude
        dictionary["report"] = self.reportOfEvent.getDictionary()
        return dictionary


class StadisticDataFromRegistrationBusStop(StadisticDataFromRegistration):
    """ Save the report done for a user to confirm or decline a bus stop event """
    reportOfEvent = models.ForeignKey('EventForBusStop', verbose_name='Bus Stop Event')


class EventRegistration(models.Model):
    """This model stores the reports of events coming from the passagers of the system of public transport buses."""
    timeStamp = models.DateTimeField('Time Stamp')  # lastime it was updated
    """ Specific date time when the server received the event registration """
    timeCreation = models.DateTimeField('Creation Time')  # the date and time when it was first reported
    """ Specific date time when the server received for the first time the event registration """
    expireTime = models.DateTimeField(null=True)
    """ Specific date time when event expired """
    event = models.ForeignKey(Event, verbose_name='The event information')
    eventConfirm = models.IntegerField('Confirmations', default=1)
    """ Amount of confirmations for this event """
    eventDecline = models.IntegerField('Declines', default=0)
    """ amount of declinations for this event """
    phoneId = models.UUIDField()
    """ To identify the AndroidRequests owner """
    fixed = models.NullBooleanField('Fixed', default=False)
    """ To know if the event is 'fixed' and stop showing it"""
    broken = models.BooleanField(default=False)
    """ to indicate that event expired by some brokenType """
    # list  of criterion of broken type
    PERCENTAGE_BETWEEN_POSITIVE_AND_NEGATIVE = 'percentage'
    brokenType = models.CharField(max_length=50, default=None, null=True)
    """ indicate why event is broken """

    class Meta:
        abstract = True

    def getDictionary(self):
        """A dictionary with the event information, just what was of interest to return to the app."""
        dictionary = dict()

        dictionary['eventConfirm'] = self.eventConfirm
        dictionary['eventDecline'] = self.eventDecline
        creation = timezone.localtime(self.timeCreation, pytz.timezone('Chile/Continental'))
        stamp = timezone.localtime(self.timeStamp, pytz.timezone('Chile/Continental'))
        dictionary['timeCreation'] = creation.strftime("%d-%m-%Y %H:%M:%S")
        dictionary['timeStamp'] = stamp.strftime("%d-%m-%Y %H:%M:%S")
        eventDictionary = self.event.getDictionary()
        dictionary.update(eventDictionary)

        return dictionary


class EventForBusStop(EventRegistration):
    """This model stores the reported events for the busStop"""
    stopCode = models.CharField(max_length=6, db_index=True, verbose_name='Stop Code')
    """Indicates the bus stop to which the event refers"""
    aditionalInfo = models.CharField('Additional Information', max_length=140, default='nothing')
    """ Saves additional information required by the event """
    timePeriod = models.ForeignKey('TimePeriod', verbose_name=b'Time Period', null=True)
    """Indicates the Transantiago Time Period of the event"""
    halfHourPeriod = models.ForeignKey('HalfHourPeriod', verbose_name=b'Half Hour Period', null=True)
    """Indicates the half hour time period of the event"""
    zonification = models.ForeignKey('zonificationTransantiago', verbose_name='zonification', null=True)
    """Indicates the zonification for the event"""
    transformed = models.NullBooleanField(default=False, verbose_name=b'Transformed')
    """Indicates if the current row was transformed """

    def getDictionary(self):
        """A dictionary with the event information"""
        dictionary = super(EventForBusStop, self).getDictionary()
        dictionary['type'] = self.event.name.capitalize()
        dictionary['id'] = self.id
        dictionary['category'] = self.event.category.capitalize()
        dictionary['stopCode'] = self.stopCode
        dictionary['fixed'] = "Si" if self.fixed else "No"
        dictionary['category'] = self.event.category.capitalize()
        dictionary['zone777'] = self.zonification.zona if self.zonification else WHITOUT_DATA_LABEL
        dictionary['commune'] = self.zonification.comuna if self.zonification else WHITOUT_DATA_LABEL
        dictionary['typeOfDay'] = self.timePeriod.day_type if self.timePeriod else WHITOUT_DATA_LABEL
        dictionary['periodHour'] = self.halfHourPeriod.name if self.halfHourPeriod else WHITOUT_DATA_LABEL
        dictionary['periodTransantiago'] = self.timePeriod.name if self.timePeriod else WHITOUT_DATA_LABEL
        dictionary['additionalInfo'] = self.aditionalInfo if self.aditionalInfo else WHITOUT_DATA_LABEL

        return dictionary

class EventForBusv2(EventRegistration):
    """This model stores the reported events for the Bus"""
    busassignment = models.ForeignKey('Busassignment', verbose_name='the bus')
    """Indicates the bus to which the event refers"""
    timePeriod = models.ForeignKey('TimePeriod', verbose_name=b'Time Period', null=True)
    """Indicates the Transantiago Time Period of the event"""
    halfHourPeriod = models.ForeignKey('HalfHourPeriod', verbose_name=b'Half Hour Period', null=True)
    """Indicates the half hour time period of the event"""
    zonification = models.ForeignKey('zonificationTransantiago', verbose_name='zonification', null=True)
    """Indicates the zonification for the event"""
    busStop1 = models.CharField(max_length=6, verbose_name='Bus Stop1', null=True)
    """Indicates the 1 nearest bus stop"""
    busStop2 = models.CharField(max_length=6, verbose_name='Bus Stop2', null=True)
    """Indicates the 2 nearest bus stop"""
    transformed = models.NullBooleanField(default=False, verbose_name=b'Transformed')
    """Indicates if the current row was transformed """
    direction = models.CharField(max_length=1, null=True)
    """ route direction that the bus was doing. It can be 'R' or 'I' """

    def getDictionary(self):
        """A dictionary with the event information"""
        dictionary = dict()

        dictionary['eventConfirm'] = self.eventConfirm
        dictionary['eventDecline'] = self.eventDecline
        creation = timezone.localtime(self.timeCreation, pytz.timezone('Chile/Continental'))
        stamp = timezone.localtime(self.timeStamp, pytz.timezone('Chile/Continental'))
        dictionary['timeCreation'] = creation.strftime("%d-%m-%Y %H:%M:%S")
        dictionary['timeStamp'] = stamp.strftime("%d-%m-%Y %H:%M:%S")
        dictionary['service'] = self.busassignment.service if self.busassignment else WHITOUT_DATA_LABEL
        dictionary['plate'] = self.busassignment.uuid.registrationPlate if self.busassignment else WHITOUT_DATA_LABEL
        dictionary['type'] = self.event.name.capitalize()
        dictionary['busStop1'] = self.busStop1#.name if self.busStop1 else WHITOUT_DATA_LABEL
        dictionary['busStop2'] = self.busStop2#.name if self.busStop2 else WHITOUT_DATA_LABEL
        dictionary['fixed'] = "Si" if self.fixed else "No"
        dictionary['id'] = self.id
        dictionary['category'] = self.event.category.capitalize()
        dictionary['zone777'] = self.zonification.zona if self.zonification else WHITOUT_DATA_LABEL
        dictionary['commune'] = self.zonification.comuna if self.zonification else WHITOUT_DATA_LABEL
        dictionary['typeOfDay'] = self.timePeriod.day_type if self.timePeriod else WHITOUT_DATA_LABEL
        dictionary['periodHour'] = self.halfHourPeriod.name if self.halfHourPeriod else WHITOUT_DATA_LABEL
        dictionary['periodTransantiago'] = self.timePeriod.name if self.timePeriod else WHITOUT_DATA_LABEL

        dictionary['direction'] = self.direction if self.direction else WHITOUT_DATA_LABEL

        return dictionary


##
#
# The end for the model for the registration
#
##

class ServicesByBusStop(models.Model):
    """This model helps to determine the direction of the bus service I or R.
    All of this is tied to the bus stop code and the service provided by it.
    It's useful to have the direction of the service to be able to determine position of the bus."""
    code = models.CharField(max_length=11, null=False,
                            blank=False)  # EX: 506I or 506R, R and I indicate "Ida" and "Retorno"
    """ Service code where the last character indicates the direction of this """
    busStop = models.ForeignKey('BusStop', verbose_name='the busStop')
    """ Bus stops where the service is stopped """
    service = models.ForeignKey('Service', verbose_name='the service')
    """ Service that stops in the bus stop """
    gtfs = models.ForeignKey('GTFS', verbose_name='gtfs version')
    """ gtfs version """

    class Meta:
        unique_together = ('code', 'busStop', 'gtfs')


class BusStop(Location):
    """Represents the busStop itself."""
    code = models.CharField('Code', max_length=6)  # For example PA443
    """ Code that identifies the bus stop """
    name = models.CharField('Name', max_length=70, null=False, blank=False)
    """ Name of the bus stop, indicating the streets """
    gtfs = models.ForeignKey('GTFS', verbose_name='gtfs version')
    """ gtfs version """
    transformed = models.NullBooleanField(default=False, verbose_name=b'Transformed')
    """Indicates if the current row was transformed """
    point = models.PointField(srid=32140, verbose_name='The point', null=True)

    class Meta:
        unique_together = ('code', 'gtfs')

    def getDictionary(self):
        """usefull information regarding the bus."""
        dictionary = dict()

        dictionary['codeBusStop'] = self.code
        dictionary['nameBusStop'] = self.name

        return dictionary


class Service(models.Model):
    """ Represent a Service like '506' and save his AndroidRequests """
    service = models.CharField('Service', max_length=11)
    """ Represent the service, like '506c' without direction """
    origin = models.CharField(max_length=100, null=False, blank=False)
    """ Indicates the place where the service start his travel """
    destiny = models.CharField(max_length=100, null=False, blank=False)
    """ Indicates the place where the service end his travel """
    color = models.CharField(max_length=7, default='#00a0f0')
    """ Indicates the color in hexadecimal for the service """
    color_id = models.IntegerField(default=0)
    """ Represent an index for a color array in the app """
    busStops = models.ManyToManyField(BusStop, verbose_name='Bus Stops', through=ServicesByBusStop)
    gtfs = models.ForeignKey('GTFS', verbose_name='gtfs version')
    """ gtfs version """

    class Meta:
        unique_together = ('service', 'gtfs')


class ServiceNotFoundException(Exception):
    """ error produced when service information does not exist in service table """


class ServiceDistanceNotFoundException(Exception):
    """ error produced when it is not possible to get distance between a service and bus stop """


class Busv2(models.Model):
    """Represent a bus like the unique combination of registration plate and service as one.
    So there can be two buses with the same service and two buses with the same registration plate.
    The last thing means that one physical bus can work in two different services."""
    registrationPlate = models.CharField(max_length=8)
    """ It's the registration plate for the bus, without hyphen """
    # service = models.CharField(max_length=5, null=False, blank=False)
    # """ It indicates the service performed by the bus """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    """ Unique ID to primarily identify Buses created without registrationPlate """
    # events = models.ManyToManyField(Event,  verbose_name='the event' ,through=EventForBus)
    transformed = models.NullBooleanField(default=False, verbose_name=b'Transformed')
    """Indicates if the current row was transformed """


class Busassignment(models.Model):
    """Represent a bus like the unique combination of registration plate and service as one.
    So there can be two buses with the same service and two buses with the same registration plate.
    The last thing means that one physical bus can work in two different services."""
    # registrationPlate = models.CharField(max_length=8)
    """ It's the registration plate for the bus, without hyphen """
    service = models.CharField(max_length=11, null=False, blank=False)
    """ It indicates the service performed by the bus """
    uuid = models.ForeignKey(Busv2, verbose_name='Thebusv2')
    """ Unique ID to primarily identify Buses created without registrationPlate """
    events = models.ManyToManyField(Event, verbose_name='the event', through=EventForBusv2)

    class Meta:
        unique_together = ('uuid', 'service')

    def getDirection(self, pBusStop, pDistance):
        """Given a bus stop and the distance from the bus to the bus stop, return the address to which point the bus."""
        try:
            serviceCode = ServicesByBusStop.objects.get(busStop=pBusStop, service=self.service).code
        except ServicesByBusStop.DoesNotExist:
            raise ServiceNotFoundException("Service {} is not present in bus stop {}".format(self.service, pBusStop))

        try:
            serviceDistance = ServiceStopDistance.objects.get(busStop=pBusStop, service=serviceCode).distance
        except ServiceStopDistance.DoesNotExist:
            raise ServiceDistanceNotFoundException(
                "The distance is not possible getting for bus stop '{}' and service '{}'".format(pBusStop, serviceCode))

        distance = serviceDistance - int(pDistance)
        # bus service distance from route origin
        greaters = ServiceLocation.objects.filter(service=serviceCode, distance__gt=distance).order_by('distance')[:1]
        # get 2 locations greater than current location (nearer to the bus stop)
        lowers = ServiceLocation.objects.filter(service=serviceCode, distance__lte=distance).order_by('-distance')[:1]
        # get 2 locations lower than current location

        # we need two point to detect the bus direction (left, right, up, down)
        lower = 0
        greater = 0
        if len(greaters) > 0 and len(lowers) > 0:
            greater = greaters[0]
            lower = lowers[0]
        elif len(greaters) == 0 and len(lowers) == 2:
            greater = lowers[0]
            lower = lowers[1]
        elif len(greaters) == 0 and len(lowers) == 1:
            greater = lowers[0]
            lower = lowers[0]
        elif len(lowers) == 0 and len(greaters) == 2:
            lower = greaters[0]
            greater = greaters[1]
        elif len(lowers) == 0 and len(greaters) == 1:
            lower = greaters[0]
            greater = greaters[0]
        elif len(lowers) == 0 and len(greaters) == 2:
            lower = greaters[0]
            greater = greaters[1]
        elif len(greaters) == 0 and len(lowers) == 0:
            # there are not points to detect direction
            # TODO: add log to register this situations
            logger = logging.getLogger(__name__)
            logger.info("There is not position to detect bus direction")
            return "left"

        epsilon = 0.00008
        x1 = lower.longitude
        # y1 = lower.latitude
        x2 = greater.longitude
        # y2 = greater.latitude

        if abs(x2 - x1) >= epsilon:
            if x2 - x1 > 0:
                return "right"
            else:
                return "left"
        else:
            # we compare bus location with bus stop location
            busStopObj = BusStop.objects.get(code=pBusStop)
            xBusStop = busStopObj.longitud
            if x2 - xBusStop > 0:
                return "left"
            else:
                return "right"

    def getLocation(self):
        """This method estimate the location of a bus given one user that is inside or gives a geo-location
        estimated."""
        tokens = Token.objects.filter(busassignment=self)
        lastDate = timezone.now() - timezone.timedelta(minutes=5)
        passengers = 0
        lat = -500
        lon = -500
        random = True
        for token in tokens:
            if not hasattr(token, 'activetoken'):
                continue
            passengers += 1
            trajectoryQuery = PoseInTrajectoryOfToken.objects.filter(token=token)
            if trajectoryQuery.exists():
                lastPose = trajectoryQuery.latest('timeStamp')
                if lastPose.timeStamp >= lastDate:
                    lastDate = lastPose.timeStamp
                    lat = lastPose.latitude
                    lon = lastPose.longitude
                    random = False

        return {'latitude': lat,
                'longitude': lon,
                'passengers': passengers,
                'random': random
                }

    def getEstimatedLocation(self, busstop, distance):
        """Given a distance from the bus to the bus stop, this method returns the global position of the machine."""
        try:
            serviceCode = ServicesByBusStop.objects.get(busStop=busstop, service=self.service).code
        except ServicesByBusStop.DoesNotExist:
            raise ServiceNotFoundException("Service {} is not present in bus stop {}".format(self.service, busstop))

        ssd = ServiceStopDistance.objects.get(busStop=busstop, service=serviceCode).distance - int(distance)

        try:
            closest_gt = ServiceLocation.objects.filter(service=serviceCode, distance__gte=ssd).order_by('distance')[
                0].distance
        except:
            closest_gt = 50000
        try:
            closest_lt = ServiceLocation.objects.filter(service=serviceCode, distance__lte=ssd).order_by('-distance')[
                0].distance
        except:
            closest_lt = 0

        if abs(closest_gt - ssd) < abs(closest_lt - ssd):
            closest = closest_gt
        else:
            closest = closest_lt

        location = ServiceLocation.objects.filter(service=serviceCode, distance=closest)[0]

        return {'latitude': location.latitude,
                'longitude': location.longitude,
                'direction': serviceCode[-1]
                }

    def getDictionary(self):
        """ Return a dictionary with useful information about the bus """
        dictionary = dict()

        dictionary['serviceBus'] = self.service
        dictionary['registrationPlateBus'] = self.uuid.registrationPlate

        return dictionary


class ServiceLocation(Location):
    """This models stores the position along the route of every bus at 20 meters apart.
    You can give the distance from the start of the travel and it return the position at that distance."""
    service = models.CharField('Service Code', max_length=11, null=False, blank=False)  # Service code i.e. 506I or 506R
    """ Service code where the last character indicates its direction """
    distance = models.IntegerField('Route Distance')
    """ Distance traveled by the service since its origin """
    gtfs = models.ForeignKey('GTFS', verbose_name='gtfs version')
    """ gtfs version """

    class Meta:
        index_together = ["service", "distance"]
        unique_together = ('service', 'distance', 'gtfs')


class ServiceStopDistance(models.Model):
    """This model stores the distance for every busStop in every bus route for every service.
    Given a bus direction code xxxI or xxxR or something alike."""
    busStop = models.ForeignKey(BusStop, verbose_name='Bus Stop')
    """ Bus stops where the service is stopped """
    service = models.CharField('Service Code', max_length=11, null=False, blank=False)  # Service code i.e. 506I or 506R
    """ It represents the Service code, ex: '506I' """
    distance = models.IntegerField('Distance Traveled')
    """ Distance traveled by the service when it reaches the bus stop """
    gtfs = models.ForeignKey('GTFS', verbose_name='gtfs version')
    """ gtfs version """

    class Meta:
        unique_together = ('busStop', 'service', 'gtfs')


class Token(models.Model):
    """This table has all the tokens that have been used ever."""
    token = models.CharField('Token', max_length=128)
    """Identifier for an incognito trip"""
    busassignment = models.ForeignKey(Busassignment, verbose_name='Bus')
    """Bus that is making the trip"""
    direction = models.CharField(max_length=1, null=True)
    """ route direction that the bus is doing. It can be 'R' or 'I' """
    color = models.CharField("Icon's color", max_length=7, default='#00a0f0')
    """Color to paint the travel icon"""
    phoneId = models.UUIDField()
    """ To identify the data owner """
    timeCreation = models.DateTimeField('Time Creation', null=True, blank=False)
    """ creation time of token """
    userEvaluation = models.IntegerField(null=True)
    """ User evaluation does at the end of trip """


class PoseInTrajectoryOfToken(Location):
    """This stores all the poses of a trajectory. The trajectory can start on foot and end on foot."""
    timeStamp = models.DateTimeField(null=False, blank=False, db_index=True)
    """ Specific date time when the server received a pose in the trajectory """
    inVehicleOrNot = models.CharField(max_length=15)  # vehicle, non_vehicle
    """ Identify if a pose was sent inside a vehicle or not """
    token = models.ForeignKey(Token, verbose_name='Token')

    class Meta:
        index_together = ["token", "timeStamp"]


class ActiveToken(models.Model):
    """This are the tokens that are currently being in use to upload positions."""
    timeStamp = models.DateTimeField('Time Stamp', null=False, blank=False)
    """ Specific date time when the server received the first pose in the trajectory, i.e. when the trip started """
    token = models.OneToOneField(Token, verbose_name='Token')


class Report(models.Model):
    """ This is the free report, it saves the message and the picture location in the system """
    timeStamp = models.DateTimeField(null=False, blank=False, db_index=True)
    """ Specific date time when the server received a pose in the trajectory """
    message = models.TextField()
    """ Text reported by the user """
    imageName = models.CharField(max_length=100, default="no image", null=True)
    """ image name that was saved """
    reportInfo = models.TextField()
    """ Additional information regarding the report. For example the user location."""
    phoneId = models.UUIDField()
    """ To identify the AndroidRequests owner """
    transformed = models.NullBooleanField(default=False, verbose_name=b'Transformed')
    """Indicates if the current row was transformed """

    def getDictionary(self):
        """Returns a dictionary with the event information"""
        dictionary = dict()
        dictionary['message'] = self.message

        if self.imageName and self.imageName != "no image":
            dictionary['imageName'] = ("/media/reported_images/" + self.imageName)
        else:
            dictionary['imageName'] = "no image"
        stamp = timezone.localtime(self.timeStamp, pytz.timezone('Chile/Continental'))
        dictionary['timeStamp'] = stamp.strftime("%d-%m-%Y %H:%M:%S")
        return dictionary


class GTFS(models.Model):
    """ manage different version presents in database """
    version = models.CharField(max_length=10, default=None, null=False, unique=True)
    """ GTFS version """
    timeCreation = models.DateTimeField('Time Creation', null=True, blank=False)
    """ creation time of token """

##
#
# Log for some requests
#
##
class NearByBusesLog(models.Model):
    """Registers an user request for bus stop"""
    timeStamp = models.DateTimeField('Time Stamp', null=False, blank=False)
    """ Specific date time when the server received the request """
    busStop = models.ForeignKey(BusStop, verbose_name='Bus Stop')
    """ Bus stops where the service is stopped """
    phoneId = models.UUIDField()
    """ To identify the AndroidRequests owner """


class Route(Location):
    """Route for each service"""
    serviceCode = models.CharField(db_index=True, max_length=11, null=False, blank=False)
    """ Bus identifier """
    sequence = models.IntegerField('Sequence')
    """ point position in a route """
    gtfs = models.ForeignKey('GTFS', verbose_name='gtfs version')
    """ gtfs version """

    class Meta:
        unique_together = ('serviceCode', 'sequence', 'gtfs')


class ZonificationTransantiago(models.Model):
    """Zonification"""
    id = models.IntegerField(primary_key=True)
    area = models.FloatField()
    zona = models.FloatField()
    com = models.CharField(max_length=80)
    comuna = models.CharField(max_length=80)
    cartodb_id = models.IntegerField()
    created_at = models.DateField()
    updated_at = models.DateField()
    comunidad_field = models.FloatField(null=True)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()


# Auto-generated `LayerMapping` dictionary for zonificationTransantiago model
zonificationtransantiago_mapping = {
    'id': 'id',
    'area': 'area',
    'zona': 'zona',
    'com': 'com',
    'comuna': 'comuna',
    'cartodb_id': 'cartodb_id',
    'created_at': 'created_at',
    'updated_at': 'updated_at',
    'comunidad_field': 'comunidad_',
    'geom': 'MULTIPOLYGON',
}


##
#
# score and login
#
##

class Level(models.Model):
    """ user level """
    name = models.CharField(max_length=50, null=False, blank=False)
    """ level name """
    minScore = models.FloatField(default=0, null=False)
    """ minimun score to keep the level """
    maxScore = models.FloatField(default=0, null=False)
    """ maximum score to keep the level """
    position = models.IntegerField(null=False, unique=True)
    """ to order levels 1,2,3,... """


class TranSappUser(models.Model):
    """ user logged with social network (Facebook, google) """
    userId = models.CharField(max_length=128, null=False, blank=False)
    """ user id given by social network(FacebookUserId or ) """
    name = models.CharField(max_length=50, null=False, blank=False)
    """ user name """
    email = models.EmailField(null=False, blank=False)
    """ user email"""
    phoneId = models.UUIDField(null=False)
    """ phone id used to log in """
    FACEBOOK = 'FACEBOOK'
    GOOGLE = 'GOOGLE'
    ACCOUNT_TYPES=(
        (FACEBOOK, 'Facebook'),
        (GOOGLE, 'Google')
    )
    accountType = models.CharField(max_length=10, choices=ACCOUNT_TYPES, null=False)
    """ type of toke id (it says where tokenID comes from) """
    globalScore = models.FloatField(default=0, null=False)
    """ global score generated by user interactions """
    level = models.ForeignKey(Level, null=False)
    """ level based on score """
    sessionToken = models.UUIDField(null=False)
    """ uuid generated each time the user log in """


class ScoreEvent(models.Model):
    """ score given by action """
    code = models.CharField(max_length=10, null=False, blank=False, unique=True)
    """ event code """
    score = models.FloatField(default=0, null=False)
    """ score given to user when he does the action associated to code """


class ScoreHistory(models.Model):
    """ history of events give score"""
    tranSappUser = models.ForeignKey(TranSappUser)
    """ user """
    scoreEvent = models.ForeignKey(ScoreEvent)
    """ event that generates the score """
    timeCreation = models.DateTimeField(null=False)
    """ time when event was generated """
    score = models.FloatField(default=0, null=False)
    """ winned score """
    meta = models.CharField(max_length=10000, null=True)
    """ addional data to score """
