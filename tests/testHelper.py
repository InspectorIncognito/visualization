from django.test import RequestFactory, Client
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from django.conf import settings

import json
import datetime as dt

# views
from AndroidRequests.models import Busv2, Busassignment, Event, EventForBusv2, GTFS, BusStop, EventForBusStop


class TestHelper():
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

    def createReportBusEvent(self, busassignment, eventObj, phoneId, timeStamp, 
            eventConfirm=1, eventDecline=0, timeCreation=timezone.now()):
        """ report a bus event """
        report = EventForBusv2.objects.create(
            busassignment=busassignment,
            timeStamp=timeStamp,
            phoneId=phoneId,
            event = eventObj,
            timeCreation=timeCreation,
            eventConfirm=eventConfirm,
            eventDecline=eventDecline)
        return report

    def createReportStopEvent(self, code, eventObj, phoneId, timeStamp, 
            eventConfirm=1, eventDecline=0, timeCreation=timezone.now()):
        """ report a stop event """
        report = EventForBusStop.objects.create(
            stopCode=code,
            timeStamp=timeStamp,
            phoneId=phoneId,
            event = eventObj,
            timeCreation=timeCreation,
            eventConfirm=eventConfirm,
            eventDecline=eventDecline)
        return report


    # ===================================================================== 

