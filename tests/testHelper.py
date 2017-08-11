from django.test import RequestFactory
from django.utils import timezone
# views
from AndroidRequests.models import Busv2, Busassignment, Event, EventForBusv2, GTFS, BusStop, EventForBusStop, Report,\
StadisticDataFromRegistrationBus, StadisticDataFromRegistrationBusStop, ReportInfo

import uuid

class TestHelper:
    """ methods that help to create test cases """

    def __init__(self, testInstance):
        self.factory = RequestFactory()
        self.test = testInstance

    def createBus(self, phoneId, licencePlate):
        """ create a bus object and assignment object """
        bus = Busv2.objects.create(registrationPlate=licencePlate, uuid=phoneId)
        return bus

    def createAssignment(self, bus, service):
        """ create an assignment object """
        assignment = Busassignment.objects.create(service=service, uuid=bus)
        return assignment

    def createEvent(self, code, name, description, lifespam):
        """ create event object """
        event = Event.objects.create(pk=code,
                                     name=name,
                                     description=description,
                                     lifespam=lifespam)
        return event

    def createGTFS(self, version):
        """ create gtfs object """
        gtfs = GTFS.objects.create(version=version, timeCreation=timezone.now())
        return gtfs

    def createStop(self, code, name, gtfs, latitude=-33.4569,
                   longitude=-70.6632, transformed=False):
        """ create stop object """
        stop = BusStop.objects.create(code=code,
                                      name=name,
                                      gtfs=gtfs,
                                      transformed=transformed,
                                      latitude=latitude,
                                      longitude=longitude)
        return stop

    def createReportBusEvent(self, bus_assignment, event_obj, phone_id, timestamp,
                             event_confirm=1, event_decline=0, time_creation=timezone.now()):
        """ report a bus event """
        report = EventForBusv2.objects.create(
            busassignment=bus_assignment,
            timeStamp=timestamp,
            phoneId=phone_id,
            event=event_obj,
            timeCreation=time_creation,
            eventConfirm=event_confirm,
            eventDecline=event_decline)

        StadisticDataFromRegistrationBus.objects.create(reportOfEvent=report, confirmDecline="confirm",
                                                        phoneId=phone_id, longitude=-70.664253,
                                                        latitude=-33.457372, timeStamp=timestamp)

        return report

    def createReportStopEvent(self, code, event_obj, phoneId, timeStamp,
                              eventConfirm=1, eventDecline=0, timeCreation=timezone.now()):
        """ report a stop event """
        report = EventForBusStop.objects.create(
            stopCode=code,
            timeStamp=timeStamp,
            phoneId=phoneId,
            event=event_obj,
            timeCreation=timeCreation,
            eventConfirm=eventConfirm,
            eventDecline=eventDecline)

        StadisticDataFromRegistrationBusStop.objects.create(reportOfEvent=report, confirmDecline="confirm",
                                                            phoneId=phoneId, longitude=-70.664253,
                                                            latitude=-33.457372, timeStamp=timeStamp)

        return report

    def createReport(self, message, timestamp, phoneId, imageName, reportInfo):
        """  """
        report = Report.objects.create(
            message=message,
            timeStamp=timestamp,
            phoneId=phoneId,
            imageName=imageName,
            reportInfo=reportInfo
        )
        return report

    def createReportInfoForStop(self, stopCode, longitude, latitude, zoneObj,
                                userLongitude, userLatitude):
        """  """
        report = self.createReport(message="", timestamp=timezone.now(), phoneId=uuid.uuid4(), imageName="", reportInfo="")
        reportType = ReportInfo.STOP
        ReportInfo.objects.create(reportType=reportType, stopCode=stopCode, longitude=longitude, latitude=latitude,
                                  userLongitude=userLongitude, userLatitude=userLatitude, zonification=zoneObj,
                                  report=report)

    def createReportInfoForBus(self, route, busUUID, licensePlate, direction, longitude, latitude,
                               userLongitude, userLatitude, zoneObj):
        """  """
        report = self.createReport(message="", timestamp=timezone.now(), phoneId=uuid.uuid4(), imageName="", reportInfo="")
        reportType = ReportInfo.BUS
        ReportInfo.objects.create(reportType=reportType, busUUID=busUUID, service=route, registrationPlate=licensePlate,
                                  longitude=longitude, latitude=latitude, zonification=zoneObj,
                                  userLongitude=userLongitude, userLatitude=userLatitude, report=report)
